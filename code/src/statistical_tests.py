"""
Statistical significance testing (Step 9 of the pipeline).

Two complementary tests are applied:

* **Friedman test** - a non-parametric test for differences across more than two
  related groups. It is used to ask whether the classifiers differ overall, and
  whether the imbalance treatment methods differ overall, by ranking their
  performance within each experimental block.

* **McNemar's test** - a paired test on the *same* test instances. It compares
  two fitted models by counting the cases where one is correct and the other is
  wrong, which is more informative than comparing summary metrics because it
  accounts for the correlation between predictions on shared data.

Where the Friedman test is significant, post-hoc pairwise Wilcoxon signed-rank
tests with Holm-Bonferroni correction identify *which* pairs differ. Holm is
used rather than plain Bonferroni because it is uniformly more powerful while
still controlling the family-wise error rate.
"""

from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon
from statsmodels.stats.contingency_tables import mcnemar

from config import ALPHA, CLASSIFIER_LABELS, METHOD_LABELS, RESULTS_DIR

PREDICTIONS_DIR = RESULTS_DIR / "predictions"


# ---------------------------------------------------------------------------
# Prediction loading
# ---------------------------------------------------------------------------
def load_predictions(config_id: str) -> dict[str, np.ndarray]:
    """Load the saved test-set predictions for one configuration."""
    path = PREDICTIONS_DIR / f"{config_id}.npz"
    if not path.exists():
        raise FileNotFoundError(
            f"No saved predictions for '{config_id}'. Run experiment.py first."
        )
    with np.load(path) as data:
        return {k: data[k] for k in data.files}


# ---------------------------------------------------------------------------
# McNemar's test
# ---------------------------------------------------------------------------
def mcnemar_test(config_a: str, config_b: str, alpha: float = ALPHA) -> dict:
    """Compare two configurations on their shared test set.

    The two models must have been evaluated on identical test instances, which
    holds whenever they share the same dataset and imbalance ratio (the split is
    driven by a fixed random seed).
    """
    a = load_predictions(config_a)
    b = load_predictions(config_b)

    if not np.array_equal(a["y_true"], b["y_true"]):
        raise ValueError(
            "McNemar's test requires identical test sets; "
            f"'{config_a}' and '{config_b}' differ."
        )

    y_true = a["y_true"]
    correct_a = a["y_pred"] == y_true
    correct_b = b["y_pred"] == y_true

    # 2x2 contingency table of agreement/disagreement.
    both_correct = int(np.sum(correct_a & correct_b))
    a_only = int(np.sum(correct_a & ~correct_b))
    b_only = int(np.sum(~correct_a & correct_b))
    both_wrong = int(np.sum(~correct_a & ~correct_b))

    table = [[both_correct, a_only], [b_only, both_wrong]]

    # The exact binomial test is used when the discordant counts are small,
    # where the chi-squared approximation is unreliable.
    discordant = a_only + b_only
    use_exact = discordant < 25
    result = mcnemar(table, exact=use_exact, correction=not use_exact)

    return {
        "model_a": config_a,
        "model_b": config_b,
        "both_correct": both_correct,
        "a_correct_b_wrong": a_only,
        "b_correct_a_wrong": b_only,
        "both_wrong": both_wrong,
        "n_discordant": discordant,
        "test": "exact binomial" if use_exact else "chi-squared (continuity corrected)",
        "statistic": round(float(result.statistic), 4),
        "p_value": float(result.pvalue),
        "significant": bool(result.pvalue < alpha),
        "favours": (
            "model_a" if a_only > b_only else "model_b" if b_only > a_only else "tie"
        ),
    }


def mcnemar_top_models(
    results: pd.DataFrame,
    metric: str = "f1",
    top_n: int = 2,
    alpha: float = ALPHA,
) -> pd.DataFrame:
    """Run McNemar's test between the best configurations within each dataset.

    Comparisons are made within a dataset because McNemar's test requires the
    same test instances.
    """
    rows = []
    for dataset, group in results.groupby("dataset"):
        best = group.nlargest(top_n, metric)
        for cfg_a, cfg_b in itertools.combinations(best["config_id"], 2):
            row = mcnemar_test(cfg_a, cfg_b, alpha=alpha)
            row["dataset"] = dataset
            row["comparison"] = f"top-{top_n} by {metric}"
            rows.append(row)
    return pd.DataFrame(rows)


def mcnemar_key_comparisons(
    all_results: pd.DataFrame,
    metric: str = "f1",
    alpha: float = ALPHA,
) -> pd.DataFrame:
    """Run the McNemar comparisons that carry the most interpretive weight.

    Ranking the top two configurations often pairs two nearly identical models
    (for example SMOTE and SMOTETomek can yield the same predictions when no
    Tomek links are removed), which produces a vacuous test. The comparisons
    below are chosen instead because each answers a distinct question:

    1. *best vs untreated baseline, same classifier* - did imbalance treatment
       actually change predictive behaviour?
    2. *best vs best of each other classifier* - is the leading classifier
       genuinely better, not just marginally ahead on a summary metric?
    3. *best vs worst* - how large is the spread across the design space?

    ``all_results`` should include the untreated baseline rows.
    """
    rows = []

    # Comparisons must stay within a single (dataset, seed) combination, because
    # a different seed produces a different train-test split and McNemar's test
    # requires both models to have been evaluated on identical instances.
    group_keys = ["dataset"]
    if "seed" in all_results.columns:
        group_keys.append("seed")

    for keys, group in all_results.groupby(group_keys):
        keys = keys if isinstance(keys, tuple) else (keys,)
        dataset = keys[0]
        seed = keys[1] if len(keys) > 1 else None

        treated = group[group["imbalance_method"] != "none"]
        if treated.empty:
            continue

        best = treated.loc[treated[metric].idxmax()]
        best_id = best["config_id"]

        def add(cfg_b, label):
            if cfg_b == best_id:
                return
            try:
                row = mcnemar_test(best_id, cfg_b, alpha=alpha)
            except FileNotFoundError:
                return
            row["dataset"] = dataset
            if seed is not None:
                row["seed"] = seed
            row["comparison"] = label
            rows.append(row)

        # 1. Best treated configuration vs the untreated baseline.
        baseline = group[
            (group["imbalance_method"] == "none")
            & (group["classifier"] == best["classifier"])
        ]
        if not baseline.empty:
            add(baseline.iloc[0]["config_id"], "best vs untreated baseline")

        # 2. Best configuration vs the best of each competing classifier.
        for clf, clf_group in treated.groupby("classifier"):
            if clf == best["classifier"]:
                continue
            add(
                clf_group.loc[clf_group[metric].idxmax()]["config_id"],
                f"best vs best {clf}",
            )

        # 3. Best vs worst overall.
        add(treated.loc[treated[metric].idxmin()]["config_id"], "best vs worst")

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Friedman test
# ---------------------------------------------------------------------------
def friedman_test(
    results: pd.DataFrame,
    group_col: str,
    block_cols: list[str],
    metric: str = "f1",
    alpha: float = ALPHA,
) -> dict:
    """Test whether the levels of ``group_col`` differ in ``metric``.

    Parameters
    ----------
    group_col
        The factor being compared, e.g. ``"classifier"`` or ``"imbalance_method"``.
    block_cols
        Columns identifying the matched blocks. For a classifier comparison the
        blocks are (dataset, imbalance method), so each classifier is measured
        once per block.
    """
    pivot = results.pivot_table(
        index=block_cols,
        columns=group_col,
        values=metric,
    ).dropna()

    if pivot.shape[0] < 2 or pivot.shape[1] < 3:
        return {
            "comparison": group_col,
            "metric": metric,
            "error": (
                "Friedman's test needs at least 3 groups and 2 blocks; "
                f"got {pivot.shape[1]} groups and {pivot.shape[0]} blocks."
            ),
        }

    samples = [pivot[c].to_numpy() for c in pivot.columns]
    statistic, p_value = friedmanchisquare(*samples)

    # Mean rank per group (rank 1 = best), the conventional Friedman summary.
    mean_ranks = pivot.rank(axis=1, ascending=False).mean().sort_values()

    return {
        "comparison": group_col,
        "metric": metric,
        "n_groups": int(pivot.shape[1]),
        "n_blocks": int(pivot.shape[0]),
        "statistic": round(float(statistic), 4),
        "p_value": float(p_value),
        "significant": bool(p_value < alpha),
        "mean_ranks": {k: round(float(v), 3) for k, v in mean_ranks.items()},
        "best_group": mean_ranks.index[0],
    }


# ---------------------------------------------------------------------------
# Post-hoc pairwise comparisons
# ---------------------------------------------------------------------------
def holm_bonferroni(p_values: list[float], alpha: float = ALPHA) -> list[bool]:
    """Return per-hypothesis significance flags under Holm-Bonferroni control.

    P-values are sorted ascending and compared against ``alpha / (m - i)``.
    Testing stops at the first non-rejection, and all remaining hypotheses are
    retained, which is what preserves the family-wise error rate.
    """
    m = len(p_values)
    order = np.argsort(p_values)
    flags = [False] * m

    for i, idx in enumerate(order):
        if p_values[idx] <= alpha / (m - i):
            flags[idx] = True
        else:
            break

    return flags


def posthoc_wilcoxon(
    results: pd.DataFrame,
    group_col: str,
    block_cols: list[str],
    metric: str = "f1",
    alpha: float = ALPHA,
) -> pd.DataFrame:
    """Pairwise Wilcoxon signed-rank tests with Holm-Bonferroni correction."""
    pivot = results.pivot_table(
        index=block_cols,
        columns=group_col,
        values=metric,
    ).dropna()

    pairs, raw_p, stats_ = [], [], []
    for a, b in itertools.combinations(pivot.columns, 2):
        x, y = pivot[a].to_numpy(), pivot[b].to_numpy()
        if np.allclose(x, y):
            # Wilcoxon is undefined when every difference is zero.
            statistic, p = 0.0, 1.0
        else:
            statistic, p = wilcoxon(x, y)
        pairs.append((a, b))
        stats_.append(float(statistic))
        raw_p.append(float(p))

    flags = holm_bonferroni(raw_p, alpha=alpha)

    return pd.DataFrame(
        {
            "group_a": [p[0] for p in pairs],
            "group_b": [p[1] for p in pairs],
            "mean_a": [round(pivot[p[0]].mean(), 4) for p in pairs],
            "mean_b": [round(pivot[p[1]].mean(), 4) for p in pairs],
            "statistic": stats_,
            "p_value": raw_p,
            "significant_holm": flags,
        }
    ).sort_values("p_value")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def run_all_tests(
    results_file: str = "results.csv",
    metric: str = "f1",
    exclude_baseline: bool = True,
    alpha: float = ALPHA,
    verbose: bool = True,
) -> dict:
    """Run the full statistical analysis and write the output tables."""
    all_results = pd.read_csv(RESULTS_DIR / results_file)

    if "error" in all_results.columns:
        all_results = all_results[all_results["error"].isna()]

    # The Friedman/post-hoc analysis compares treatment methods, so the
    # untreated baseline is excluded there but retained for McNemar comparisons.
    results = (
        all_results[all_results["imbalance_method"] != "none"]
        if exclude_baseline
        else all_results
    )

    # When the sweep has been repeated under several seeds, each seed forms an
    # additional matched block. This is what lifts the post-hoc tests out of the
    # very low power regime that a single replication suffers from.
    extra_block = ["seed"] if "seed" in results.columns and results["seed"].nunique() > 1 else []

    friedman_classifiers = friedman_test(
        results, "classifier", ["dataset", "imbalance_method"] + extra_block, metric, alpha
    )
    friedman_methods = friedman_test(
        results, "imbalance_method", ["dataset", "classifier"] + extra_block, metric, alpha
    )

    friedman_df = pd.DataFrame(
        [
            {
                "comparison_group": "Classifiers",
                "metric": metric,
                "n_groups": friedman_classifiers.get("n_groups"),
                "n_blocks": friedman_classifiers.get("n_blocks"),
                "statistic": friedman_classifiers.get("statistic"),
                "p_value": friedman_classifiers.get("p_value"),
                "significant": friedman_classifiers.get("significant"),
                "best_group": friedman_classifiers.get("best_group"),
            },
            {
                "comparison_group": "Imbalance methods",
                "metric": metric,
                "n_groups": friedman_methods.get("n_groups"),
                "n_blocks": friedman_methods.get("n_blocks"),
                "statistic": friedman_methods.get("statistic"),
                "p_value": friedman_methods.get("p_value"),
                "significant": friedman_methods.get("significant"),
                "best_group": friedman_methods.get("best_group"),
            },
        ]
    )
    friedman_df.to_csv(RESULTS_DIR / "friedman_tests.csv", index=False)

    posthoc_clf = posthoc_wilcoxon(
        results, "classifier", ["dataset", "imbalance_method"] + extra_block, metric, alpha
    )
    posthoc_mth = posthoc_wilcoxon(
        results, "imbalance_method", ["dataset", "classifier"] + extra_block, metric, alpha
    )
    posthoc_clf.to_csv(RESULTS_DIR / "posthoc_classifiers.csv", index=False)
    posthoc_mth.to_csv(RESULTS_DIR / "posthoc_methods.csv", index=False)

    mcnemar_df = mcnemar_key_comparisons(all_results, metric=metric, alpha=alpha)
    mcnemar_df.to_csv(RESULTS_DIR / "mcnemar_tests.csv", index=False)

    if verbose:
        _print_report(
            friedman_classifiers, friedman_methods, posthoc_clf, posthoc_mth, mcnemar_df, metric
        )

    return {
        "friedman_classifiers": friedman_classifiers,
        "friedman_methods": friedman_methods,
        "posthoc_classifiers": posthoc_clf,
        "posthoc_methods": posthoc_mth,
        "mcnemar": mcnemar_df,
    }


def _print_report(fried_clf, fried_mth, posthoc_clf, posthoc_mth, mcnemar_df, metric):
    def fmt_p(p):
        return "< 0.001" if p < 0.001 else f"{p:.4f}"

    print("=" * 78)
    print(f"STATISTICAL SIGNIFICANCE TESTING  (metric = {metric}, alpha = {ALPHA})")
    print("=" * 78)

    for title, res, labels in (
        ("Classifiers", fried_clf, CLASSIFIER_LABELS),
        ("Imbalance methods", fried_mth, METHOD_LABELS),
    ):
        print(f"\nFriedman test - {title}")
        if "error" in res:
            print(f"  {res['error']}")
            continue
        print(f"  H0: no difference in {metric} across {title.lower()}")
        print(f"  chi-squared = {res['statistic']}, p = {fmt_p(res['p_value'])}, "
              f"blocks = {res['n_blocks']}, groups = {res['n_groups']}")
        print(f"  -> H0 {'REJECTED' if res['significant'] else 'NOT rejected'} at alpha = {ALPHA}")
        print("  Mean ranks (1 = best):")
        for name, rank in res["mean_ranks"].items():
            print(f"    {labels.get(name, name):28s} {rank}")

    for title, df in (("classifiers", posthoc_clf), ("imbalance methods", posthoc_mth)):
        sig = df[df["significant_holm"]]
        print(f"\nPost-hoc Wilcoxon (Holm-corrected) - {title}: "
              f"{len(sig)} of {len(df)} pairs significant")
        for _, r in sig.iterrows():
            print(f"    {r['group_a']} ({r['mean_a']}) vs {r['group_b']} ({r['mean_b']}) "
                  f"p = {fmt_p(r['p_value'])}")

    print("\nMcNemar's test - paired comparisons on identical test sets")
    if mcnemar_df.empty:
        print("  No comparisons available.")
    else:
        for _, r in mcnemar_df.iterrows():
            print(f"  [{r['dataset']}] {r['comparison']}")
            print(f"    A: {r['model_a']}")
            print(f"    B: {r['model_b']}")
            print(f"    contingency: both correct = {r['both_correct']}, "
                  f"A only = {r['a_correct_b_wrong']}, B only = {r['b_correct_a_wrong']}, "
                  f"both wrong = {r['both_wrong']}")
            print(f"    {r['test']}: statistic = {r['statistic']}, p = {fmt_p(r['p_value'])}")
            print(f"    -> {'significant' if r['significant'] else 'not significant'} "
                  f"(favours {r['favours']})")

    print("\n" + "=" * 78)
    print(f"Tables written to {RESULTS_DIR}")
    print("=" * 78)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run statistical significance tests.")
    parser.add_argument("--results", default="results.csv")
    parser.add_argument("--metric", default="f1")
    parser.add_argument("--include-baseline", action="store_true")
    args = parser.parse_args()

    run_all_tests(
        results_file=args.results,
        metric=args.metric,
        exclude_baseline=not args.include_baseline,
    )
