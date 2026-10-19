"""
Unit tests for ranking evaluation metrics: NDCG@K, MAP@10, MRR, Precision@K, Recall@K.
"""

import pytest
import numpy as np
from src.evaluation import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    average_precision_at_k,
    ndcg_at_k,
    relevance_to_binary,
)


def test_relevance_to_binary():
    assert relevance_to_binary("Accepted") == 1
    assert relevance_to_binary("rejected") == 0
    assert relevance_to_binary(1) == 1
    assert relevance_to_binary(0) == 0
    with pytest.raises(ValueError):
        relevance_to_binary("invalid_label")


def test_precision_and_recall():
    labels = [1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
    # Total relevant = 3
    # Top 5: [1, 0, 1, 1, 0] -> 3 relevant out of 5 -> P@5 = 0.6
    assert precision_at_k(labels, k=5) == 0.6
    # R@5 = 3 / 3 = 1.0
    assert recall_at_k(labels, k=5) == 1.0
    
    # Top 2: [1, 0] -> 1 relevant out of 2 -> P@2 = 0.5, R@2 = 1/3
    assert precision_at_k(labels, k=2) == 0.5
    assert np.isclose(recall_at_k(labels, k=2), 1.0 / 3.0)


def test_reciprocal_rank():
    # First relevant at rank 1 -> RR = 1.0
    assert reciprocal_rank([1, 0, 0]) == 1.0
    
    # First relevant at rank 3 -> RR = 1/3
    assert np.isclose(reciprocal_rank([0, 0, 1, 0]), 1.0 / 3.0)
    
    # No relevant items -> RR = 0.0
    assert reciprocal_rank([0, 0, 0]) == 0.0


def test_average_precision():
    # Labels: [1, 0, 1]
    # rank 1 (hit 1): P@1 = 1/1 = 1.0
    # rank 2: no hit
    # rank 3 (hit 2): P@3 = 2/3
    # Total relevant = 2 -> AP = (1.0 + 2/3) / 2 = (5/3) / 2 = 5/6 ~ 0.8333
    labels = [1, 0, 1]
    assert np.isclose(average_precision_at_k(labels, k=3), 5.0 / 6.0)


def test_ndcg_at_k():
    labels = [1, 0, 1]
    scores = [0.9, 0.8, 0.7]
    val = ndcg_at_k(labels, scores, k=3)
    assert 0.0 < val <= 1.0
    
    # Perfect ranking
    labels_perf = [1, 1, 0]
    scores_perf = [0.9, 0.8, 0.1]
    assert np.isclose(ndcg_at_k(labels_perf, scores_perf, k=3), 1.0)
