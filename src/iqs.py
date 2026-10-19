"""
Intrinsic Quality Score (IQS) Module.
Combines semantic alignment, duration-based structural depth proxy,
lexical diversity (TTR), and LLM teaching evaluation.
"""

from typing import Union, Optional
import numpy as np
import pandas as pd


def compute_iqs(
    semantic_alignment: Union[float, np.ndarray, pd.Series],
    depth_score: Union[float, np.ndarray, pd.Series],
    lexical_diversity: Union[float, np.ndarray, pd.Series],
    teaching_score: Union[float, np.ndarray, pd.Series],
    w_sem: float = 0.3,
    w_depth: float = 0.2,
    w_lex: float = 0.2,
    w_teach: float = 0.3,
) -> Union[float, np.ndarray, pd.Series]:
    """
    Computes Intrinsic Quality Score (IQS):
    IQS = w_sem * SemanticAlignment + w_depth * DepthScore + w_lex * LexicalDiversity + w_teach * TeachingScore
    
    Default weights:
        w_sem = 0.3 (Semantic query-title-description alignment)
        w_depth = 0.2 (Structural depth proxy based on video duration)
        w_lex = 0.2 (Type-Token Ratio lexical diversity)
        w_teach = 0.3 (LLM rubric-based pedagogical teaching score)
        Total weight sum = 1.0
        
    Note: DepthScore represents video duration as a structural proxy for topic coverage,
    not as evidence that longer videos are inherently educationally superior.
    """
    weight_sum = w_sem + w_depth + w_lex + w_teach
    if not np.isclose(weight_sum, 1.0):
        w_sem /= weight_sum
        w_depth /= weight_sum
        w_lex /= weight_sum
        w_teach /= weight_sum

    iqs = (
        w_sem * semantic_alignment
        + w_depth * depth_score
        + w_lex * lexical_diversity
        + w_teach * teaching_score
    )
    return iqs
