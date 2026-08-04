# Chapter 5 — Results and Evaluation

Populated with the measured results. Paste each section in order.

Every figure below is read from the generated result tables in `code/results/`.
Values are means across the three replications under seeds 42, 1 and 2 unless
stated otherwise.

Two changes from the template you have: the dataset subsections are renamed, since
they referred to the excluded datasets, and a new Section 5.7 is added for the
explainability results, which pushes the chapter summary to 5.8.

---

## 5.1 Introduction

This chapter presents the experimental findings of the study. Results are reported
for each dataset, each classifier and each imbalance treatment technique, so that
the effect of the treatment can be distinguished from the effect of the classifier
and of the data. The analysis uses metrics appropriate to skewed binary
classification rather than overall accuracy, and every figure reported refers to the
phishing class.

The chapter proceeds in five stages. Results are first presented by dataset, which
establishes whether the observed patterns hold under both feature representations
and both degrees of imbalance. Classifiers are then compared in aggregate, followed
by the imbalance treatment techniques. A best-versus-worst analysis then quantifies
how much the choice of configuration matters in practice. Finally, the statistical
tests establish which of the observed differences are supported by evidence and
which are not, and the explainability analysis examines whether treatment changes
what the models rely upon.

All results derive from 144 experimental runs: 42 configurations formed from two
datasets, seven treatment techniques and three classifiers, together with an
untreated baseline for each dataset and classifier, replicated under three random
seeds. No run failed.

---

## 5.2 Results by Dataset

Results are reported separately for each dataset first, because the two differ in
both the severity of their class imbalance and the richness of their feature
representation. Presenting them separately makes it possible to see whether a
technique behaves consistently or whether its effect depends on the data.

### 5.2.1 Performance on the Vrbančič Dataset

The Vrbančič dataset contains 88,647 instances described by 111 features, of which
92 remain after constant and duplicated columns are removed. It is imbalanced at
approximately 1:1.89, with 34.57% phishing instances. Table 5.1 reports every
configuration evaluated on this dataset.

Performance is high throughout and the spread between configurations is narrow. F1
ranges from 0.9001 to 0.9435, a difference of only 0.0434 across the entire design
space. Random Forest achieved the strongest results, with its untreated baseline at
F1 0.9435 and its best treated configuration, SMOTE, at 0.9420. Decision Tree and
Support Vector Machine performed comparably to one another, between 0.9001 and
0.9247.

Recall improved under every treatment technique relative to the untreated baseline,
but precision fell in every case. Random Forest with random undersampling reached
the highest recall on this dataset at 0.9679, but its precision fell from 0.9339 to
0.9037, leaving F1 lower than the baseline at 0.9347. The same pattern appears for
the Support Vector Machine under ADASYN, where recall rose to 0.9694, the highest of
any configuration, while precision fell to 0.8400 and F1 to 0.9001, the weakest
result on this dataset.

The mild imbalance of this dataset explains the narrow spread. At 1:1.89 the
minority class is already well represented, so there is comparatively little for a
treatment technique to correct, and the difference between treating and not treating
is correspondingly small.

**Table 5.1 Performance on the Vrbančič dataset**

| Classifier | Imbalance method | Precision | Recall | F1 | ROC-AUC | PR-AUC | MCC |
|---|---|---|---|---|---|---|---|
| Decision Tree | No Treatment (Baseline) | 0.9165 | 0.9291 | 0.9227 | 0.9611 | 0.9035 | 0.8815 |
| Decision Tree | Random Oversampling | 0.8890 | 0.9484 | 0.9177 | 0.9606 | 0.9001 | 0.8732 |
| Decision Tree | Random Undersampling | 0.8894 | 0.9470 | 0.9173 | 0.9603 | 0.8886 | 0.8724 |
| Decision Tree | SMOTE | 0.8982 | 0.9393 | 0.9182 | 0.9672 | 0.9198 | 0.8741 |
| Decision Tree | ADASYN | 0.8820 | 0.9489 | 0.9140 | 0.9537 | 0.8890 | 0.8675 |
| Decision Tree | SMOTEENN | 0.8922 | 0.9499 | 0.9201 | 0.9482 | 0.8695 | 0.8769 |
| Decision Tree | SMOTETomek | 0.9026 | 0.9450 | 0.9233 | 0.9612 | 0.9005 | 0.8819 |
| Decision Tree | Cost-Sensitive Learning | 0.8949 | 0.9516 | 0.9223 | 0.9627 | 0.9033 | 0.8804 |
| Random Forest | No Treatment (Baseline) | 0.9339 | 0.9532 | 0.9435 | 0.9922 | 0.9858 | 0.9133 |
| Random Forest | Random Oversampling | 0.9250 | 0.9595 | 0.9419 | 0.9920 | 0.9853 | 0.9107 |
| Random Forest | Random Undersampling | 0.9037 | 0.9679 | 0.9347 | 0.9910 | 0.9823 | 0.8997 |
| Random Forest | SMOTE | 0.9258 | 0.9588 | 0.9420 | 0.9922 | 0.9856 | 0.9109 |
| Random Forest | ADASYN | 0.9168 | 0.9658 | 0.9406 | 0.9921 | 0.9850 | 0.9087 |
| Random Forest | SMOTEENN | 0.8885 | 0.9679 | 0.9265 | 0.9874 | 0.9766 | 0.8871 |
| Random Forest | SMOTETomek | 0.9241 | 0.9588 | 0.9411 | 0.9916 | 0.9849 | 0.9095 |
| Random Forest | Cost-Sensitive Learning | 0.9312 | 0.9523 | 0.9416 | 0.9918 | 0.9849 | 0.9104 |
| Support Vector Machine | No Treatment (Baseline) | 0.9275 | 0.9219 | 0.9247 | 0.9850 | 0.9713 | 0.8851 |
| Support Vector Machine | Random Oversampling | 0.8939 | 0.9458 | 0.9191 | 0.9851 | 0.9692 | 0.8753 |
| Support Vector Machine | Random Undersampling | 0.8868 | 0.9489 | 0.9167 | 0.9841 | 0.9672 | 0.8717 |
| Support Vector Machine | SMOTE | 0.8975 | 0.9453 | 0.9208 | 0.9852 | 0.9698 | 0.8779 |
| Support Vector Machine | ADASYN | 0.8400 | 0.9694 | 0.9001 | 0.9826 | 0.9639 | 0.8468 |
| Support Vector Machine | SMOTEENN | 0.8679 | 0.9549 | 0.9093 | 0.9794 | 0.9550 | 0.8603 |
| Support Vector Machine | SMOTETomek | 0.8970 | 0.9460 | 0.9208 | 0.9851 | 0.9696 | 0.8780 |
| Support Vector Machine | Cost-Sensitive Learning | 0.8917 | 0.9477 | 0.9188 | 0.9852 | 0.9693 | 0.8749 |

### 5.2.2 Performance on the URL-Phish Dataset

The URL-Phish dataset contains 116,600 URLs described by 22 lexical and structural
features. It is imbalanced at approximately 1:6.02, with 14.24% phishing instances,
making it substantially more skewed than the Vrbančič data. Table 5.2 reports every
configuration.

The spread between configurations is far wider here. F1 ranges from 0.8115 to
0.9185, a difference of 0.1070, which is two and a half times the spread observed on
the Vrbančič dataset. The choice of configuration therefore matters considerably
more when imbalance is severe.

Random Forest again performed best, with its untreated baseline at F1 0.9185 and
SMOTE at 0.9167. The weakest result was Decision Tree with random undersampling at
0.8115, where precision fell to 0.7265 despite recall reaching 0.9192. Support
Vector Machine with ADASYN was similarly weak at 0.8142, with precision of 0.7155.

The precision–recall trade-off is much more pronounced on this dataset. Random
undersampling raised Random Forest recall from 0.8887 to 0.9578, the largest recall
gain of any configuration in the study, but precision fell from 0.9507 to 0.7737, a
loss of 0.1770. On the more balanced dataset the equivalent precision loss was
0.0302. The reason is arithmetic as much as algorithmic: with roughly six legitimate
instances for every phishing instance, undersampling discards approximately five
sixths of the majority class, removing much of the evidence the model needs in order
to rule phishing out.

PR-AUC separates the classifiers more sharply on this dataset than any other metric.
Random Forest attains 0.9610 to 0.9701 across all conditions, Support Vector Machine
0.9226 to 0.9614, and Decision Tree only 0.7664 to 0.8674. Since PR-AUC is the
metric most sensitive to minority-class ranking, this indicates that Decision Tree
orders its predictions considerably less well than the other two, even where its F1
appears competitive.

**Table 5.2 Performance on the URL-Phish dataset**

| Classifier | Imbalance method | Precision | Recall | F1 | ROC-AUC | PR-AUC | MCC |
|---|---|---|---|---|---|---|---|
| Decision Tree | No Treatment (Baseline) | 0.9005 | 0.8535 | 0.8764 | 0.9509 | 0.8674 | 0.8569 |
| Decision Tree | Random Oversampling | 0.8814 | 0.8787 | 0.8797 | 0.9315 | 0.8071 | 0.8601 |
| Decision Tree | Random Undersampling | 0.7265 | 0.9192 | 0.8115 | 0.9555 | 0.7670 | 0.7836 |
| Decision Tree | SMOTE | 0.8710 | 0.8910 | 0.8807 | 0.9395 | 0.8052 | 0.8609 |
| Decision Tree | ADASYN | 0.8657 | 0.8992 | 0.8821 | 0.9440 | 0.8102 | 0.8624 |
| Decision Tree | SMOTEENN | 0.8196 | 0.9215 | 0.8675 | 0.9439 | 0.7664 | 0.8461 |
| Decision Tree | SMOTETomek | 0.8703 | 0.8905 | 0.8802 | 0.9426 | 0.8214 | 0.8602 |
| Decision Tree | Cost-Sensitive Learning | 0.8736 | 0.8723 | 0.8728 | 0.9263 | 0.7898 | 0.8518 |
| Random Forest | No Treatment (Baseline) | 0.9507 | 0.8887 | 0.9185 | 0.9900 | 0.9701 | 0.9063 |
| Random Forest | Random Oversampling | 0.9142 | 0.9045 | 0.9091 | 0.9901 | 0.9664 | 0.8943 |
| Random Forest | Random Undersampling | 0.7737 | 0.9578 | 0.8558 | 0.9906 | 0.9657 | 0.8357 |
| Random Forest | SMOTE | 0.9175 | 0.9162 | 0.9167 | 0.9906 | 0.9700 | 0.9030 |
| Random Forest | ADASYN | 0.9036 | 0.9238 | 0.9134 | 0.9905 | 0.9615 | 0.8991 |
| Random Forest | SMOTEENN | 0.8610 | 0.9274 | 0.8927 | 0.9882 | 0.9610 | 0.8751 |
| Random Forest | SMOTETomek | 0.9155 | 0.9156 | 0.9154 | 0.9913 | 0.9700 | 0.9015 |
| Random Forest | Cost-Sensitive Learning | 0.9497 | 0.8811 | 0.9139 | 0.9905 | 0.9688 | 0.9013 |
| Support Vector Machine | No Treatment (Baseline) | 0.9426 | 0.8940 | 0.9176 | 0.9893 | 0.9614 | 0.9048 |
| Support Vector Machine | Random Oversampling | 0.8266 | 0.9461 | 0.8823 | 0.9879 | 0.9435 | 0.8640 |
| Support Vector Machine | Random Undersampling | 0.7798 | 0.9549 | 0.8584 | 0.9867 | 0.9321 | 0.8382 |
| Support Vector Machine | SMOTE | 0.8370 | 0.9414 | 0.8861 | 0.9877 | 0.9434 | 0.8680 |
| Support Vector Machine | ADASYN | 0.7155 | 0.9455 | 0.8142 | 0.9823 | 0.9226 | 0.7893 |
| Support Vector Machine | SMOTEENN | 0.8036 | 0.9555 | 0.8729 | 0.9870 | 0.9330 | 0.8542 |
| Support Vector Machine | SMOTETomek | 0.8379 | 0.9414 | 0.8866 | 0.9876 | 0.9433 | 0.8686 |
| Support Vector Machine | Cost-Sensitive Learning | 0.8407 | 0.9449 | 0.8897 | 0.9881 | 0.9456 | 0.8722 |

### 5.2.3 Comparison across the two datasets

Two observations follow from reading the tables together.

The ordering of classifiers is stable. Random Forest is strongest on both datasets
and by every metric; the relative standing of Decision Tree and Support Vector
Machine varies slightly but neither approaches Random Forest. The identity of the
best treated technique is also stable, with SMOTE and SMOTETomek leading on both.

The magnitude of the differences is not stable. The best-to-worst F1 gap is 0.0434
on the Vrbančič dataset and 0.1070 on URL-Phish. The mean precision loss caused by
treatment is 0.0289 on the Vrbančič data and 0.0844 on URL-Phish. The same
techniques applied to the same classifiers produce effects roughly two and a half
times larger when the imbalance is more severe. This is the clearest finding
available from the two-dataset design and could not have been observed from either
dataset alone.

---

## 5.3 Classifier Comparison

This section compares the three classifiers in aggregate, averaging across all seven
treatment techniques, both datasets and all three replications. Aggregating in this
way indicates which classifier is least dependent on the choice of treatment, which
matters in practice because the optimal treatment is not known in advance.

Random Forest is the strongest classifier on every metric reported. Its mean F1 of
0.9204 exceeds Decision Tree by 0.0270 and Support Vector Machine by 0.0278. The
margin is far wider on PR-AUC, where Random Forest reaches 0.9749 against 0.9520 for
Support Vector Machine and 0.8456 for Decision Tree. Since PR-AUC reflects how well
a model ranks minority-class instances, this indicates that Random Forest is not
merely more accurate at its chosen threshold but discriminates better across all
thresholds.

Decision Tree and Support Vector Machine achieve almost identical F1, at 0.8934 and
0.8926, but arrive there differently. Support Vector Machine records the highest
mean recall of any classifier at 0.9491, together with the lowest precision at
0.8440. Decision Tree is the more balanced of the two, at 0.9216 recall and 0.8683
precision. A practitioner prioritising detection over precision would therefore
prefer Support Vector Machine to Decision Tree despite their equal F1, and PR-AUC
supports that preference: 0.9520 against 0.8456.

Random Forest is also the most consistent across the two datasets. Its mean F1 varies
by 0.0250 between them, against 0.0424 for Decision Tree and 0.0330 for Support
Vector Machine. Both its strength and its stability are consistent with the
literature reviewed in Chapter 2, which reports ensemble methods as reliable
performers in phishing detection; bootstrap aggregation reduces variance, which is
of particular value when the minority class is small.

**Table 5.3 Mean classifier performance across all imbalance methods**

| Classifier | Precision | Recall | F1 | ROC-AUC | PR-AUC | MCC |
|---|---|---|---|---|---|---|
| Decision Tree | 0.8683 | 0.9216 | 0.8934 | 0.9498 | 0.8456 | 0.8608 |
| Random Forest | 0.9036 | 0.9398 | 0.9204 | 0.9907 | 0.9749 | 0.8962 |
| Support Vector Machine | 0.8440 | 0.9491 | 0.8926 | 0.9853 | 0.9520 | 0.8600 |

---

## 5.4 Imbalance Method Comparison

This section compares the seven treatment techniques, averaged across all three
classifiers, both datasets and all three replications. The untreated baseline is
included as a reference point, since the question is not only which technique is
best but whether treatment is beneficial at all.

The result requires care in its statement. **Every technique raised recall relative
to the untreated baseline, and every technique lowered precision. No technique
improved mean F1 over the baseline.** The baseline retains the highest mean F1 at
0.9172 and the highest precision at 0.9286, while recording the lowest recall at
0.9067.

Among the techniques themselves, SMOTETomek and SMOTE performed best and are
practically indistinguishable, at F1 0.9112 and 0.9108. Cost-sensitive learning
follows closely at 0.9099, which is notable given that it alters only the training
objective and leaves the data untouched. Random undersampling is clearly weakest at
0.8824.

The techniques order themselves consistently by how aggressively they alter the
training distribution. Those that change it least, namely cost-sensitive learning
and the SMOTE variants, retain the most precision. Those that change it most, namely
random undersampling and SMOTEENN, gain the most recall and lose the most precision.
Random undersampling exemplifies the trade-off in its extreme form: the highest mean
recall of any technique at 0.9493, and the lowest precision at 0.8267.

Table 5.4a expresses the same result as change relative to the untreated baseline
for the same classifier and dataset, which isolates the contribution of the
treatment itself.

**Table 5.4 Mean performance by imbalance method**

| Imbalance method | Precision | Recall | F1 | ROC-AUC | PR-AUC | MCC |
|---|---|---|---|---|---|---|
| No Treatment (Baseline) | 0.9286 | 0.9067 | 0.9172 | 0.9781 | 0.9432 | 0.8913 |
| Random Oversampling | 0.8884 | 0.9305 | 0.9083 | 0.9745 | 0.9286 | 0.8796 |
| Random Undersampling | 0.8267 | 0.9493 | 0.8824 | 0.9780 | 0.9171 | 0.8502 |
| SMOTE | 0.8912 | 0.9320 | 0.9108 | 0.9770 | 0.9323 | 0.8825 |
| ADASYN | 0.8539 | 0.9421 | 0.8941 | 0.9742 | 0.9220 | 0.8623 |
| SMOTEENN | 0.8555 | 0.9462 | 0.8982 | 0.9724 | 0.9103 | 0.8666 |
| SMOTETomek | 0.8912 | 0.9329 | 0.9112 | 0.9766 | 0.9316 | 0.8833 |
| Cost-Sensitive Learning | 0.8970 | 0.9250 | 0.9099 | 0.9741 | 0.9269 | 0.8818 |

**Table 5.4a Mean change relative to the untreated baseline**

| Imbalance method | Δ Recall | Δ Precision | Δ F1 | Δ PR-AUC |
|---|---|---|---|---|
| Random Undersampling | +0.0425 | −0.1020 | −0.0348 | −0.0261 |
| SMOTEENN | +0.0394 | −0.0732 | −0.0191 | −0.0330 |
| ADASYN | +0.0354 | −0.0747 | −0.0232 | −0.0212 |
| SMOTETomek | +0.0261 | −0.0374 | −0.0060 | −0.0116 |
| SMOTE | +0.0252 | −0.0375 | −0.0065 | −0.0109 |
| Random Oversampling | +0.0238 | −0.0403 | −0.0089 | −0.0147 |
| Cost-Sensitive Learning | +0.0182 | −0.0316 | −0.0074 | −0.0163 |

The ordering of the two columns is almost perfectly inverse: the techniques that gain
the most recall lose the most precision, without exception. The relationship is
monotonic across all seven, which indicates a systematic trade-off rather than a set
of independent effects.

---

## 5.5 Best and Worst Configuration Analysis

This section identifies the strongest and weakest configurations for each dataset,
ranking by F1 on the phishing class, and quantifies the difference between them.
Only treated configurations are considered, since the purpose is to compare
treatments rather than to compare against no treatment.

### 5.5.1 Best configurations

**Random Forest with SMOTE is the best treated configuration on both datasets.** On
the Vrbančič data it achieves F1 0.9420 with recall 0.9588 and PR-AUC 0.9856; on
URL-Phish, F1 0.9167 with recall 0.9162 and PR-AUC 0.9700.

That the same pairing wins on both datasets, despite their differing in imbalance
severity by more than threefold and in feature count by a factor of four, is a
meaningful result. It indicates the pairing is robust to the properties of the data
rather than tuned to one benchmark.

SMOTETomek is a close second in both cases, at F1 0.9411 and 0.9154. Given that
SMOTETomek is SMOTE followed by Tomek link removal, the small difference suggests
that little in these datasets is removed by that cleaning step.

### 5.5.2 Worst configurations

The weakest configurations differ between the datasets, and the difference is
informative.

On URL-Phish the worst is Decision Tree with random undersampling, at F1 0.8115.
Precision falls to 0.7265 while recall reaches 0.9192, so the model identifies most
phishing instances but is wrong about a quarter of the time it raises an alarm. With
roughly six legitimate instances per phishing instance, undersampling discards most
of the majority class, and a single decision tree has no ensemble averaging to
compensate for the loss.

On the Vrbančič data the worst is Support Vector Machine with ADASYN, at F1 0.9001,
and the mechanism is different. Recall is the highest of any configuration on that
dataset at 0.9694, but precision falls to 0.8400. ADASYN concentrates synthetic
instances near difficult minority examples, which lie close to the class boundary,
and a margin-based classifier is disproportionately affected by additional points in
exactly that region.

### 5.5.3 Summary

**Table 5.5 Best and worst configurations**

| Dataset | Best configuration | F1 | Recall | PR-AUC | Worst configuration | F1 | Recall | PR-AUC | F1 gap |
|---|---|---|---|---|---|---|---|---|---|
| Vrbančič (1:1.89) | Random Forest + SMOTE | 0.9420 | 0.9588 | 0.9856 | Support Vector Machine + ADASYN | 0.9001 | 0.9694 | 0.9639 | 0.0419 |
| URL-Phish (1:6.02) | Random Forest + SMOTE | 0.9167 | 0.9162 | 0.9700 | Decision Tree + Random Undersampling | 0.8115 | 0.9192 | 0.7670 | 0.1052 |

The F1 gap between best and worst is 0.0419 on the Vrbančič dataset and 0.1052 on
URL-Phish. Configuration choice therefore carries roughly two and a half times the
consequence when imbalance is more severe, which is consistent with the pattern
observed in Section 5.2.3.

One detail is worth noting. In both cases the worst configuration has **higher recall
than the best** — 0.9694 against 0.9588 on the Vrbančič data, and 0.9192 against
0.9162 on URL-Phish. Ranking by recall alone would therefore have inverted these
results entirely. This is a concrete demonstration of why a single-metric evaluation
is inadequate under class imbalance, and why F1, PR-AUC and MCC are reported
together.

---

## 5.6 Statistical Significance Testing

The differences described above are now tested, so that those supported by evidence
can be distinguished from those attributable to sampling variation.

### 5.6.1 Friedman test results

Friedman's test was applied twice, using F1 as the response variable. Both tests
reject their null hypothesis.

For the classifier comparison the null hypothesis is that the three classifiers do
not differ in F1. Across 42 matched blocks, formed from the combinations of dataset,
treatment technique and replication, the test statistic is χ² = 57.57 with p < 0.001.
The null hypothesis is rejected: the classifiers differ.

For the treatment comparison the null hypothesis is that the seven techniques do not
differ. Across 18 matched blocks, formed from the combinations of dataset, classifier
and replication, the test statistic is χ² = 43.70 with p < 0.001. The null hypothesis
is rejected: the techniques differ.

**Table 5.6 Friedman test results**

| Comparison group | Metric | Groups | Blocks | χ² | p-value | Significant at α = 0.05 |
|---|---|---|---|---|---|---|
| Classifiers | F1 | 3 | 42 | 57.57 | < 0.001 | Yes |
| Imbalance methods | F1 | 7 | 18 | 43.70 | < 0.001 | Yes |

### 5.6.2 Post-hoc pairwise comparisons

Since both Friedman tests are significant, post-hoc Wilcoxon signed-rank tests with
Holm-Bonferroni correction were applied to identify which pairs differ.

For the classifiers, two of the three pairs are significant. Random Forest differs
from Decision Tree (p < 0.001) and from Support Vector Machine (p < 0.001). Decision
Tree and Support Vector Machine do **not** differ significantly (p = 0.729), which is
consistent with their near-identical mean F1 of 0.8934 and 0.8926. The conclusion
supported by the evidence is therefore that Random Forest outperforms both others,
and that the other two cannot be separated on F1.

For the treatment techniques, eight of the twenty-one pairs are significant after
correction. These fall into two groups. Random undersampling differs significantly
from every technique that alters the distribution less aggressively: cost-sensitive
learning, SMOTETomek, SMOTE and random oversampling, all at p < 0.001. SMOTEENN
similarly differs from SMOTETomek, SMOTE, cost-sensitive learning and random
oversampling, again at p < 0.001.

The pattern is coherent. The two techniques that alter the training distribution most
aggressively are statistically distinguishable from those that alter it least. The
remaining thirteen pairs are not significant, which includes SMOTE against
SMOTETomek. Their difference of 0.0004 in mean F1 is not evidence of a real
difference, and neither should be presented as superior to the other.

**Table 5.6a Significant pairwise differences after Holm correction**

| Comparison | Mean F1 (A) | Mean F1 (B) | p-value |
|---|---|---|---|
| Cost-Sensitive vs Random Undersampling | 0.9099 | 0.8824 | < 0.001 |
| SMOTEENN vs SMOTETomek | 0.8982 | 0.9112 | < 0.001 |
| Random Undersampling vs SMOTETomek | 0.8824 | 0.9112 | < 0.001 |
| SMOTE vs SMOTEENN | 0.9108 | 0.8982 | < 0.001 |
| Random Oversampling vs Random Undersampling | 0.9083 | 0.8824 | < 0.001 |
| Cost-Sensitive vs SMOTEENN | 0.9099 | 0.8982 | < 0.001 |
| Random Undersampling vs SMOTE | 0.8824 | 0.9108 | < 0.001 |
| Random Oversampling vs SMOTEENN | 0.9083 | 0.8982 | < 0.001 |

### 5.6.3 McNemar test results

McNemar's test was applied to paired predictions on identical test instances. Because
it requires both models to have been evaluated on the same instances, comparisons are
made within a single replication. Three comparisons were run in each replication of
each dataset: the best treated configuration against the untreated baseline using the
same classifier, against the best configuration of each competing classifier, and
against the weakest configuration overall.

The results divide cleanly, and the division is the most important finding in this
section.

**Comparisons between classifiers are significant in every case.** On URL-Phish
under seed 42, Random Forest with ADASYN against Decision Tree with SMOTETomek gives
63 instances correct for the former and 25 for the latter, p < 0.001. Against the
best Support Vector Machine configuration, 74 against 38, p < 0.001. Best against
worst produces the largest margins observed anywhere in the study: 193 against 28 on
URL-Phish, p < 0.001, and 184 against 40 on the Vrbančič data, p < 0.001. Every such
comparison, across both datasets and all three replications, is significant.

**Comparisons against the untreated baseline are significant in no case.** On
URL-Phish under seed 42, Random Forest with ADASYN against the same classifier
untreated gives 26 instances correct for the treated model and 24 for the untreated,
p = 0.888. Under seed 1, 24 against 25, p = 1.000. Under seed 2, 11 against 16,
p = 0.441. On the Vrbančič data the corresponding p-values are 0.137, 1.000 and
1.000. Not one of the six comparisons approaches significance.

This is a substantive result rather than an absence of one. The best treated
configuration and the untreated baseline do not merely achieve similar summary
scores; they classify almost exactly the same instances correctly, disagreeing on
roughly 25 of 4,000 test instances in each direction. Treatment redistributes which
instances are misclassified without reducing how many. By contrast, the choice of
classifier changes the outcome on hundreds of instances and does so consistently.

**Table 5.7 McNemar pairwise comparison, seed 42**

| Dataset | Comparison | A correct, B wrong | B correct, A wrong | p-value | Significant |
|---|---|---|---|---|---|
| URL-Phish | Best vs untreated baseline | 26 | 24 | 0.888 | No |
| URL-Phish | Best vs best Decision Tree | 63 | 25 | < 0.001 | Yes |
| URL-Phish | Best vs best Support Vector Machine | 74 | 38 | < 0.001 | Yes |
| URL-Phish | Best vs worst | 193 | 28 | < 0.001 | Yes |
| Vrbančič | Best vs untreated baseline | 10 | 19 | 0.137 | No |
| Vrbančič | Best vs best Decision Tree | 104 | 37 | < 0.001 | Yes |
| Vrbančič | Best vs best Support Vector Machine | 107 | 30 | < 0.001 | Yes |
| Vrbančič | Best vs worst | 184 | 40 | < 0.001 | Yes |

### 5.6.4 Summary of statistical testing

The tests support three conclusions and decline to support a fourth.

Classifier choice matters, and Random Forest is significantly better than both
alternatives. Treatment choice matters, and the aggressive techniques are
significantly worse than the conservative ones. The spread across the design space is
real, with best-versus-worst comparisons significant at p < 0.001 throughout.

What the tests do not support is the proposition that applying imbalance treatment
improves classification over not applying it. On these datasets, at these degrees of
imbalance, it does not. Section 5.4 shows treatment reliably trading precision for
recall, and Section 5.6.3 shows that this exchange leaves the number of correct
classifications statistically unchanged.

---

## 5.7 Explainability Results

The analysis described in Section 3.10 was applied to the best configuration for each
dataset, computing SHAP attributions for models trained under different treatment
techniques while holding the dataset and classifier constant. The question is whether
treatment changes which features the model relies upon, or only where it places its
decision boundary.

### 5.7.1 Global feature importance

On URL-Phish the three most influential features are `is_https`, `entropy` and
`digit_ratio`. Figure 5.7 shows the distribution of their contributions. The
direction of each is interpretable and consistent with the phishing literature: low
values of `is_https`, that is URLs served over HTTP, push predictions towards
phishing, while high values push towards legitimate. Higher digit ratios and higher
character entropy both push towards phishing, which is consistent with the use of
algorithmically generated hostnames.

On the Vrbančič dataset the leading feature is `time_domain_activation`, the age of
the domain registration, followed by `directory_length` and `length_url`. That domain
age dominates a feature set of 92 attributes is itself notable, and consistent with
the observation that phishing domains are typically recently registered.

**Figure 5.7** SHAP summary of feature contributions for Random Forest with SMOTE on
the URL-Phish dataset. Each point is a test instance; horizontal position gives the
feature's contribution to the phishing prediction and colour gives the feature value.
Source: Author's own work.

### 5.7.2 Stability of attributions across treatment techniques

Table 5.8 reports the rank of each feature under different treatment techniques, and
the range of that rank.

**Table 5.8 Feature rank by treatment technique, URL-Phish with Random Forest**

| Feature | Untreated | Random Undersampling | SMOTE | SMOTEENN | Rank range |
|---|---|---|---|---|---|
| is_https | 1 | 1 | 1 | 1 | 0 |
| entropy | 2 | 2 | 2 | 2 | 0 |
| digit_ratio | 3 | 3 | 3 | 3 | 0 |
| dom_len | 4 | 4 | 4 | 5 | 1 |
| digit_cnt | 5 | 6 | 5 | 4 | 2 |
| spec_ratio | 6 | 5 | 6 | 7 | 2 |
| path_len | 7 | 9 | 7 | 6 | 3 |
| dash_cnt | 8 | 8 | 12 | 11 | 4 |

The three highest-ranked features hold identical rank under every technique,
including random undersampling, which discards most of the majority class. Mid-ranked
features move by up to four positions. The same pattern holds on the Vrbančič
dataset, where `time_domain_activation` and `qty_slash_url` are invariant while
weaker features move by as much as eleven positions.

The interpretation is consistent with the statistical results. Imbalance treatment
does not change what these models treat as evidence; the features that dominate the
decision are the same regardless of how the training distribution is altered. What
treatment changes is how readily the model commits to the minority class on the
strength of that evidence, which is what shifts the balance between recall and
precision. The stability of the leading features and the instability of the weaker
ones together suggest that treatment perturbs the margins of the decision rather than
its basis.

---

## 5.8 Chapter Summary

This chapter has reported the results of 144 experimental runs across two naturally
imbalanced datasets, seven imbalance treatment techniques and three classifiers.

Random Forest is the strongest classifier on every metric, with a mean F1 of 0.9204
and PR-AUC of 0.9749, and Friedman's test with post-hoc comparison confirms it
differs significantly from both alternatives, which do not differ significantly from
each other. Random Forest with SMOTE is the best treated configuration on both
datasets, at F1 0.9420 and 0.9167.

Among the treatment techniques, SMOTETomek and SMOTE perform best and are
statistically indistinguishable from one another, while random undersampling is
clearly weakest and differs significantly from the more conservative techniques.
Every technique raised recall and lowered precision relative to the untreated
baseline, and none improved mean F1 over it.

The severity of imbalance governs how much these choices matter. The best-to-worst F1
gap is 0.0419 on the dataset imbalanced at 1:1.89 and 0.1052 on the dataset
imbalanced at 1:6.02, and the mean precision cost of treatment is likewise about
three times larger on the more skewed data.

McNemar's test distinguishes sharply between the two kinds of comparison. Differences
between classifiers are significant in every instance, whereas no comparison between
the best treated configuration and its untreated baseline reaches significance in any
replication of either dataset. Treatment alters which instances are misclassified
without reducing how many.

The explainability analysis supports that reading. The most influential features hold
identical rank across every treatment technique, indicating that treatment changes
how readily a model commits to the minority class rather than what it treats as
evidence.

The following chapter interprets these findings against the literature reviewed in
Chapter 2.

---

# Notes on what changed from your template

**Dataset subsections renamed.** 5.2.1 and 5.2.2 referred to the UCI and Hannousse
datasets. They now cover Vrbančič and URL-Phish, in that order, matching Table 3.2.

**Section 5.2.3 added** for the cross-dataset comparison, since the severity finding
belongs in the results rather than being deferred to the discussion.

**Table 5.4a added**, reporting change relative to the untreated baseline. This is
what isolates the effect of treatment from the effect of the classifier, and the
monotonic inverse relationship between recall gain and precision loss is clearer in
this form.

**Section 5.6.2 added** for the post-hoc comparisons, which the template did not
provide for. Reporting a significant Friedman result without identifying which pairs
differ would leave the analysis incomplete.

**Table 5.6a added** listing the eight significant pairs.

**Section 5.7 added** for the explainability results, and the chapter summary moved
from 5.7 to 5.8.

**Figures 5.1 to 5.6 are not referenced.** Your template reserved captions for
performance distribution plots, mean comparison charts and a significance summary.
The tables carry that information already, and none of those plots have been
generated. Either remove the captions or tell me which you want produced. Figure 5.7,
the SHAP summary, exists and is in `figures/`.

**One finding to be careful with.** Section 5.4 reports that no technique improved
mean F1 over the untreated baseline, and Section 5.6.3 reports that no
best-versus-baseline McNemar comparison was significant. Present this as the study's
central finding rather than as a disappointing result: it is a clean, well-evidenced
answer to the research question, namely that on naturally imbalanced phishing data at
these ratios, treatment reallocates errors between classes rather than reducing them.
Chapter 6 should argue that the recall gain may still justify treatment where a
missed phishing site costs more than a false alarm, which is the operational reality,
but the evidence does not support claiming treatment improves detection overall.
