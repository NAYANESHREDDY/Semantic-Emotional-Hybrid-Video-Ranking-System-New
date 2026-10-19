"""
Unit tests for core component scoring: TTR, FES, IQS, adaptive alpha, and Hybrid ranking.
"""

import pytest
import numpy as np
from src.preprocessing import compute_ttr, clean_text
from src.fes import compute_fes
from src.iqs import compute_iqs
from src.hybrid_ranking import compute_adaptive_alpha, compute_hybrid_score


def test_clean_text():
    raw = "<p>Learn Python in 10 minutes! Check out https://example.com</p>"
    cleaned = clean_text(raw)
    assert "<p>" not in cleaned
    assert "https" not in cleaned
    assert "Learn Python" in cleaned


def test_compute_ttr():
    # 4 distinct tokens out of 4 total -> TTR = 1.0
    text_distinct = "python data science machine"
    assert compute_ttr(text_distinct) == 1.0
    
    # 2 distinct tokens out of 4 total -> TTR = 0.5
    text_repeated = "python python data data"
    assert compute_ttr(text_repeated) == 0.5
    
    # Empty string
    assert compute_ttr("") == 0.0


def test_compute_fes():
    # Equal 0.5 across all 4 factors
    # FES = 0.4*0.5 + 0.2*(1 - 0.5) + 0.2*0.5 + 0.2*0.5 = 0.2 + 0.1 + 0.1 + 0.1 = 0.5
    score = compute_fes(
        emotional_engagement=0.5,
        emotional_variance=0.5,
        likes_norm=0.5,
        comments_norm=0.5
    )
    assert np.isclose(score, 0.5)
    
    # Perfect engagement with 0 variance
    # FES = 0.4*1.0 + 0.2*1.0 + 0.2*1.0 + 0.2*1.0 = 1.0
    perfect = compute_fes(1.0, 0.0, 1.0, 1.0)
    assert np.isclose(perfect, 1.0)


def test_compute_iqs():
    # IQS = 0.3*sem + 0.2*depth + 0.2*lex + 0.3*teach
    score = compute_iqs(
        semantic_alignment=0.8,
        depth_score=0.5,
        lexical_diversity=0.6,
        teaching_score=0.9
    )
    expected = 0.3 * 0.8 + 0.2 * 0.5 + 0.2 * 0.6 + 0.3 * 0.9
    assert np.isclose(score, expected)


def test_adaptive_alpha():
    # With 0 comments: alpha = min(1.0, ln(1)/5) = 0.0
    assert compute_adaptive_alpha(0, k=5.0) == 0.0
    
    # With large comment count: alpha should cap at 1.0
    assert compute_adaptive_alpha(10000, k=5.0) == 1.0
    
    # Intermediate comment count: C_rel = 100 -> ln(101) / 5 ~ 4.615 / 5 = 0.923
    alpha_100 = compute_adaptive_alpha(100, k=5.0)
    assert 0.9 < alpha_100 < 1.0


def test_compute_hybrid_score():
    fes = 0.8
    iqs = 0.4
    alpha = 0.5
    # Hybrid = 0.5 * 0.8 + 0.5 * 0.4 = 0.6
    assert np.isclose(compute_hybrid_score(fes, iqs, alpha), 0.6)
    
    # When alpha is 0.0 (no comments), Hybrid strictly equals IQS
    assert np.isclose(compute_hybrid_score(fes, iqs, 0.0), 0.4)
    
    # When alpha is 1.0 (high comments), Hybrid strictly equals FES
    assert np.isclose(compute_hybrid_score(fes, iqs, 1.0), 0.8)
