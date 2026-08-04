"""
Model persistence for the dashboard (Section 3.10).

The dashboard needs a fitted model to explain, but retraining on every page load
would make it unusable. This module trains the best-performing configuration for
each dataset once and writes it to ``models/`` together with everything the
dashboard needs to interpret it: the feature names, a held-out sample for
instance selection, and the metrics the configuration achieved.

The configuration to persist is read from the experiment results rather than
hard-coded, so the dashboard always reflects the study's own conclusion about
which configuration performed best.
"""

from __future__ import annotations

import argparse
import json
import warnings

import joblib
import numpy as np
import pandas as pd

from config import (
    DATASETS,
    MINORITY_RATIO,
    MODELS_DIR,
    RANDOM_STATE,
    RESULTS_DIR,
    SUBSAMPLE_SIZE,
)
from data_loader import load_dataset
from evaluation import evaluate
from models import build_search, get_scores
from preprocessing import prepare

# Number of test instances kept for the dashboard's instance browser.
SAMPLE_SIZE = 300


def best_configuration(
    dataset: str,
    results_file: str = "results_multiseed.csv",
    metric: str = "f1",
) -> tuple[str, str]:
    """Return the (imbalance_method, classifier) that scored best on ``dataset``.

    Untreated baseline rows are excluded, since the dashboard is meant to
    demonstrate a model produced by the study's treatment pipeline. Where the
    sweep was replicated, configurations are ranked by their mean across
    replications rather than by a single lucky seed.
    """
    path = RESULTS_DIR / results_file
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run experiment.py before persisting models."
        )

    df = pd.read_csv(path)
    if "error" in df.columns:
        df = df[df["error"].isna()]

    df = df[(df["dataset"] == dataset) & (df["imbalance_method"] != "none")]
    if df.empty:
        raise ValueError(f"No treated results found for dataset '{dataset}'.")

    ranked = (
        df.groupby(["imbalance_method", "classifier"], as_index=False)[metric]
        .mean()
        .sort_values(metric, ascending=False)
    )
    top = ranked.iloc[0]
    return str(top["imbalance_method"]), str(top["classifier"])


def persist(
    dataset: str,
    method: str | None = None,
    classifier: str | None = None,
    seed: int = RANDOM_STATE,
    verbose: bool = True,
) -> dict:
    """Train one configuration and write it to ``models/``.

    Returns the metadata that was saved alongside the model.
    """
    if method is None or classifier is None:
        method, classifier = best_configuration(dataset)

    if verbose:
        print(f"  {dataset}: training {classifier} with {method} (seed {seed})", flush=True)

    X, y = load_dataset(
        dataset,
        minority_ratio=MINORITY_RATIO,
        random_state=seed,
        subsample=SUBSAMPLE_SIZE,
    )
    X_train, X_test, y_train, y_test = prepare(X, y, random_state=seed)

    search = build_search(classifier, method, random_state=seed)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        search.fit(X_train, y_train)

    model = search.best_estimator_
    y_pred = model.predict(X_test)
    metrics = evaluate(y_test, y_pred, get_scores(model, X_test))

    # A held-out sample lets the dashboard show real instances with known labels
    # without shipping the whole test partition.
    rng = np.random.RandomState(seed)
    n = min(SAMPLE_SIZE, len(X_test))
    idx = rng.choice(len(X_test), size=n, replace=False)
    sample = X_test.iloc[idx].copy()
    sample["__true_label"] = np.asarray(y_test)[idx]

    metadata = {
        "dataset": dataset,
        "imbalance_method": method,
        "classifier": classifier,
        "seed": seed,
        "features": list(X_train.columns),
        "n_features": X_train.shape[1],
        "train_size": int(len(y_train)),
        "test_size": int(len(y_test)),
        "test_phishing_pct": round(100 * float(np.mean(y_test)), 2),
        "best_params": {
            k.replace("classifier__", ""): v for k, v in search.best_params_.items()
        },
        "metrics": {
            k: (round(v, 4) if isinstance(v, float) else v) for k, v in metrics.items()
        },
    }

    joblib.dump(model, MODELS_DIR / f"{dataset}_model.joblib")
    sample.to_csv(MODELS_DIR / f"{dataset}_sample.csv", index=False)
    with open(MODELS_DIR / f"{dataset}_metadata.json", "w") as fh:
        json.dump(metadata, fh, indent=2)

    if verbose:
        m = metadata["metrics"]
        print(
            f"    F1={m['f1']} recall={m['recall']} precision={m['precision']} "
            f"PR-AUC={m['pr_auc']}"
        )
        print(f"    saved to {MODELS_DIR}")

    return metadata


def load_persisted(dataset: str):
    """Load a persisted model, its held-out sample and its metadata."""
    model_path = MODELS_DIR / f"{dataset}_model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(
            f"No persisted model for '{dataset}'. Run persist_models.py first."
        )

    model = joblib.load(model_path)
    sample = pd.read_csv(MODELS_DIR / f"{dataset}_sample.csv")
    with open(MODELS_DIR / f"{dataset}_metadata.json") as fh:
        metadata = json.load(fh)

    return model, sample, metadata


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train and persist the best configuration for each dataset."
    )
    parser.add_argument("--datasets", nargs="*", default=None)
    parser.add_argument("--method", default=None, help="Override the imbalance method.")
    parser.add_argument("--classifier", default=None, help="Override the classifier.")
    parser.add_argument("--seed", type=int, default=RANDOM_STATE)
    args = parser.parse_args()

    print("Persisting models for the dashboard:")
    for dataset in (args.datasets or DATASETS):
        persist(dataset, args.method, args.classifier, args.seed)


if __name__ == "__main__":
    main()
