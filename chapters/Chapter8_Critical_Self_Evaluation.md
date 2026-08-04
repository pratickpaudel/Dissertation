# Chapter 8 — Critical Self Evaluation

Paste-ready. Written in the first person, which is the convention for critical
self-evaluation and distinguishes it from the impersonal register of the preceding
chapters. Check that your department permits this; if not, the passive equivalents are
straightforward but the chapter will read considerably more weakly.

This chapter is also the single home for the study's limitations. They should not appear
again in Chapter 6 or Chapter 7 beyond a cross-reference.

---

## 8.1 Introduction

This chapter evaluates the conduct of the project rather than its findings. It examines
the decisions that shaped the study, including several that were wrong and were
subsequently corrected, assesses the limitations of what was ultimately produced, and
identifies what I would do differently. The account is deliberately specific: the value
of a self-evaluation lies in the particular judgements it examines, not in general
statements about time management or the value of persistence.

Four episodes structure the evaluation. I selected datasets that were unsuitable for the
research question and did not recognise this until my supervisor raised it. I designed a
method for creating class imbalance that I subsequently rejected as artificial. I built a
software component that I later removed from the project. And I obtained a central result
that contradicted what I had expected and what most of the literature reported, which
required me to decide whether to trust it. Each is examined in turn, followed by the
limitations of the completed study and a statement of what I would change.

---

## 8.2 Evaluation of the Research Design

### 8.2.1 Selecting datasets that could not answer the research question

My initial design used two widely cited phishing datasets. Both are well established in
the literature, both are used by studies I had reviewed, and I selected them for exactly
that reason: they offered comparability with prior work. What I failed to consider was
that both are approximately class-balanced.

This was not a minor mismatch. My research question concerns how imbalance treatment
techniques affect classification performance. A balanced dataset contains no imbalance to
treat. I would have been applying SMOTE, ADASYN and undersampling to data that did not
require them, and measuring differences that reflected the noise those techniques
introduced rather than any corrective effect. The study would have produced numbers, and
the numbers would have been meaningless.

My supervisor identified this. I did not. In retrospect the error has a clear cause: I
selected datasets on the criterion of whether they were established in the field rather
than on the criterion of whether their properties matched my research question. Those are
different tests, and I applied the easier one. The datasets were appropriate for phishing
detection research in general and inappropriate for this study in particular, and I did
not distinguish between the two.

The correction required replacing both datasets with naturally imbalanced alternatives:
the Vrbančič dataset at 1:1.89 and URL-Phish at 1:6.02. This came at real cost. It
invalidated the dataset sections of my methodology chapter, required the feature
extraction pipeline for URL-Phish to be written from scratch, and consumed time I had
allocated to analysis.

The lasting lesson concerns the order in which design decisions should be made. I had
chosen my datasets before fully specifying what my research question required of them.
The dependency runs the other way: the question determines the properties the data must
have, and only then can candidate datasets be assessed. I now state the required
properties before searching, which is a small procedural change that would have prevented
the error entirely.

### 8.2.2 Rejecting induced imbalance

Faced with the need for imbalanced data, my first solution was to induce imbalance
artificially by randomly discarding minority-class instances from a balanced dataset until
a target ratio was reached. This is straightforward to implement, gives exact control over
the imbalance ratio, and would have allowed me to test several ratios rather than two.
That last advantage is significant, and Section 8.5 notes that its loss is one of the
study's real limitations.

I rejected the approach on the grounds that it would not have measured what I claimed to
measure. Downsampling a balanced dataset produces a minority class that is smaller but
statistically unchanged in character: the same regions of feature space, the same internal
diversity, merely fewer examples. Natural imbalance is different in kind. When phishing
sites are genuinely rare, they are rare because of how they are created and distributed,
and their scarcity is bound up with their properties. A technique that performs well on
artificially thinned data has been shown to cope with reduced sample size, which is not
the same as coping with genuine class rarity.

I am satisfied this was the right decision, and it is reinforced by the study's actual
findings. Section 6.8 identifies the mechanism by which treatment operates: it displaces
the model's operating point relative to the true prevalence of the minority class. That
mechanism is directly tied to prevalence being real. Under induced imbalance I would have
been measuring the interaction between resampling and an artificial prevalence I had
imposed, and it is doubtful the finding would have transferred to deployment conditions —
precisely the criticism El Aassal et al. (2020) make of benchmark-driven phishing
research, and which I would have reproduced.

The episode illustrates something I found genuinely difficult. Accepting natural imbalance
meant accepting only two prevalence values, whichever two the available datasets happened
to offer, rather than the controlled series I wanted. It meant less experimental power and
a weaker claim about how effects scale with prevalence. Choosing the valid design over the
convenient one meant choosing the design that could answer less, and it took me some time
to accept that this was still the correct trade.

### 8.2.3 Including an untreated baseline

The decision that most shaped the study's outcome was including an untreated baseline as a
condition in its own right, giving eight conditions per classifier per dataset rather than
seven.

I would like to claim this as a piece of methodological insight. It was closer to
symmetry: it seemed obviously incomplete to compare seven treatments without measuring
what happened with none. Only after the results arrived did I appreciate that the baseline
carried the study's central finding. Every treatment technique reduced mean F1 relative to
it, and McNemar's test found no significant difference between the best treated
configuration and the baseline in any of six replications.

What makes this worth reflecting on is what the literature does with this comparison.
Reviewing the studies in Chapter 2 after obtaining my results, I found that most compare
treatment techniques against one another and report which performed best, without
establishing whether any outperformed leaving the data alone. Their conclusions are not
wrong, but they are narrower than they appear: they identify the best treatment, not
whether treating is better than not treating. My study can address the second question
only because of a decision I made for reasons of tidiness rather than insight.

I take two things from this. The first is that a control condition is worth including even
when its result seems predictable, because the cost is one additional condition and the
value is the interpretability of everything else. The second is more uncomfortable: I made
the most consequential design decision in the study without understanding why it mattered.
That it happened to be right does not mean my reasoning was adequate.

---

## 8.3 Evaluation of the Implementation

Two implementation decisions are worth examining, both involving a trade between rigour
and feasibility.

**Subsampling to 20,000 instances.** The full datasets contain 88,647 and 116,600
instances. Training a Support Vector Machine scales roughly quadratically with sample
size, and a full-scale run of all 144 configurations was not achievable in the time
available. I therefore drew a stratified subsample of 20,000 instances per dataset,
verifying that the class ratios were preserved to within 0.01 percentage points, at 34.57%
and 14.23% against the full-data values of 34.57% and 14.24%.

This preserved what mattered most for my research question, which concerns the effect of
class ratio, but it is a genuine restriction. Learning curves have not flattened at 20,000
instances for a problem of this dimensionality, and absolute performance would likely be
somewhat higher at full scale. I judged the comparison between conditions more important
than the absolute level of any one of them, since every condition is affected equally, and
I still consider that judgement correct. It nonetheless means my reported figures should be
read as a comparison rather than as an estimate of achievable performance.

**Replicating across three seeds.** My initial design used a single random seed. When I ran
the statistical tests on that basis, the Friedman test for treatment techniques was
significant but not one of the twenty-one post-hoc pairwise comparisons survived
Holm-Bonferroni correction. With one observation per combination, there was insufficient
power to identify which techniques actually differed, and the analysis could establish only
that some difference existed somewhere.

I extended the design to three seeds, which raised the number of significant pairs from
zero to eight and made the treatment comparison interpretable. I am satisfied this was
necessary, but I should have anticipated it. The number of observations required for a
post-hoc test is a question I could have asked during design rather than discovering after
execution. Three seeds remains modest, and a fourth or fifth would likely have separated
further pairs; I stopped at three because of the time the full matrix took to run, not
because three was sufficient on any principled ground.

A third point belongs here. Chapter 5 records five defects found during verification, three
of which produced plausible but incorrect results without causing any failure. The most
serious matched baseline rows on dataset and classifier alone, a key that ceased to be
unique once replication was introduced, so configurations were being compared against
baselines drawn from other replications. This corrupted the treatment-effect analysis that
carries the study's principal claim. All three of these defects were introduced by changes
that were themselves corrections. The lesson I draw is that my verification effort was
concentrated at the wrong point in the project: I checked the pipeline most carefully when
first building it, and least carefully when revising it, which is the reverse of where the
risk lay.

---

## 8.4 Responding to an Unexpected Result

When the results indicated that no treatment technique improved F1 over the untreated
baseline, my first assumption was that I had made a mistake. This was a reasonable
assumption, given that three defects had already been found, and I spent time checking
whether the samplers were being applied at all, whether the baseline was correctly
identified, and whether the treated and untreated conditions had been swapped.

They had not. The finding was real, and I then had to decide what to do with a result that
contradicted most of the literature I had reviewed.

My initial instinct was to present it defensively, as a limitation of my study rather than
a finding of it. Several formulations occurred to me: that the datasets were insufficiently
imbalanced for treatment to demonstrate its value, that the subsample was too small, that
my tuning may have favoured the baseline. Each is a way of reporting the result while
implying it should be discounted.

I came to regard this as the wrong approach, for two reasons. The result is well evidenced:
it holds on both datasets, for all three classifiers, across three replications, and by
McNemar's test on paired predictions as well as by mean F1. Discounting it would have meant
discounting my own most robust evidence. And the recall gains were real and consistent —
every technique increased recall — which means the finding is not that treatment does
nothing but that F1 does not credit what it does.

That reframing led to the two most substantial pieces of analysis in the dissertation.
Section 6.8 asks why the effect is absent and finds a mechanism: treatment does not degrade
the models' ranking ability, which ROC-AUC shows to be almost invariant, nor change what
they treat as evidence, which the SHAP attributions show to be stable, but displaces their
operating point past the true prevalence of the minority class, with that displacement
accounting for the F1 loss at r = −0.765 across 126 runs. Section 6.9 asks whether the
exchange is nonetheless worthwhile and finds break-even cost ratios between 1.43 and 3.59,
low enough that the recall gain is likely to justify the precision loss in most deployment
settings.

Neither analysis was in my plan. Both exist because the result was not what I expected and
explaining it required work I had not anticipated. I regard this as the most valuable thing
I learned during the project: an unexpected result is more informative than a confirmatory
one, but only if it is investigated rather than excused. My instinct was to excuse it, and
recognising that instinct as the thing to resist was the point at which the project became
genuinely research rather than execution.

---

## 8.5 Scope Management: A Component Built and Removed

Chapter 3 of my interim submission committed to a Streamlit dashboard presenting SHAP
explanations and performance summaries interactively. I built it, and it worked. It is not
in the dissertation, and the code has been moved to a directory of material excluded from
the submission.

I removed it because it did not contribute to the research question. My question asks how
imbalance treatment techniques affect classification performance. That question is answered
by the results tables and the statistical tests. A dashboard demonstrates that I can build
software, which is not what this dissertation is assessed on, and it appeared in none of my
stated objectives in Chapter 1. Having built it, I could see that it added presentational
polish to work that was already complete rather than advancing the work itself.

The honest assessment is that I should not have committed to it. I included it in my
methodology because it sounded substantial and because interactive explainability seemed a
defensible extension, without asking which part of my research question it addressed. The
answer is none. The time it consumed was time not spent on the analysis in Sections 6.8 and
6.9, which is the material that most strengthens the dissertation.

One element was worth retaining. Building the dashboard required a live URL feature
extractor, and that extractor became the basis for the validation reported in Section 5.4,
where features computed for 2,000 published URLs were compared against the dataset's own
values across 44,000 individual comparisons with a match rate of 1.0000. That verification
is stronger than anything I would otherwise have produced, and it exists as a by-product of
work I subsequently discarded. This does not justify the decision to build the dashboard,
but it is a fair record of what came of it.

I take from this a sharper test for scope. Before committing to a component, I should be
able to name the specific claim in the dissertation that it makes possible. For the
dashboard there was no such claim; for the feature extractor, which I built for the wrong
reason, there turned out to be one.

---

## 8.6 Limitations of the Study

The following limitations are stated as constraints on what the study establishes. They are
consolidated here rather than distributed across the results and conclusions chapters.

### 8.6.1 The most significant limitation

Section 6.8 finds that imbalance treatment operates by displacing the model's decision
threshold relative to the true prevalence of the minority class, and that this displacement
accounts for most of the variation in F1 loss. This finding has an implication the study
does not test. **If treatment works by moving the operating point, then moving the operating
point directly — by adjusting the decision threshold on the untreated model — should
achieve a comparable effect at no cost in training data or precision.**

Every model in this study classified at the default threshold of 0.5. Threshold adjustment
was not included as a condition, and the study therefore cannot say whether the seven
techniques achieve anything that a single tuned threshold would not. Given the mechanism
identified, that is the comparison a reader is most likely to want, and its absence is the
clearest gap in the design.

I do not think I could have anticipated this at the design stage, because the mechanism only
became apparent from the results. But I could have run it afterwards: the trained models and
their predicted probabilities were stored, and a threshold sweep would have required little
additional computation. I identified the implication too late in the timetable to act on it.
It is the first item in the future work recommended in Chapter 7, and I would raise it myself
in the viva rather than wait to be asked.

### 8.6.2 Dataset limitations

Only two prevalence levels were examined, at 1:1.89 and 1:6.02. Section 6.2.3 establishes
that the magnitude of treatment effects depends on prevalence, and Section 6.8 predicts that
treatment should become beneficial once the untreated model sits far enough from the
prevalence-matched operating point. With two points, the study can establish that the effect
depends on prevalence but cannot locate the threshold at which treatment begins to help, and
cannot characterise the shape of the relationship. This is the direct cost of the decision in
Section 8.2.2 to use naturally imbalanced data, and I accept it as the price of validity.

Both datasets are also static snapshots. Chapter 2 emphasises that phishing is adversarial
and that attackers adapt, but nothing in this study examines performance under distributional
change, so the results describe detection at a fixed point in time.

A discrepancy should also be recorded. The URL-Phish file obtained contains 116,600
instances, whereas the accompanying publication describes 111,660 legitimate and 11,660
phishing instances. I used and documented the file as obtained, since its composition is
internally consistent and verified in Section 5.3, but I was unable to reconcile it with the
published description.

### 8.6.3 Methodological limitations

Three classifiers were evaluated: Decision Tree, Random Forest and Support Vector Machine.
Gradient boosting is absent, which limits comparability with parts of the literature, since
both He et al. (2021) and Omari and Oukhatar (2025) use XGBoost. The choice was deliberate,
covering one interpretable model, one ensemble and one margin-based method, but it means the
finding that treatment does not improve F1 is established for these three families only.

The explainability analysis was applied to Random Forest alone. Since Section 6.7 reports
that feature attributions are stable across treatment techniques, it would have been valuable
to know whether that stability also holds across classifiers, and the study cannot say.

McNemar's test requires paired predictions on identical instances and can therefore only be
applied within a single replication. The finding that no best-versus-baseline comparison is
significant rests on three tests per dataset rather than on pooled evidence across
replications. The p-values are consistently far from significance, at 0.888, 1.000, 0.441,
0.137, 1.000 and 1.000, so I am confident in the conclusion, but the evidence is six separate
tests rather than one powerful one.

Finally, all results derive from 20,000-instance subsamples with three replications. As
Section 8.3 notes, absolute performance would likely be higher at full scale, and additional
replications would likely resolve further pairwise comparisons.

---

## 8.7 Skills Developed

Three areas of development are worth recording, each tied to a specific difficulty rather
than to general improvement.

**Distinguishing statistical from practical significance.** At the outset I would have
reported that SMOTETomek outperformed SMOTE, because 0.9112 exceeds 0.9108. I now understand
why that statement is unsupportable: the post-hoc test does not separate them, and a
difference of 0.0004 across eighteen matched blocks is not evidence. Learning to report that
two techniques cannot be distinguished, rather than ranking them anyway, was the single
largest change in how I handle quantitative results.

**Verification as a research practice.** I began the project treating testing as a matter of
whether code ran. The three silent defects described in Chapter 5 taught me that the
dangerous failure is code that runs and produces plausible but wrong numbers, and that
detecting it requires checking results against independently derived expectations rather than
checking for errors. This is why Chapter 5 reports match rates and cross-validated feature
values rather than assertions that the pipeline worked.

**Interpreting a negative result.** Described in Section 8.4. The specific skill is
recognising that "no effect on the chosen metric" and "no effect" are different claims, and
that the gap between them is where the analysis lies.

---

## 8.8 What I Would Do Differently

Five changes, in order of how much difference they would have made.

**Include threshold adjustment as an experimental condition.** For the reasons in Section
8.6.1, this is the change that would most have strengthened the study. An eighth condition
applying a tuned decision threshold to the untreated model would have tested whether the
seven techniques achieve anything beyond what a threshold change achieves, and the mechanism
in Section 6.8 makes that the natural question.

**Specify required dataset properties before searching for datasets.** Stating that the data
must be naturally imbalanced, at a known and non-trivial ratio, would have made the initial
selection error impossible. The failure was procedural rather than conceptual, and a
procedural fix addresses it.

**Determine the required number of replications during design.** The power of a post-hoc test
with Holm correction is calculable in advance. Doing so would have avoided running the full
matrix once, obtaining an uninterpretable comparison, and running it again.

**Verify most carefully when revising, not when building.** All three silent defects entered
through changes that were themselves improvements. I would re-run verification after every
structural change, rather than concentrating it at the point of initial construction.

**Commit only to components with an identified claim.** The test proposed in Section 8.5:
before building anything, name the claim in the dissertation it makes possible. This would
have prevented the dashboard.

---

## 8.9 Chapter Summary

This chapter has evaluated the conduct of the project. The study's design was initially
unsound, in that I selected datasets whose class balance made them incapable of addressing my
research question, and I did not identify this myself. Having corrected it, I rejected a
convenient method of inducing imbalance in favour of naturally imbalanced data, accepting
reduced experimental control in exchange for validity, and Section 6.8 subsequently vindicated
that choice by identifying a mechanism that depends on prevalence being genuine.

The implementation involved defensible compromises in subsampling and replication, both of
which I would specify more rigorously in advance. Verification exposed defects that produced
plausible but incorrect results, and taught me that the greatest risk arises when a working
pipeline is revised rather than when it is built.

The study's central result was not what I expected. My first response was to look for an
error, my second to present the finding defensively, and neither was correct. Investigating
it instead produced the mechanistic explanation in Section 6.8 and the cost analysis in
Section 6.9, which are the strongest analytical contributions in the dissertation and exist
only because the expected result did not occur.

The clearest limitation is one the findings themselves expose: having established that
treatment works by shifting the decision threshold, the study did not test threshold
adjustment directly, and so cannot say whether the seven techniques achieve anything a single
tuned threshold would not. Identifying that gap is, in a modest way, a result of the study
having explained its own findings well enough to see what it failed to ask.

---

# Notes on this chapter

## Why it is written in the first person

Critical self-evaluation is conventionally first person, and it is very difficult to write
honestly about your own errors in the passive voice — "datasets were selected which proved
unsuitable" conceals who selected them, which defeats the purpose. Confirm your department
permits it. If it does not, I can convert the chapter, but expect it to weaken.

## Where the material came from

Nothing here is invented. Every episode is one that actually occurred during the project, and
every figure is drawn from the results or from the verification in Chapter 5:

| Episode | Evidence |
|---|---|
| Dataset selection error | Supervisor feedback; datasets replaced mid-project |
| Induced imbalance rejected | Design decision recorded before implementation |
| Untreated baseline | 8 conditions rather than 7; carries the central finding |
| Subsample 20,000 | Ratios preserved to 0.01pp, verified in Section 5.3 |
| Single seed insufficient | 0 of 21 post-hoc pairs significant, rising to 8 of 21 with three seeds |
| Three silent defects | Section 5.8 |
| Dashboard built and withdrawn | Code in `code/extras/`; feature extractor retained for Section 5.4 |
| Threshold never swept | All models classified at 0.5 |

## The section to lead on

Section 8.6.1 is the strongest content in this chapter, because it is a limitation the study
identified through its own analysis rather than one imposed from outside. It says: I found the
mechanism, the mechanism implies an obvious further test, and I did not run it. Examiners
reward that far more than a list of generic constraints, and it converts a gap in the design
into evidence that you understood your own results.

I would volunteer it in the viva rather than wait. If an examiner raises threshold tuning and
you have already named it as your principal limitation, the exchange is about your judgement.
If they raise it first, it is about your oversight.

## One thing to consider adding

If you have any record of the supervision meeting where the dataset problem was raised —
notes, an email, a date — a single clause locating it in time would strengthen Section 8.2.1.
"My supervisor identified this in [month]" is more convincing than an undated account, and it
demonstrates that supervision was used rather than merely received.

## Cross-references to fix once the chapters are final

- Section 8.2.2 cites El Aassal et al. (2020) — already in your reference list, verified
- Section 8.6.3 cites He et al. (2021) and Omari and Oukhatar (2025) — both already cited in
  Chapter 2
- Section 8.5 refers to "Chapter 3 of my interim submission" — adjust if the dashboard
  commitment has been removed from the final Chapter 3, in which case say "my interim
  submission" without the section reference
- Chapter 7 should cite Section 8.6 for limitations rather than restating them, and Section
  8.6.1 supplies the first item of future work
