# Dissertation

Comparative study of class imbalance treatment techniques for machine learning-based
phishing website detection.

## Repository Structure

```
.
├── chapters/                 # Dissertation chapters (.md are paste-ready, .docx are drafts)
│   ├── Interim Report.docx                          # Chapters 2-3 as submitted at interim
│   ├── InterimReport_Revisions.md                    # Pending edits to the interim report
│   ├── Chapter3_Revisions.md                        # Pending edits to Chapter 3
│   ├── Design and Implementation Draft V1.docx      # Chapter 4
│   ├── Chapter4_Revisions.md                        # Applied edits to Chapter 4
│   ├── Chapter4_Deduplication.md                    # De-duplication of Ch4 against Ch3
│   ├── Chapter4_Final_Fix.md                        # Final Ch4 corrections
│   ├── Chapter5_Testing.md                          # Chapter 5 — Testing
│   ├── Chapter6_Results_and_Analysis.md             # Chapter 6 — Results and Analysis
│   ├── Chapter7_Conclusions_and_Recommendations.md  # Chapter 7 — Conclusions
│   └── Chapter8_Critical_Self_Evaluation.md         # Chapter 8 — Critical Self Evaluation
├── figures/                  # Diagrams and figures
│   ├── Figure_3_1_Experimental_Procedure.*          # Fig 3.1 (Section 3.9) experimental procedure
│   ├── Figure_4_1_System_Architecture.*             # Fig 4.1 modular pipeline
│   ├── Figure_4_2_Preprocessing_Workflow.*          # Fig 4.2 preprocessing
│   ├── Figure_4_3_Classifier_Comparison.*           # Fig 4.3 classifier comparison
│   │   (diagrams available as .svg source, .png, _HighRes.png and .pdf)
│   └── Figure_6_1_SHAP_Summary_URLPhish.*           # Fig 6.1 SHAP summary (.png 300dpi, .pdf)
└── code/                     # Implementation of the experimental pipeline
    ├── README.md             # Step-by-step implementation guide
    ├── run_pipeline.py       # End-to-end runner
    ├── src/                  # Pipeline modules
    ├── results/              # Generated result tables and statistical tests
    ├── figures/              # Generated SHAP plots
    └── extras/               # Material built but excluded from the dissertation
```

See [`code/README.md`](code/README.md) for setup instructions, a stage-by-stage
walkthrough of the implementation, and the results obtained.

## Chapter Structure

Chapters map one-to-one onto the assessment criteria.

| Ch | Title | Weight |
|---|---|---|
| 1 | Introduction | 5% |
| 2 | Literature Review | 15% |
| 3 | Research Design and Methodology | 10% |
| 4 | Design and Implementation | 20% |
| 5 | Testing | 10% |
| 6 | Results and Analysis | 10% |
| 7 | Conclusions and Recommendations | 10% |
| 8 | Critical Self Evaluation | 10% |
| — | Structure, Style and References | 10% |

There is no separate Discussion chapter. Its content is distributed between the analysis
sections of Chapter 6, the recommendations in Chapter 7, and the limitations in Chapter 8.

## Study Overview

- **Datasets (2, both naturally imbalanced):**
  - Vrbančič phishing dataset — 88,647 instances, 111 features (92 after cleaning),
    34.57% phishing, imbalance ratio 1:1.89
  - URL-Phish — 116,600 URLs, 22 lexical and structural features, 14.24% phishing,
    imbalance ratio 1:6.02
- **Imbalance treatment techniques (7):** Random Oversampling, Random Undersampling,
  SMOTE, ADASYN, SMOTEENN, SMOTETomek, Cost-Sensitive Learning
- **Baseline:** an untreated condition is included for every classifier and dataset,
  giving 8 conditions rather than 7
- **Classifiers (3):** Decision Tree, Random Forest, Support Vector Machine
- **Experimental matrix:** 2 datasets × 8 conditions × 3 classifiers × 3 random seeds
  (42, 1, 2) = **144 runs**, all completed without failure
- **Sampling:** stratified 20,000-instance subsample per dataset, preserving class ratios
  to within 0.01 percentage points, adopted because Support Vector Machine training scales
  quadratically
- **Evaluation metrics:** Precision, Recall, F1-score, ROC-AUC, PR-AUC, MCC
- **Statistical testing:** Friedman test, post-hoc Wilcoxon signed-rank with
  Holm-Bonferroni correction, and McNemar's test on paired predictions (α = 0.05)
- **Explainability:** SHAP attributions, compared across treatment techniques

Imbalance is **natural, not induced.** An earlier design used two near-balanced benchmark
datasets with imbalance induced by downsampling the minority class; both the datasets and
the induced-imbalance approach were rejected, since downsampling produces a minority class
that is smaller but statistically unchanged in character, which is not what treatment
techniques are intended to address. See Section 8.2 of the dissertation.

## Principal Findings

- Random Forest is the strongest classifier on every metric (mean F1 0.9204, PR-AUC 0.9749)
  and significantly better than both alternatives; Decision Tree and Support Vector Machine
  cannot be separated (p = 0.729)
- **No treatment technique improved mean F1 over the untreated baseline** (0.9172). Every
  technique raised recall and lowered precision. McNemar's test found no significant
  difference between the best treated configuration and its baseline in any of six
  replications
- Among techniques, SMOTETomek (0.9112) and SMOTE (0.9108) are jointly best and not
  statistically separable; random undersampling (0.8824) is reliably worst
- The mechanism is displacement of the operating point, not degraded discrimination.
  ROC-AUC varies by only 0.0057 across all eight conditions, SHAP feature rankings are
  invariant, and displacement past the true prevalence accounts for the F1 loss at
  r = −0.765 across 126 treated runs (r = −0.963 across the seven techniques)
- Treatment remains justified under modest cost asymmetry: break-even cost ratios fall
  between 1.43 and 3.59, so SMOTETomek pays for itself once a missed phishing site is
  judged more than 1.64 times as costly as a false alarm
- Imbalance severity moderates the magnitude but not the direction. The best-to-worst F1
  gap is 0.0419 at 1:1.89 and 0.1052 at 1:6.02

## Experimental Procedure

`figures/Figure_3_1_Experimental_Procedure.*` illustrates the end-to-end workflow: dataset
loading and preprocessing, stratified 80/20 train-test split, application of one imbalance
treatment technique **to the training partition only**, classifier selection, model
training with hyperparameter optimisation under stratified 5-fold cross-validation,
evaluation on the untouched test set, comparative performance analysis, and statistical
significance testing. The process is repeated for every combination of dataset, imbalance
technique, classifier and random seed.

Verification of the implementation is reported in Chapter 5, including validation of URL
feature extraction against 2,000 published URLs across 44,000 individual comparisons
(match rate 1.0000), confirmation that stratification and the train-test boundary hold
across all 144 runs, and reproducibility of re-executed configurations.
