"""
Statistical Significance and Bootstrap Confidence Interval Module.
Implements paired Wilcoxon signed-rank tests and non-parametric bootstrap resampling.
"""

from typing import Dict, Tuple, List, Optional
import numpy as np
from scipy import stats


def paired_wilcoxon_test(
    hybrid_scores: np.ndarray,
    baseline_scores: np.ndarray,
    zero_method: str = "wilcox",
    alternative: str = "two-sided",
) -> Dict[str, float]:
    """
    Computes paired Wilcoxon signed-rank test across matching topics.
    Returns test statistic, p-value, mean difference, and median difference.
    """
    hybrid = np.asarray(hybrid_scores, dtype=float)
    baseline = np.asarray(baseline_scores, dtype=float)
    
    if len(hybrid) != len(baseline):
        raise ValueError(
            f"Array length mismatch: hybrid has {len(hybrid)}, baseline has {len(baseline)}"
        )
        
    diff = hybrid - baseline
    mean_diff = float(np.mean(diff))
    median_diff = float(np.median(diff))
    
    # Check if differences are all zero
    non_zero = diff[diff != 0]
    if len(non_zero) == 0:
        return {
            "statistic": 0.0,
            "p_value": 1.0,
            "mean_difference": 0.0,
            "median_difference": 0.0,
            "n_pairs": len(diff),
            "n_non_zero": 0,
        }
        
    try:
        res = stats.wilcoxon(
            hybrid, baseline, zero_method=zero_method, alternative=alternative
        )
        stat = float(res.statistic)
        p_val = float(res.pvalue)
    except Exception as e:
        stat = 0.0
        p_val = 1.0
        
    return {
        "statistic": stat,
        "p_value": p_val,
        "mean_difference": mean_diff,
        "median_difference": median_diff,
        "n_pairs": len(diff),
        "n_non_zero": len(non_zero),
    }


def bootstrap_confidence_interval(
    values: np.ndarray,
    n_rounds: int = 5000,
    confidence_level: float = 0.95,
    random_seed: int = 42,
) -> Tuple[float, float, float]:
    """
    Computes non-parametric bootstrap confidence interval for the mean.
    Returns (mean_estimate, ci_lower, ci_upper).
    """
    vals = np.asarray(values, dtype=float)
    n = len(vals)
    if n == 0:
        return (0.0, 0.0, 0.0)
    if n == 1:
        return (float(vals[0]), float(vals[0]), float(vals[0]))
        
    rng = np.random.default_rng(random_seed)
    # Resample with replacement
    indices = rng.integers(0, n, size=(n_rounds, n))
    bootstrap_means = np.mean(vals[indices], axis=1)
    
    alpha = (1.0 - confidence_level) / 2.0
    lower = float(np.percentile(bootstrap_means, alpha * 100.0))
    upper = float(np.percentile(bootstrap_means, (1.0 - alpha) * 100.0))
    point_mean = float(np.mean(vals))
    
    return (point_mean, lower, upper)
