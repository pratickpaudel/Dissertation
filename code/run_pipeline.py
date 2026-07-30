#!/usr/bin/env python
"""
End-to-end pipeline runner.

Executes the complete experimental procedure in the order shown in the
methodology diagram:

    dataset loading -> preprocessing -> stratified split -> imbalance treatment
    -> classifier selection -> training and tuning -> evaluation
    -> comparative analysis -> statistical significance testing
    -> (optional) SHAP explainability

Usage
-----
    python run_pipeline.py                    # full pipeline
    python run_pipeline.py --quick            # small subset, for a smoke test
    python run_pipeline.py --skip-experiments # re-analyse existing results
    python run_pipeline.py --with-shap        # include the SHAP stage
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import (  # noqa: E402
    DATASETS,
    MINORITY_RATIO,
    RESULTS_DIR,
    SUBSAMPLE_SIZE,
)


def banner(step: str, title: str) -> None:
    print("\n" + "=" * 78)
    print(f"STEP {step}: {title}")
    print("=" * 78)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full experimental pipeline.")
    parser.add_argument("--ratio", type=float, default=MINORITY_RATIO)
    parser.add_argument("--quick", action="store_true", help="Run a reduced subset.")
    parser.add_argument("--skip-experiments", action="store_true",
                        help="Reuse the existing results.csv.")
    parser.add_argument("--with-shap", action="store_true",
                        help="Also run the SHAP explainability stage.")
    parser.add_argument("--results", default="results.csv")
    args = parser.parse_args()

    started = time.time()

    # -- Step 1: describe the input data ------------------------------------
    banner("1", "Dataset summary")
    from data_loader import describe

    for ds in DATASETS:
        native = describe(ds)
        used = describe(ds, args.ratio, subsample=SUBSAMPLE_SIZE)
        print(f"  {ds}:")
        print(f"    as published : {native['instances']:6d} rows, "
              f"{native['features']:3d} features, "
              f"{native['phishing_pct']}% phishing (ratio {native['imbalance_ratio']})")
        print(f"    as used      : {used['instances']:6d} rows, "
              f"{used['phishing_pct']}% phishing (ratio {used['imbalance_ratio']})")

    print("\n  Rejected candidates (balanced, hence unusable for this study):")
    for ds in ("uci", "hannousse"):
        d = describe(ds)
        print(f"    {ds:10s} {d['phishing_pct']}% phishing (ratio {d['imbalance_ratio']})")

    # -- Steps 2-7: run the experimental matrix ----------------------------
    if not args.skip_experiments:
        banner("2-7", "Experimental matrix (split, treatment, training, evaluation)")
        from experiment import run_all

        if args.quick:
            run_all(
                datasets=[DATASETS[0]],
                methods=["none", "smote", "random_undersampling"],
                classifiers=["decision_tree"],
                minority_ratio=args.ratio,
                output_name=args.results,
            )
        else:
            run_all(minority_ratio=args.ratio, output_name=args.results)
    else:
        banner("2-7", "Experimental matrix (skipped, reusing existing results)")
        if not (RESULTS_DIR / args.results).exists():
            print(f"  ERROR: {RESULTS_DIR / args.results} not found.")
            return 1

    # -- Step 8: comparative analysis --------------------------------------
    banner("8", "Comparative performance analysis")
    from analysis import generate_all

    generate_all(results_file=args.results)

    # -- Step 9: statistical significance ----------------------------------
    banner("9", "Statistical significance testing")
    from statistical_tests import run_all_tests

    try:
        run_all_tests(results_file=args.results)
    except Exception as exc:
        print(f"  Statistical testing skipped: {type(exc).__name__}: {exc}")
        print("  (this is expected when running --quick, which produces too few blocks)")

    # -- Step 10: explainability -------------------------------------------
    if args.with_shap:
        banner("10", "SHAP explainability")
        from explainability import compare_across_methods

        compare_across_methods(
            dataset="uci",
            classifier="random_forest",
            minority_ratio=args.ratio,
        )

    elapsed = time.time() - started
    print(f"\nPipeline complete in {elapsed / 60:.1f} minutes.")
    print(f"Outputs in {RESULTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
