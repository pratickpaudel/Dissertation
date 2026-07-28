# Implementation Guide

Working implementation of the experimental procedure described in Chapter 3 and
Chapter 4: a comparison of class imbalance treatment techniques for machine
learning based phishing website detection.

Each stage below corresponds to one node in the experimental procedure diagram
(`../figures/Figure_Experimental_Procedure.png`).

---

## 1. Setup

Python 3.11 is used. From the `code/` directory:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Package versions are pinned to match those reported in Chapter 4 (scikit-learn
1.3.0, imbalanced-learn 0.11.0, pandas 2.0.3, numpy 1.24.3, SHAP 0.42.1).

---

## 2. Run everything

The whole procedure can be executed with a single command:

```bash
.venv/bin/python run_pipeline.py
```

Runtime is roughly 5 minutes for the full 48-configuration sweep. Useful flags:

| Flag | Purpose |
|---|---|
| `--quick` | Small subset, for checking the setup works |
| `--skip-experiments` | Re-run only the analysis on existing `results.csv` |
| `--with-shap` | Also run the SHAP explainability stage |
| `--ratio 0.05` | Use a different induced imbalance ratio |

Everything below explains what each stage does and how to run it on its own.

---

## 3. Stage-by-stage

All individual modules are run from the `src/` directory.

### Step 1-2: Dataset loading and preprocessing

```bash
cd src
../.venv/bin/python data_loader.py
```

`data_loader.py` fetches both benchmarks and caches them in `data/`:

* **UCI Phishing Websites** — downloaded via `ucimlrepo` (id 327).
* **Hannousse & Yahiouche** — downloaded from the authors' Mendeley record.

Two decisions are enforced here:

**Label convention.** Phishing is the positive class (`1`), legitimate is `0`.
The UCI target uses `-1` for phishing, so it is remapped. Every recall,
precision, F1 and PR-AUC figure therefore refers to the phishing class.

**Induced imbalance.** Neither published dataset is actually imbalanced:

| Dataset | As published | % phishing |
|---|---|---|
| UCI | 11,055 rows, 30 features | 44.31% (1:1.26) |
| Hannousse & Yahiouche | 11,430 rows, 87 features | 50.00% (1:1.00) |

Since the research question concerns imbalance *treatment*, a 10% minority
share (≈1:9) is induced by randomly downsampling the phishing class. Only
minority instances are removed, so no data is fabricated before treatment. The
ratio is set by `MINORITY_RATIO` in `config.py`.

`preprocessing.py` then drops zero-variance and duplicate columns, handles any
non-finite values, and produces a **stratified 80/20 split** with
`random_state=42`. The test set is separated before any treatment or scaling.

### Step 3: Imbalance treatment

`imbalance.py` provides the seven techniques plus an untreated baseline:

| Method | Family |
|---|---|
| Random Oversampling | Data-level (resampling) |
| Random Undersampling | Data-level (resampling) |
| SMOTE | Data-level (synthetic) |
| ADASYN | Data-level (synthetic) |
| SMOTEENN | Hybrid |
| SMOTETomek | Hybrid |
| Cost-Sensitive Learning | Algorithm-level |

The first six return an imbalanced-learn sampler. Cost-sensitive learning is
different in kind — it changes the training objective rather than the data — so
it returns `None` and is applied through the classifier's `class_weight`
instead. Resampling and class weighting are therefore never combined.

### Step 4-5: Classifier selection, training and tuning

`models.py` builds the pipeline that keeps the experiment leakage-free:

```python
ImbPipeline([
    ("scaler",     StandardScaler()),   # fitted per fold
    ("sampler",    <sampler>),          # resamples that fold's training part only
    ("classifier", <estimator>),
])
```

This pipeline is passed to `GridSearchCV` with `StratifiedKFold(5)`. Because the
sampler lives *inside* the pipeline, resampling is re-executed within each fold
and applied only to that fold's training partition — synthetic samples never
reach the validation partition. Doing the resampling before cross-validation
would inflate the scores.

Tuned hyperparameters:

| Classifier | Parameters |
|---|---|
| Decision Tree | `max_depth`, `min_samples_split`, `criterion` |
| Random Forest | `n_estimators`, `max_depth`, `max_features` |
| SVM | `C`, `gamma`, `kernel` |

Selection uses F1 on the minority class. The winning configuration is refit on
the full training set (`refit=True`).

### Step 6: Evaluation

`evaluation.py` computes precision, recall, F1, ROC-AUC, PR-AUC, MCC, balanced
accuracy and the confusion matrix on the untouched test set. Accuracy is
recorded but not used to draw conclusions, since a majority-class predictor
scores highly on imbalanced data.

Threshold-free metrics use `predict_proba` where available and
`decision_function` for the SVM.

### Step 7: Run the experimental matrix

```bash
../.venv/bin/python experiment.py
```

Runs 2 datasets × 8 methods × 3 classifiers = 48 configurations (the 42 reported
in Chapter 4, plus 6 untreated baselines for reference). Outputs:

* `results/results.csv` — one row per configuration
* `results/predictions/*.npz` — per-configuration test predictions, needed
  because McNemar's test operates on paired predictions rather than summary
  scores

Subsets can be run with `--datasets`, `--methods`, `--classifiers`, `--ratio`.

### Step 8: Comparative performance analysis

```bash
../.venv/bin/python analysis.py
```

Generates the Chapter 5 tables as both `.csv` and `.md` (paste-ready):

| Output | Content |
|---|---|
| `table_5_1/5_2_performance_*` | Every configuration, per dataset |
| `table_5_3_by_classifier` | Mean performance per classifier |
| `table_5_4_by_method` | Mean performance per imbalance method |
| `table_5_5_best_worst` | Best and worst configuration per dataset |
| `table_treatment_effect` | Change vs the untreated baseline |

`table_treatment_effect` is the one that isolates the contribution of imbalance
treatment itself, by comparing each treated configuration against the same
classifier trained on untreated data.

### Step 9: Statistical significance testing

```bash
../.venv/bin/python statistical_tests.py
```

* **Friedman test** — whether classifiers differ overall, and whether imbalance
  methods differ overall, using matched blocks and mean ranks.
* **Post-hoc Wilcoxon** signed-rank tests with **Holm-Bonferroni** correction,
  identifying which specific pairs differ. Holm is used rather than plain
  Bonferroni because it is uniformly more powerful at the same error rate.
* **McNemar's test** — paired comparison on identical test instances. The exact
  binomial version is used when there are fewer than 25 discordant cases, where
  the chi-squared approximation is unreliable.

The McNemar comparisons are chosen to be informative rather than merely
top-ranked: best vs untreated baseline (did treatment change behaviour?), best
vs the best of each other classifier, and best vs worst.

### Step 10: SHAP explainability (Section 3.10)

```bash
# global + local attributions for one configuration
../.venv/bin/python explainability.py --dataset uci --method smote --classifier random_forest --plot

# does treatment change which features the model relies on?
../.venv/bin/python explainability.py --compare --dataset uci --classifier random_forest
```

`TreeExplainer` is used for Decision Tree and Random Forest (exact and fast).
The SVM falls back to `KernelExplainer`, which is an approximation and is **much
slower** — around 4 minutes for 40 instances. Prefer the tree models for SHAP
analysis, or reduce `sample_size`.

Local explanations report feature values on their **original scale**, not the
standardised values the model sees, so they are readable.

---

## 4. Project layout

```
code/
├── run_pipeline.py          # end-to-end orchestrator
├── requirements.txt
├── src/
│   ├── config.py            # all experimental constants
│   ├── data_loader.py       # loading + induced imbalance
│   ├── preprocessing.py     # cleaning + stratified split
│   ├── imbalance.py         # the seven techniques
│   ├── models.py            # pipeline, grids, GridSearchCV
│   ├── evaluation.py        # metrics
│   ├── experiment.py        # the configuration sweep
│   ├── analysis.py          # Chapter 5 tables
│   ├── statistical_tests.py # Friedman, Wilcoxon, McNemar
│   └── explainability.py    # SHAP
├── data/                    # cached datasets (downloaded on first run)
├── results/                 # results.csv, tables, test outputs
└── figures/                 # SHAP plots
```

---

## 5. Reproducibility

`RANDOM_STATE = 42` is applied to the induced downsampling, the train-test
split, the cross-validation folds, every sampler, and every classifier. Deleting
`results/` and re-running `run_pipeline.py` reproduces identical numbers.

---

## 6. Results obtained

Run at a 10% minority ratio (≈1:9), F1 used for model selection.

**By classifier** (treated configurations only):

| Classifier | Precision | Recall | F1 | ROC-AUC | PR-AUC | MCC |
|---|---|---|---|---|---|---|
| Decision Tree | 0.8021 | 0.8390 | 0.8147 | 0.9199 | 0.7370 | 0.7963 |
| **Random Forest** | **0.8861** | 0.8624 | **0.8692** | **0.9862** | **0.9427** | **0.8576** |
| Support Vector Machine | 0.8052 | **0.8691** | 0.8323 | 0.9795 | 0.8904 | 0.8156 |

**By imbalance method** (averaged over classifiers and datasets):

| Method | Precision | Recall | F1 | PR-AUC |
|---|---|---|---|---|
| No Treatment (Baseline) | 0.9195 | 0.8208 | 0.8664 | 0.8824 |
| Random Oversampling | 0.8754 | 0.8379 | 0.8558 | 0.8592 |
| Random Undersampling | 0.6610 | **0.8948** | 0.7575 | 0.8307 |
| SMOTE | 0.8773 | 0.8503 | 0.8603 | 0.8664 |
| ADASYN | 0.8753 | 0.8448 | 0.8585 | 0.8735 |
| SMOTEENN | 0.7890 | 0.8830 | 0.8321 | 0.8383 |
| SMOTETomek | 0.8784 | 0.8503 | **0.8609** | 0.8659 |
| Cost-Sensitive Learning | 0.8615 | 0.8367 | 0.8462 | 0.8631 |

**Best and worst configurations:**

| Dataset | Best | F1 | Worst | F1 | Gap |
|---|---|---|---|---|---|
| UCI | Decision Tree + SMOTE | 0.9134 | Decision Tree + Random Undersampling | 0.7476 | 0.1658 |
| Hannousse & Yahiouche | Random Forest + SMOTETomek | 0.8984 | Decision Tree + Random Undersampling | 0.6728 | 0.2257 |

**Statistical tests:**

| Test | Statistic | p | Significant |
|---|---|---|---|
| Friedman — classifiers | χ² = 8.14 | 0.0171 | yes |
| Friedman — imbalance methods | χ² = 19.16 | 0.0039 | yes |
| Post-hoc: Random Forest vs SVM | — | < 0.001 | yes |
| McNemar: UCI best vs untreated baseline | — | 0.0075 | yes |
| McNemar: Hannousse best vs worst | — | < 0.001 | yes |

Mean Friedman ranks (1 = best): Random Forest 1.43, Decision Tree 2.07, SVM
2.50; SMOTETomek 2.42 best method, Random Undersampling 7.00 worst.

**SHAP, UCI / Random Forest:** the four highest-ranked features
(`sslfinal_state`, `url_of_anchor`, `web_traffic`, `having_sub_domain`) hold
identical rank across all treatment methods, while mid-ranked features move by
up to four positions. Imbalance treatment therefore perturbs the ordering of
weaker features without changing which evidence dominates the decision.

---

## 7. Interpreting these results

Three points need care in the write-up.

**Treatment trades precision for recall.** Every technique raised recall over
the untreated baseline (+0.016 to +0.074 mean), but all of them lowered
precision, so the baseline retains the highest mean F1 (0.8664). This is not a
null result — it is the central trade-off, and it means the choice of technique
should follow from the relative cost of a missed phishing site versus a false
alarm. For phishing detection, recall usually dominates, which favours
treatment even at some precision cost.

**Random undersampling is the clearest failure case.** It produced the best
recall (0.8948) and the worst precision (0.6610), because discarding roughly 90%
of the legitimate training data removes the information needed to rule phishing
out. It is the worst configuration on both datasets.

**Post-hoc power for methods is limited.** Comparing seven methods across only
six blocks (2 datasets × 3 classifiers) left 0 of 21 pairs significant after
Holm correction, even though the overall Friedman test was significant. Report
this honestly. To strengthen it, repeat the sweep under several random seeds and
treat each seed as an additional block — the code supports this via `--output`:

```bash
for seed in 1 2 3; do
  # edit RANDOM_STATE in config.py, or parameterise it
  .venv/bin/python src/experiment.py --output results_seed${seed}.csv
done
```

---

## 8. Optional sensitivity analysis

`SENSITIVITY_RATIOS` in `config.py` supports re-running at other imbalance
levels, which lets Chapter 6 discuss how technique effectiveness changes with
imbalance severity:

```bash
../.venv/bin/python experiment.py --ratio 0.05 --classifiers random_forest --output results_r05.csv
../.venv/bin/python experiment.py --ratio 0.20 --classifiers random_forest --output results_r20.csv
```

Restricting to one classifier keeps this to 8 runs per ratio.
