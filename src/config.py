"""
Configuration module for the Educational Video Ranking Framework.
Defines model identifiers, component weights, adaptive thresholds, random seeds, and directory paths.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class PipelineConfig:
    # Model identifiers
    EMBEDDING_MODEL: str = "intfloat/e5-base-v2"
    SENTIMENT_MODEL: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    TEACHING_SCORE_MODEL: str = "gemini-3.5-flash-lite"
    
    # Feature-based Engagement Score (FES) weights
    # FES = 0.4 * EE + 0.2 * (1 - EV) + 0.2 * LikesNorm + 0.2 * CommentsNorm
    FES_WEIGHT_ENGAGEMENT: float = 0.4
    FES_WEIGHT_VARIANCE: float = 0.2
    FES_WEIGHT_LIKES: float = 0.2
    FES_WEIGHT_COMMENTS: float = 0.2
    
    # Intrinsic Quality Score (IQS) weights
    # IQS = 0.3 * SemanticAlignment + 0.2 * Depth + 0.2 * LexicalDiversity + 0.3 * TeachingScore
    IQS_WEIGHT_SEMANTIC: float = 0.3
    IQS_WEIGHT_DEPTH: float = 0.2
    IQS_WEIGHT_LEXICAL: float = 0.2
    IQS_WEIGHT_TEACHING: float = 0.3
    
    # Adaptive weighting hyperparameter
    # alpha = min(1.0, ln(1 + C_rel) / k), default k = 5.0
    ADAPTIVE_K: float = 5.0
    
    # Random seed for statistical bootstrap and RankNet
    RANDOM_SEED: int = 42
    BOOTSTRAP_ROUNDS: int = 5000
    
    # Expected cohort sizes verified from empirical evidence
    INTERNAL_FROZEN_COHORT_SIZE: int = 98
    LAK_BENCHMARK_TOTAL_PAIRS: int = 914
    LAK_BENCHMARK_ACCESSIBLE_PAIRS: int = 888
    LAK_BENCHMARK_TOPICS: int = 54
    LAK_BENCHMARK_ACCESSIBLE_VIDEOS: int = 841
    
    # API Keys loaded securely from environment variables
    YOUTUBE_API_KEY: str = field(default_factory=lambda: os.getenv("YOUTUBE_API_KEY", ""))
    GEMINI_API_KEY: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    
    # Project paths
    BASE_DIR: Path = field(default_factory=lambda: Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parent.parent)))
    DATA_DIR: Path = field(init=False)
    RESULTS_DIR: Path = field(init=False)
    
    def __post_init__(self):
        self.DATA_DIR = self.BASE_DIR / "data"
        self.RESULTS_DIR = self.BASE_DIR / "results"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "embedding_model": self.EMBEDDING_MODEL,
            "sentiment_model": self.SENTIMENT_MODEL,
            "teaching_score_model": self.TEACHING_SCORE_MODEL,
            "fes_weights": {
                "emotional_engagement": self.FES_WEIGHT_ENGAGEMENT,
                "emotional_variance": self.FES_WEIGHT_VARIANCE,
                "likes_norm": self.FES_WEIGHT_LIKES,
                "comments_norm": self.FES_WEIGHT_COMMENTS,
            },
            "iqs_weights": {
                "semantic_alignment": self.IQS_WEIGHT_SEMANTIC,
                "depth": self.IQS_WEIGHT_DEPTH,
                "lexical_diversity": self.IQS_WEIGHT_LEXICAL,
                "teaching_score": self.IQS_WEIGHT_TEACHING,
            },
            "adaptive_k": self.ADAPTIVE_K,
            "random_seed": self.RANDOM_SEED,
            "bootstrap_rounds": self.BOOTSTRAP_ROUNDS,
            "internal_frozen_cohort_size": self.INTERNAL_FROZEN_COHORT_SIZE,
            "lak_benchmark_accessible_pairs": self.LAK_BENCHMARK_ACCESSIBLE_PAIRS,
            "lak_benchmark_topics": self.LAK_BENCHMARK_TOPICS,
        }
