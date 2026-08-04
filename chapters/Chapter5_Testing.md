# Chapter 5 — Testing

Draft of the Testing chapter, which the marking scheme weights at 10% and for which
no chapter currently exists.

Every figure quoted below was produced by running the verification described, against
the implementation as submitted. Nothing is asserted that was not measured.

**Note on numbering.** The marking scheme places Testing between Design and
Implementation and Results and Analysis, which makes Testing Chapter 5 and moves
Results to Chapter 6, Conclusions to Chapter 7 and Critical Self Evaluation to
Chapter 8. The chapter is drafted on that basis. See the note at the end regarding
the consequences for the Results chapter and its table numbering.

---

## 5.1 Introduction

Testing an experimental study differs from testing a software product. The
deliverable is not a system that users operate but a set of measurements from which
conclusions are drawn, so the question testing must answer is not whether features
behave as specified but whether the measurements can be trusted. A defect that
crashes the pipeline is comparatively harmless, because it is immediately visible. A
defect that silently produces plausible but incorrect numbers is far more serious,
because it propagates into the results and the conclusions without announcing itself.

Testing was therefore directed at four properties on which the validity of the
results depends. The data must be what it is claimed to be. The experimental controls
that separate the effect under study from confounding influences must actually hold.
The results must be reproducible. And the execution must be complete, so that no
configuration is silently absent from the comparison.

This chapter reports what was tested, what the tests found, and what the testing
approach does not establish. Section 5.8 records the defects that testing exposed,
including three that produced incorrect results rather than failures, since those
cases are the clearest evidence of why the testing was necessary.

---

## 5.2 Testing Strategy

Four categories of test were applied, chosen to correspond to the four properties
above.

**Data integrity testing** confirms that each dataset loads with the composition its
publication describes, and that the transformations applied to it preserve the
properties the study depends upon.

**Behavioural verification** confirms that the experimental controls hold in the
implementation and not merely in the design. The most important of these is that
resampling is confined to training data, since a failure here would inflate every
result in the study.

**Reproducibility testing** confirms that re-executing a configuration returns the
same measurements, which is a precondition for the results being independently
checkable.

**Execution testing** confirms that the full experimental matrix completed, since a
configuration that failed and was excluded would bias the comparison in a direction
that could not be determined after the fact.

Testing was carried out against the implementation as it ran, rather than through a
separate unit test suite. For an experimental pipeline this is the more informative
approach: the property of interest is whether the experiment as executed was sound,
which is established by verifying its actual inputs, intermediate states and outputs
rather than by exercising its functions in isolation.

---

## 5.3 Data Integrity Verification

Each dataset was verified on loading against the composition reported by its
publication. This matters because a silent discrepancy in class counts would
invalidate every imbalance ratio quoted in the study.

**Table 5.1 Dataset composition, verified on loading**

| Property | Vrbančič | URL-Phish |
|---|---|---|
| Instances loaded | 88,647 | 116,600 |
| Phishing instances | 30,647 | 16,600 |
| Legitimate instances | 58,000 | 100,000 |
| Phishing proportion | 34.57% | 14.24% |
| Imbalance ratio | 1:1.89 | 1:6.02 |
| Missing values | 0 | 0 |
| Features as published | 111 | 22 |
| Features after cleaning | 92 | 22 |

Two findings from this verification are worth recording.

The Vrbančič feature count reduces from 111 to 92. Nineteen columns are either
invariant across every row or exact duplicates of another column, and are removed
because they cannot contribute to any decision. This is reported rather than passed
over silently, since the discrepancy between the published feature count and the
count used would otherwise appear to be an error.

The URL-Phish composition does not match its publication. The accompanying paper
describes 111,660 URLs of which 11,660 are phishing; the distributed file contains
116,600 rows of which 16,600 are phishing. The measured values were adopted, since
the data rather than the description determines what the experiment actually used.
This was found only because the counts were verified rather than assumed, and it is
the clearest illustration of why that verification is worth performing.

The stratified reduction to 20,000 instances was verified to preserve the class
distribution. The Vrbančič proportion is unchanged at 34.57%, and URL-Phish moves
from 14.24% to 14.23%, a deviation of one hundredth of a percentage point arising
from integer rounding in the per-class allocation. The reduction therefore alters the
volume of data without altering the property under study.

---

## 5.4 Validation of Feature Extraction

The most substantial single verification concerns the derivation of features from raw
URLs, which was required so that the URL-Phish feature set could be computed for
inputs not present in the dataset.

The risk here is specific. The published dataset provides feature values but not the
code that produced them, so the definitions had to be recovered by inspection. A
recovered definition that differed from the original, even slightly, would present a
model with inputs drawn from a different distribution than the one it was trained on.
The model would still return predictions, and those predictions would still look
plausible, so the error would not be detectable from the output.

Validation was therefore performed against the published data directly. Features were
extracted from 2,000 URLs drawn at random from the dataset and compared with the
stored values for those same URLs.

**Table 5.2 Feature extraction validation, 2,000 URLs**

| Result | Value |
|---|---|
| URLs tested | 2,000 |
| Features tested per URL | 22 |
| Individual comparisons | 44,000 |
| Features matching exactly | 22 of 22 |
| Mean match rate | 1.0000 |
| Mismatches | 0 |

All twenty-two features reproduced the published values exactly across all 2,000
URLs. Several definitions were non-obvious and were only established by this process.
The public suffix is not simply the final label of the hostname: for a host such as
`www.hnehealth.nsw.gov.au` the suffix is `gov.au` rather than `au`, which requires a
public suffix list rather than string manipulation. The registrable domain is the
suffix plus one further label, and the subdomain count is the number of remaining
labels. Character counts and ratios are computed over the entire URL string including
the scheme, not over the hostname alone.

Each of these could plausibly have been implemented otherwise, and any such choice
would have produced values that were wrong but not obviously wrong. The exact match
across 44,000 comparisons is what establishes that the recovered definitions are the
original ones.

---

## 5.5 Verification of Experimental Controls

The controls that separate the effect under study from confounding influences were
verified in the implementation rather than assumed from the design.

### 5.5.1 Prevention of information leakage

The single most consequential control is that resampling operates only on training
data. Were synthetic instances derived from validation data to influence model
fitting, every result in the study would be optimistically biased, and the bias would
be invisible because the affected scores would simply appear better.

The control is structural rather than procedural: resampling is a stage of an
`imblearn` pipeline that is passed to the cross-validation routine, so the resampler
is re-fitted within each fold on that fold's training partition alone. The
verification confirmed that the resampling stage is present inside the pipeline
object rather than applied to the data beforehand, and that feature scaling is
likewise fitted within the pipeline rather than on the full training set.

This design makes the leakage failure difficult to introduce rather than merely
absent. The alternative arrangement, in which resampling is applied before
cross-validation, would require restructuring the pipeline rather than a single
oversight.

### 5.5.2 Mutual exclusivity of treatment mechanisms

The seven techniques act through two distinct mechanisms: six resample the training
data, while cost-sensitive learning re-weights the classifier's objective. A
configuration that applied both would produce a measurement attributable to neither.

All eight conditions, including the untreated baseline, were inspected to confirm
that the two mechanisms never co-occur.

**Table 5.3 Treatment mechanism by condition**

| Condition | Resampling stage present | Class weighting applied |
|---|---|---|
| No treatment | No | No |
| Random Oversampling | Yes | No |
| Random Undersampling | Yes | No |
| SMOTE | Yes | No |
| ADASYN | Yes | No |
| SMOTEENN | Yes | No |
| SMOTETomek | Yes | No |
| Cost-Sensitive Learning | No | Yes |

No condition combines the two. Each measurement is therefore attributable to a single
mechanism.

### 5.5.3 Stratification of the train-test split

Stratification must hold in practice for the test partition to be representative,
particularly for the minority class on which every reported metric depends. The
realised proportions were recorded for all 144 runs.

**Table 5.4 Realised class proportions across all 144 runs**

| Dataset | Population | Training partition | Test partition | Train size | Test size |
|---|---|---|---|---|---|
| Vrbančič | 34.57% | 34.57% | 34.58% | 16,000 | 4,000 |
| URL-Phish | 14.24% | 14.23% | 14.22% | 16,000 | 4,000 |

The proportions are constant across all runs, varying by no more than one hundredth
of a percentage point from the population value, and the partition sizes are exactly
16,000 and 4,000 throughout. Stratification therefore held in every run rather than
on average.

---

## 5.6 Reproducibility Testing

Reproducibility was tested by re-executing configurations and comparing the results
against the values stored when the experiment was first run.

Before that, seed independence was confirmed. Because each replication is intended to
be an independent sample rather than a repetition, the three seeds must select
genuinely different subsets. Content fingerprints of the reduced URL-Phish data under
each seed are `d2fb1105ced4332a`, `b683d7fbbedce057` and `66f3b6c77d7cf6ff`. The
three subsets are distinct, so the replications are independent as intended.

Five configurations were then re-executed, selected to span both datasets, all three
classifiers, several treatment techniques and all three seeds.

**Table 5.5 Reproducibility of re-executed configurations**

| Configuration | Confusion matrix identical | Max difference, label-based metrics | Max difference, threshold-free metrics |
|---|---|---|---|
| Vrbančič, SMOTE, Decision Tree, seed 42 | Yes | 0 | 0 |
| URL-Phish, Cost-Sensitive, Random Forest, seed 2 | Yes | 0 | 0 |
| Vrbančič, ADASYN, Support Vector Machine, seed 2 | Yes | 1.1 × 10⁻¹⁶ | 1.1 × 10⁻¹⁶ |
| Vrbančič, SMOTETomek, Random Forest, seed 1 | Yes | 1.1 × 10⁻¹⁶ | 1.1 × 10⁻¹⁶ |
| URL-Phish, SMOTEENN, Support Vector Machine, seed 1 | Yes | 1.1 × 10⁻¹⁶ | 2.1 × 10⁻⁵ |

Four of the five configurations reproduced to within floating-point representation
error, which is exact reproduction for practical purposes.

The fifth requires an honest account. Its confusion matrix was identical, at 548 true
positives, 132 false positives, 21 false negatives and 3,299 true negatives, so every
instance received the same classification as before. Precision, F1 and MCC were
identical to seventeen decimal places. However ROC-AUC differed by 1.0 × 10⁻⁶ and
PR-AUC by 2.1 × 10⁻⁵.

The explanation follows from what these metrics measure. Label-based metrics depend
only on which side of the decision boundary each instance falls, and that was
unchanged. The threshold-free metrics depend on the ordering of instances by margin,
and the fitted margins differed in their final bits. The Support Vector Machine
solver accumulates floating-point operations in an order that is not fully determined
by the random seed, so two runs may converge to numerically marginally different
solutions that classify identically. A second Support Vector Machine configuration
was tested for comparison and reproduced exactly, confirming that this is an
occasional numerical effect rather than a systematic property of the classifier.

The discrepancy is immaterial at the precision reported. Results are quoted to four
decimal places, and the largest deviation observed is at the fifth. It is recorded
because claiming exact reproducibility without qualification would misrepresent what
was measured, and because the distinction between reproducible classifications and
reproducible rankings is itself worth stating.

---

## 5.7 Execution Integrity

A configuration that failed and was silently omitted would bias the comparison, and
the direction of that bias could not be recovered afterwards. The runner therefore
records an explicit error for any configuration that does not complete, rather than
allowing it to be absent.

**Table 5.6 Execution summary**

| Property | Value |
|---|---|
| Configurations expected | 144 |
| Configurations completed | 144 |
| Failures | 0 |
| Runs per dataset per seed | 24 |
| Distinct configuration identifiers | 144 |
| Total execution time | 68.9 minutes |
| Fastest configuration | 2.7 seconds |
| Slowest configuration | 77.2 seconds |

The count of distinct configuration identifiers equals the number of runs, which
confirms that no configuration was inadvertently executed twice or overwritten by
another. The composition was also verified: exactly 24 runs for each combination of
dataset and seed, each comprising all eight treatment conditions across all three
classifiers. The matrix is therefore complete and balanced, and no cell of the
comparison rests on missing data.

---

## 5.8 Defects Identified and Corrected

Testing exposed five defects. Two produced visible failures, and three produced
incorrect results without any failure. The latter group is the more instructive,
since those defects would have propagated into the conclusions undetected.

### 5.8.1 Defects producing incorrect results

**Baseline mismatch in the treatment-effect table.** The analysis that reports each
treated configuration's change relative to its untreated baseline matched rows on
dataset and classifier alone. Once the experiment was replicated under three seeds,
that key was no longer unique: three baseline rows existed for each combination.
Configurations were therefore compared against a baseline drawn from a different
replication, producing differences that were plausible in magnitude and entirely
wrong in attribution. The key now includes the seed, and the reported changes are
averaged across replications. This defect is the reason the study's central
quantitative claim, that no technique improves F1 over the untreated baseline, can be
relied upon; before the correction, those figures were not comparing what they
appeared to compare.

**Best and worst configurations selected from a single replication.** The same
duplicate-key problem affected the identification of the strongest and weakest
configurations, which was performed on individual rows rather than on means across
replications. A configuration that performed unusually well under one seed could
therefore be reported as best overall. Selection is now made on the mean across the
three replications.

**Explainability computed on the wrong data.** The SHAP analysis loaded each dataset
in full rather than applying the stratified reduction used by the experiments. The
attributions it produced therefore described models fitted to 88,647 and 116,600
instances, whereas the models actually evaluated were fitted to 20,000. The
explanations were internally valid but described a model that formed no part of the
study. The module now applies the same reduction as the experiments.

### 5.8.2 Defects producing visible failures

**Dataset retrieval rejected by both hosts.** Both the repository hosting the
Vrbančič data and the Mendeley record hosting URL-Phish return HTTP 403 to the
default user agent of the Python standard library. An explicit user agent is now
supplied. This failed loudly and was corrected immediately.

**Configuration identifiers and progress reporting assumed a numeric imbalance
ratio.** When the induced-imbalance mechanism was disabled in favour of using each
dataset's own distribution, the ratio parameter became null, and two code paths that
formatted it arithmetically raised type errors. Both now handle the null case,
recording the condition as native rather than as a percentage.

### 5.8.3 Observation

The three defects in Section 5.8.1 share a characteristic: each produced output that
was well-formed and plausible. None raised an error, none produced obviously
anomalous values, and each would have survived any inspection short of checking the
computation against its intended definition. All three were introduced by changes
that were themselves corrections, namely the addition of replication and the change
of dataset, which suggests that verification is most necessary precisely when a study
is being revised rather than when it is first built.

---

## 5.9 Stability Testing

Replication under multiple seeds was introduced as a means of strengthening the
statistical analysis, but it also functions as a stability test, since it establishes
whether a conclusion drawn from one execution survives re-execution on different
subsets.

It did not, in one respect. Under a single seed, Decision Tree recorded a higher mean
F1 than Support Vector Machine. Averaged across three replications the ordering
reverses, at 0.8934 against 0.8926. The two classifiers are separated by 0.0008, and
the post-hoc test declines to distinguish them at p = 0.729. The single-seed ordering
was therefore not a finding but an artefact of one partition, and reporting it would
have asserted a difference the data does not support.

Replication also altered the statistical conclusions materially. With one seed the
imbalance-method comparison had six matched blocks and no pair of techniques was
separable after correction for multiple comparisons. With three seeds there are
eighteen blocks and eight of the twenty-one pairs are significant. The underlying
performance figures barely moved; what changed was the power to distinguish between
them.

**Table 5.7 Effect of replication on statistical conclusions**

| Measure | One replication | Three replications |
|---|---|---|
| Matched blocks, classifier comparison | 14 | 42 |
| Friedman χ², classifiers | 8.14 | 57.57 |
| Matched blocks, method comparison | 6 | 18 |
| Friedman χ², methods | 19.16 | 43.70 |
| Significant classifier pairs | 1 of 3 | 2 of 3 |
| Significant method pairs | 0 of 21 | 8 of 21 |

---

## 5.10 Limitations of the Testing Approach

Four limitations bound what this testing establishes.

The verification confirms that the implementation does what the methodology
specifies, but not that the methodology is the right one. A stratified split, a
five-fold cross-validation and F1 as the selection criterion were all verified to be
implemented correctly; whether they are the best choices for this problem is a
question of design rather than of correctness, and testing cannot settle it.

Reproducibility was established within a single environment. The results reproduce on
the software versions recorded in Section 4.11, and no claim is made about behaviour
under different releases of scikit-learn or imbalanced-learn, whose resampling and
tree-fitting implementations may differ between versions.

Labels were taken as correct. Both datasets are treated as ground truth, and no
attempt was made to verify individual labels or to quantify how sensitive the results
would be to labelling error. Any mislabelled instances in either dataset propagate
into the results unchallenged.

Reproducibility was tested on a sample rather than exhaustively. Five of the 144
configurations were re-executed. A larger sample would give greater assurance,
although the near-exact reproduction observed, together with the seeding of every
stochastic component, makes systematic irreproducibility unlikely.

---

## 5.11 Summary

Testing addressed the properties on which the validity of the results depends.

Both datasets load with the composition their publications describe, except for
URL-Phish, whose distributed file contains 116,600 rows against the 111,660 reported;
the measured values were adopted. Feature extraction from raw URLs was validated
against 2,000 published URLs, with all twenty-two features reproducing exactly across
44,000 comparisons. The experimental controls were verified in the implementation:
resampling is structurally confined to training partitions, no condition combines
resampling with class weighting, and stratification held in all 144 runs to within
one hundredth of a percentage point. Re-execution reproduced the stored results
exactly for four of five configurations tested, and in the fifth reproduced every
classification exactly while differing in ROC-AUC and PR-AUC at the fifth decimal
place. The full matrix of 144 configurations completed without failure.

Testing exposed five defects, of which three produced plausible but incorrect
results without failing. One of these had corrupted the comparison against the
untreated baseline, which is the study's principal quantitative claim. That defect
was introduced by the addition of replication, itself an improvement, which indicates
that verification is most necessary when a study is being revised.

The following chapter presents the experimental results.

---

# Notes

**Chapter numbering.** Placing Testing as Chapter 5, which the marking scheme's
ordering implies, moves the Results chapter to 6, Conclusions to 7 and Critical Self
Evaluation to 8. This affects the draft in `Chapter5_Populated.md`, whose sections
would become 6.1 to 6.8 and whose tables would become 6.1 to 6.8. Say the word and I
will renumber that draft, including the SHAP figure, which becomes Figure 6.7.

If your programme expects Testing after Results instead, the chapter works equally
well in that position with only the closing sentence of Section 5.11 changed.

**Tables.** This chapter introduces seven tables, numbered 5.1 to 5.7 on the
assumption above. None duplicate content from other chapters; Table 5.1 overlaps
Table 4.1 in subject but reports verification outcomes rather than dataset
description.

**No figures.** The chapter is deliberately tabular. If a figure is wanted, the most
useful would be a diagram of where each verification sits in the pipeline, which
would complement Figure 4.2. I can produce it if you want one.

**On Section 5.8.** Reporting defects candidly is a strength rather than an
admission, and markers reward it: it demonstrates that the verification was real
rather than asserted. Resist any temptation to soften that section, and note that it
also supplies material for the Critical Self Evaluation chapter, where the same
episodes can be discussed reflectively rather than factually.
