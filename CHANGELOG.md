# Changelog — Project-Wide Audit and Cleanup

All notable changes made during the engineering and reproducibility audit of the **Explainable Educational Video Ranking** research project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.0.0] - 2026-10-19

### Fixed
- **Phase 12D-B Cohort Size Bug in Notebook v17:**
  - *Location:* `notebooks/NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb` (Cell 75).
  - *Issue:* Legacy assertion `if frozen_n < 99: raise ValueError(...)` crashed when executed on the authoritative 98-video cohort.
  - *Fix:* Replaced hardcoded assertion with `EXPECTED_INTERNAL_COHORT_SIZE = 98`, matching `phase9_cohort_manifest.json` and manuscript Tables 1 and 20. Updated `cohort_sizes` to evaluate `[20, 40, 60, 80, frozen_n]`.
  - *Mathematical Behavior:* Unchanged. The ranking sort and timing calculations remain mathematically identical.
  - *Validation:* Executed deterministic scalability sorting benchmark; generated `phase12_empirical_scalability.csv` and `phase12_scalability_summary.csv`. Cell 76 completeness check passed 16/16.
- **Typing Import Error in `src/hybrid_ranking.py`:**
  - *Issue:* `Optional[str]` was referenced without import.
  - *Fix:* Added `from typing import Union, Optional`.
  - *Validation:* All 18 automated unit and regression tests in `tests/` passed.
- **Windows CP-1252 Shell Encoding:**
  - *Issue:* Console scripts crashed when logging Unicode characters (`\u2192`, checkmarks).
  - *Fix:* Added `sys.stdout.reconfigure(encoding='utf-8')` across all scripts.

### Added
- **Audited Modular Python Package (`src/`):**
  - `src/__init__.py`: Package entry point.
  - `src/config.py`: Centralized configuration, weights, hyperparameter defaults, and environment paths.
  - `src/preprocessing.py`: Text cleaning and Type-Token Ratio (TTR) lexical diversity.
  - `src/fes.py`: Feature-based Engagement Score fusion.
  - `src/iqs.py`: Intrinsic Quality Score fusion with duration depth proxy.
  - `src/hybrid_ranking.py`: Adaptive logarithmic alpha weighting and hybrid fusion.
  - `src/evaluation.py`: Per-topic ranking evaluation for NDCG@5, NDCG@10, MAP@10, MRR, P@5, P@10, R@5, R@10.
  - `src/significance.py`: Paired Wilcoxon signed-rank tests and 5,000-round bootstrap confidence intervals.
- **Automated Test Suite (`tests/`):**
  - `tests/test_components.py`: Unit tests for scoring formulas and adaptive weighting.
  - `tests/test_evaluation.py`: Hand-calculated ground-truth verification of ranking metrics.
  - `tests/test_cohort_and_data_integrity.py`: Regression verification of 98-video internal cohort and 888-pair accessible LAK cohort.
  - `tests/test_significance.py`: Statistical test validity verification.
- **Structured Project Organization:**
  - `data/raw/`: Raw YouTube metadata and comments across 5 domains.
  - `data/processed/`: Processed features, sentiment scores, FES, IQS, and cohort manifests.
  - `data/benchmark/`: LAK 2026 expert relevance judgments and YouTube accessible feature sets.
  - `results/internal_cohort/`: Ablation, sensitivity, runtime, cost, and scalability results.
  - `results/lak_benchmark/`: Full hybrid evaluation metrics, baseline comparisons, Wilcoxon tests, and bootstrap CIs.
  - `configs/`: Pipeline configuration (`config.yaml`) and template `.env.example`.
  - `archive/`: Untouched original notebooks and raw zip archives.
- **Complete Project Documentation:**
  - `PROJECT_FILE_INVENTORY.md`
  - `PROJECT_FILE_MANIFEST.csv`
  - `NOTEBOOK_VERSION_MAP.md`
  - `DEPENDENCY_MAP.md`
  - `REPRODUCIBILITY_REPORT.md`
  - `BUG_FIX_LOG.md`
  - `README.md`
  - `requirements.txt`

### Preserved
- All raw datasets, expert annotations, and model predictions were preserved without modification.
- All original experimental outputs and baseline rankings (including negative findings where E5 or RankNet outperform Hybrid) were strictly preserved.
