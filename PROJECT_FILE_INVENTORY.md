# Project File Inventory — Complete Audit & Manifest

**Project Title:** Explainable Educational Video Ranking Using Hybrid Semantic Intelligence and LLM-Assisted Engagement Analysis  
**Principal Investigator:** Chennareddy Nayanesh Reddy  
**Audit Status:** Audited, Cleaned, Modularized, and Validated  

---

## 1. Directory Structure Overview

```text
Educational_Video_Ranking_Audited/
├── configs/               # Environment (.env.example) and pipeline configurations (config.yaml)
├── data/
│   ├── raw/               # Phase 9A raw YouTube metadata and comments across 5 domains
│   ├── processed/         # Phase 9B-9G processed features, sentiment, FES, IQS, cohort freeze
│   └── benchmark/         # LAK 2026 expert relevance benchmark database and accessible pairs
├── notebooks/             # Authoritative notebooks (v17 for full LAK evaluation, v16 for internal)
├── reports/               # Final reports, Reviewer response letters, and compliance documentation
├── results/
│   ├── internal_cohort/   # Phase 9H ablation, sensitivity, Phase 12 runtime, cost, scalability
│   └── lak_benchmark/     # Phase 10, 11, and Phase 13 full hybrid evaluation results and significance
├── src/                   # Audited modular Python package implementing all pipeline components
├── tests/                 # Automated pytest test suite (18 unit, regression, and integrity tests)
└── archive/               # Historical raw zip outputs and untouched original notebooks
```

---

## 2. File Inventory by Category

### Authoritative Results (24 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `lak2026_benchmark_eval_accessible.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/lak2026_benchmark_eval_accessible.csv` | 12.50 MB | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `lak_teaching_scores.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/lak_teaching_scores.csv` | 50,521 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `lak_unavailable_video_ids.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/lak_unavailable_video_ids.csv` | 309 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `lak_youtube_comments.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/lak_youtube_comments.csv` | 4.81 MB | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `lak_youtube_metadata.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/lak_youtube_metadata.csv` | 1.17 MB | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `phase13_lak_bm25_commoncohort_topic_metrics.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/phase13_lak_bm25_commoncohort_topic_metrics.csv` | 4,881 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `phase13_lak_dpr_commoncohort_topic_metrics.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/phase13_lak_dpr_commoncohort_topic_metrics.csv` | 4,963 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `phase13_lak_e5_commoncohort_topic_metrics.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/phase13_lak_e5_commoncohort_topic_metrics.csv` | 4,918 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `phase13_lak_hybrid_bootstrap_ci.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/phase13_lak_hybrid_bootstrap_ci.csv` | 4,210 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `phase13_lak_hybrid_commoncohort_topic_metrics.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/phase13_lak_hybrid_commoncohort_topic_metrics.csv` | 5,045 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `phase13_lak_hybrid_completeness_check.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/phase13_lak_hybrid_completeness_check.csv` | 1,102 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `phase13_lak_hybrid_components.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/phase13_lak_hybrid_components.csv` | 15.17 MB | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `phase13_lak_hybrid_component_ablation.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/phase13_lak_hybrid_component_ablation.csv` | 1,000 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `phase13_lak_hybrid_component_ablation_comparison.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/phase13_lak_hybrid_component_ablation_comparison.csv` | 2,522 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| `phase13_lak_hybrid_component_ablation_topic_metrics.csv` | `results/lak_benchmark/phase13_full_hybrid_evaluation/phase13_lak_hybrid_component_ablation_topic_metrics.csv` | 30,141 B | Phase 13 | Full Hybrid LAK evaluation, ablation, baseline comparison, Wilcoxon significance, bootstrap CI | Preserve and reference in evaluations |
| *... and 9 more files* | *See PROJECT_FILE_MANIFEST.csv* | | | | |

### Automated Unit Tests (11 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `paired_significance_tests.csv` | `archive/journal_revision_raw/revision_phase9h/paired_significance_tests.csv` | 227 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Preserve in archive untouched |
| `conftest.py` | `tests/conftest.py` | 238 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Maintain and execute |
| `test_cohort_and_data_integrity.py` | `tests/test_cohort_and_data_integrity.py` | 2,257 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Maintain and execute |
| `test_components.py` | `tests/test_components.py` | 2,661 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Maintain and execute |
| `test_evaluation.py` | `tests/test_evaluation.py` | 1,969 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Maintain and execute |
| `test_significance.py` | `tests/test_significance.py` | 1,127 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Maintain and execute |
| `conftest.cpython-311-pytest-9.1.1.pyc` | `tests/__pycache__/conftest.cpython-311-pytest-9.1.1.pyc` | 835 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Maintain and execute |
| `test_cohort_and_data_integrity.cpython-311-pytest-9.1.1.pyc` | `tests/__pycache__/test_cohort_and_data_integrity.cpython-311-pytest-9.1.1.pyc` | 16,862 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Maintain and execute |
| `test_components.cpython-311-pytest-9.1.1.pyc` | `tests/__pycache__/test_components.cpython-311-pytest-9.1.1.pyc` | 17,327 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Maintain and execute |
| `test_evaluation.cpython-311-pytest-9.1.1.pyc` | `tests/__pycache__/test_evaluation.cpython-311-pytest-9.1.1.pyc` | 16,867 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Maintain and execute |
| `test_significance.cpython-311-pytest-9.1.1.pyc` | `tests/__pycache__/test_significance.cpython-311-pytest-9.1.1.pyc` | 7,105 B | General | Pytest validation suite for scoring formulas, metrics, and cohort integrity | Maintain and execute |

### Benchmark Data (27 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `lak2026_benchmark_eval_accessible_888.csv` | `data/benchmark/lak2026_benchmark_eval_accessible_888.csv` | 12.50 MB | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `lak2026_benchmark_eval_all914.csv` | `data/benchmark/lak2026_benchmark_eval_all914.csv` | 12.72 MB | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `lak_teaching_scores.csv` | `data/benchmark/lak_teaching_scores.csv` | 50,521 B | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `lak_unavailable_video_ids_25.csv` | `data/benchmark/lak_unavailable_video_ids_25.csv` | 309 B | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `lak_youtube_comments.csv` | `data/benchmark/lak_youtube_comments.csv` | 4.81 MB | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `lak_youtube_metadata_841.csv` | `data/benchmark/lak_youtube_metadata_841.csv` | 1.17 MB | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `README.md` | `data/benchmark/README.md` | 2,248 B | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `benchmark_download` | `data/benchmark/lak2026_sqlite/benchmark_download` | 71,524 B | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `db.sqlite3` | `data/benchmark/lak2026_sqlite/db.sqlite3` | 356.48 MB | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `cli.py` | `data/benchmark/lak2026_sqlite/lak2026_repo/cli.py` | 2,416 B | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `const.py` | `data/benchmark/lak2026_sqlite/lak2026_repo/const.py` | 3,259 B | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `db_ops.py` | `data/benchmark/lak2026_sqlite/lak2026_repo/db_ops.py` | 5,559 B | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `embeddings_ops.py` | `data/benchmark/lak2026_sqlite/lak2026_repo/embeddings_ops.py` | 8,992 B | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `llm_ops.py` | `data/benchmark/lak2026_sqlite/lak2026_repo/llm_ops.py` | 4,838 B | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| `metric_ops.py` | `data/benchmark/lak2026_sqlite/lak2026_repo/metric_ops.py` | 3,567 B | LAK Benchmark | LAK 2026 expert relevance judgments and YouTube accessible feature sets | Preserve and reference in evaluations |
| *... and 12 more files* | *See PROJECT_FILE_MANIFEST.csv* | | | | |

### Derived Data (9 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `phase9d_fes_full.csv` | `data/processed/phase9d/phase9d_fes_full.csv` | 216,170 B | Phase 9D | Feature-based Engagement Score (FES) tables | Preserve and reference in evaluations |
| `phase9d_fes_top10.csv` | `data/processed/phase9d/phase9d_fes_top10.csv` | 30,900 B | Phase 9D | Feature-based Engagement Score (FES) tables | Preserve and reference in evaluations |
| `phase9e_iqs_components.csv` | `data/processed/phase9e/phase9e_iqs_components.csv` | 431,718 B | Phase 9E | Intrinsic Quality Score (IQS) components and Teaching Scores | Preserve and reference in evaluations |
| `phase9e_iqs_domain_summary.csv` | `data/processed/phase9e/phase9e_iqs_domain_summary.csv` | 916 B | Phase 9E | Intrinsic Quality Score (IQS) components and Teaching Scores | Preserve and reference in evaluations |
| `phase9e_iqs_full.csv` | `data/processed/phase9e/phase9e_iqs_full.csv` | 446,675 B | Phase 9E | Intrinsic Quality Score (IQS) components and Teaching Scores | Preserve and reference in evaluations |
| `phase9e_iqs_top10.csv` | `data/processed/phase9e/phase9e_iqs_top10.csv` | 70,106 B | Phase 9E | Intrinsic Quality Score (IQS) components and Teaching Scores | Preserve and reference in evaluations |
| `phase9e_teaching_score_input.csv` | `data/processed/phase9e/phase9e_teaching_score_input.csv` | 209,909 B | Phase 9E | Intrinsic Quality Score (IQS) components and Teaching Scores | Preserve and reference in evaluations |
| `raw_llm_responses.jsonl` | `data/processed/phase9e/teaching_score_results/raw_llm_responses.jsonl` | 22,485 B | Phase 9E | Intrinsic Quality Score (IQS) components and Teaching Scores | Preserve and reference in evaluations |
| `teaching_scores.csv` | `data/processed/phase9e/teaching_score_results/teaching_scores.csv` | 14,201 B | Phase 9E | Intrinsic Quality Score (IQS) components and Teaching Scores | Preserve and reference in evaluations |

### Evaluation Data (4 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `phase9g_annotation_codebook.csv` | `data/processed/phase9g/phase9g_annotation_codebook.csv` | 291 B | Phase 9G | Human annotation codebook and annotator scoring sheets | Preserve and reference in evaluations |
| `phase9g_annotator1.csv` | `data/processed/phase9g/phase9g_annotator1.csv` | 204,808 B | Phase 9G | Human annotation codebook and annotator scoring sheets | Preserve and reference in evaluations |
| `phase9g_annotator2.csv` | `data/processed/phase9g/phase9g_annotator2.csv` | 204,808 B | Phase 9G | Human annotation codebook and annotator scoring sheets | Preserve and reference in evaluations |
| `phase9g_human_annotation_sheet.csv` | `data/processed/phase9g/phase9g_human_annotation_sheet.csv` | 204,808 B | Phase 9G | Human annotation codebook and annotator scoring sheets | Preserve and reference in evaluations |

### Frozen Artifact (6 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `phase9f_alpha_summary.csv` | `data/processed/phase9f/phase9f_alpha_summary.csv` | 150 B | Phase 9F | Authoritative 98-video cohort manifest and Adaptive Hybrid rankings | Preserve and reference in evaluations |
| `phase9f_domain_summary.csv` | `data/processed/phase9f/phase9f_domain_summary.csv` | 1,015 B | Phase 9F | Authoritative 98-video cohort manifest and Adaptive Hybrid rankings | Preserve and reference in evaluations |
| `phase9f_hybrid_full.csv` | `data/processed/phase9f/phase9f_hybrid_full.csv` | 28,273 B | Phase 9F | Authoritative 98-video cohort manifest and Adaptive Hybrid rankings | Preserve and reference in evaluations |
| `phase9f_hybrid_top10.csv` | `data/processed/phase9f/phase9f_hybrid_top10.csv` | 3,113 B | Phase 9F | Authoritative 98-video cohort manifest and Adaptive Hybrid rankings | Preserve and reference in evaluations |
| `phase9f_hybrid_top20.csv` | `data/processed/phase9f/phase9f_hybrid_top20.csv` | 6,104 B | Phase 9F | Authoritative 98-video cohort manifest and Adaptive Hybrid rankings | Preserve and reference in evaluations |
| `phase9_cohort_manifest.json` | `data/processed/phase9f/phase9_cohort_manifest.json` | 336 B | Phase 9F | Authoritative 98-video cohort manifest and Adaptive Hybrid rankings | Preserve and reference in evaluations |

### Historical Archive (143 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `scan_summary.json` | `archive/scan_summary.json` | 105,576 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `OUTPUT_FILE_INVENTORY.txt` | `archive/journal_revision_raw/OUTPUT_FILE_INVENTORY.txt` | 11,069 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `benchmark_download` | `archive/journal_revision_raw/lak2026_benchmark/benchmark_download` | 71,524 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `db.sqlite3` | `archive/journal_revision_raw/lak2026_benchmark/db.sqlite3` | 356.48 MB | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `cli.py` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/cli.py` | 2,416 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `const.py` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/const.py` | 3,259 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `db_ops.py` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/db_ops.py` | 5,559 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `embeddings_ops.py` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/embeddings_ops.py` | 8,992 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `llm_ops.py` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/llm_ops.py` | 4,838 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `metric_ops.py` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/metric_ops.py` | 3,567 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `paper_result.ipynb` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/paper_result.ipynb` | 9,472 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `pyproject.toml` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/pyproject.toml` | 710 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `README.md` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/README.md` | 2,802 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `uv.lock` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/uv.lock` | 398,745 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| `.gitignore` | `archive/journal_revision_raw/lak2026_benchmark/lak2026_repo/.idea/.gitignore` | 228 B | General | Original untouched notebooks and raw zip extracts preserved for research provenance | Preserve in archive untouched |
| *... and 128 more files* | *See PROJECT_FILE_MANIFEST.csv* | | | | |

### Intermediate Data (23 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `semantic_relevance_summary.csv` | `data/processed/phase9b/semantic_relevance_summary.csv` | 1,559 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `comments_cleaned.csv` | `data/processed/phase9b/human_anatomy/comments_cleaned.csv` | 463,748 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `comments_relevant.csv` | `data/processed/phase9b/human_anatomy/comments_relevant.csv` | 430,201 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `comments_cleaned.csv` | `data/processed/phase9b/linear_algebra/comments_cleaned.csv` | 582,286 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `comments_relevant.csv` | `data/processed/phase9b/linear_algebra/comments_relevant.csv` | 533,693 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `comments_cleaned.csv` | `data/processed/phase9b/machine_learning/comments_cleaned.csv` | 458,495 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `comments_relevant.csv` | `data/processed/phase9b/machine_learning/comments_relevant.csv` | 453,420 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `comments_cleaned.csv` | `data/processed/phase9b/python/comments_cleaned.csv` | 576,580 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `comments_relevant.csv` | `data/processed/phase9b/python/comments_relevant.csv` | 500,048 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `comments_cleaned.csv` | `data/processed/phase9b/quantum_mechanics/comments_cleaned.csv` | 668,975 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `comments_relevant.csv` | `data/processed/phase9b/quantum_mechanics/comments_relevant.csv` | 598,424 B | Phase 9B | Cleaned comments and E5 semantic relevance scores | Preserve and reference in evaluations |
| `all_domains_video_emotional_engagement.csv` | `data/processed/phase9c/all_domains_video_emotional_engagement.csv` | 8,611 B | Phase 9C | RoBERTa sentiment scores and emotional engagement metrics | Preserve and reference in evaluations |
| `sentiment_emotional_engagement_summary.csv` | `data/processed/phase9c/sentiment_emotional_engagement_summary.csv` | 1,831 B | Phase 9C | RoBERTa sentiment scores and emotional engagement metrics | Preserve and reference in evaluations |
| `relevant_comments_sentiment.csv` | `data/processed/phase9c/human_anatomy/relevant_comments_sentiment.csv` | 537,570 B | Phase 9C | RoBERTa sentiment scores and emotional engagement metrics | Preserve and reference in evaluations |
| `video_emotional_engagement.csv` | `data/processed/phase9c/human_anatomy/video_emotional_engagement.csv` | 1,739 B | Phase 9C | RoBERTa sentiment scores and emotional engagement metrics | Preserve and reference in evaluations |
| *... and 8 more files* | *See PROJECT_FILE_MANIFEST.csv* | | | | |

### Modular Python Library (16 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `config.py` | `src/config.py` | 3,400 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `evaluation.py` | `src/evaluation.py` | 4,956 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `fes.py` | `src/fes.py` | 1,499 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `hybrid_ranking.py` | `src/hybrid_ranking.py` | 2,555 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `iqs.py` | `src/iqs.py` | 1,681 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `preprocessing.py` | `src/preprocessing.py` | 1,252 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `significance.py` | `src/significance.py` | 2,785 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `__init__.py` | `src/__init__.py` | 960 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `config.cpython-311.pyc` | `src/__pycache__/config.cpython-311.pyc` | 4,602 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `evaluation.cpython-311.pyc` | `src/__pycache__/evaluation.cpython-311.pyc` | 8,474 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `fes.cpython-311.pyc` | `src/__pycache__/fes.cpython-311.pyc` | 2,035 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `hybrid_ranking.cpython-311.pyc` | `src/__pycache__/hybrid_ranking.cpython-311.pyc` | 4,261 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `iqs.cpython-311.pyc` | `src/__pycache__/iqs.cpython-311.pyc` | 2,274 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `preprocessing.cpython-311.pyc` | `src/__pycache__/preprocessing.cpython-311.pyc` | 2,166 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| `significance.cpython-311.pyc` | `src/__pycache__/significance.cpython-311.pyc` | 4,352 B | General | Audited, clean, reusable implementation of scoring, retrieval, and evaluation | Maintain and execute |
| *... and 1 more files* | *See PROJECT_FILE_MANIFEST.csv* | | | | |

### Notebook (13 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `NLP_PUBLIC.ipynb` | `archive/original_notebooks/NLP_PUBLIC.ipynb` | 668,550 B | General |  | Preserve in archive untouched |
| `NLP_PUBLIC_JOURNAL_REVISION.ipynb` | `archive/original_notebooks/NLP_PUBLIC_JOURNAL_REVISION.ipynb` | 1.09 MB | General |  | Preserve in archive untouched |
| `NLP_PUBLIC_JOURNAL_REVISION_v10_COHORT_FROZEN.ipynb` | `archive/original_notebooks/NLP_PUBLIC_JOURNAL_REVISION_v10_COHORT_FROZEN.ipynb` | 1.36 MB | General |  | Preserve in archive untouched |
| `NLP_PUBLIC_JOURNAL_REVISION_v10_EXTENDED_FIXED_main.ipynb` | `archive/original_notebooks/NLP_PUBLIC_JOURNAL_REVISION_v10_EXTENDED_FIXED_main.ipynb` | 1.51 MB | General |  | Preserve in archive untouched |
| `NLP_PUBLIC_JOURNAL_REVISION_v4_DYNAMIC_COHORT.ipynb` | `archive/original_notebooks/NLP_PUBLIC_JOURNAL_REVISION_v4_DYNAMIC_COHORT.ipynb` | 1.48 MB | General |  | Preserve in archive untouched |
| `NLP_PUBLIC_JOURNAL_REVISION_v6_RESTART_SAFE_PHASE11.ipynb` | `archive/original_notebooks/NLP_PUBLIC_JOURNAL_REVISION_v6_RESTART_SAFE_PHASE11.ipynb` | 1.35 MB | General |  | Preserve in archive untouched |
| `NLP_REVISION_v12_FIXED.ipynb` | `archive/original_notebooks/NLP_REVISION_v12_FIXED.ipynb` | 1.74 MB | General |  | Preserve in archive untouched |
| `NLP_REVISION_v13_FINAL_CHECKED.ipynb` | `archive/original_notebooks/NLP_REVISION_v13_FINAL_CHECKED.ipynb` | 1.74 MB | General |  | Preserve in archive untouched |
| `NLP_REVISION_v15_FINAL_COMPLETE.ipynb` | `archive/original_notebooks/NLP_REVISION_v15_FINAL_COMPLETE.ipynb` | 1.76 MB | General |  | Preserve in archive untouched |
| `NLP_REVISION_v16_FINAL_COMPLETE.ipynb` | `archive/original_notebooks/NLP_REVISION_v16_FINAL_COMPLETE.ipynb` | 1.76 MB | Historical Record (Phase 9-12) | Supporting experimental record for internal cohort validation | Preserve in archive untouched |
| `NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb` | `archive/original_notebooks/NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb` | 1.52 MB | Authoritative Pipeline (Phase 9-13) | Primary reproducible research notebook executing complete LAK Hybrid evaluation | Preserve in archive untouched |
| `NLP_REVISION_v16_FINAL_COMPLETE.ipynb` | `notebooks/NLP_REVISION_v16_FINAL_COMPLETE.ipynb` | 1.76 MB | Historical Record (Phase 9-12) | Supporting experimental record for internal cohort validation | Maintain as primary reproducible artifact |
| `NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb` | `notebooks/NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb` | 1.94 MB | Authoritative Pipeline (Phase 9-13) | Primary reproducible research notebook executing complete LAK Hybrid evaluation | Maintain as primary reproducible artifact |

### Raw Data (11 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `query_summary.csv` | `data/raw/youtube_5domains/query_summary.csv` | 988 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |
| `comments.csv` | `data/raw/youtube_5domains/human_anatomy/comments.csv` | 308,316 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |
| `videos.csv` | `data/raw/youtube_5domains/human_anatomy/videos.csv` | 27,517 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |
| `comments.csv` | `data/raw/youtube_5domains/linear_algebra/comments.csv` | 371,642 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |
| `videos.csv` | `data/raw/youtube_5domains/linear_algebra/videos.csv` | 39,601 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |
| `comments.csv` | `data/raw/youtube_5domains/machine_learning/comments.csv` | 304,279 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |
| `videos.csv` | `data/raw/youtube_5domains/machine_learning/videos.csv` | 63,203 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |
| `comments.csv` | `data/raw/youtube_5domains/python/comments.csv` | 378,277 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |
| `videos.csv` | `data/raw/youtube_5domains/python/videos.csv` | 62,453 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |
| `comments.csv` | `data/raw/youtube_5domains/quantum_mechanics/comments.csv` | 419,247 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |
| `videos.csv` | `data/raw/youtube_5domains/quantum_mechanics/videos.csv` | 29,929 B | Phase 9A | Raw YouTube metadata and comment records across 5 domains | Preserve and reference in evaluations |

### Results (45 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `ablation_rankings_full.csv` | `results/internal_cohort/ablation_and_sensitivity/ablation_rankings_full.csv` | 41,082 B | Phase 9H | Internal 98-video component ablation and weight sensitivity analysis | Preserve and reference in evaluations |
| `paired_significance_tests.csv` | `results/internal_cohort/ablation_and_sensitivity/paired_significance_tests.csv` | 227 B | Phase 9H | Internal 98-video component ablation and weight sensitivity analysis | Maintain and execute |
| `true_ablation_results.csv` | `results/internal_cohort/ablation_and_sensitivity/true_ablation_results.csv` | 538 B | Phase 9H | Internal 98-video component ablation and weight sensitivity analysis | Preserve and reference in evaluations |
| `weight_sensitivity.csv` | `results/internal_cohort/ablation_and_sensitivity/weight_sensitivity.csv` | 1,343 B | Phase 9H | Internal 98-video component ablation and weight sensitivity analysis | Preserve and reference in evaluations |
| `dpr_topic_metrics.csv` | `results/internal_cohort/extended_audit_and_cost/dpr_topic_metrics.csv` | 5,148 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| `phase12_complexity_summary.csv` | `results/internal_cohort/extended_audit_and_cost/phase12_complexity_summary.csv` | 435 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| `phase12_component_ablation.csv` | `results/internal_cohort/extended_audit_and_cost/phase12_component_ablation.csv` | 604 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| `phase12_component_ablation_rankings.csv` | `results/internal_cohort/extended_audit_and_cost/phase12_component_ablation_rankings.csv` | 33,557 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| `phase12_dataset_statistics_by_domain.csv` | `results/internal_cohort/extended_audit_and_cost/phase12_dataset_statistics_by_domain.csv` | 676 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| `phase12_dataset_statistics_overall.csv` | `results/internal_cohort/extended_audit_and_cost/phase12_dataset_statistics_overall.csv` | 251 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| `phase12_dpr_predictions.csv` | `results/internal_cohort/extended_audit_and_cost/phase12_dpr_predictions.csv` | 69,663 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| `phase12_empirical_scalability.csv` | `results/internal_cohort/extended_audit_and_cost/phase12_empirical_scalability.csv` | 820 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| `phase12_error_analysis_examples.csv` | `results/internal_cohort/extended_audit_and_cost/phase12_error_analysis_examples.csv` | 5,590 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| `phase12_error_analysis_full.csv` | `results/internal_cohort/extended_audit_and_cost/phase12_error_analysis_full.csv` | 37,523 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| `phase12_error_analysis_representative_cases.csv` | `results/internal_cohort/extended_audit_and_cost/phase12_error_analysis_representative_cases.csv` | 9,630 B | Phase 12 | Grounding audit, token monetary costs, runtime, and scalability analysis | Preserve and reference in evaluations |
| *... and 30 more files* | *See PROJECT_FILE_MANIFEST.csv* | | | | |

### Source (291 files)

| Filename | Relative Path | Size | Phase | Purpose | Recommended Action |
|:---|:---|:---|:---|:---|:---|
| `.env.example` | `.env.example` | 877 B | General |  | Maintain |
| `.gitignore` | `.gitignore` | 803 B | General |  | Maintain |
| `BUG_FIX_LOG.md` | `BUG_FIX_LOG.md` | 5,011 B | General |  | Maintain |
| `CHANGELOG.md` | `CHANGELOG.md` | 4,009 B | General |  | Maintain |
| `DEPENDENCY_MAP.md` | `DEPENDENCY_MAP.md` | 7,211 B | General |  | Maintain |
| `LICENSE` | `LICENSE` | 1,732 B | General |  | Maintain |
| `NOTEBOOK_VERSION_MAP.md` | `NOTEBOOK_VERSION_MAP.md` | 6,845 B | General |  | Maintain |
| `PROJECT_FILE_INVENTORY.md` | `PROJECT_FILE_INVENTORY.md` | 37,698 B | General |  | Maintain |
| `PROJECT_FILE_MANIFEST.csv` | `PROJECT_FILE_MANIFEST.csv` | 105,350 B | General |  | Maintain |
| `README.md` | `README.md` | 11,202 B | General |  | Maintain |
| `REPRODUCIBILITY_REPORT.md` | `REPRODUCIBILITY_REPORT.md` | 6,602 B | General |  | Maintain |
| `requirements.txt` | `requirements.txt` | 568 B | General |  | Maintain |
| `COMMIT_EDITMSG` | `.git/COMMIT_EDITMSG` | 70 B | General |  | Maintain |
| `config` | `.git/config` | 346 B | General |  | Maintain |
| `description` | `.git/description` | 73 B | General |  | Maintain |
| *... and 276 more files* | *See PROJECT_FILE_MANIFEST.csv* | | | | |
