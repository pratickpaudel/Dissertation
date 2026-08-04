# Chapter 4 — one remaining fix

The de-duplication has been applied correctly. Sections 4.3, 4.6, 4.7 and 4.8 now
carry mechanism rather than justification, all three tables and the Figure 4.3
caption are intact, the software versions match the environment that produced the
results, and no reference to the excluded datasets remains outside the cross-
reference to Section 3.4.1.

One problem remains, and it was introduced by the replacement text rather than by
anything in the original draft. Sections 4.5 and 4.7 now both list the
hyperparameter grids.

---

## The duplication between 4.5 and 4.7

Section 4.5 currently ends its second paragraph with:

> For Decision Tree, the tuned parameters include max_depth, min_samples_split and
> criterion. For Random Forest, n_estimators, max_depth and max_features are
> optimised. For Support Vector Machine, the grid search covers C, gamma and kernel
> type. These parameters were selected because they directly influence model
> complexity, generalisation and sensitivity to class imbalance.

Section 4.7 now says the same thing in its second paragraph:

> For the Decision Tree the search covers maximum depth, the minimum number of
> samples required to split a node, and the splitting criterion. For the Random
> Forest it covers the number of estimators, maximum depth, and the number of
> features considered at each split. For the Support Vector Machine it covers the
> regularisation parameter, the kernel coefficient, and the kernel function.

The two also give the same reason for the choice, once as "directly influence model
complexity, generalisation and sensitivity to class imbalance" and once as "govern
model capacity, which is the property most likely to interact with a change in class
distribution".

This is an oversight in the replacement text supplied for 4.7. Fixing it requires
one deletion.

---

## The fix

The grids belong in **4.7**, with the classifiers they configure, rather than in the
section about the cross-validation scheme. Section 4.5 should describe the tuning
procedure; Section 4.7 should state what was tuned.

**In Section 4.5, delete the following from the end of the second paragraph:**

> For Decision Tree, the tuned parameters include max_depth, min_samples_split and
> criterion. For Random Forest, n_estimators, max_depth and max_features are
> optimised. For Support Vector Machine, the grid search covers C, gamma and kernel
> type. These parameters were selected because they directly influence model
> complexity, generalisation and sensitivity to class imbalance.

So that the paragraph ends at:

> ...This makes it appropriate for controlled model comparison because the parameter
> search itself is conducted under the same cross-validation framework as model
> evaluation.

Leave Section 4.7 exactly as it is. Nothing else changes.

---

## Why this way round

Section 4.5 is about the evaluation scheme: stratified folds, the search procedure,
and the pipeline that keeps resampling inside each fold. Section 4.7 is about the
classifiers. A reader looking for what was tuned for the Support Vector Machine will
look under the classifier, not under cross-validation, and keeping the grids beside
the two implementation decisions that also concern the Support Vector Machine — the
absence of probability estimation, and what the threshold-free metrics use instead —
keeps that discussion in one place.

---

## After this change

Chapter 4 should be complete. Worth a final check on these:

- [ ] The hyperparameter grids appear once, in 4.7
- [ ] Section 4.5 ends its second paragraph at "...as model evaluation."
- [ ] Sections run 4.1 to 4.14 with no gaps
- [ ] Tables run 4.1 to 4.3
- [ ] Figures run 4.1 to 4.3, with no Figure 4.4
- [ ] Software versions read Python 3.11, scikit-learn 1.3.0, imbalanced-learn 0.11.0

---

# Still outstanding in the interim report

The interim report has not changed since the previous round, so these four items
remain. They are all quick, and the first is the most consequential item in either
document.

**a) The stated aim still names the excluded datasets.** Section 1 reads "we will
use the UCI Phishing Websites dataset and the Hannousse and Yahiouche 87-feature
benchmark dataset", which Section 3.4.1 then explains were both rejected.
Replacement text is item 1 of `InterimReport_Revisions.md`.

**b) The software versions still do not match.** The interim report reports Python
3.12 with scikit-learn 1.4.2 and imbalanced-learn 0.12.3. Chapter 4 now correctly
reports Python 3.11 with scikit-learn 1.3.0 and imbalanced-learn 0.11.0, which is
the environment that produced the results, so the two documents currently disagree
with each other. The full table is in `Chapter4_Deduplication.md`, item b.

**c) Two dashboard references remain** in Section 4, Plan for Completion.
Replacement text is item 5 of `InterimReport_Revisions.md`.

**d) Two sections are both numbered 3.10.** Validity and Reliability should become
3.11, Ethical and Practical Considerations 3.12, and Summary and Conclusion 3.13,
with the contents page updated to match.
