# Chapter 3 revisions

Replacement text for the sections of `Methodology Final.docx` that no longer
match the study as implemented. Paste each block over the section it names.

The Methodology file is a Word document with its own styling, so the text is
supplied here rather than edited in place, to avoid disturbing formatting.

Three things drive these revisions:

1. The datasets changed. Both original datasets are close to balanced, which
   leaves the imbalance treatment techniques with nothing to correct.
2. Each dataset is now reduced by stratified sampling to keep training tractable.
3. The experiment is now replicated under three random seeds, which changes both
   the reproducibility statement and the statistical testing.

---

## 1. Section 3.4 — Research Datasets

**Replace the whole of 3.4, including subsections 3.4.1 and 3.4.2.**

### 3.4 Research Datasets

Two datasets are used in this study. Dataset selection was governed by a
requirement that follows directly from the research question: because the study
evaluates techniques for treating class imbalance, the datasets themselves must
exhibit class imbalance. This requirement excluded several of the most widely
cited phishing benchmarks, and the selection is therefore explained before the
chosen datasets are described.

The two datasets used differ in three respects that strengthen the comparison.
Both are imbalanced as published, so the treatment techniques operate on genuine
skew rather than on an artificially constructed distribution. They differ
substantially in the severity of that skew, which permits analysis of whether the
effectiveness of a technique depends on how severe the imbalance is. They also
differ considerably in feature richness, which supports cross-dataset
interpretation and reduces the likelihood that conclusions are specific to a
single feature representation.

### 3.4.1 Datasets Considered and Excluded

Two benchmarks were examined first and then rejected. The UCI Phishing Websites
dataset contains 11,055 instances described by 30 integer-valued attributes, of
which 4,898 are phishing and 6,157 legitimate. This is 44.31% phishing, an
imbalance ratio of approximately 1:1.26. The benchmark of Hannousse and Yahiouche
contains 11,430 URLs described by 87 features and is balanced by design, at
exactly 50% phishing.

Neither is suitable for the present study. Oversampling methods such as SMOTE and
ADASYN operate by generating minority instances until the classes are comparable
in size; on data that is already close to balanced they have almost nothing to
do. Cost-sensitive learning is affected more severely still, because the class
weights it derives approach unity on balanced data, making the condition
equivalent to no treatment at all. Retaining these datasets would therefore have
produced a comparison in which the techniques could not meaningfully differ, and
any absence of difference in the results would have been an artefact of the data
rather than a finding about the techniques.

Both remain valuable benchmarks for phishing classification accuracy in general,
and both are widely used for that purpose. The objection is specific to the
research question of this dissertation.

### 3.4.2 Vrbancic et al. Dataset

The first dataset used is that of Vrbancic, Fister and Podgorelec (2020),
published in Data in Brief. It contains 88,647 instances described by 111 numeric
features. Of these, 96 are extracted from the domain name and the hosting
infrastructure and 15 describe the web page itself, covering URL syntax,
character-level composition, domain properties and network attributes.

The dataset contains 30,647 phishing and 58,000 legitimate instances, giving
34.57% phishing and an imbalance ratio of approximately 1:1.89. There are no
missing values, so the data can be used for controlled experiments without
imputation. The dataset is well cited in the phishing detection literature, which
supports comparison with prior work, and its large feature set allows the effect
of imbalance treatment to be observed in a high-dimensional space.

### 3.4.3 URL-Phish Dataset

The second dataset is URL-Phish (2025), published through Mendeley Data. It
contains 116,600 URLs described by 22 numeric lexical and structural features,
including URL length, domain length, subdomain count, digit ratio, character
entropy and HTTPS usage. The phishing samples were drawn from the PhishTank
repository between November 2024 and September 2025.

The dataset contains 16,600 phishing and 100,000 legitimate instances, giving
14.24% phishing and an imbalance ratio of approximately 1:6.02. It is therefore
substantially more skewed than the Vrbancic dataset, and closer to the
distribution a detection system would encounter in operation, where legitimate
traffic greatly outnumbers phishing attempts. Its recency also addresses a
recurring criticism of phishing research, namely that widely used benchmarks
predate current phishing tactics.

It should be noted that the publication accompanying URL-Phish describes 111,660
URLs of which 11,660 are phishing, whereas the distributed data file contains
116,600 rows of which 16,600 are phishing. The counts reported here were measured
directly from the file and are the figures used throughout this study.

### Table 3.2 Dataset summary

| Dataset | Instances | Features | Phishing | Legitimate | % phishing | Ratio |
|---|---|---|---|---|---|---|
| Vrbancic et al. (2020) | 88,647 | 111 | 30,647 | 58,000 | 34.57% | 1:1.89 |
| URL-Phish (2025) | 116,600 | 22 | 16,600 | 100,000 | 14.24% | 1:6.02 |

### Table 3.3 Datasets considered and excluded

| Dataset | Instances | Features | % phishing | Ratio | Reason for exclusion |
|---|---|---|---|---|---|
| UCI Phishing Websites | 11,055 | 30 | 44.31% | 1:1.26 | Close to balanced; leaves imbalance treatment with little to correct |
| Hannousse and Yahiouche | 11,430 | 87 | 50.00% | 1:1.00 | Balanced by design; cost-sensitive weighting reduces to no treatment |

---

## 2. Section 3.5 — Data Preparation

**Replace paragraphs two and five.** Paragraphs three and four, on scaling and on
maintaining one pipeline across models, remain accurate.

### Replacement for paragraph two (the 80/20 split paragraph)

Each dataset is first reduced to 20,000 instances by stratified sampling. This
step is a computational measure rather than a methodological one. The Support
Vector Machine has approximately quadratic complexity in the number of training
instances, and the full comparison matrix is executed repeatedly, so the complete
datasets of 88,647 and 116,600 rows would make the study impractical to run.
Sampling is proportional within each class, so the natural imbalance is preserved
exactly: the reduced Vrbancic data retains 34.57% phishing instances and the
reduced URL-Phish data 14.23%. Only the volume of data is reduced, and the class
distribution under study is unaffected.

The datasets are then split into training and test sets in an 80/20 ratio using a
stratified split. Stratification maintains the class distribution of the full
dataset in both partitions and guarantees that the minority class is represented
in the test set. The test set is separated before any imbalance treatment or
feature scaling is applied and is not examined again until final evaluation,
which prevents information from the test partition influencing training and
avoids the optimistic bias that would follow.

To support reproducibility, all randomness is seeded. The complete comparison
matrix is executed three times, under the seeds 42, 1 and 2. Each seed controls
the stratified subsampling, the train-test split, the cross-validation folds, the
resampling procedures and the classifiers, so each execution constitutes an
independent replication rather than a repeat of the same partition. Reported
metrics are means across the three replications. This design also strengthens the
statistical analysis, since each replication contributes an additional matched
block to the tests described in Section 3.9.

### Replacement for paragraph five (the software paragraph)

All experiments are carried out using Python 3.11. Model training, cross-
validation and evaluation use scikit-learn 1.3.0. The data-level resampling
methods, namely random oversampling, random undersampling, SMOTE, ADASYN,
SMOTEENN and SMOTETomek, are implemented using imbalanced-learn 0.11.0.
Cost-sensitive learning is applied through the class_weight parameter of the
scikit-learn classifiers rather than by resampling. Data handling uses pandas
2.0.3 and NumPy 1.24.3, statistical testing uses SciPy 1.10.1 and statsmodels
0.14.0, and the explainability analysis uses SHAP 0.42.1. Specific versions are
recorded so that the experimental environment can be reconstructed. These
libraries are widely used in phishing detection research and support reproducible
and independently verifiable experiments.

---

## 3. Section 3.9 — Experimental Procedure

**Replace the whole section.** This is where Figure 3.1 belongs.

### 3.9 Experimental Procedure

The experiment proceeds in a fixed sequence, shown in Figure 3.1. First, each
dataset is loaded and preprocessed as described in Section 3.5, which includes
the stratified reduction to 20,000 instances. Second, the data are split 80/20
using a stratified split. Third, an imbalance treatment technique is applied to
the training partition only. Fourth, a classifier is trained on the treated
training data, with stratified 5-fold cross-validation used to guide
hyperparameter selection and to reduce sensitivity to any particular split.
Fifth, the selected configuration is refitted on the full treated training set
and evaluated once on the untouched test set, using the same metrics under every
experimental condition.

Resampling is executed inside the cross-validation procedure rather than before
it. Each fold applies scaling and resampling to its own training partition only,
so synthetic instances never enter the partition against which that fold is
validated. Performing the resampling beforehand would allow synthetic instances
derived from validation data to influence training and would inflate the
resulting estimates.

This procedure is repeated for every combination of dataset, imbalance treatment
technique and classifier, giving 42 experimental configurations from two
datasets, seven techniques and three classifiers. An untreated condition is
additionally run for each dataset and classifier, so that the effect attributable
to imbalance treatment can be isolated by direct comparison. Because the whole
matrix is replicated under three random seeds, 144 individual runs are executed.
The result is a complete comparison matrix showing how each balancing method
performs under each modelling condition, which supports comparison both within
and across datasets.

Statistical testing is used to establish whether observed differences are
meaningful rather than attributable to chance. Friedman's test, a non-parametric
test for differences across more than two related groups, is applied twice: once
to compare the three classifiers and once to compare the seven imbalance
treatment techniques. In each case performance is ranked within matched blocks
formed by the remaining factors and the replications. Where Friedman's test
indicates a significant difference, post-hoc pairwise Wilcoxon signed-rank tests
with Holm-Bonferroni correction identify which specific pairs differ; Holm's
correction is preferred to a plain Bonferroni adjustment because it is uniformly
more powerful while still controlling the family-wise error rate.

McNemar's test is used for paired comparison of individual models evaluated on
identical test instances. It is appropriate for this purpose because it examines
the cases on which two models disagree, rather than comparing summary metrics
computed independently, and therefore accounts for the correlation between
predictions made on shared data. Because it requires both models to have seen the
same test instances, these comparisons are made within a single replication.

A significance level of p < 0.05 is applied throughout. Differences that do not
reach this threshold are reported as descriptive trends rather than as confirmed
effects, so that conclusions remain appropriately qualified.

**Figure 3.1** Experimental procedure for comparative evaluation.
Source: Author's own work.

---

## 4. Section 3.10 — smaller wording changes

Two points, both discussed previously.

**Grammar.** Replace:

> This will enable to describe the character of a website (whether it is a
> phishing or a legitimate site) and compare the changes of feature importance
> over classifiers and imbalance treatment methods.

with:

> This makes it possible to explain why a given website is classified as phishing
> or legitimate, and to compare how feature importance shifts across classifiers
> and imbalance treatment methods.

**Usability claim.** The sentence describing the dashboard as providing "a
practical evaluation layer for interpretability and usability" invites the
question of how usability was evaluated. Unless a user study with participants
and an instrument such as SUS is planned, it is safer to present the dashboard as
a demonstration artefact:

> The SHAP outputs are surfaced through a Streamlit-based dashboard that serves as
> a demonstration interface, presenting predictions and feature attributions
> alongside summary performance metrics. The dashboard illustrates how the
> explainability outputs could support interpretation in an operational setting;
> it is not subjected to a formal usability study, which lies beyond the scope of
> this dissertation.

---

## 5. Two errors found while reading the chapter

**Section 3.4.1 has the UCI class proportions inverted.** The chapter states
"56% phishing, 44% legitimate". The dataset actually contains 4,898 phishing and
6,157 legitimate instances, which is 44.31% phishing and 55.69% legitimate. The
figures are the right pair of numbers assigned to the wrong classes. This is
corrected in the replacement text above. Worth noting in case the same
proportions are quoted elsewhere, for example in the literature review.

**Sections 3.9 and 4.10 describe the same sequence.** With Figure 3.1 now in
Section 3.9, Section 4.10 of Chapter 4 has been changed to cross-reference it
rather than repeat it. If both sections are kept, the cleanest division is for 3.9
to state the design and its justification, and for 4.10 to carry implementation
specifics only, such as the configuration counts, the loop structure and what is
persisted for later analysis.

---

## 6. Consistency checklist

After applying the above, check these claims wherever else they appear,
particularly in the abstract, introduction and literature review:

- [ ] No remaining reference to UCI or Hannousse as a dataset **used** in the study
- [ ] Dataset sizes quoted as 88,647 and 116,600, with 111 and 22 features
- [ ] Imbalance ratios quoted as 1:1.89 and 1:6.02
- [ ] Any statement of "a fixed random state" updated to three seeds
- [ ] The stratified reduction to 20,000 instances mentioned wherever the dataset
      sizes are discussed
- [ ] Statistical testing described as Friedman plus post-hoc Wilcoxon plus
      McNemar, not McNemar alone
- [ ] Python version stated as 3.11 rather than 3.x
- [ ] Figure and table numbering consistent, given that Table 3.2 and Table 3.3
      are introduced in Section 3.4
