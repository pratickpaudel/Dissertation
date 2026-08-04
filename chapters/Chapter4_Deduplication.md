# Removing the Chapter 3 / Chapter 4 overlap

Replacement text for the four Chapter 4 sections that still repeat Chapter 3.

**Read the section at the end of this document first.** Five corrections from the
previous round were not applied to the interim report, and one new numbering error
has appeared. Those are quicker to fix than the work below and matter more.

---

## Where the overlap now stands

Six pairs were identified. Two are already resolved:

| Pair | Status |
|---|---|
| 3.5 Data Preparation ↔ 4.4 Data Preprocessing | **Resolved.** 4.4 is now implementation-only |
| 3.9 Experimental Procedure ↔ 4.10 Implementation Workflow | **Resolved.** 4.10 cross-references Figure 3.1 |
| 3.4 Research Datasets ↔ 4.3 Dataset Design | Still duplicated — section 1 below |
| 3.6 Imbalance Treatment Techniques ↔ 4.6 Imbalance Treatment Design | Still duplicated — section 2 below |
| 3.7 Machine Learning Models ↔ 4.7 ML Model Design | Still duplicated — section 3 below |
| 3.8 Evaluation Metrics ↔ 4.8 Performance Evaluation Design | Still duplicated — section 4 below |

The four remaining cases are close to verbatim. For example, Section 3.8 says
"accuracy is not the primary measure as it can be distorted in imbalance
classification problems", and Section 4.8 says "Accuracy is not used as the main
measure because it can be misleading when the majority class dominates". Both then
list the same six metrics and explain each in the same order.

The principle applied below is the one already used for 4.4. **Chapter 3 states
what was decided and why. Chapter 4 states how it was built.** Every justification
that already appears in Chapter 3 is removed from Chapter 4, and what replaces it is
the mechanism, the concrete parameters and the values that resulted.

A useful side effect is that Chapter 4 becomes more specific. Details that could not
sensibly appear in a methodology chapter, such as which scikit-learn class is used
or why the Support Vector Machine avoids probability estimation, now have somewhere
to live.

---

## 1. Section 4.3 — Dataset Design

**Replace the prose. Keep Table 4.1 as it is.**

Section 3.4 already carries the selection rationale, the description of both
datasets, the reason the two earlier candidates were excluded, and the note about
the discrepancy in the URL-Phish publication. None of that needs restating.

### 4.3 Dataset Design

Both datasets are retrieved programmatically rather than being included in the
project, so that the data used can be traced to its published source. The Vrbančič
data is downloaded from the authors' repository and the URL-Phish data from its
Mendeley record. Each is cached locally on first use, so subsequent runs are
reproducible without repeated downloads and without depending on network
availability. An explicit user agent is supplied with each request, since both hosts
reject the default agent used by the Python standard library.

The class distributions were verified against the published figures on loading
rather than assumed from the accompanying papers. The Vrbančič data loads as 88,647
rows with 30,647 phishing instances, and URL-Phish as 116,600 rows with 16,600
phishing instances. These measured counts are the ones reported in Table 4.1 and
used throughout the study.

The two datasets present the target variable differently, and the loader normalises
this. The Vrbančič data encodes the target as a numeric indicator in a column named
for the phishing class, while URL-Phish uses a separate label column. Both are
mapped so that phishing is the positive class, which is the convention every metric
in this study is computed against.

The loaders for the two excluded datasets are retained in the implementation, though
they take no part in the experiments. This allows the class distributions reported
in Section 3.4.1 to be reproduced and verified independently, rather than having to
be taken on trust.

---

## 2. Section 4.6 — Imbalance Treatment Design

**Replace the prose. Keep Table 4.2 as it is.**

Section 3.6 already explains what each technique does and why the set spans the
three families, and Table 3.3 summarises them. Chapter 4 should record how each is
applied.

### 4.6 Imbalance Treatment Design

The seven techniques divide into two implementation categories, and the distinction
matters because they enter the pipeline at different points.

Six of the seven are data-level methods and are implemented as imbalanced-learn
sampler objects: RandomOverSampler, RandomUnderSampler, SMOTE, ADASYN, SMOTEENN and
SMOTETomek. Each is instantiated with the run's random seed, so the synthetic
instances a technique generates are reproducible. The sampler is inserted as a stage
of the pipeline rather than applied to the training data beforehand, which means it
is re-executed independently within every cross-validation fold and operates only on
that fold's training partition.

Cost-sensitive learning is not a sampler and is not applied to the data at all. It
is implemented by setting the class_weight parameter of the classifier to
"balanced", which weights the contribution of each class in inverse proportion to
its frequency. The pipeline for this condition therefore contains no resampling
stage.

The two mechanisms are mutually exclusive by construction. Where a sampler is
present, class_weight is left unset; where cost-sensitive learning is in use, no
sampler is added. This prevents any configuration from silently combining
data-level and algorithm-level treatment, which would make the resulting measurement
impossible to attribute to either.

An untreated condition is also implemented, in which the pipeline contains neither a
sampler nor a class weight. This is not one of the seven techniques under
comparison, but it provides the reference point against which the effect of each
treatment is measured.

---

## 3. Section 4.7 — Machine Learning Model Design

**Replace the prose. Keep the Figure 4.3 caption.**

Section 3.7 already justifies the three classifiers as distinct learning paradigms.
Chapter 4 should give the tuning configuration and the implementation decisions each
classifier forces.

### 4.7 Machine Learning Model Design

Each classifier is tuned by exhaustive grid search under the cross-validation
scheme described in Section 4.5. The parameters searched were chosen because they
govern model capacity, which is the property most likely to interact with a change
in class distribution.

For the Decision Tree the search covers maximum depth, the minimum number of
samples required to split a node, and the splitting criterion. For the Random
Forest it covers the number of estimators, maximum depth, and the number of
features considered at each split. For the Support Vector Machine it covers the
regularisation parameter, the kernel coefficient, and the kernel function.

Selection is by F1-score on the phishing class rather than by accuracy, so that the
tuning objective matches the evaluation criterion and does not reward a model for
predicting the majority class. The configuration that scores highest is then refitted
on the full treated training set before being evaluated.

Two implementation decisions follow from the classifiers themselves. The Random
Forest is fitted across multiple processes, since its trees are independent and its
grid is the largest of the three. The Support Vector Machine is fitted without
probability estimation enabled, because scikit-learn implements that through an
internal cross-validation procedure that would substantially increase training time;
the threshold-free metrics instead use the signed distance from the decision
boundary, which ranks instances equivalently. Every classifier receives the run's
random seed.

Because each classifier is trained on every treated version of the training data
across both datasets, and the partitions and tuning protocol are held constant, any
difference in outcome is attributable to the classifier rather than to the
experimental setup.

---

## 4. Section 4.8 — Performance Evaluation Design

**Replace the prose. Keep Table 4.3 as it is.**

Section 3.8 already argues why accuracy is unsuitable and what each metric
contributes. Chapter 4 should state how the metrics are computed.

### 4.8 Performance Evaluation Design

The metrics divide into two groups according to what they require as input, and this
determines how each is computed.

Precision, recall, F1-score and the Matthews Correlation Coefficient are computed
from predicted class labels. Each is evaluated with respect to the phishing class,
following the label convention established during preprocessing. Where a
configuration predicts no instances of the phishing class at all, precision is
undefined; this is handled by returning zero rather than raising an error, so that
such a configuration is recorded as a legitimate result rather than removed from the
comparison.

ROC-AUC and PR-AUC are threshold-free and require a continuous ranking of instances
rather than hard labels. For the tree-based classifiers this ranking is the predicted
class probability. For the Support Vector Machine, which is fitted without
probability estimation for the reason given in Section 4.7, it is the signed
distance from the decision boundary. Both quantities order instances by confidence,
which is all these metrics require.

Accuracy and balanced accuracy are also recorded, though neither informs the
conclusions. They are retained so that the difference between them can be observed
directly: on imbalanced data the gap between the two is itself an indication of how
unevenly a classifier treats the two classes.

The full confusion matrix is stored for every configuration, together with the
individual test-set predictions. Retaining the predictions rather than only the
summary metrics is what makes McNemar's test possible, since that test operates on
the specific instances where two models disagree and cannot be computed from
aggregate scores.

---

## 5. What to do about Section 4.12

No change needed. Section 3.10 explains why SHAP is used and what the comparison
across treatments is for; Section 4.12 covers the explainability implementation.
The two are already divided correctly.

---

## 6. Checklist for this change

- [ ] 4.3 no longer explains why the datasets were chosen or why others were excluded
- [ ] 4.6 no longer explains what SMOTE, ADASYN or the hybrid methods do
- [ ] 4.7 no longer explains why three classifiers, or why each paradigm was chosen
- [ ] 4.8 no longer explains why accuracy is misleading
- [ ] Tables 4.1, 4.2 and 4.3 are unchanged
- [ ] Figure 4.3 caption is retained in 4.7
- [ ] No sentence in Chapter 4 contains a "because" that already appears in Chapter 3

---

# Outstanding items from the previous round

Five corrections from `InterimReport_Revisions.md` are not in the uploaded interim
report, and one new error has appeared. These are faster to fix than the
de-duplication above.

## a) The aim still names the rejected datasets

**Highest severity, and still present.** Section 1 continues to read:

> Specifically, in this study, we will use the UCI Phishing Websites dataset and the
> Hannousse and Yahiouche 87-feature benchmark dataset

Section 3.4.1 explains why both were excluded. Replacement text is item 1 of
`InterimReport_Revisions.md`.

## b) The software versions are still not the ones used

The versions have changed but not to the environment that produced the results. The
report now reads:

| Library | Report says | Actually used |
|---|---|---|
| Python | 3.12 | **3.11** |
| scikit-learn | 1.4.2 | **1.3.0** |
| imbalanced-learn | 0.12.3 | **0.11.0** |
| pandas | 2.2.3 | **2.0.3** |
| NumPy | 1.26.4 | **1.24.3** |
| SciPy | 1.11.4 | **1.10.1** |
| statsmodels | 0.14.2 | **0.14.0** |
| SHAP | 0.46.0 | **0.42.1** |

The right-hand column is read directly from the environment that generated every
result in the repository. Chapter 4 already states Python 3.11, so the two documents
also now contradict each other.

If you have since upgraded your local environment to the versions in the report,
then the results would need regenerating under those versions for the claim to hold,
because resampling and tree-fitting behaviour can differ between releases. The
simpler course is to state the versions that produced the results.

## c) Two dashboard references remain in Section 4

The chapter summary was cleaned correctly, but Section 4, Plan for Completion, still
promises Streamlit integration in two places. Replacement text for the whole section
is item 5 of `InterimReport_Revisions.md`.

## d) The status paragraph still describes the experiments as pending

Section 1 still reads "Left to-do is the execution of all 42 experimental setups".
All 144 runs are complete. Replacement text is item 2 of
`InterimReport_Revisions.md`.

## e) New: two sections are both numbered 3.10

Adding the explainability section introduced a duplicate. The chapter currently runs:

| Current | Should be |
|---|---|
| 3.10 Explainability Analysis | 3.10 Explainability Analysis |
| **3.10** Validity and Reliability | **3.11** Validity and Reliability |
| **3.11** Ethical and Practical Considerations | **3.12** Ethical and Practical Considerations |
| **3.12** Summary and Conclusion | **3.13** Summary and Conclusion |

Update the contents page to match.
