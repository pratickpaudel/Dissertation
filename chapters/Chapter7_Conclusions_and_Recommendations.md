# Chapter 7 — Conclusions and Recommendations

Paste-ready, with one important caveat. **Section 7.3 answers the aim as I have had to
reconstruct it, because the aim in your interim report still names the two datasets you
excluded.** Read the note at the end of this file before pasting Section 7.3. Everything
else is safe to use as written.

Limitations are cross-referenced to Chapter 8 rather than restated, so they appear in one
marked place only.

---

## 7.1 Introduction

This chapter draws the study to a conclusion. It summarises the principal findings, states
the answer they provide to the research question, sets out the contributions the study
makes, and offers recommendations both for practitioners deploying phishing detection
systems and for subsequent research. The limitations bounding these conclusions are set out
in Section 8.6 and are referenced rather than repeated here.

---

## 7.2 Summary of Key Findings

The study evaluated seven class imbalance treatment techniques, three classifiers and an
untreated baseline across two naturally imbalanced phishing datasets, replicated under
three random seeds, giving 144 experimental runs. Seven findings emerged.

**Random Forest was the strongest classifier by a significant margin.** Its mean F1 of
0.9204 and PR-AUC of 0.9749 exceeded both alternatives on every metric, and Friedman's test
with Holm-corrected post-hoc comparison confirmed the difference (p < 0.001 against each).
Decision Tree and Support Vector Machine could not be separated from one another (p =
0.729), despite differing in how they achieved their near-identical F1.

**No imbalance treatment technique improved classification over the untreated baseline.**
The baseline retained the highest mean F1 at 0.9172 and the highest precision at 0.9286.
Every technique raised recall and lowered precision, and McNemar's test found no significant
difference between the best treated configuration and its untreated baseline in any of six
replications across the two datasets.

**Among the techniques, SMOTETomek and SMOTE were jointly best and random undersampling
reliably worst.** SMOTETomek at F1 0.9112 and SMOTE at 0.9108 were not statistically
separable, so neither should be presented as superior. Random undersampling at 0.8824
differed significantly from every more conservative technique. Cost-sensitive learning
reached 0.9099 while leaving the training data untouched.

**The effect of treatment was traced to a single mechanism.** Treatment did not degrade the
models' ability to rank instances, since ROC-AUC varied by only 0.0057 across all eight
conditions, nor change what the models treated as evidence, since SHAP attributions held the
leading features at identical rank under every technique. Instead it displaced the models'
operating point beyond the true prevalence of the minority class. That displacement accounts
for the loss in F1 with a correlation of r = −0.765 across the 126 treated runs and r =
−0.963 across the seven techniques.

**The severity of imbalance governed how much these choices mattered.** The best-to-worst F1
gap was 0.0419 on the dataset imbalanced at 1:1.89 and 0.1052 at 1:6.02, and the mean
precision cost of treatment was around three times larger on the more skewed data. The
ranking of techniques transferred between the two datasets; the magnitude of their effects
did not.

**The precision–recall exchange was nonetheless favourable under modest cost asymmetry.**
Expressed as an error exchange, SMOTETomek eliminated approximately 21 false negatives per
4,000 test instances at a cost of approximately 35 false positives, a break-even cost ratio
of 1.64. Across all techniques and both datasets the ratios fell between 1.43 and 3.59.

**Classifier choice mattered considerably more than treatment choice.** Every
between-classifier comparison was significant at p < 0.001, changing the classification of
hundreds of test instances, whereas treatment changed tens and never significantly.

---

## 7.3 Answer to the Research Question

The study set out to investigate the impact of class imbalance treatment techniques on the
performance of machine learning models for phishing website detection, comparing the
effectiveness of different balancing strategies across differing feature representations.
The evidence supports a four-part answer.

**Imbalance treatment has a substantial and systematic effect on performance, but that
effect is a redistribution rather than an improvement.** Every technique increased recall
and decreased precision, in a strictly inverse ordering across all seven, and none improved
the balanced measures. The effect is real and predictable; it is not a gain. On the evidence
of these two datasets, a practitioner who applies SMOTE to naturally imbalanced phishing
data should expect to detect more phishing sites and to raise more false alarms, with no net
improvement in F1, PR-AUC or MCC.

**The mechanism is displacement of the decision threshold, not improvement of the model.**
This is the study's substantive answer to *how* treatment affects performance. The seven
techniques differ considerably in mechanism, from random duplication to informed
interpolation to boundary cleaning to loss reweighting, yet they act on these datasets
through one common pathway: making the model commit to the minority class more readily than
its prevalence warrants. This explains why cost-sensitive learning, which never alters the
data, produces a result statistically indistinguishable from SMOTE, which synthesises
thousands of instances, and why the techniques order themselves by how aggressively they
alter the training distribution rather than by the sophistication of their approach.

**Which strategy is most effective depends on how the two error types are valued, and the
answer changes accordingly.** Judged by F1, no treatment is effective and the untreated
baseline is preferable. Judged by cost, where a missed phishing site is more consequential
than a false alarm, SMOTETomek and SMOTE become worthwhile once that asymmetry exceeds
roughly 1.6 to 1.8, which is a low threshold for this domain. Both answers are correct
under their respective assumptions, and the study's contribution is to make the assumption
explicit rather than to leave it embedded in the choice of metric.

**Feature representation and imbalance severity moderate the magnitude but not the
direction.** Across a 92-feature engineered representation at 1:1.89 and a 22-feature
lexical URL representation at 1:6.02, the ranking of techniques and of classifiers was
stable, while the size of the differences between them differed by a factor of roughly two
and a half. Recommendations about *which* technique to prefer therefore transfer between
settings; expectations about *how much* difference it will make do not, since that depends
on the prevalence of phishing in the data at hand.

Taken together, the study answers its question in the negative on the terms in which the
question is usually posed, and then reframes it. Imbalance treatment does not improve
phishing detection at these degrees of imbalance. What it does is offer a controllable
exchange between two kinds of error, and the useful question is not which technique performs
best but whether that exchange is worth making in a given deployment.

---

## 7.4 Contributions

The study makes four contributions.

**An empirical contribution.** It provides a comparison of seven imbalance treatment
techniques against a like-for-like untreated baseline, across two naturally imbalanced
datasets, three classifiers and three replications, with full statistical testing. Chapter 2
identified that the literature offers no coherent answer as to which technique is best. This
study supplies a partial answer, in that SMOTETomek and SMOTE are jointly best and random
undersampling reliably worst, and simultaneously shows that the question is incomplete,
because the entire ranking sits below the untreated reference.

**A mechanistic contribution.** The identification of operating-point displacement as the
common pathway through which structurally dissimilar techniques act, quantified at r =
−0.765 across 126 runs, explains a pattern that has been observed in the literature without
being accounted for. El Aassal et al. (2020) report that phishing detection gains diminish
as class skew becomes more realistic; the mechanism identified here supplies a reason, since
treatment helps in proportion to how far the untreated model sits from the prevalence-matched
operating point, and that distance narrows as prevalence rises. The finding is corroborated
independently by the invariance of SHAP feature rankings and by the McNemar agreement between
treated and untreated predictions.

**A methodological contribution.** The study demonstrates that a comparative evaluation of
imbalance techniques without an untreated control cannot support the conclusion that
treatment is beneficial, however many techniques it compares. Studies of that design
establish which treatment is best, which is a narrower claim than it appears. The cost of
adding the control is one experimental condition per classifier and dataset; the value is
the interpretability of every other comparison in the study.

**A practical contribution.** By expressing the precision–recall exchange as a break-even
cost ratio computed from confusion matrices, the study converts a null result on F1 into an
actionable decision rule. A practitioner does not need to estimate absolute costs, only to
judge whether a missed phishing site is more than roughly twice as costly as a false alarm,
which is a tractable question in a way that interpreting a 0.006 difference in F1 is not.

---

## 7.5 Recommendations for Practice

Six recommendations follow for practitioners building phishing detection systems on
imbalanced data.

**Establish an untreated baseline before applying any treatment.** This is the single most
useful step suggested by the study. It costs one additional training run and it determines
whether treatment is helping at all. Had the present study omitted it, it would have
concluded that SMOTETomek was the best approach, without discovering that no approach beat
leaving the data alone.

**Select the classifier before selecting the treatment.** Classifier choice changed the
classification of hundreds of test instances and was significant in every comparison;
treatment changed tens and was significant in none. Effort spent choosing and tuning the
model returns considerably more than effort spent choosing a resampling technique. On this
evidence Random Forest is the appropriate default for tabular phishing features.

**If treatment is applied, prefer SMOTETomek or SMOTE, and avoid random undersampling.**
The two leading techniques cannot be separated from one another, so either is defensible.
Random undersampling should be avoided not because it fails to increase detection — it
achieved the largest reduction in false negatives of any technique — but because it does so
inefficiently, purchasing that reduction at nearly three times the false-positive cost of
SMOTETomek for a gain only half again as large.

**Consider cost-sensitive learning as the efficient default where a recall increase is
wanted.** It achieved a result statistically indistinguishable from SMOTE while leaving the
training data untouched, and incurred the lowest false-positive cost of any technique. It
requires no synthetic data generation, no discarding of real observations, and no additional
pipeline stage, which also makes it the easiest option to audit.

**Decide the acceptable error exchange before selecting a metric, not after.** F1 weights a
false alarm equally with a missed phishing site. If that is not the operational reality,
optimising F1 will systematically select against recall-oriented approaches. Stating the
cost ratio first, then choosing the metric or applying the break-even calculation in Section
6.9, avoids embedding an unexamined assumption in the evaluation.

**Expect the benefit of treatment to depend on prevalence.** The effect of treatment was
roughly two and a half times larger at 1:6.02 than at 1:1.89. Results obtained at one
prevalence should not be assumed to transfer to another, and a technique validated on
near-balanced benchmark data may behave differently on data collected at operational
prevalence.

---

## 7.6 Limitations

The conclusions above are bounded by the limitations set out in Section 8.6, which should be
read alongside them. The most consequential is recorded in Section 8.6.1: having established
that imbalance treatment operates by displacing the decision threshold, the study did not
test threshold adjustment directly, since all models classified at the default threshold of
0.5. The study therefore cannot establish whether the seven techniques achieve anything that
a single tuned threshold would not, and the recommendations in Section 7.5 should be read as
comparisons among treatment techniques rather than as a claim that treatment is the best
available means of shifting a model's operating point.

---

## 7.7 Recommendations for Future Work

Six directions follow, in order of priority.

**Compare imbalance treatment against direct threshold adjustment.** This follows directly
from the mechanism identified in Section 6.8 and is the most informative extension available.
If treatment operates by displacing the operating point, then tuning the decision threshold
on an untreated model should achieve a comparable effect without synthesising data,
discarding observations, or incurring the precision cost that arises from training on an
altered distribution. The comparison is inexpensive, since it requires no retraining, and it
would establish whether resampling contributes anything beyond what a threshold parameter
provides. Should it turn out that it does not, the practical implications for the literature
reviewed in Chapter 2 would be considerable.

**Extend the design across more prevalence levels.** The present study establishes that
treatment effects depend on prevalence but, with two datasets, cannot locate the point at
which treatment begins to be beneficial or characterise the shape of the relationship.
Testing across a range of natural prevalences, ideally from near-balanced to 1:100 or beyond,
would allow the mechanism in Section 6.8 to be tested as a prediction: treatment should
become beneficial once the untreated model sits far enough from the prevalence-matched
operating point.

**Include gradient boosting.** Both He et al. (2021) and Omari and Oukhatar (2025) use
XGBoost, and its absence here limits direct comparability with the studies whose findings
this dissertation most closely engages. Given that classifier choice mattered more than
treatment choice, extending the classifier set is likely to be more informative than
extending the treatment set.

**Evaluate at full data scale.** Results here derive from stratified 20,000-instance
subsamples, adopted because Support Vector Machine training scales quadratically. Confirming
that the findings hold at 88,647 and 116,600 instances would establish whether the null
result is a property of the problem or of the sample size.

**Evaluate under temporal and adversarial conditions.** Both datasets are static snapshots,
while Chapter 2 emphasises that phishing is adversarial and rapidly changing. Training on
one period and testing on a later one, or against adversarially modified URLs, would
establish whether imbalance treatment affects robustness to distributional change even where
it does not affect performance on a fixed partition.

**Establish empirical cost ratios for the domain.** The break-even ratios in Section 6.9 are
computed from confusion matrices, but the study does not attempt to determine the actual cost
asymmetry between a missed phishing site and a false alarm. Work establishing that ratio
empirically, whether through incident cost data or user studies of warning fatigue, would
convert the break-even analysis from a conditional statement into a definite recommendation.

---

## 7.8 Final Remarks

This study set out to determine which class imbalance treatment technique performs best for
phishing website detection, and found that on naturally imbalanced data none of them
outperforms doing nothing. That was not the anticipated result, and the more valuable
outcome was the explanation rather than the finding. Imbalance treatment does not make these
models better at distinguishing phishing sites from legitimate ones; it makes them readier
to say so. Whether that is an improvement depends on a judgement about the relative cost of
two kinds of mistake, and that judgement belongs to the person deploying the system rather
than to the metric.

The wider implication concerns how such techniques are evaluated. Class imbalance is
consistently described in the literature as a problem to be corrected, and the techniques
for correcting it are compared against one another on the assumption that correction is
beneficial. The evidence here suggests that the assumption warrants testing in each
application rather than being inherited, and that the test is inexpensive: train one model
without treatment and compare. Where treatment helps, that comparison will show it. Where it
does not, the comparison is the only thing that will reveal it.

---

# Notes on this chapter

## Read this before pasting Section 7.3

**Your aim statement still names the datasets you excluded.** In the interim report the aim
reads, in part: *"we will use the UCI Phishing Websites dataset and the Hannousse and
Yahiouche 87-feature benchmark dataset to compare the effectiveness of different class
balancing strategies under various feature settings."*

Your Chapter 3 has been corrected — Section 3.4.1 is now "Datasets Considered and Excluded"
and correctly rejects both. But two places still commit to them:

1. **The aim statement in the introduction**, quoted above
2. **The Research Variables table**, where the controlled variable "Dataset" is given as
   "UCI Phishing Websites dataset and Hannousse and Yahiouche benchmark dataset"

This matters more than the other outstanding interim-report items you asked me to leave
alone, because Chapter 7 answers the aim. If Chapter 1 states an aim naming UCI and
Hannousse and Chapter 7 reports results from Vrbančič and URL-Phish, an examiner reading the
two together sees a study that did not do what it said it would. That is the kind of
inconsistency that is noticed immediately and is trivial to fix.

I have written Section 7.3 against the aim with the dataset clause removed and the phrase
"across differing feature representations" retained, since that part still holds: your two
datasets genuinely do differ in representation, at 92 engineered features against 22 lexical
URL features. Suggested replacement for the aim:

> The overall aim of this project is to investigate the impact of class imbalance treatment
> techniques on the performance of machine learning models for phishing website detection.
> Specifically, this study uses two naturally imbalanced datasets — the Vrbančič phishing
> dataset and URL-Phish — to compare the effectiveness of different class balancing
> strategies across differing feature representations and degrees of class imbalance.

Update the Research Variables table row to match.

## No numbered objectives found

A conclusions chapter conventionally answers the aim and then each numbered objective in
turn. I could not find a list of numbered objectives in the interim report, so Section 7.3
answers the aim and research question directly. If your final Chapter 1 does contain
numbered objectives, tell me what they are and I will restructure 7.3 to address each
explicitly, which reads more strongly and is easier for a marker to award against.

## How the marking scheme is served

Your criterion is "Conclusions **and Recommendations**", so recommendations carry real
weight. I have therefore given them two sections rather than one:

- **7.5 Recommendations for Practice** — the practical implications that would have sat in
  the Discussion chapter, aimed at practitioners
- **7.7 Recommendations for Future Work** — aimed at researchers

Section 7.6 is deliberately short and points to Section 8.6. Do not expand it; limitations
are marked under Critical Self Evaluation, and repeating them here costs you under Structure
and Style without gaining anything.

## Also done in this change

The SHAP figure files have been renamed from `Figure_5_7_SHAP_Summary_URLPhish.*` to
`Figure_6_1_SHAP_Summary_URLPhish.*`, matching the caption in Section 6.7.1.

## Chapter status after this

| Ch | Title | Weight | Status |
|---|---|---|---|
| 1 | Introduction | 5% | Yours — **fix the aim** |
| 2 | Literature Review | 15% | Yours |
| 3 | Research Design and Methodology | 10% | Revised, one duplicate 3.10 outstanding |
| 4 | Design and Implementation | 20% | Complete |
| 5 | Testing | 10% | Complete |
| 6 | Results and Analysis | 10% | Complete |
| 7 | Conclusions and Recommendations | 10% | This chapter |
| 8 | Critical Self Evaluation | 10% | Complete |
