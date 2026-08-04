# Chapter 7 — Conclusions and Recommendations

Paste-ready. Now written against the research question, aim and six objectives as recorded
in your signed project specification (B01829081, submitted 24/06/2026), rather than against
a reconstruction. Section 7.3 addresses each objective in turn, which is what a marker
looks for.

Limitations are cross-referenced to Chapter 8 rather than restated, so they appear in one
marked place only. See the notes at the end for the one objective the study deviated from
and how I have handled it.

---

## 7.1 Introduction

This chapter draws the study to a conclusion. It summarises the principal findings, assesses
the extent to which each research objective was achieved, states the answer the evidence
provides to the research question, sets out the contributions the study makes, and offers
recommendations both for practitioners deploying phishing detection systems and for
subsequent research. The limitations bounding these conclusions are set out in Section 8.6
and are referenced rather than repeated here.

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

## 7.3 Achievement of the Research Objectives

Six objectives were set in the project specification. Table 7.1 records where each is
addressed and the extent to which it was met, and the discussion that follows examines the
two that require qualification.

**Table 7.1 Achievement of the research objectives**

| # | Objective | Addressed in | Outcome |
|---|---|---|---|
| 1 | Conduct a structured literature review on phishing detection, class imbalance and imbalance-aware evaluation | Chapter 2 | Achieved |
| 2 | Identify and analyse imbalance treatment techniques such as no resampling, SMOTE, undersampling and class weighting | Chapters 2 and 4 | Achieved and extended |
| 3 | Acquire and preprocess the specified datasets | Chapters 3 and 4 | Achieved with substituted datasets |
| 4 | Train selected classifiers using the same preprocessing pipeline across both datasets and all treatment techniques | Chapter 4, verified in Chapter 5 | Achieved |
| 5 | Evaluate model performance under different treatment techniques using appropriate metrics | Chapter 6 | Achieved and extended |
| 6 | Analyse which treatment approach performs best and discuss the implications | Chapter 6, Sections 6.4 to 6.10 | Achieved with a qualified answer |

**Objective 1** was met in Chapter 2, which reviews phishing detection, the class imbalance
problem, the four families of treatment technique, and the evaluation practices appropriate
to skewed data. Section 2.7 identified the research gap the study addresses.

**Objective 2** was met and extended. The specification named four conditions as examples:
no resampling, SMOTE, undersampling and class weighting. The study implemented all four and
added three more, giving random oversampling, random undersampling, SMOTE, ADASYN, SMOTEENN,
SMOTETomek and cost-sensitive learning, together with the untreated baseline. This covers
all four families identified in Chapter 2 rather than a sample of them, and it is what
allows Section 6.4 to establish that techniques order themselves by how aggressively they
alter the training distribution, a pattern that would not have been visible with four
conditions.

**Objective 3 was achieved in modified form and represents the study's one deviation from
its specification.** The specification named the UCI Phishing Websites dataset and the
Hannousse and Yahiouche 87-feature benchmark. Both were subsequently found to be
approximately class-balanced, at 44.31% and 50.00% minority share, which makes them unable
to support a study of class imbalance treatment: there would have been no imbalance to
treat. They were replaced with two naturally imbalanced datasets, the Vrbančič phishing
dataset at 1:1.89 and URL-Phish at 1:6.02. Section 3.4 documents both the exclusion and the
replacement, and Section 8.2.1 examines how the error arose and what it indicates about the
order in which design decisions should be taken.

The substitution preserved the substance of the objective. The specification's concern was
to compare balancing strategies "under various feature settings", and the replacement
datasets differ in feature representation more sharply than the originals did, at 92
engineered website features against 22 lexical URL features. What changed is that the
comparison is now conducted at genuine operational prevalence rather than on data where the
phenomenon under investigation is absent.

**Objective 4** was met and independently verified. A single preprocessing pipeline was
applied to both datasets and all eight conditions, and Chapter 5 confirms rather than
assumes this: stratification held across all 144 runs at 34.57% and 14.23% in training
against 34.58% and 14.22% in testing, partitions were exactly 16,000 and 4,000 throughout,
treatment was confirmed to be applied only to the training partition, and no condition was
found to combine resampling with class weighting.

**Objective 5** was met and extended. The specification called for appropriate evaluation
metrics; six were reported, comprising precision, recall, F1, ROC-AUC, PR-AUC and MCC, all
computed with respect to the phishing class as Chapter 2 recommends. The study went beyond
the objective by adding formal statistical testing that the specification did not require:
Friedman tests, post-hoc Wilcoxon signed-rank comparisons with Holm-Bonferroni correction,
and McNemar's test on paired predictions. Section 6.6.2 shows why this mattered, since it is
what establishes that SMOTE and SMOTETomek cannot be distinguished from one another and that
the difference between them should not be reported as a result.

**Objective 6 was met, but the answer it produced is qualified rather than
straightforward.** The objective asks which treatment approach performs best. Section 6.4
establishes that among the seven techniques SMOTETomek and SMOTE are jointly best and cannot
be separated, while random undersampling is reliably worst. But it also establishes that
none of them outperforms applying no treatment at all, which is a finding the objective did
not anticipate and which required the additional analysis in Sections 6.8 to 6.10 to
interpret. The implications the objective calls for are therefore discussed at greater
length than planned, across the mechanism in Section 6.8, the cost analysis in Section 6.9,
and the reconciliation with prior work in Section 6.10.

---

## 7.4 Answer to the Research Question

The research question asked: *how do different class imbalance treatment techniques affect
the performance of machine learning models for phishing website detection?* The evidence
supports a four-part answer.

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

## 7.5 Contributions

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

## 7.6 Recommendations for Practice

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

## 7.7 Limitations

The conclusions above are bounded by the limitations set out in Section 8.6, which should be
read alongside them. The most consequential is recorded in Section 8.6.1: having established
that imbalance treatment operates by displacing the decision threshold, the study did not
test threshold adjustment directly, since all models classified at the default threshold of
0.5. The study therefore cannot establish whether the seven techniques achieve anything that
a single tuned threshold would not, and the recommendations in Section 7.6 should be read as
comparisons among treatment techniques rather than as a claim that treatment is the best
available means of shifting a model's operating point.

---

## 7.8 Recommendations for Future Work

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

## 7.9 Final Remarks

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

## What changed now that I have your specification

Two things, and the first is good news.

**Your research question is dataset-neutral.** It reads: *"How do different class imbalance
treatment techniques affect the performance of machine learning models for phishing website
detection?"* No dataset is named. Section 7.4 therefore answers it exactly as posed, with no
adjustment required. The dataset substitution does not touch your research question at all.

**"No resampling" was in Objective 2 from the start.** Your specification lists the
techniques to be analysed as "no resampling, SMOTE, under sampling, and class weighting".
The untreated baseline was therefore part of your plan, not something added later. This
matters, and I have corrected Section 8.2.3 of the Critical Self Evaluation, which
previously said you included it for reasons of symmetry rather than insight. The accurate
account is that it was specified from the outset, but listed as one technique among four
examples rather than recognised as the control that makes the others interpretable. That is
still a fair self-criticism and it is now supported by the document.

## The deviation, and why I have put it in the open

Objective 3 names the UCI Phishing Websites dataset and the Hannousse and Yahiouche
benchmark. Your specification is a signed, submitted form dated 24/06/2026, so it cannot be
retrospectively amended, and the dissertation must therefore acknowledge that it did not do
what the specification said.

I have handled this in three places rather than hiding it:

- **Section 7.3** states plainly that Objective 3 is the study's one deviation, gives the
  reason (both datasets are approximately balanced, at 44.31% and 50.00% minority share, so
  there was no imbalance to treat), and argues that the substitution preserved the
  objective's substance, since the specification asked for comparison "under various feature
  settings" and the replacements differ more sharply in representation than the originals
- **Section 3.4** documents the exclusion and replacement
- **Section 8.2.1** examines how the error arose

This is the right way round. A deviation that is declared, justified and reflected upon
reads as research judgement. The same deviation left implicit reads as carelessness, and a
marker comparing your specification against your dissertation will notice either way.

## Chapter 1 still needs fixing

The aim sentence in your interim report reproduces the specification's wording, including
both excluded datasets, and so does your Research Variables table. The specification is
fixed, but Chapter 1 is not. Suggested aim:

> The overall aim of this project is to investigate the impact of class imbalance treatment
> techniques on the performance of machine learning models for phishing website detection.
> Specifically, this study uses two naturally imbalanced datasets — the Vrbančič phishing
> dataset and URL-Phish — to compare the effectiveness of different class balancing
> strategies across differing feature representations and degrees of class imbalance. The
> datasets originally specified were found to be approximately class-balanced and were
> substituted for this reason, as set out in Section 3.4.

The final sentence is worth including. It turns a discrepancy an examiner might find into
one you have already declared.

Update the Research Variables table row for "Dataset" to match, and restate Objective 3 in
Chapter 1 as acquisition and preprocessing of the two datasets actually used.

## Two objectives you exceeded — say so

Markers award against objectives, so do not undersell these:

- **Objective 2** asked for four conditions by name; you implemented **eight**, covering all
  four families from Chapter 2 rather than a sample
- **Objective 5** asked for appropriate metrics; you reported **six** and added statistical
  testing the specification never required — Friedman, post-hoc Wilcoxon with Holm
  correction, and McNemar

Section 7.3 records both as "achieved and extended" for this reason.

## Structure of this chapter

Your criterion is "Conclusions **and Recommendations**", so recommendations get two sections:
7.6 for practitioners and 7.8 for researchers. Section 7.7 is deliberately three sentences
pointing at Section 8.6 — do not expand it, since limitations are marked under Critical Self
Evaluation and repeating them here costs you under Structure and Style for no gain.

Sections renumbered from the previous draft: Answer to the Research Question is now 7.4,
Contributions 7.5, Recommendations for Practice 7.6, Limitations 7.7, Future Work 7.8, Final
Remarks 7.9. Table 7.1 is new.

## One thing worth checking

Your specification's indicative reading list contains seven sources, of which
**Hannousse and Yahiouche (2021)** and **Sutter et al. (2022)** and **Ul Hassan et al.
(2022)** appear in your literature review. The other four — Kocyigit et al. (2024), Mousa et
al. (2025), Salah et al. (2024) and Tan Kian Hua and Macgregor (2022) — do not appear to be
cited anywhere in the interim report. That is not a problem in itself, since an indicative
list is not binding, but if your supervisor expects to see them engaged with, Chapter 2 is
where that belongs. Tell me if you want them worked in.
