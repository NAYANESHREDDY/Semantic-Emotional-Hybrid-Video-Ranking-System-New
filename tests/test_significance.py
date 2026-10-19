"""
Unit tests for statistical significance: paired Wilcoxon signed-rank test and bootstrap CI.
"""

import pytest
import numpy as np
from src.significance import paired_wilcoxon_test, bootstrap_confidence_interval


def test_paired_wilcoxon_identical():
    # When arrays are identical, p-value should be 1.0 and mean diff 0.0
    a = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
    res = paired_wilcoxon_test(a, a)
    assert res["mean_difference"] == 0.0
    assert res["p_value"] == 1.0


def test_paired_wilcoxon_distinct():
    # System A consistently higher than System B
    a = np.array([0.6, 0.7, 0.8, 0.85, 0.9, 0.75, 0.82, 0.88, 0.91, 0.79])
    b = np.array([0.4, 0.5, 0.6, 0.65, 0.7, 0.55, 0.62, 0.68, 0.71, 0.59])
    res = paired_wilcoxon_test(a, b)
    assert res["mean_difference"] > 0.0
    assert res["p_value"] < 0.01


def test_bootstrap_confidence_interval():
    data = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
    mean, lower, upper = bootstrap_confidence_interval(data, n_rounds=2000, random_seed=42)
    assert np.isclose(mean, 0.7)
    assert lower < mean < upper
    assert 0.5 <= lower
    assert upper <= 0.9
