"""
Feature-based Engagement Score (FES) Module.
Computes audience engagement using sentiment, emotional variance, and normalized metadata.
"""

from typing import Union, Optional
import numpy as np
import pandas as pd


def compute_fes(
    emotional_engagement: Union[float, np.ndarray, pd.Series],
    emotional_variance: Union[float, np.ndarray, pd.Series],
    likes_norm: Union[float, np.ndarray, pd.Series],
    comments_norm: Union[float, np.ndarray, pd.Series],
    w_ee: float = 0.4,
    w_ev: float = 0.2,
    w_likes: float = 0.2,
    w_comments: float = 0.2,
) -> Union[float, np.ndarray, pd.Series]:
    """
    Computes Feature-based Engagement Score (FES):
    FES = w_ee * EE + w_ev * (1.0 - EV) + w_likes * LikesNorm + w_comments * CommentsNorm
    
    Default weights:
        w_ee = 0.4 (Emotional Engagement)
        w_ev = 0.2 (Emotional Consistency / Inverted Variance)
        w_likes = 0.2 (Normalized Likes)
        w_comments = 0.2 (Normalized Comments)
        Total weight sum = 1.0
    """
    weight_sum = w_ee + w_ev + w_likes + w_comments
    if not np.isclose(weight_sum, 1.0):
        # Normalize weights to sum to 1.0
        w_ee /= weight_sum
        w_ev /= weight_sum
        w_likes /= weight_sum
        w_comments /= weight_sum

    inverted_variance = 1.0 - emotional_variance
    
    fes = (
        w_ee * emotional_engagement
        + w_ev * inverted_variance
        + w_likes * likes_norm
        + w_comments * comments_norm
    )
    return fes
