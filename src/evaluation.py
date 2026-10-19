"""
Evaluation Metrics Module for Information Retrieval and Educational Video Ranking.
Implements per-topic NDCG@K, MAP@K, MRR, Precision@K, and Recall@K on expert binary ground truth.
"""

from typing import List, Dict, Union, Any, Optional
import numpy as np
import pandas as pd
from sklearn.metrics import ndcg_score


def relevance_to_binary(value: Any) -> int:
    """
    Normalizes diverse relevance representations to binary integer {0, 1}.
    """
    val_str = str(value).strip().lower()
    if val_str in {"accepted", "accept", "relevant", "1", "true", "1.0"}:
        return 1
    if val_str in {"rejected", "reject", "irrelevant", "0", "false", "0.0"}:
        return 0
    raise ValueError(f"Unknown or ambiguous relevance label: {value}")


def precision_at_k(labels: Union[List[int], np.ndarray], k: int) -> float:
    """
    Computes Precision@K:
    P@K = (Number of relevant items in top-K) / K
    """
    labels = np.asarray(labels, dtype=int)
    if len(labels) == 0 or k <= 0:
        return 0.0
    k_eff = min(k, len(labels))
    return float(labels[:k_eff].mean())


def recall_at_k(labels: Union[List[int], np.ndarray], k: int) -> float:
    """
    Computes Recall@K:
    R@K = (Number of relevant items in top-K) / (Total relevant items in pool)
    """
    labels = np.asarray(labels, dtype=int)
    relevant = int(labels.sum())
    if relevant == 0 or len(labels) == 0 or k <= 0:
        return 0.0
    k_eff = min(k, len(labels))
    return float(labels[:k_eff].sum() / relevant)


def reciprocal_rank(labels: Union[List[int], np.ndarray]) -> float:
    """
    Computes Mean Reciprocal Rank (MRR) component:
    RR = 1.0 / (rank of first relevant item)
    Returns 0.0 if no relevant items are present.
    """
    labels = np.asarray(labels, dtype=int)
    positions = np.where(labels == 1)[0]
    if len(positions) == 0:
        return 0.0
    return float(1.0 / (positions[0] + 1))


def average_precision_at_k(labels: Union[List[int], np.ndarray], k: int = 10) -> float:
    """
    Computes Average Precision at K (MAP component):
    AP@K = sum_{i=1..k} (P@i * rel(i)) / min(TotalRelevant, K)
    """
    labels = np.asarray(labels, dtype=int)
    if len(labels) == 0 or k <= 0:
        return 0.0
    k_eff = min(k, len(labels))
    relevant_total = int(labels.sum())
    if relevant_total == 0:
        return 0.0

    hits = 0
    score = 0.0
    for i in range(k_eff):
        if labels[i] == 1:
            hits += 1
            score += hits / (i + 1)
            
    denominator = min(relevant_total, k_eff)
    return float(score / denominator)


def ndcg_at_k(labels: Union[List[int], np.ndarray], scores: Union[List[float], np.ndarray], k: int) -> float:
    """
    Computes Normalized Discounted Cumulative Gain at K (NDCG@K).
    Uses standard scikit-learn NDCG formulation.
    Returns 0.0 if all labels are 0.
    """
    labels = np.asarray(labels, dtype=float)
    scores = np.asarray(scores, dtype=float)
    if len(labels) == 0 or labels.sum() == 0 or k <= 0:
        return 0.0
    k_eff = min(k, len(labels))
    return float(ndcg_score([labels], [scores], k=k_eff))


def compute_ranking_metrics_for_topic(
    topic_df: pd.DataFrame,
    score_col: str,
    relevance_col: str = "relevance",
) -> Dict[str, float]:
    """
    Sorts items within a topic by score_col (descending) and computes all 8 evaluation metrics.
    """
    sorted_df = topic_df.sort_values(by=score_col, ascending=False).reset_index(drop=True)
    labels = sorted_df[relevance_col].map(relevance_to_binary).to_numpy(dtype=int)
    scores = sorted_df[score_col].to_numpy(dtype=float)

    return {
        "NDCG@5": ndcg_at_k(labels, scores, k=5),
        "NDCG@10": ndcg_at_k(labels, scores, k=10),
        "MAP@10": average_precision_at_k(labels, k=10),
        "MRR": reciprocal_rank(labels),
        "Precision@5": precision_at_k(labels, k=5),
        "Precision@10": precision_at_k(labels, k=10),
        "Recall@5": recall_at_k(labels, k=5),
        "Recall@10": recall_at_k(labels, k=10),
        "n_candidates": len(labels),
        "n_relevant": int(labels.sum()),
    }


def evaluate_ranking_dataframe(
    df: pd.DataFrame,
    score_col: str,
    topic_col: str = "topic_id",
    relevance_col: str = "relevance",
) -> pd.DataFrame:
    """
    Computes per-topic evaluation metrics for an entire prediction dataframe.
    Returns a dataframe indexed by topic_col with metric columns.
    """
    topic_results = []
    for topic_id, group in df.groupby(topic_col):
        metrics = compute_ranking_metrics_for_topic(
            group, score_col=score_col, relevance_col=relevance_col
        )
        metrics[topic_col] = topic_id
        if "domain" in group.columns:
            metrics["domain"] = group["domain"].iloc[0]
        if "topic" in group.columns:
            metrics["topic"] = group["topic"].iloc[0]
        topic_results.append(metrics)
        
    return pd.DataFrame(topic_results)
