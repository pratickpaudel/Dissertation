"""
SHAP explainability analysis (Section 3.10).

Two questions are addressed that the performance metrics alone cannot answer:

1. **Global attribution** - which features drive the model's decisions overall?
2. **Comparative attribution** - does applying an imbalance treatment technique
   change *which* features the model relies on, not merely how accurate it is?

The second question is the more interesting one for this dissertation, because
it connects the explainability layer directly to the research question about
imbalance treatment.

Explainer selection
-------------------
``TreeExplainer`` is used for the tree-based models because it is exact and
fast. For the SVM there is no tree structure to exploit, so ``KernelExplainer``
is used on a small background sample; this is an approximation and is
computationally expensive, hence the conservative default sample sizes.
"""

from __future__ import annotations

import argparse
import warnings
from typing import NamedTuple

import numpy as np
import pandas as pd

from config import (
    CLASSIFIER_LABELS,
    DATASET_LABELS,
    FIGURES_DIR,
    METHOD_LABELS,
    MINORITY_RATIO,
    RANDOM_STATE,
    RESULTS_DIR,
)
from data_loader import load_dataset
from models import build_search
from preprocessing import prepare

# Sample sizes keep the kernel-based approximation tractable.
TREE_SAMPLE = 500
KERNEL_SAMPLE = 100
KERNEL_BACKGROUND = 50


class ShapResult(NamedTuple):
    """Bundle of SHAP output and the data it was computed on.

    ``X_scaled`` is the space the classifier and SHAP operate in, while
    ``X_raw`` holds the original untransformed feature values. Both are kept
    because plots need the former but human-readable explanations need the
    latter (a standardised value such as ``-0.44`` means nothing to a reader).
    """

    values: np.ndarray
    X_scaled: pd.DataFrame
    X_raw: pd.DataFrame
    model: object


def _fit_model(dataset: str, method: str, classifier: str, minority_ratio: float):
    """Refit one configuration and return the model with its train/test data."""
    X, y = load_dataset(dataset, minority_ratio=minority_ratio)
    X_train, X_test, y_train, y_test = prepare(X, y)

    search = build_search(classifier, method)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        search.fit(X_train, y_train)

    return search.best_estimator_, X_train, X_test, y_test


def _transform_through_pipeline(pipeline, X: pd.DataFrame) -> pd.DataFrame:
    """Apply every pipeline step except the final classifier.

    SHAP must see the data in the same space the classifier was trained in, so
    the scaler is applied first. Resampling steps are skipped because they alter
    row counts rather than the feature space.
    """
    X_out = X
    for name, step in pipeline.steps[:-1]:
        if hasattr(step, "transform"):
            X_out = step.transform(X_out)
    return pd.DataFrame(np.asarray(X_out), columns=X.columns, index=X.index)


def compute_shap_values(
    dataset: str = "uci",
    method: str = "smote",
    classifier: str = "random_forest",
    minority_ratio: float = MINORITY_RATIO,
    sample_size: int | None = None,
):
    """Compute SHAP values for one configuration.

    Returns
    -------
    ShapResult
        Named tuple of ``(values, X_scaled, X_raw, model)``, where ``values`` is
        a 2-D array of per-instance contributions towards the phishing class.
    """
    import shap

    model, X_train, X_test, _ = _fit_model(dataset, method, classifier, minority_ratio)
    estimator = model.named_steps["classifier"]

    X_test_t = _transform_through_pipeline(model, X_test)
    rng = np.random.RandomState(RANDOM_STATE)

    is_tree = classifier in {"decision_tree", "random_forest"}
    n = sample_size or (TREE_SAMPLE if is_tree else KERNEL_SAMPLE)
    n = min(n, len(X_test_t))
    idx = rng.choice(len(X_test_t), size=n, replace=False)
    X_sample = X_test_t.iloc[idx]
    X_sample_raw = X_test.iloc[idx]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if is_tree:
            explainer = shap.TreeExplainer(estimator)
            shap_values = explainer.shap_values(X_sample)
        else:
            X_train_t = _transform_through_pipeline(model, X_train)
            bg_idx = rng.choice(
                len(X_train_t), size=min(KERNEL_BACKGROUND, len(X_train_t)), replace=False
            )
            explainer = shap.KernelExplainer(
                estimator.decision_function, X_train_t.iloc[bg_idx]
            )
            shap_values = explainer.shap_values(X_sample, silent=True)

    shap_values = _select_positive_class(shap_values)
    return ShapResult(shap_values, X_sample, X_sample_raw, model)


def _select_positive_class(shap_values) -> np.ndarray:
    """Reduce SHAP output to a 2-D array of contributions to the phishing class.

    SHAP returns different shapes depending on the explainer and model: a list
    of per-class arrays, a 3-D array, or a plain 2-D array. All three are
    normalised here so downstream code can assume ``(n_samples, n_features)``.
    """
    if isinstance(shap_values, list):
        # One array per class; index 1 is the positive (phishing) class.
        return np.asarray(shap_values[1] if len(shap_values) > 1 else shap_values[0])

    values = np.asarray(shap_values)
    if values.ndim == 3:
        return values[:, :, 1] if values.shape[2] > 1 else values[:, :, 0]
    return values


def global_importance(shap_values: np.ndarray, X_sample: pd.DataFrame) -> pd.DataFrame:
    """Rank features by mean absolute SHAP value (global importance)."""
    mean_abs = np.abs(shap_values).mean(axis=0)
    mean_signed = shap_values.mean(axis=0)

    return (
        pd.DataFrame(
            {
                "feature": X_sample.columns,
                "mean_abs_shap": mean_abs,
                "mean_shap": mean_signed,
            }
        )
        .sort_values("mean_abs_shap", ascending=False)
        .reset_index(drop=True)
        .assign(rank=lambda d: d.index + 1)
    )


def local_explanation(
    result: ShapResult,
    instance_index: int = 0,
    top_n: int = 10,
) -> pd.DataFrame:
    """Per-feature contributions for a single website (local explanation).

    Feature values are reported on their original scale so the explanation is
    readable, while the SHAP contributions come from the scaled space the model
    was trained in.
    """
    contributions = result.values[instance_index]
    return (
        pd.DataFrame(
            {
                "feature": result.X_scaled.columns,
                "feature_value": result.X_raw.iloc[instance_index].to_numpy(),
                "shap_value": contributions,
                "direction": np.where(contributions > 0, "towards phishing", "towards legitimate"),
            }
        )
        .assign(abs_shap=lambda d: d["shap_value"].abs())
        .sort_values("abs_shap", ascending=False)
        .head(top_n)
        .drop(columns="abs_shap")
        .reset_index(drop=True)
    )


def compare_across_methods(
    dataset: str = "uci",
    classifier: str = "random_forest",
    methods: list[str] | None = None,
    minority_ratio: float = MINORITY_RATIO,
    top_n: int = 15,
    verbose: bool = True,
) -> pd.DataFrame:
    """Compare global feature importance across imbalance treatment methods.

    This is the analysis that supports the argument in Section 3.10: if the
    ranking shifts between methods, then imbalance treatment changes not only
    predictive performance but also which evidence the model uses.
    """
    methods = methods or ["none", "smote", "smoteenn", "random_undersampling"]
    frames = []

    for method in methods:
        if verbose:
            print(f"  SHAP: {dataset} / {method} / {classifier}", flush=True)
        result = compute_shap_values(dataset, method, classifier, minority_ratio)
        imp = global_importance(result.values, result.X_scaled)
        imp["imbalance_method"] = method
        frames.append(imp)

    combined = pd.concat(frames, ignore_index=True)

    # Wide ranking table: features as rows, methods as columns.
    ranks = combined.pivot(index="feature", columns="imbalance_method", values="rank")
    baseline = methods[0]
    ranks = ranks.sort_values(baseline).head(top_n)
    ranks["rank_range"] = ranks.max(axis=1) - ranks.min(axis=1)

    out = RESULTS_DIR / f"shap_method_comparison_{dataset}_{classifier}.csv"
    combined.to_csv(RESULTS_DIR / f"shap_importance_{dataset}_{classifier}.csv", index=False)
    ranks.to_csv(out)

    if verbose:
        print(f"\nTop {top_n} features by baseline rank ({dataset}, {CLASSIFIER_LABELS[classifier]}):")
        print(ranks.to_string())
        print(f"\nWritten to {out}")

    return ranks


def plot_summary(
    shap_values: np.ndarray,
    X_sample: pd.DataFrame,
    dataset: str,
    method: str,
    classifier: str,
    max_display: int = 15,
) -> None:
    """Save a SHAP beeswarm summary plot for use as a figure."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import shap

    plt.figure()
    shap.summary_plot(
        shap_values,
        X_sample,
        max_display=max_display,
        show=False,
    )
    plt.title(
        f"{DATASET_LABELS.get(dataset, dataset)} - "
        f"{CLASSIFIER_LABELS.get(classifier, classifier)} - "
        f"{METHOD_LABELS.get(method, method)}",
        fontsize=10,
    )
    plt.tight_layout()

    path = FIGURES_DIR / f"shap_summary_{dataset}_{method}_{classifier}.png"
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close("all")
    print(f"Figure saved to {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SHAP explainability analysis.")
    parser.add_argument("--dataset", default="uci")
    parser.add_argument("--classifier", default="random_forest")
    parser.add_argument("--method", default="smote")
    parser.add_argument("--ratio", type=float, default=MINORITY_RATIO)
    parser.add_argument("--compare", action="store_true", help="Compare across imbalance methods.")
    parser.add_argument("--methods", nargs="*", default=None)
    parser.add_argument("--plot", action="store_true", help="Save a beeswarm summary figure.")
    args = parser.parse_args()

    if args.compare:
        compare_across_methods(
            dataset=args.dataset,
            classifier=args.classifier,
            methods=args.methods,
            minority_ratio=args.ratio,
        )
        return

    result = compute_shap_values(
        args.dataset, args.method, args.classifier, args.ratio
    )

    print(f"\nGlobal feature importance ({args.dataset} / {args.method} / {args.classifier}):")
    print(global_importance(result.values, result.X_scaled).head(15).to_string(index=False))

    print("\nLocal explanation for test instance 0:")
    print(local_explanation(result).to_string(index=False))

    if args.plot:
        plot_summary(
            result.values, result.X_scaled, args.dataset, args.method, args.classifier
        )


if __name__ == "__main__":
    main()
