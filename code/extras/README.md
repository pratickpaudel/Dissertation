# Extras — not part of the submitted dissertation

Code in this directory is **outside the scope of the dissertation**. It is kept
because it works and may be useful later, but nothing here is referenced by any
chapter, and none of it is required to reproduce the study's results.

To reproduce the dissertation, use `../run_pipeline.py`. This directory can be
ignored entirely.

## Contents

| File | Purpose |
|---|---|
| `dashboard.py` | Streamlit interface presenting predictions, SHAP attributions and the result tables |
| `persist_models.py` | Trains the best configuration per dataset and saves it, so the dashboard need not retrain |
| `url_features.py` | Recovers the 22 URL-Phish lexical features from a raw URL, with a verification harness |

## Why it was excluded

An interactive dashboard demonstrates software engineering rather than research,
and the dissertation is assessed on the latter. It does not appear among the
objectives in Chapter 1, and the explainability analysis that does bear on the
research question — the SHAP attributions and their comparison across imbalance
treatment techniques — is implemented in `../src/explainability.py` and reported
in the results chapter without needing an interface.

## One result worth keeping on record

`url_features.py` recovers the feature definitions used to build the URL-Phish
dataset, so features can be computed from a raw URL string. This was verified
rather than assumed: extraction was compared against 2,000 URLs drawn at random
from the published data, and **all 22 features reproduced the stored values
exactly**.

```bash
cd extras
../.venv/bin/python url_features.py --samples 2000
../.venv/bin/python url_features.py --url "http://smbc-card565.club"
```

Note that the imports in these files assume `../src` is on the path, since they
were written while they lived alongside the pipeline modules. Add it before
running:

```bash
PYTHONPATH=../src ../.venv/bin/python url_features.py --samples 2000
```

## If the dashboard is ever revived

It needs two dependencies that the main pipeline does not:

```bash
../.venv/bin/pip install streamlit==1.60.0 tldextract==5.3.1
```

Then persist a model and launch it:

```bash
PYTHONPATH=../src ../.venv/bin/python persist_models.py
PYTHONPATH=../src ../.venv/bin/streamlit run dashboard.py
```

A limitation found during testing should be carried forward if it is revived. The
model scores real URLs from the dataset accurately in both classes, but URLs
following classic phishing conventions, such as a credential path on a raw IP
address, are frequently scored as legitimate. The dataset's phishing samples are
dominated by abuse of free hosting and site-builder services, while its legitimate
samples are largely established institutional domains, so the model learned that
narrower distinction. This is a property of the training distribution rather than
a defect in the code.
