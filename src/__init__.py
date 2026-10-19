"""
Explainable Educational Video Ranking Framework
Package Initialization
"""

__version__ = "2.0.0"
__author__ = "Chennareddy Nayanesh Reddy"
__title__ = "Explainable Educational Video Ranking Using Hybrid Semantic Intelligence and LLM-Assisted Engagement Analysis"

from .config import PipelineConfig
from .preprocessing import compute_ttr, clean_text
from .fes import compute_fes
from .iqs import compute_iqs
from .hybrid_ranking import compute_adaptive_alpha, compute_hybrid_score
from .evaluation import compute_ranking_metrics_for_topic, evaluate_ranking_dataframe
from .significance import paired_wilcoxon_test, bootstrap_confidence_interval

__all__ = [
    "PipelineConfig",
    "compute_ttr",
    "clean_text",
    "compute_fes",
    "compute_iqs",
    "compute_adaptive_alpha",
    "compute_hybrid_score",
    "compute_ranking_metrics_for_topic",
    "evaluate_ranking_dataframe",
    "paired_wilcoxon_test",
    "bootstrap_confidence_interval",
]
