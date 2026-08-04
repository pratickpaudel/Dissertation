# Chapter 4 revisions

Replacement text for `Design and Implementation Draft V1.docx`. Paste each block
over the section it names, in the order given.

The uploaded draft predates the dataset change, so it currently describes the two
datasets that were rejected. It also predates the three-seed replication and the
explainability work. The edits below bring it into line with Chapter 3 and with
the results that were actually produced.

**Work top to bottom.** Sections 8 and 9 renumber tables and figures, so doing
those last avoids having to renumber twice.

---

## 0. First, two quick fixes

**a) One editing annotation is still in the document.** The References heading
currently reads:

> References · (Improvement #5 - Proper Citation Added)

Change it to just:

> References

**b) The software list in 4.11 has collapsed into a single paragraph.** The four
bullets now run together on one line separated by `•` characters. When you paste
the replacement in section 7 below, apply Word's bullet list formatting rather
than typing the bullet characters manually.

---

## 1. Section 4.3 — Dataset Design

**Replace the whole section, including Table 4.1, and add a second table.**

### 4.3 Dataset Design

Dataset selection was governed by a requirement that follows directly from the
research question. Because this study evaluates techniques for treating class
imbalance, the datasets themselves must exhibit class imbalance. This requirement
excluded two of the most widely cited phishing benchmarks. The UCI Phishing
Websites dataset contains 44.31% phishing instances, an imbalance ratio of
approximately 1:1.26, and the benchmark of Hannousse and Yahiouche is balanced by
design at exactly 50%. Applied to such data, oversampling methods have almost
nothing to correct, and cost-sensitive learning reduces to no treatment at all
because the class weights it derives approach unity. Both were therefore examined
and set aside, although they remain sound benchmarks for classification accuracy
in general.

The first dataset used is that of Vrbančič et al. (2020), which contains 88,647
instances described by 111 numeric features. Of these features, 96 are extracted
from the domain name and hosting infrastructure and 15 describe the web page
itself. The dataset contains 30,647 phishing and 58,000 legitimate instances,
giving 34.57% phishing and an imbalance ratio of approximately 1:1.89. It contains
no missing values.

The second dataset is URL-Phish (2025), which contains 116,600 URLs described by
22 numeric lexical and structural features such as URL length, domain length,
digit ratio, character entropy and HTTPS usage. It comprises 16,600 phishing and
100,000 legitimate instances, giving 14.24% phishing and an imbalance ratio of
approximately 1:6.02. Its phishing samples were drawn from the PhishTank
repository between November 2024 and September 2025, making it a substantially
more recent benchmark than most datasets in circulation.

It should be noted that the publication accompanying URL-Phish describes 111,660
URLs of which 11,660 are phishing, whereas the distributed data file contains
116,600 rows of which 16,600 are phishing. The counts reported here were measured
directly from the file and are the figures used throughout this study.

Using these two datasets strengthens the design in three respects. First, both are
imbalanced as published, so the treatment techniques operate on genuine skew
rather than on an artificially constructed distribution. Second, the two differ
substantially in the severity of that skew, at approximately 1:1.89 and 1:6.02,
which permits analysis of whether the effectiveness of a technique depends on how
severe the imbalance is. Third, they differ considerably in feature richness, at
111 and 22 features respectively, which supports cross-dataset interpretation and
reduces the likelihood that conclusions are specific to a single feature
representation.

### Table 4.1 Dataset summary

| Dataset | Instances | Features | Phishing | Imbalance ratio | Key characteristics |
|---|---|---|---|---|---|
| Vrbančič et al. (2020) | 88,647 | 111 | 30,647 (34.57%) | 1:1.89 | Naturally imbalanced; URL, domain and hosting features; no missing values |
| URL-Phish (2025) | 116,600 | 22 | 16,600 (14.24%) | 1:6.02 | Naturally imbalanced; recent PhishTank data (Nov 2024 to Sep 2025); lexical and structural features |

### Table 4.2 Datasets examined and excluded

| Dataset | Instances | Features | Phishing | Imbalance ratio | Reason for exclusion |
|---|---|---|---|---|---|
| UCI Phishing Websites | 11,055 | 30 | 4,898 (44.31%) | 1:1.26 | Close to balanced; leaves imbalance treatment with little to correct |
| Hannousse and Yahiouche | 11,430 | 87 | 5,715 (50.00%) | 1:1.00 | Balanced by design; cost-sensitive weighting reduces to no treatment |

---
## 2. Section 4.4 — Data Preprocessing

**Replace the whole section.**

This section currently repeats Section 3.5 of the methodology almost point for
point. Both describe checking structure and duplicates, both justify the stratified
80/20 split in the same terms, both state the fixed random state, and both explain
that holding the test set back prevents leakage and inflated performance. Only the
wording differs.

The replacement below removes that repetition by confining the section to
implementation. The reasoning for each decision belongs in Section 3.5 and is not
restated here; what appears instead is the concrete mechanism, the order of
operations and the values that resulted. See section 12 of this document, which
records the same problem in five other section pairs.

### 4.4 Data Preprocessing

Preprocessing is implemented as a single module applied identically to both
datasets, so that no dataset receives incidental special treatment. It executes in
four stages: label normalisation, column removal, stratified reduction, and the
train-test split.

Labels are first mapped onto a single convention in which phishing is the positive
class. This is necessary because the two datasets encode the target differently:
the Vrbančič data uses a numeric phishing indicator, while URL-Phish uses a
separate label column with string values. Every precision, recall, F1 and PR-AUC
figure reported in this dissertation is computed with respect to that positive
class.

Column removal then discards three categories of attribute. Identifier columns are
dropped, which for URL-Phish means the URL, domain and top-level domain strings,
since these are records of the instance rather than features of it. Constant
columns are dropped, having the same value in every row and therefore carrying no
information. Exact duplicate columns are dropped, retaining the first occurrence.
For the Vrbančič data this reduces the published 111 features to 92. Non-finite
values are replaced by the column median, though in practice neither dataset
contains any.

Stratified reduction then samples each dataset down to 20,000 instances, drawing
from each class in proportion to its existing frequency. The resulting class
proportions are 34.57% phishing for the Vrbančič data and 14.23% for URL-Phish,
matching the published distributions to within one hundredth of a percentage
point.

The stratified train-test split is applied last, producing 16,000 training and
4,000 test instances. Splitting occurs before any imbalance treatment or feature
scaling, so the test partition is never involved in fitting any component of the
pipeline. Feature scaling is deliberately not applied at this stage: it is fitted
inside each cross-validation fold, as described in Section 4.5, so that no
scaling statistic is ever derived from data the model is later evaluated against.

Every stage above is driven by a seed. Three seeds are used, 42, 1 and 2, and each
governs the stratified reduction, the split, the cross-validation folds, the
resampling and the classifiers. Because the seed changes which instances are
retained and how they are partitioned, the three executions constitute independent
replications rather than repeated runs over one fixed partition. All reported
metrics are means across them.

## 3. Section 4.5 — Cross-Validation and Tuning

**One sentence only.** In the third paragraph, replace:

> The implementation will use an imblearn.pipeline.Pipeline so that preprocessing,
> resampling and model training are executed sequentially within each
> cross-validation fold.

with:

> The implementation uses an imblearn.pipeline.Pipeline so that preprocessing,
> resampling and model training are executed sequentially within each
> cross-validation fold.

The chapter documents what was built, so the future tense is no longer correct.
Check the rest of the chapter for the same issue.

---

## 4. Section 4.9 — Statistical Testing

**Replace the whole section.** The existing text mentions the right tests but does
not describe how they are applied, and omits the post-hoc procedure entirely.

### 4.9 Statistical Testing

Statistical significance testing is used to establish whether observed differences
between configurations are meaningful rather than attributable to sampling
variation. This matters particularly when the leading methods differ by a small
margin, where a difference in mean performance alone is weak evidence.

Friedman's test, a non-parametric test for differences across more than two
related groups, is applied in two contexts: once to compare the three classifiers
and once to compare the seven imbalance treatment techniques. In each case
performance is ranked within matched blocks formed by the remaining factors and by
the replications, so that each group is measured once per block. Where Friedman's
test indicates a significant difference, post-hoc pairwise Wilcoxon signed-rank
tests with Holm-Bonferroni correction identify which specific pairs differ.
Holm's correction is used rather than a plain Bonferroni adjustment because it is
uniformly more powerful while still controlling the family-wise error rate.

McNemar's test is used for paired comparison of individual models. It is
appropriate for this purpose because it examines the instances on which two models
disagree, rather than comparing summary metrics computed independently, and
therefore accounts for the correlation between predictions made on shared data.
Because it requires both models to have been evaluated on identical instances,
these comparisons are made within a single replication. The exact binomial form is
used when the number of discordant cases is small, where the chi-squared
approximation is unreliable.

A significance level of p < 0.05 is applied throughout. Differences that do not
reach this threshold are reported as descriptive trends rather than as confirmed
effects. Including these tests prevents the analysis from resting on mean
performance values alone and makes the resulting comparison defensible.

---

## 5. Section 4.10 — Implementation Workflow

**Replace the whole section, and delete the figure caption at the end of it.**

Figure 4.4 has moved to Chapter 3 as Figure 3.1, since Sections 3.9 and 4.10
describe the same sequence and the figure belongs with the research design. Delete
the line reading "Figure 4.4 Experimental workflow for comparative evaluation.
Source: Author's own work." from this section.

### 4.10 Implementation Workflow

The implementation workflow follows a repeated experimental sequence. First, the
dataset is loaded, cleaned and reduced by stratified sampling. Second, the
train-test split is created using stratified sampling. Third, one imbalance
treatment technique is applied within the training portion of each
cross-validation fold. Fourth, one classifier is trained on the treated data.
Fifth, the selected configuration is refitted on the full treated training set and
evaluated once on the held-out test set.

This process is repeated across all combinations of dataset, imbalance treatment
technique and classifier, yielding 42 experimental configurations from two
datasets, seven techniques and three classifiers. An untreated condition is
additionally run for each dataset and classifier, so that the effect attributable
to imbalance treatment can be isolated by direct comparison, giving 48 conditions
in total. Because the entire matrix is replicated under three random seeds, 144
individual experimental runs are executed. Test-set predictions are retained for
every run, since McNemar's test operates on paired predictions rather than on
summary metrics.

The overall sequence described here is the one set out in the research design and
illustrated in Figure 3.1 of Section 3.9. This section documents the
implementation-level detail of that sequence rather than restating the design.

This repeated workflow produces a structured comparison matrix that can be used to
analyse which balancing methods work best under which conditions. For example, it
becomes possible to compare whether SMOTE-based techniques improve recall more
effectively than undersampling, or whether Random Forest benefits more
consistently from resampling than Support Vector Machine. The implementation is
therefore designed not just to build models, but to generate evidence that answers
the dissertation research question.

---

## 6. Section 4.11 — Software and Implementation Environment

**Replace the whole section.** Format the list as a proper Word bulleted list.

### 4.11 Software and Implementation Environment

The implementation was conducted using Python 3.11 and the following core
libraries:

- Scikit-learn 1.3.0 for machine learning models, cross-validation and evaluation metrics
- Imbalanced-learn 0.11.0 for imbalance treatment techniques including SMOTE, ADASYN, SMOTEENN and SMOTETomek
- Pandas 2.0.3 for data loading and manipulation
- NumPy 1.24.3 for numerical computation
- SciPy 1.10.1 and statsmodels 0.14.0 for the Friedman, Wilcoxon and McNemar significance tests
- SHAP 0.42.1 for feature attribution
- Joblib 1.5.3 for model persistence

These versions are specified to support reproducibility, so that the experimental
environment can be reconstructed. The use of widely adopted open-source libraries
also strengthens the transparency and credibility of the implementation.

---

## 7. New Section 4.12 — Explainability Implementation

**Insert this as a new section**, immediately after 4.11 and before the current
"4.12 Design Justification".

### 4.12 Explainability Implementation

The explainability analysis introduced in Section 3.10 is implemented using SHAP.
Because the two best-performing configurations are both tree ensembles, the exact
TreeExplainer algorithm is used rather than the slower model-agnostic
approximation. Attributions are computed on data transformed through every
pipeline step preceding the classifier, so that the explanation describes the
feature space in which the model was actually fitted. Resampling steps are
excluded from this transformation, because they alter the number of training rows
rather than the representation of an individual instance.

Two forms of attribution are produced. Global importance ranks features by their
mean absolute contribution across a sample of held-out instances, indicating which
features move predictions most overall. Local attribution decomposes a single
prediction, showing which feature values pushed the model towards or away from the
phishing class. Feature values are reported on their original scale rather than
the standardised scale used internally, since a standardised value carries no
interpretable meaning for a reader.

To support the comparison that Section 3.10 sets out, attributions are computed
separately for models trained under different imbalance treatment techniques,
holding the dataset and classifier constant. The resulting feature rankings are
then placed side by side, so that any change in the ordering can be attributed to
the treatment rather than to differences in model family or data. The rank range
across treatments is recorded for each feature, giving a direct measure of how
stable that feature's influence is. Results are reported in Chapter 5.

---

## 8. Renumber the two sections that follow

Adding 4.12 above pushes the last two sections down by one:

| Current | Becomes |
|---|---|
| 4.12 Design Justification | **4.13 Design Justification** |
| 4.13 Chapter Summary | **4.14 Chapter Summary** |

The text of both sections stays as it is.

---

## 9. Renumber the tables

Adding Table 4.2 in section 1 above shifts the two existing tables:

| Current | Becomes |
|---|---|
| Table 4.1 Dataset summary | **Table 4.1** (replaced with new content) |
| *(new)* | **Table 4.2** Datasets examined and excluded |
| Table 4.2 Imbalance treatment methods | **Table 4.3** Imbalance treatment methods |
| Table 4.3 Evaluation metrics | **Table 4.4** Evaluation metrics |

Update any in-text references to these table numbers as well.

Figures need no renumbering. Figures 4.1, 4.2 and 4.3 keep their numbers, and
Figure 4.4 is removed because it has moved to Chapter 3 as Figure 3.1.

---

## 10. References

Add these two entries in alphabetical position:

> URL-Phish (2025) *URL-Phish: A Feature-Engineered Dataset for Phishing
> Detection*. Mendeley Data, V1. doi:10.17632/65z9twcx3r.1.

> Vrbančič, G., Fister, I. and Podgorelec, V. (2020) 'Datasets for phishing
> websites detection', *Data in Brief*, 33, 106438.

Keep the existing UCI and Hannousse and Yahiouche references. They are still cited
in Section 4.3 as the datasets that were examined and excluded, so both remain
required.

Also remember to strip the annotation from the References heading, as noted in
section 0 above.

---

## 11. Consistency checklist

After applying everything, search the chapter for these and confirm:

- [ ] No occurrence of "UCI" or "Hannousse" outside Section 4.3 and the references
- [ ] No occurrence of "11,055" or "11,430" outside Table 4.2
- [ ] Dataset sizes read 88,647 and 116,600, with 111 and 22 features
- [ ] Imbalance ratios read 1:1.89 and 1:6.02
- [ ] No remaining reference to a single fixed random seed
- [ ] "42 experimental configurations" is accompanied by the 48 conditions and 144 runs
- [ ] Python version reads 3.11
- [ ] No occurrence of "Figure 4.4"
- [ ] Tables run 4.1 to 4.4 with no duplicates or gaps
- [ ] Sections run 4.1 to 4.14 with no duplicates or gaps
- [ ] No remaining "(Improvement #N)" annotations or stray tick characters
- [ ] Future tense replaced with present tense where the chapter describes what was built


---

## 12. The overlap between Chapters 3 and 4

Section 4.4 repeating Section 3.5 is not an isolated case. Chapter 4 currently
mirrors Chapter 3 almost section for section:

| Chapter 3 | Chapter 4 | Shared subject |
|---|---|---|
| 3.4 Research Datasets | 4.3 Dataset Design | The two datasets and why they were chosen |
| 3.5 Data Preparation | 4.4 Data Preprocessing | Cleaning, the stratified split, seeding |
| 3.6 Imbalance Treatment Techniques | 4.6 Imbalance Treatment Design | The seven techniques and their families |
| 3.7 Machine Learning Models | 4.7 Machine Learning Model Design | The three classifiers and why each was included |
| 3.8 Evaluation Metrics | 4.8 Performance Evaluation Design | Why accuracy is unsuitable and what replaces it |
| 3.9 Experimental Procedure | 4.10 Implementation Workflow | The five-step experimental sequence |

Six pairs. In each case both chapters state the same decision and offer the same
justification for it. A reader moving from Chapter 3 to Chapter 4 encounters the
argument twice, which reads as padding and invites the question of why the chapters
are separate at all.

### The division of labour to apply

The two chapters answer different questions, and each section should answer only
its own:

- **Chapter 3 answers "what was decided, and why".** It should carry the
  justification: why stratified sampling, why these seven techniques, why PR-AUC
  over accuracy. A reader should be able to judge whether the design is sound
  without seeing any implementation detail.

- **Chapter 4 answers "how it was built".** It should carry mechanism: the order
  of operations, the concrete parameter grids, which component fits what and when,
  and the values that actually resulted. A reader should be able to rebuild the
  system without needing the justification repeated.

The practical test for any sentence in Chapter 4 is whether it contains a *because*
that already appears in Chapter 3. If it does, delete it and let the mechanism
stand on its own.

### How this applies to each pair

**4.3 Dataset Design.** The replacement in section 1 above still carries the
selection rationale, which properly belongs in 3.4. Once 3.4 is updated, reduce
4.3 to what the implementation does with the data: the loading mechanism, the
cached files, the measured class counts and the resulting feature dimensionality.
Keep Table 4.1 and Table 4.2, since tables are reference material rather than
argument and are useful in both chapters.

**4.6 Imbalance Treatment Design.** Section 3.6 already explains what each
technique does and why the set spans the three families. Chapter 4 should instead
record how each is applied: that six are samplers placed inside the pipeline, that
cost-sensitive learning is applied through the classifier's class weighting rather
than by resampling, and that the two are mutually exclusive so no configuration
combines them. Keep Table 4.3 as reference.

**4.7 Machine Learning Model Design.** Section 3.7 justifies the three classifiers
as distinct learning paradigms. Chapter 4 should give the hyperparameter grids, the
selection metric, and the implementation choices that follow from each classifier,
such as the Support Vector Machine using its decision function rather than
probability estimation for the threshold-free metrics.

**4.8 Performance Evaluation Design.** Section 3.8 argues why accuracy is
misleading under imbalance. Chapter 4 should state how the metrics are computed:
which require a continuous score rather than a hard label, how that score is
obtained for each classifier, and that the confusion matrix is retained per
configuration.

**4.10 Implementation Workflow.** Already addressed in section 5 above, which
cross-references Figure 3.1 rather than restating the design.

### Scope of this change

Reducing all five remaining sections is a larger edit than the rest of this
document and is worth attempting only once Chapter 3 is settled, since Chapter 4
should be trimmed against the final version of Chapter 3 rather than the current
one. If time is short, the highest-value cases are 4.4, addressed above, and 4.6,
because those two carry the most near-verbatim repetition.
