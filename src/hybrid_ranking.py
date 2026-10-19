"""
Adaptive Hybrid Ranking Module.
Dynamically balances Feature-based Engagement Score (FES) and Intrinsic Quality Score (IQS)
based on engagement strength derived from relevant comment count.
"""

from typing import Union, Optional
import numpy as np
import pandas as pd


def compute_engagement_strength(
    c_rel: Union[int, float, np.ndarray, pd.Series]
) -> Union[float, np.ndarray, pd.Series]:
    """
    Computes logarithmic Engagement Strength:
    ES_i = ln(1 + C_rel_i)
    Reduces the distortive impact of viral videos with massive comment volumes.
    """
    # Ensure non-negative counts
    if isinstance(c_rel, (int, float)):
        c_rel = max(0.0, float(c_rel))
    elif isinstance(c_rel, (np.ndarray, pd.Series)):
        c_rel = np.maximum(0.0, c_rel.astype(float))
    return np.log1p(c_rel)


def compute_adaptive_alpha(
    c_rel: Union[int, float, np.ndarray, pd.Series],
    k: float = 5.0,
) -> Union[float, np.ndarray, pd.Series]:
    """
    Computes adaptive weighting coefficient alpha_i in [0, 1]:
    alpha_i = min(1.0, ES_i / k) = min(1.0, ln(1 + C_rel_i) / k)
    
    When comment evidence is low, alpha approaches 0, prioritizing IQS.
    When comment evidence is rich, alpha approaches 1, allowing audience signals (FES) to contribute.
    """
    if k <= 0:
        raise ValueError(f"Adaptive scaling hyperparameter k must be > 0, got {k}")
    es = compute_engagement_strength(c_rel)
    alpha = np.clip(es / k, 0.0, 1.0)
    return alpha


def compute_hybrid_score(
    fes: Union[float, np.ndarray, pd.Series],
    iqs: Union[float, np.ndarray, pd.Series],
    alpha: Union[float, np.ndarray, pd.Series],
) -> Union[float, np.ndarray, pd.Series]:
    """
    Computes final Adaptive Hybrid Ranking Score:
    Hybrid_i = alpha_i * FES_i + (1.0 - alpha_i) * IQS_i
    """
    return alpha * fes + (1.0 - alpha) * iqs


def rank_items(
    df: pd.DataFrame,
    score_column: str = "hybrid_score",
    ascending: bool = False,
    group_by: Optional[str] = None,
) -> pd.DataFrame:
    """
    Assigns 1-indexed ranks based on score_column.
    If group_by is provided, ranks are computed per group (e.g. per topic).
    """
    df = df.copy()
    if group_by and group_by in df.columns:
        df["rank"] = df.groupby(group_by)[score_column].rank(
            ascending=ascending, method="min"
        ).astype(int)
    else:
        df["rank"] = df[score_column].rank(
            ascending=ascending, method="min"
        ).astype(int)
    return df.sort_values(by=[group_by, "rank"] if group_by else "rank")
