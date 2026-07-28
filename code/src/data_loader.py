"""
Dataset loading for the phishing detection experiments (Step 1 of the pipeline).

Two benchmark datasets are supported:

* ``uci``       - UCI Phishing Websites (Mohammad & McCluskey, 2012)
                  11,055 instances, 30 features.
* ``hannousse`` - Hannousse & Yahiouche (2021) benchmark,
                  11,430 URLs, 87 features.

Label convention
----------------
Throughout the project the **phishing class is the positive class (1)** and
the legitimate class is the negative class (0). This matters because recall,
precision, F1 and PR-AUC are all reported with respect to the positive class,
and phishing detection is the minority-class problem of interest.

Controlled imbalance
--------------------
Both published datasets are close to balanced (UCI is ~44% phishing, the
Hannousse benchmark is exactly 50/50). Because the research question concerns
*class imbalance treatment*, an imbalance ratio can be induced by randomly
downsampling the phishing (minority) class. See ``load_dataset`` for details.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import DATA_DIR, RANDOM_STATE

UCI_CACHE = DATA_DIR / "uci_phishing.csv"
HANNOUSSE_FILE = DATA_DIR / "dataset_B_05_2020.csv"
HANNOUSSE_URL = (
    "https://data.mendeley.com/public-files/datasets/c2gw7fy2j4/"
    "files/575316f4-ee1d-453e-a04f-7b950915b61b/file_downloaded"
)


# ---------------------------------------------------------------------------
# Individual loaders
# ---------------------------------------------------------------------------
def load_uci() -> tuple[pd.DataFrame, pd.Series]:
    """Load the UCI Phishing Websites dataset.

    The raw target uses ``-1`` for phishing and ``1`` for legitimate; it is
    remapped so that phishing is ``1`` and legitimate is ``0``.
    """
    if UCI_CACHE.exists():
        df = pd.read_csv(UCI_CACHE)
    else:
        from ucimlrepo import fetch_ucirepo

        repo = fetch_ucirepo(id=327)
        df = pd.concat([repo.data.features, repo.data.targets], axis=1)
        df.to_csv(UCI_CACHE, index=False)

    target_col = df.columns[-1]
    X = df.drop(columns=[target_col])
    y = df[target_col].map({-1: 1, 1: 0}).astype(int)
    y.name = "phishing"
    return X, y


def load_hannousse() -> tuple[pd.DataFrame, pd.Series]:
    """Load the Hannousse & Yahiouche benchmark dataset.

    The ``url`` column is dropped because it is an identifier rather than a
    predictive feature. The ``status`` column is mapped to the project label
    convention (phishing = 1).
    """
    if not HANNOUSSE_FILE.exists():
        import urllib.request

        urllib.request.urlretrieve(HANNOUSSE_URL, HANNOUSSE_FILE)

    df = pd.read_csv(HANNOUSSE_FILE)
    y = df["status"].map({"phishing": 1, "legitimate": 0}).astype(int)
    y.name = "phishing"
    X = df.drop(columns=["status", "url"])
    return X, y


LOADERS = {"uci": load_uci, "hannousse": load_hannousse}


# ---------------------------------------------------------------------------
# Controlled imbalance
# ---------------------------------------------------------------------------
def induce_imbalance(
    X: pd.DataFrame,
    y: pd.Series,
    minority_ratio: float,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.Series]:
    """Randomly downsample the phishing class to a target proportion.

    Parameters
    ----------
    minority_ratio
        Desired share of phishing instances in the returned data, e.g. ``0.10``
        for a 10% phishing / 90% legitimate split.

    Notes
    -----
    Only the minority (phishing) class is reduced; every legitimate instance is
    retained. This produces a realistic imbalance without fabricating data.
    """
    if not 0 < minority_ratio < 0.5:
        raise ValueError("minority_ratio must be between 0 and 0.5 (exclusive)")

    rng = np.random.RandomState(random_state)
    pos_idx = y[y == 1].index.to_numpy()
    neg_idx = y[y == 0].index.to_numpy()

    # n_pos / (n_pos + n_neg) = ratio  ->  n_pos = ratio * n_neg / (1 - ratio)
    n_pos_target = int(round(minority_ratio * len(neg_idx) / (1 - minority_ratio)))
    n_pos_target = max(1, min(n_pos_target, len(pos_idx)))

    keep_pos = rng.choice(pos_idx, size=n_pos_target, replace=False)
    keep = np.concatenate([neg_idx, keep_pos])
    keep.sort()

    return X.loc[keep].reset_index(drop=True), y.loc[keep].reset_index(drop=True)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def load_dataset(
    name: str,
    minority_ratio: float | None = None,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.Series]:
    """Load a dataset by name, optionally inducing a target imbalance ratio.

    Parameters
    ----------
    name
        Either ``"uci"`` or ``"hannousse"``.
    minority_ratio
        If given, the phishing class is downsampled to this proportion.
        If ``None`` the dataset is returned with its native class balance.
    random_state
        Controls which minority instances are retained when inducing the
        imbalance. Varying this across repeated runs is what makes each repeat
        an independent sample rather than a re-run of the same subset.
    """
    if name not in LOADERS:
        raise ValueError(f"Unknown dataset '{name}'. Expected one of {list(LOADERS)}.")

    X, y = LOADERS[name]()

    # Guard against non-numeric columns slipping through.
    non_numeric = X.select_dtypes(exclude="number").columns.tolist()
    if non_numeric:
        X = X.drop(columns=non_numeric)

    if minority_ratio is not None:
        X, y = induce_imbalance(X, y, minority_ratio, random_state=random_state)

    return X, y


def describe(
    name: str,
    minority_ratio: float | None = None,
    random_state: int = RANDOM_STATE,
) -> dict:
    """Return summary statistics used for the dataset table in Chapter 5."""
    X, y = load_dataset(name, minority_ratio, random_state=random_state)
    n_pos = int((y == 1).sum())
    n_neg = int((y == 0).sum())
    return {
        "dataset": name,
        "instances": len(y),
        "features": X.shape[1],
        "phishing": n_pos,
        "legitimate": n_neg,
        "phishing_pct": round(100 * n_pos / len(y), 2),
        "imbalance_ratio": f"1:{round(n_neg / n_pos, 2)}",
        "missing_values": int(X.isnull().sum().sum()),
    }


if __name__ == "__main__":
    for ds in LOADERS:
        print(describe(ds))
