"""
Experiment runner (Steps 1-7 executed across the full comparison matrix).

Each configuration is one (dataset, imbalance method, classifier) triple. For
every configuration the runner:

1. loads the dataset and induces the controlled imbalance ratio,
2. cleans the features and produces the stratified train-test split,
3. fits a grid search whose pipeline resamples inside each CV fold,
4. refits the winning hyperparameters on the full treated training set,
5. evaluates once on the untouched test set.

Per-configuration test predictions are persisted alongside the metrics because
McNemar's test operates on paired predictions rather than summary scores.
"""

from __future__ import annotations

import argparse
import json
import time
import warnings
from itertools import product

import numpy as np
import pandas as pd

from config import (
    CLASSIFIERS,
    CORE_IMBALANCE_METHODS,
    DATASETS,
    IMBALANCE_METHODS,
    MINORITY_RATIO,
    RANDOM_STATE,
    RESULTS_DIR,
)
from data_loader import load_dataset
from evaluation import evaluate
from imbalance import method_family
from models import build_search, get_scores
from preprocessing import prepare, split_summary

PREDICTIONS_DIR = RESULTS_DIR / "predictions"
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)


def config_id(
    dataset: str,
    method: str,
    classifier: str,
    ratio: float,
    seed: int = RANDOM_STATE,
) -> str:
    """Stable identifier used for result rows and prediction filenames.

    The seed is part of the identifier so that repeated runs do not overwrite
    one another's saved predictions.
    """
    return (
        f"{dataset}__{method}__{classifier}"
        f"__r{int(round(ratio * 100))}__s{seed}"
    )


def run_configuration(
    dataset: str,
    method: str,
    classifier: str,
    minority_ratio: float = MINORITY_RATIO,
    save_predictions: bool = True,
    seed: int = RANDOM_STATE,
) -> dict:
    """Execute a single experimental configuration and return its metrics.

    ``seed`` drives the induced downsampling, the train-test split, the
    cross-validation folds, the sampler and the classifier. Repeating the sweep
    under different seeds therefore produces independent replications rather
    than identical re-runs.
    """
    started = time.time()

    X, y = load_dataset(dataset, minority_ratio=minority_ratio, random_state=seed)
    X_train, X_test, y_train, y_test = prepare(X, y, random_state=seed)

    search = build_search(classifier, method, random_state=seed)
    with warnings.catch_warnings():
        # Convergence and sampling warnings are expected on some folds and are
        # not informative once the configuration completes.
        warnings.simplefilter("ignore")
        search.fit(X_train, y_train)

    best_model = search.best_estimator_
    y_pred = best_model.predict(X_test)
    y_scores = get_scores(best_model, X_test)

    metrics = evaluate(y_test, y_pred, y_scores)

    cid = config_id(dataset, method, classifier, minority_ratio, seed)
    if save_predictions:
        np.savez_compressed(
            PREDICTIONS_DIR / f"{cid}.npz",
            y_true=np.asarray(y_test),
            y_pred=np.asarray(y_pred),
            y_scores=np.asarray(y_scores),
        )

    row = {
        "config_id": cid,
        "dataset": dataset,
        "imbalance_method": method,
        "method_family": method_family(method),
        "classifier": classifier,
        "minority_ratio": minority_ratio,
        "seed": seed,
        **metrics,
        "cv_best_score": round(float(search.best_score_), 4),
        "best_params": json.dumps(
            {k.replace("classifier__", ""): v for k, v in search.best_params_.items()}
        ),
        "runtime_sec": round(time.time() - started, 1),
    }
    row.update(split_summary(y_train, y_test))
    return row


def run_all(
    datasets=None,
    methods=None,
    classifiers=None,
    minority_ratio: float = MINORITY_RATIO,
    include_baseline: bool = True,
    output_name: str = "results.csv",
    verbose: bool = True,
    seeds=None,
) -> pd.DataFrame:
    """Run the full comparison matrix and write the results table to disk.

    Parameters
    ----------
    seeds
        One or more random seeds. Each seed repeats the entire matrix as an
        independent replication, which increases the number of matched blocks
        available to the Friedman and post-hoc tests. Defaults to the single
        project seed.
    """
    datasets = datasets or DATASETS
    classifiers = classifiers or CLASSIFIERS
    seeds = list(seeds) if seeds else [RANDOM_STATE]
    if methods is None:
        methods = IMBALANCE_METHODS if include_baseline else CORE_IMBALANCE_METHODS

    combinations = list(product(seeds, datasets, methods, classifiers))
    total = len(combinations)
    rows = []

    if verbose:
        seed_note = f"{len(seeds)} seed(s) {seeds}" if len(seeds) > 1 else f"seed {seeds[0]}"
        print(
            f"Running {total} configurations at {minority_ratio:.0%} "
            f"minority ratio, {seed_note}\n"
        )

    for i, (seed, dataset, method, classifier) in enumerate(combinations, start=1):
        if verbose:
            print(
                f"[{i:>3}/{total}] s{seed:<3} {dataset:10s} {method:22s} {classifier:15s}",
                end=" ",
                flush=True,
            )

        try:
            row = run_configuration(
                dataset, method, classifier, minority_ratio, seed=seed
            )
            rows.append(row)
            if verbose:
                print(
                    f"F1={row['f1']:.4f} recall={row['recall']:.4f} "
                    f"PR-AUC={row['pr_auc']:.4f} ({row['runtime_sec']}s)"
                )
        except Exception as exc:  # keep the sweep alive, record the failure
            if verbose:
                print(f"FAILED: {type(exc).__name__}: {exc}")
            rows.append(
                {
                    "config_id": config_id(
                        dataset, method, classifier, minority_ratio, seed
                    ),
                    "dataset": dataset,
                    "imbalance_method": method,
                    "classifier": classifier,
                    "minority_ratio": minority_ratio,
                    "seed": seed,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    results = pd.DataFrame(rows)
    out_path = RESULTS_DIR / output_name
    results.to_csv(out_path, index=False)

    if verbose:
        print(f"\nResults written to {out_path}")

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the phishing detection experiments.")
    parser.add_argument("--datasets", nargs="*", default=None, help="Subset of datasets.")
    parser.add_argument("--methods", nargs="*", default=None, help="Subset of imbalance methods.")
    parser.add_argument("--classifiers", nargs="*", default=None, help="Subset of classifiers.")
    parser.add_argument("--ratio", type=float, default=MINORITY_RATIO, help="Minority class ratio.")
    parser.add_argument("--no-baseline", action="store_true", help="Exclude the untreated baseline.")
    parser.add_argument("--output", default="results.csv", help="Output CSV filename.")
    parser.add_argument(
        "--seeds",
        nargs="*",
        type=int,
        default=None,
        help="Random seeds; each one repeats the whole matrix as a replication.",
    )
    args = parser.parse_args()

    run_all(
        datasets=args.datasets,
        methods=args.methods,
        classifiers=args.classifiers,
        minority_ratio=args.ratio,
        include_baseline=not args.no_baseline,
        output_name=args.output,
        seeds=args.seeds,
    )


if __name__ == "__main__":
    main()
