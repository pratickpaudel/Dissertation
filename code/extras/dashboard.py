"""
Explainability dashboard (Section 3.10).

Presents the trained detection models through an interactive interface, so that
predictions and their SHAP feature attributions can be inspected alongside the
comparative results of the study.

The dashboard is a demonstration artefact. It shows how the explainability
outputs could support interpretation in an operational setting; it is not
subjected to a formal usability study.

Run with:

    streamlit run dashboard.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from config import (  # noqa: E402
    CLASSIFIER_LABELS,
    DATASET_LABELS,
    DATASETS,
    METHOD_LABELS,
    RESULTS_DIR,
)

st.set_page_config(page_title="Phishing Detection Explainability", layout="wide")

POSITIVE = "Phishing"
NEGATIVE = "Legitimate"


# ---------------------------------------------------------------------------
# Cached loaders
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading model...")
def load_model(dataset: str):
    from persist_models import load_persisted

    return load_persisted(dataset)


@st.cache_resource(show_spinner="Preparing explainer...")
def load_explainer(dataset: str):
    """Build a SHAP TreeExplainer for the persisted model."""
    import shap

    model, _, _ = load_model(dataset)
    return shap.TreeExplainer(model.named_steps["classifier"])


@st.cache_data(show_spinner=False)
def load_table(name: str) -> pd.DataFrame | None:
    path = RESULTS_DIR / f"{name}.csv"
    return pd.read_csv(path) if path.exists() else None


def scale_features(model, X: pd.DataFrame) -> pd.DataFrame:
    """Apply every pipeline step before the classifier.

    SHAP has to see the data in the space the classifier was fitted in, so the
    scaler is applied first. Resampling steps are skipped: they change how many
    rows exist during training, not how a single instance is represented.
    """
    out = X
    for _, step in model.steps[:-1]:
        if hasattr(step, "transform"):
            out = step.transform(out)
    return pd.DataFrame(np.asarray(out), columns=X.columns, index=X.index)


def positive_class_shap(values) -> np.ndarray:
    """Reduce SHAP output to contributions towards the phishing class.

    SHAP returns a list per class, a 3-D array, or a 2-D array depending on the
    model and version, so all three shapes are normalised here.
    """
    if isinstance(values, list):
        return np.asarray(values[1] if len(values) > 1 else values[0])
    arr = np.asarray(values)
    if arr.ndim == 3:
        return arr[:, :, 1] if arr.shape[2] > 1 else arr[:, :, 0]
    return arr


def predict_one(model, X_row: pd.DataFrame) -> tuple[int, float]:
    """Return the predicted label and the probability of the phishing class."""
    label = int(model.predict(X_row)[0])
    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(X_row)[0][1])
    else:
        # Map a decision-function margin into (0, 1) for display only.
        prob = float(1 / (1 + np.exp(-model.decision_function(X_row)[0])))
    return label, prob


def contribution_frame(
    shap_row: np.ndarray, X_row: pd.DataFrame, top_n: int = 12
) -> pd.DataFrame:
    """Per-feature contributions for one instance, ranked by magnitude."""
    df = pd.DataFrame(
        {
            "Feature": X_row.columns,
            "Value": X_row.iloc[0].to_numpy(),
            "Contribution": shap_row,
        }
    )
    df["Direction"] = np.where(
        df["Contribution"] > 0, f"towards {POSITIVE}", f"towards {NEGATIVE}"
    )
    return (
        df.assign(magnitude=df["Contribution"].abs())
        .sort_values("magnitude", ascending=False)
        .head(top_n)
        .drop(columns="magnitude")
        .reset_index(drop=True)
    )


def plot_contributions(df: pd.DataFrame):
    """Horizontal bar chart of signed feature contributions."""
    fig, ax = plt.subplots(figsize=(7, max(3.0, 0.34 * len(df))))
    ordered = df.iloc[::-1]
    colours = ["#b03a2e" if v > 0 else "#2e6b46" for v in ordered["Contribution"]]
    ax.barh(ordered["Feature"], ordered["Contribution"], color=colours)
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_xlabel(f"SHAP contribution  (negative favours {NEGATIVE}, positive favours {POSITIVE})")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


def verdict(label: int, prob: float) -> None:
    """Render the prediction prominently."""
    col1, col2 = st.columns([2, 1])
    with col1:
        if label == 1:
            st.error(f"### Predicted: {POSITIVE}")
        else:
            st.success(f"### Predicted: {NEGATIVE}")
    with col2:
        st.metric("Probability of phishing", f"{prob:.1%}")


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("Configuration")

available = [d for d in DATASETS if (Path(__file__).parent / "models" / f"{d}_model.joblib").exists()]

if not available:
    st.title("Phishing Detection Explainability Dashboard")
    st.error(
        "No trained models found. Run the following from the `code` directory "
        "before starting the dashboard:\n\n"
        "```bash\n.venv/bin/python src/persist_models.py\n```"
    )
    st.stop()

dataset = st.sidebar.selectbox(
    "Dataset",
    available,
    format_func=lambda d: DATASET_LABELS.get(d, d),
)

model, sample, meta = load_model(dataset)
features = meta["features"]

st.sidebar.markdown("---")
st.sidebar.subheader("Model")
st.sidebar.write(f"**Classifier:** {CLASSIFIER_LABELS.get(meta['classifier'], meta['classifier'])}")
st.sidebar.write(f"**Imbalance treatment:** {METHOD_LABELS.get(meta['imbalance_method'], meta['imbalance_method'])}")
st.sidebar.write(f"**Features:** {meta['n_features']}")
st.sidebar.write(f"**Training instances:** {meta['train_size']:,}")
st.sidebar.caption(
    "This configuration was selected because it achieved the highest mean "
    "F1-score for this dataset in the comparative experiments."
)

st.sidebar.markdown("---")
st.sidebar.subheader("Test-set performance")
m = meta["metrics"]
c1, c2 = st.sidebar.columns(2)
c1.metric("F1", f"{m['f1']:.3f}")
c2.metric("Recall", f"{m['recall']:.3f}")
c1.metric("Precision", f"{m['precision']:.3f}")
c2.metric("PR-AUC", f"{m['pr_auc']:.3f}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
st.title("Phishing Detection Explainability Dashboard")
st.caption(
    "Interactive interface to the models produced by the comparative study of "
    "class imbalance treatment techniques."
)

tab_predict, tab_global, tab_results = st.tabs(
    ["Prediction and explanation", "Global feature importance", "Comparative results"]
)

# --- Tab 1: prediction ------------------------------------------------------
with tab_predict:
    supports_url = dataset == "urlphish"

    if supports_url:
        mode = st.radio(
            "Input method",
            ["Enter a URL", "Select a test instance"],
            horizontal=True,
        )
    else:
        mode = "Select a test instance"
        st.info(
            f"The {DATASET_LABELS.get(dataset, dataset)} dataset includes domain "
            "registration and hosting attributes that cannot be derived from a URL "
            "string alone, so instances are selected from the held-out test set."
        )

    X_row = None
    true_label = None

    if mode == "Enter a URL":
        from url_features import extract_frame, parse_url

        st.warning(
            "**Interpret URL input with care.** The model reflects the distribution "
            "it was trained on. In this dataset the phishing samples are dominated by "
            "abuse of free hosting and site-builder services, while the legitimate "
            "samples are largely established institutional domains. URLs that follow "
            "other phishing patterns, such as a login path on a raw IP address, may "
            "be scored as legitimate because that pattern is under-represented in the "
            "training data. This is a property of the dataset rather than a defect in "
            "the model, and is discussed as a limitation of the study.",
            icon=":material/warning:",
        )

        examples = {
            "Phishing — site-builder abuse": "https://mypnbkewane.weebly.com/",
            "Phishing — suspicious TLD": "http://smbc-card565.club",
            "Phishing — file-sharing abuse": "https://forms.gle/arMkMEDaJqC865aS8",
            "Legitimate — university": "http://www.nu.edu/",
            "Legitimate — government": "http://en.bmfj.gv.at/",
        }
        choice = st.selectbox(
            "Start from an example drawn from the dataset, or edit it freely below",
            list(examples),
        )

        url = st.text_input(
            "URL",
            value=examples[choice],
            help="Features are derived from the URL exactly as defined in the source dataset.",
        )

        if url.strip():
            X_row = extract_frame(url, feature_order=features)
            parts = parse_url(url)
            with st.expander("Parsed URL components and extracted features"):
                st.write(
                    f"**Host:** `{parts['host']}` | "
                    f"**Registrable domain:** `{parts['registrable']}` | "
                    f"**Public suffix:** `{parts['suffix'] or 'none (IP address)'}`"
                )
                st.dataframe(X_row.T.rename(columns={0: "Value"}), use_container_width=True)
    else:
        max_idx = len(sample) - 1
        idx = st.number_input(
            f"Test instance (0 to {max_idx})", 0, max_idx, 0, step=1
        )
        row = sample.iloc[[int(idx)]]
        true_label = int(row["__true_label"].iloc[0])
        X_row = row[features].reset_index(drop=True)

        st.write(
            f"**Actual label:** "
            f"{POSITIVE if true_label == 1 else NEGATIVE}"
        )

    if X_row is not None:
        label, prob = predict_one(model, X_row)
        verdict(label, prob)

        if true_label is not None:
            if label == true_label:
                st.caption("The prediction matches the recorded label.")
            else:
                st.caption(
                    "The prediction differs from the recorded label; this instance "
                    "is misclassified by the model."
                )

        st.subheader("Why this prediction was made")
        st.caption(
            "SHAP attributes the prediction to individual features. Bars extending "
            f"right push the model towards {POSITIVE}; bars extending left push it "
            f"towards {NEGATIVE}."
        )

        explainer = load_explainer(dataset)
        shap_values = positive_class_shap(
            explainer.shap_values(scale_features(model, X_row))
        )
        contributions = contribution_frame(shap_values[0], X_row)

        left, right = st.columns([3, 2])
        with left:
            st.pyplot(plot_contributions(contributions))
        with right:
            display = contributions.copy()
            display["Value"] = display["Value"].map(lambda v: f"{v:,.4g}")
            display["Contribution"] = display["Contribution"].map(lambda v: f"{v:+.4f}")
            st.dataframe(display, use_container_width=True, hide_index=True)

        if supports_url and mode == "Enter a URL":
            from url_features import FEATURE_DESCRIPTIONS

            with st.expander("What these features mean"):
                for name in contributions["Feature"]:
                    st.write(f"**{name}** — {FEATURE_DESCRIPTIONS.get(name, 'n/a')}")

# --- Tab 2: global importance ----------------------------------------------
with tab_global:
    st.subheader("Which features drive the model overall")
    st.caption(
        "Mean absolute SHAP value across a sample of held-out instances. This "
        "measures how much each feature moves predictions, regardless of direction."
    )

    n_global = st.slider("Instances to analyse", 50, min(300, len(sample)), 150, step=50)

    with st.spinner("Computing attributions..."):
        X_global = sample[features].iloc[:n_global]
        explainer = load_explainer(dataset)
        values = positive_class_shap(explainer.shap_values(scale_features(model, X_global)))

        importance = (
            pd.DataFrame(
                {
                    "Feature": features,
                    "Mean |SHAP|": np.abs(values).mean(axis=0),
                    "Mean SHAP": values.mean(axis=0),
                }
            )
            .sort_values("Mean |SHAP|", ascending=False)
            .reset_index(drop=True)
        )

    top = importance.head(15)
    fig, ax = plt.subplots(figsize=(8, 5))
    ordered = top.iloc[::-1]
    ax.barh(ordered["Feature"], ordered["Mean |SHAP|"], color="#2c3e66")
    ax.set_xlabel("Mean absolute SHAP value")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    left, right = st.columns([3, 2])
    with left:
        st.pyplot(fig)
    with right:
        st.dataframe(
            top.round(4), use_container_width=True, hide_index=True
        )

    comparison = load_table(f"shap_method_comparison_{dataset}_{meta['classifier']}")
    if comparison is not None:
        st.subheader("Does imbalance treatment change what the model relies on?")
        st.caption(
            "Rank of each feature under different treatment methods. A rank range "
            "of zero means the feature holds the same position throughout, so the "
            "treatment changed the decision boundary without changing which "
            "evidence dominates."
        )
        st.dataframe(comparison, use_container_width=True, hide_index=True)

# --- Tab 3: comparative results --------------------------------------------
with tab_results:
    st.subheader("Results of the comparative study")
    st.caption(
        "Means across three replications, covering both datasets, seven imbalance "
        "treatment techniques and three classifiers."
    )

    by_classifier = load_table("table_5_3_by_classifier")
    by_method = load_table("table_5_4_by_method")
    best_worst = load_table("table_5_5_best_worst")
    friedman = load_table("friedman_tests")

    if by_classifier is not None:
        st.markdown("**Performance by classifier**")
        st.dataframe(by_classifier, use_container_width=True, hide_index=True)

    if by_method is not None:
        st.markdown("**Performance by imbalance treatment method**")
        st.dataframe(by_method, use_container_width=True, hide_index=True)
        st.caption(
            "Every technique raises recall relative to the untreated baseline but "
            "lowers precision. The appropriate choice therefore depends on the "
            "relative cost of a missed phishing site against a false alarm."
        )

    if best_worst is not None:
        st.markdown("**Best and worst configuration per dataset**")
        st.dataframe(best_worst, use_container_width=True, hide_index=True)

    if friedman is not None:
        st.markdown("**Statistical significance**")
        st.dataframe(friedman, use_container_width=True, hide_index=True)

    if all(t is None for t in (by_classifier, by_method, best_worst, friedman)):
        st.warning(
            "No result tables found. Run `src/experiment.py`, then `src/analysis.py` "
            "and `src/statistical_tests.py` to generate them."
        )
