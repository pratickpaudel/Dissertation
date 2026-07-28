"""
Central configuration for the phishing detection experiments.

All experimental constants live here so that a single change propagates
through the whole pipeline. This supports the reproducibility requirement
described in Chapter 4.
"""

import os
from pathlib import Path

# joblib probes for physical cores and emits a noisy traceback in containerised
# environments where that probe fails. Declaring the count up front avoids it.
os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(os.cpu_count() or 1))

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
RANDOM_STATE = 42

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
CODE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = CODE_DIR / "data"
RESULTS_DIR = CODE_DIR / "results"
FIGURES_DIR = CODE_DIR / "figures"

for _d in (DATA_DIR, RESULTS_DIR, FIGURES_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Experimental design
# ---------------------------------------------------------------------------
TEST_SIZE = 0.20          # stratified 80/20 train-test split
CV_FOLDS = 5              # stratified 5-fold cross-validation
SCORING = "f1"            # metric used to select hyperparameters
ALPHA = 0.05              # significance level for statistical tests

# Controlled imbalance.
# Both published datasets are close to balanced (UCI 44.3% phishing, the
# Hannousse benchmark exactly 50%). A 10% minority share (~1:9) is induced so
# that imbalance treatment has a measurable effect while retaining enough
# phishing instances in the held-out test set for reliable estimation.
MINORITY_RATIO = 0.10

# Ratios used for the optional sensitivity analysis (Chapter 6).
SENSITIVITY_RATIOS = [0.05, 0.10, 0.20]

DATASETS = ["uci", "hannousse"]

IMBALANCE_METHODS = [
    "none",                     # baseline: no treatment
    "random_oversampling",
    "random_undersampling",
    "smote",
    "adasyn",
    "smoteenn",
    "smotetomek",
    "cost_sensitive",
]

CLASSIFIERS = ["decision_tree", "random_forest", "svm"]

# The 42-configuration matrix in Chapter 4 excludes the "none" baseline.
# It is included above so a reference point is always available.
CORE_IMBALANCE_METHODS = [m for m in IMBALANCE_METHODS if m != "none"]

# ---------------------------------------------------------------------------
# Display names (used in tables and figures)
# ---------------------------------------------------------------------------
METHOD_LABELS = {
    "none": "No Treatment (Baseline)",
    "random_oversampling": "Random Oversampling",
    "random_undersampling": "Random Undersampling",
    "smote": "SMOTE",
    "adasyn": "ADASYN",
    "smoteenn": "SMOTEENN",
    "smotetomek": "SMOTETomek",
    "cost_sensitive": "Cost-Sensitive Learning",
}

CLASSIFIER_LABELS = {
    "decision_tree": "Decision Tree",
    "random_forest": "Random Forest",
    "svm": "Support Vector Machine",
}

DATASET_LABELS = {
    "uci": "UCI Phishing Websites",
    "hannousse": "Hannousse & Yahiouche",
}
