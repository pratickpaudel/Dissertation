# Interim Report revisions

Corrections for `Interim Report.docx` and one leftover in
`Design and Implementation Draft V1.docx`.

Most of the Chapter 3 revisions have been applied correctly. Sections 3.4, 3.5 and
3.9 now describe the right datasets, the stratified reduction, the three seeded
replications and the full statistical testing procedure. Figure 3.1 is in place in
Section 3.9.

What remains are seven items. The first is the most serious: **the aim of the
project still names the two datasets the methodology explains were rejected.**

Items are ordered by severity.

---

## 1. Section 1, Introduction — the aim names the rejected datasets

**Severity: high.** This is the single most damaging inconsistency in the report.
Section 3.4.1 explains at length why the UCI and Hannousse datasets were excluded,
but the stated aim of the project still says they will be used. A reader
encountering both will not know which is true.

Find this in the third paragraph of Section 1:

> The overall aim of this project is to investigate the impact of class imbalance
> treatment techniques on the performance of various machine learning models for
> phishing website detection. Specifically, in this study, we will use the UCI
> Phishing Websites dataset and the Hannousse and Yahiouche 87-feature benchmark
> dataset to compare the effectiveness of different class balancing strategies
> under various conditions.

**Replace with:**

The overall aim of this project is to investigate the impact of class imbalance
treatment techniques on the performance of various machine learning models for
phishing website detection. Specifically, this study uses two naturally imbalanced
benchmark datasets, that of Vrbančič et al. (2020) with 88,647 instances and 111
features, and URL-Phish (2025) with 116,600 URLs and 22 features, to compare the
effectiveness of different class balancing strategies. The two datasets differ in
both the severity of their class imbalance, at approximately 1:1.89 and 1:6.02, and
in the richness of their feature representation, which allows the study to examine
whether the effectiveness of a balancing strategy depends on either factor.

---

## 2. Section 1, Introduction — the status paragraph describes finished work as pending

Find this near the end of Section 1:

> The literature review and methodology have been completed. This project is
> underway and is currently in the implementation/evaluation phase. Left to-do is
> the execution of all 42 experimental setups, analysis of the results by the
> chosen metrics and application of McNemar's test for pairwise comparison of
> classifiers.

The experiments have since been executed. The paragraph also mentions only
McNemar's test, whereas Section 3.9 now describes Friedman's test and a post-hoc
procedure as well.

**Replace with:**

The literature review and methodology have been completed, and the experimental
work has been carried out. All 42 configurations have been executed, together with
an untreated baseline for each dataset and classifier, and the complete matrix has
been replicated under three random seeds, giving 144 individual runs. The remaining
work consists of analysing and interpreting these results and writing the results,
discussion and conclusion chapters.

---

## 3. Section 3.5 — the software versions are incorrect

**Severity: high.** This is a reproducibility claim, and it is currently false. The
report states Python 3.12 with scikit-learn 1.4.2 and imbalanced-learn 0.12.3. The
environment actually used is Python 3.11 with scikit-learn 1.3.0 and
imbalanced-learn 0.11.0. Anyone attempting to reproduce the study from these
figures would install a different environment from the one that produced the
results.

Replace the final paragraph of Section 3.5 with:

All experiments are carried out using Python 3.11. Model training,
cross-validation and evaluation use scikit-learn 1.3.0. The data-level resampling
methods, namely random oversampling, random undersampling, SMOTE, ADASYN, SMOTEENN
and SMOTETomek, are implemented using imbalanced-learn 0.11.0. Cost-sensitive
learning is applied through the class_weight parameter of the scikit-learn
classifiers rather than by resampling. Data handling uses pandas 2.0.3 and NumPy
1.24.3. The statistical tests use SciPy 1.10.1 and statsmodels 0.14.0, and the
feature attribution analysis uses SHAP 0.42.1. Specific versions are recorded so
that the experimental environment can be reconstructed. These libraries are widely
used in phishing detection research and support reproducible and independently
verifiable experiments.

**Verified versions, for reference:**

| Library | Version |
|---|---|
| Python | 3.11 |
| scikit-learn | 1.3.0 |
| imbalanced-learn | 0.11.0 |
| pandas | 2.0.3 |
| NumPy | 1.24.3 |
| SciPy | 1.10.1 |
| statsmodels | 0.14.0 |
| SHAP | 0.42.1 |

---

## 4. Section 3.12 — the summary refers to a section that no longer exists

Section 3.10 on explainability and the dashboard has been removed, but the chapter
summary still reports it, and in the past tense.

Find and **delete** this paragraph entirely:

> Furthermore, the chapter has recorded the explainability and dashboard evaluation
> phase, where a dashboard was created with Streamlit and SHAP to aid in the
> operational understanding of model behaviour. The next chapter will present the
> experimental results and their analysis.

**Replace with** a single closing sentence appended to the preceding paragraph, or
kept as its own short paragraph:

The next chapter presents the experimental results and their analysis.

If you decide to reinstate a brief explainability subsection, see item 6 below.

---

## 5. Section 4, Plan for Completion — three separate problems

This section needs rewriting rather than patching. It promises a Streamlit
dashboard twice, describes completed work as still to be done, and includes a
phrase suggesting the research question is not yet settled.

**Replace the whole of Section 4 with:**

### 4. Plan for Completion

The literature review and methodology are complete, and the experimental work has
been carried out. The full comparison matrix has been executed: 42 configurations
drawn from two datasets, seven imbalance treatment techniques and three
classifiers, together with an untreated baseline for each dataset and classifier,
replicated under three random seeds for a total of 144 runs. Performance has been
recorded for every configuration using precision, recall, F1-score, ROC-AUC, PR-AUC
and the Matthews Correlation Coefficient, and the statistical testing described in
Section 3.9 has been applied.

The remaining work is analytical and expository rather than technical. The results
chapter will present the comparison in three layers: performance by dataset,
aggregate performance by classifier and by imbalance treatment technique, and an
identification of the strongest and weakest configurations. The outcomes of
Friedman's test, the post-hoc pairwise comparisons and McNemar's test will be
reported alongside these tables, so that differences in mean performance are
qualified by whether they are statistically supported.

The discussion chapter will interpret these findings against the literature
reviewed in Section 2. Particular attention will be given to the trade-off between
precision and recall that imbalance treatment produces, to whether the severity of
imbalance affects how much the choice of technique matters, and to whether
treatment alters which features a model relies upon or only the position of its
decision boundary. The conclusion will then answer the research question directly
and identify the limitations that bound that answer.

Should any part of the analysis prove inconclusive, the cause will be investigated
rather than left unexplained, considering class overlap, feature redundancy,
insensitivity to the degree of imbalance, and instability across folds. Weak
performance from a particular technique will be reported as evidence that the
technique is poorly suited to this problem configuration, which is itself a finding,
and the limitations identified will inform the recommendations for future work.

**Note on one phrase.** The current text ends by saying the remaining work is
concentrated in "re-defining the research question, implementation, and
evaluation/interpretation". Redefining the research question at this stage would
concern an examiner, since the question should be settled before the experiments
are run. The replacement above removes it.

---

## 6. SHAP is now unanchored

Deleting Section 3.10 removed the only methodological grounding for the SHAP
analysis, but Section 4 of the interim report still refers to SHAP, and the
explainability results and the SHAP summary figure are intended for the results
chapter. As it stands, a figure would appear in the results with nothing in the
methodology to justify the technique that produced it.

Two consistent options:

**Option A — reinstate a short subsection.** Add the following as Section 3.10,
before Validity and Reliability, and renumber the two sections that follow. It makes
no mention of a dashboard and claims nothing about usability.

### 3.10 Explainability Analysis

Alongside the quantitative comparison, the best-performing models are examined
using SHAP (SHapley Additive exPlanations) to determine the contribution of
individual features to model predictions. SHAP is selected because it attributes a
prediction additively across features, so the contributions sum to the difference
between that prediction and the average prediction, which makes the resulting
explanation internally consistent rather than merely indicative.

The analysis serves a specific purpose within this study rather than being
presented for its own sake. By computing attributions separately for models trained
under different imbalance treatment techniques, while holding the dataset and
classifier constant, it becomes possible to establish whether those techniques
alter the evidential basis of a decision or only the position of the decision
boundary. If the ranking of features is stable across treatments, the techniques
change how readily a model commits to the minority class without changing what it
treats as evidence. Establishing which of these holds contributes directly to
characterising what imbalance treatment does, and the results are reported in
Chapter 5.

**Option B — remove SHAP entirely.** Delete the reference to SHAP from Section 4,
omit the explainability results from Chapter 5, and do not use the SHAP summary
figure. This is internally consistent but discards a finding that bears on the
research question.

Option A is recommended. It costs two paragraphs and no additional work, since the
analysis has already been run.

---

## 7. Figure 3.1 — caption placement and attribution

Two small conventions:

- The caption currently appears **above** the figure and before the paragraph that
  introduces it. Move it **below** the figure, and place the figure after the
  paragraph beginning "The experiment proceeds in a fixed sequence, shown in
  Figure 3.1."
- The caption is missing its source line. It should read:

> **Figure 3.1** Overview of the experimental procedure.
> Source: Author's own work.

The other figures in the report already follow this convention, so this is only for
consistency.

---

## 8. Chapter 4 — one leftover paragraph in Section 4.4

`Design and Implementation Draft V1.docx` is otherwise correct. Sections 4.1 to
4.14 are in place, Section 4.12 covers the explainability implementation, Figure 4.4
has been removed, the software list reads Python 3.11, and no editing annotations
remain.

One paragraph from the previous version has been left at the end of Section 4.4:

> Where feature scaling is needed, it is applied only after splitting and only using
> statistics derived from the training data. This is especially relevant for the
> Support Vector Machine classifier, which is sensitive to feature magnitude.
> Tree-based models such as Decision Tree and Random Forest are generally less
> dependent on scaling, but the same preprocessing logic is maintained across all
> experiments.

This now conflicts with the paragraph above it, which states that scaling is
deliberately deferred and fitted inside each cross-validation fold. Read together,
the section says scaling happens at two different points.

**Delete that paragraph.** If you want to retain the point about the Support Vector
Machine, add this single sentence to the end of the paragraph that begins "The
stratified train-test split is applied last":

Scaling matters most for the Support Vector Machine, which is sensitive to feature
magnitude, but it is applied uniformly so that every classifier is trained under
identical preprocessing.

---

## 9. Optional: Table 4.2 in Chapter 4

Section 4.3 of Chapter 4 names the two excluded datasets in prose but the
corresponding table was not added, so the tables were not renumbered and Table 4.2
remains "Imbalance treatment methods". This is perfectly acceptable, since the
prose carries the point and the same information appears in Table 3.2 of the
methodology. No action needed unless you would prefer the table for emphasis.

---

## 10. Checklist

After applying the above, search the interim report and confirm:

- [ ] "UCI" and "Hannousse" appear only in Section 3.4.1 and the reference list
- [ ] The aim in Section 1 names Vrbančič and URL-Phish
- [ ] No occurrence of "Streamlit" or "dashboard" anywhere
- [ ] Python version reads 3.11, scikit-learn 1.3.0, imbalanced-learn 0.11.0
- [ ] No statement that the experiments are still to be run
- [ ] No reference to redefining the research question
- [ ] Statistical testing described as Friedman, post-hoc Wilcoxon and McNemar
- [ ] Figure 3.1 has a source line and sits below its caption position
- [ ] Section numbering after 3.9 is consistent with whichever option in item 6 you choose
- [ ] The contents page reflects any renumbering
