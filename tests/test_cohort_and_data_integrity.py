"""
Regression and data integrity tests for internal frozen cohort (98 videos)
and external LAK benchmark evaluation cohort (888 pairs, 54 topics, 841 unique videos).
"""

from pathlib import Path
import pandas as pd
import json
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent


def test_internal_cohort_count_and_domains():
    hybrid_path = BASE_DIR / "data" / "processed" / "phase9f" / "phase9f_hybrid_full.csv"
    assert hybrid_path.exists(), f"Missing {hybrid_path}"
    
    df = pd.read_csv(hybrid_path)
    assert len(df) == 98, f"Expected 98 internal cohort videos, found {len(df)}"
    assert df["video_id"].nunique() == 98, "Duplicate video IDs in internal cohort"
    
    counts = df["domain"].value_counts().to_dict()
    assert counts.get("Biology") == 20
    assert counts.get("Mathematics") == 20
    assert counts.get("Programming") == 20
    assert counts.get("Physics") == 19
    assert counts.get("Data Science") == 19


def test_internal_manifest_matches_data():
    manifest_path = BASE_DIR / "data" / "processed" / "phase9f" / "phase9_cohort_manifest.json"
    assert manifest_path.exists(), f"Missing {manifest_path}"
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    assert manifest["cohort_size"] == 98
    assert manifest["domain_counts"]["Physics"] == 19
    assert manifest["domain_counts"]["Data Science"] == 19


def test_lak_benchmark_accessible_cohort():
    lak_acc_path = BASE_DIR / "data" / "benchmark" / "lak2026_benchmark_eval_accessible_888.csv"
    assert lak_acc_path.exists(), f"Missing {lak_acc_path}"
    
    df = pd.read_csv(lak_acc_path)
    assert len(df) == 888, f"Expected 888 accessible pairs, found {len(df)}"
    assert df["topic_id"].nunique() == 54, f"Expected 54 topics, found {df['topic_id'].nunique()}"
    assert df["video_id"].nunique() == 841, f"Expected 841 unique videos, found {df['video_id'].nunique()}"


def test_lak_unavailable_videos_count():
    unavail_path = BASE_DIR / "data" / "benchmark" / "lak_unavailable_video_ids_25.csv"
    assert unavail_path.exists(), f"Missing {unavail_path}"
    
    df = pd.read_csv(unavail_path)
    assert len(df) == 25, f"Expected 25 unavailable video IDs, found {len(df)}"
