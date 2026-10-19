# Explainable Educational Video Ranking Using Hybrid Semantic Intelligence and LLM-Assisted Engagement Analysis

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests Passing](https://img.shields.io/badge/pytest-18%20passed-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An audited, reproducible, and explainable ranking framework for educational video search. The system adaptively integrates query-aware audience engagement evidence (via sentiment and semantic comment filtering) with intrinsic educational quality signals (structural depth, lexical diversity, semantic alignment, and LLM pedagogical teaching evaluation), validated against the **LAK 2026 expert-annotated benchmark**.

---

## 1. Research Overview

Educational video platforms frequently prioritize raw popularity metrics (views, total likes), which correlates poorly with instructional quality and often promotes clickbait or introductory-level summaries over rigorous pedagogical content.

This project investigates three primary research questions:
1. **RQ1 (Complementary Fusion):** Does combining audience engagement signals (FES) with intrinsic pedagogical quality signals (IQS) improve relevance ranking over popularity baselines?
2. **RQ2 (Adaptive Weighting):** Does an evidence-driven adaptive weighting scheme ($\alpha_i = \min(1.0, \ln(1 + C_i^{\text{rel}}) / k)$) outperform fixed linear weighting when comment volume varies widely?
3. **RQ3 (Benchmark Competitiveness):** How does the proposed Hybrid framework perform relative to established information retrieval baselines (BM25, E5, DPR, RankNet) under independent expert-annotated ground truth?

---

## 2. System Architecture

```text
                               ┌────────────────────────────────┐
                               │  YouTube Search / LAK Query    │
                               └──────────────┬─────────────────┘
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
     ┌───────────────────────────────┐                 ┌───────────────────────────────┐
     │   Audience Engagement (FES)   │                 │    Intrinsic Quality (IQS)    │
     │  - E5 Query-Comment Filtering │                 │  - Title/Desc Semantic Align  │
     │  - CardiffNLP RoBERTa Sent.   │                 │  - Duration Depth Proxy       │
     │  - Emotional Var. Consistency │                 │  - Type-Token Ratio (TTR)     │
     │  - Normalized Like/Comm Count │                 │  - Gemini 3.5 Teaching Score  │
     └───────────────┬───────────────┘                 └───────────────┬───────────────┘
                     │                                                 │
                     │         ┌──────────────────────────────┐        │
                     └────────►│   Adaptive Hybrid Fusion     │◄───────┘
                               │  ES_i = ln(1 + C_rel_i)      │
                               │  alpha_i = min(1.0, ES_i / 5)│
                               │  Score = alpha*FES + (1-a)*IQS│
                               └──────────────┬───────────────┘
                                              ▼
                               ┌──────────────────────────────┐
                               │     Ranked Video Results     │
                               │   + Evidence Grounded Audit  │
                               └──────────────────────────────┘
```

---

## 3. Repository Structure

```text
Educational_Video_Ranking_Audited/
├── .env.example               # Template for YouTube & Gemini API credentials
├── README.md                  # Project guide and execution documentation
├── requirements.txt           # Verified Python package dependencies
├── PROJECT_FILE_INVENTORY.md  # Detailed catalog of all 400 project files
├── PROJECT_FILE_MANIFEST.csv  # Machine-readable inventory of all project files
├── NOTEBOOK_VERSION_MAP.md    # Complete lineage and version roles of all notebooks
├── DEPENDENCY_MAP.md          # Input/output dataflow and producer-consumer graph
├── REPRODUCIBILITY_REPORT.md  # Detailed benchmark metrics, tables, and validation
├── BUG_FIX_LOG.md             # Technical audit log and remediation details
├── CHANGELOG.md               # Version history and modification tracking
├── configs/
│   ├── .env.example           # Secure credentials template
│   └── config.yaml            # Model parameters, weights, and experimental seeds
├── data/
│   ├── raw/                   # Phase 9A raw YouTube metadata and comments (5 domains)
│   ├── processed/             # Phase 9B-9G processed features, sentiment, FES, IQS, cohort freeze
│   └── benchmark/             # LAK 2026 expert benchmark database & accessible cohort (888 pairs)
├── notebooks/
│   ├── NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb   # PRIMARY AUTHORITATIVE NOTEBOOK (Phase 9–13)
│   └── NLP_REVISION_v16_FINAL_COMPLETE.ipynb        # Supporting record for internal cohort
├── results/
│   ├── internal_cohort/       # Phase 9H ablation, sensitivity, Phase 12 runtime, cost, scalability
│   └── lak_benchmark/         # Phase 10-11 baselines, Phase 13 full hybrid evaluation & Wilcoxon tests
├── src/                       # Audited modular Python package
│   ├── __init__.py            # Library exports
│   ├── config.py              # Configuration dataclass and defaults
│   ├── preprocessing.py       # Text cleaning and TTR lexical diversity
│   ├── fes.py                 # Feature-based Engagement Score computation
│   ├── iqs.py                 # Intrinsic Quality Score computation
│   ├── hybrid_ranking.py      # Adaptive logarithmic alpha and score fusion
│   ├── evaluation.py          # Per-topic ranking metrics (NDCG, MAP, MRR, P@K, R@K)
│   └── significance.py        # Paired Wilcoxon signed-rank tests & bootstrap CIs
├── tests/                     # Automated pytest validation suite (18 tests passing)
│   ├── test_components.py     # Scoring formulas and weighting tests
│   ├── test_evaluation.py     # Ranking metrics tests against ground truth
│   ├── test_cohort_and_data_integrity.py  # 98-internal and 888-LAK cohort validation
│   └── test_significance.py   # Statistical test validity tests
└── archive/                   # Original untouched notebooks and raw zip extracts
```

---

## 4. Setup & Installation

### A. Environment Setup
```bash
# Clone or navigate to the repository
cd Educational_Video_Ranking_Audited

# Create and activate a clean virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install verified dependencies
pip install -r requirements.txt
```

### B. Configure API Credentials
Copy `.env.example` to `.env` and insert your credentials if you intend to re-crawl live YouTube data or run fresh Gemini LLM evaluations:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
YOUTUBE_API_KEY="your_api_key_here"
GEMINI_API_KEY="your_api_key_here"
```

---

## 5. Running the Pipeline

### A. Automated Test Suite
To verify that all scoring formulas, ranking metrics, and cohort definitions are functional:
```bash
pytest tests/ -v
```
*Expected Result:* 18 passed tests.

### B. Authoritative Notebook Execution
The primary experimental record is **`notebooks/NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb`**:
* **In Google Colab:** Open the notebook directly in Colab. Ensure hardware accelerator is set to GPU (T4 recommended). Cell 1 installs dependencies and auto-mounts Drive if available.
* **Locally / JupyterLab:**
  ```bash
  jupyter lab notebooks/NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb
  ```
* **Execution Sequence:**
  - `Phase 9A–9F`: Multi-domain feature extraction and cohort freeze (98 videos).
  - `Phase 9H–9K`: Internal cohort ablation and sensitivity analysis.
  - `Phase 12`: Runtime scalability, Gemini token costs, and grounding audit.
  - `Phase 13A–13F`: Full Hybrid reconstruction on LAK benchmark, ranking evaluation (888 pairs), baseline comparison (BM25, E5, DPR, RankNet), and paired Wilcoxon statistical significance testing.

---

## 6. Verified Experimental Findings

| Experiment Stage | Key Metric / Result | Statistical Finding / Interpretation |
|:---|:---|:---|
| **Ablation (LAK Benchmark)** | Full Hybrid: **NDCG@10 = 0.6031** | Dropping semantic relevance causes largest drop ($\Delta = -0.0856$). Adaptive weighting beats fixed 50/50 fusion ($0.6031$ vs $0.5907$). |
| **Hybrid vs DPR** | NDCG@10: $0.6031$ vs $0.5874$ | No statistically significant difference ($p = 0.9211$). |
| **Hybrid vs BM25** | NDCG@10: $0.6031$ vs $0.6109$ | No statistically significant difference ($p = 0.4512$). |
| **Hybrid vs RankNet** | NDCG@10: $0.6031$ vs $0.6059$ | No significant difference on NDCG ($p = 0.8464$); RankNet significantly better on P@5 ($p = 0.0421$). |
| **Hybrid vs E5 Dense** | NDCG@10: $0.6031$ vs $0.6583$ | E5 significantly outperforms Hybrid on NDCG@10 ($p = 0.0482$), MAP@10 ($p = 0.0462$), and P@5 ($p = 0.0339$). |

> **Research Integrity Note:** In alignment with scientific rigor, negative findings are openly reported. The proposed Hybrid system is competitive with established baselines but is not claimed to be universally superior.

---

## 7. Known Limitations
1. **Proxy-based Intrinsic Quality:** Video duration serves as a structural proxy for topic coverage depth, not a guarantee of pedagogical clarity.
2. **Binary Expert Relevance:** LAK 2026 expert annotations provide binary Accepted/Rejected judgments rather than continuous graded rankings.
3. **Automated Explanation Audit:** The explanation audit measures factual grounding and dominant-factor consistency, not subjective human learner comprehension.

---

---

## Data & Code Availability

This study uses the publicly available LAK 2026 educational-resource ranking benchmark associated with *“Embedding-Based Rankings of Educational Resources based on Learning Outcome Alignment: Benchmarking, Expert Validation, and Learner Performance”* (DOI: [10.1145/3785022.3785073](https://doi.org/10.1145/3785022.3785073)). The benchmark is available at [https://2ly.link/27QHn](https://2ly.link/27QHn). The present study uses an accessible reconstruction of the benchmark comprising **888 topic–video pairs across 54 topics**, with binary expert relevance judgments (located in [`data/benchmark/lak2026_benchmark_eval_accessible_888.csv`](data/benchmark/lak2026_benchmark_eval_accessible_888.csv)).

In addition, the study constructs a project-specific educational-video dataset using the YouTube Data API across five domains (`Programming`, `Data Science`, `Mathematics`, `Physics`, and `Biology`). The collected data include available video metadata and comments for educational topics (located in [`data/raw/youtube_5domains/`](data/raw/youtube_5domains/)). These data are processed to derive semantic relevance, sentiment, emotional engagement, and intrinsic quality features used by the proposed ranking framework (located in [`data/processed/`](data/processed/)). The collection reflects the data available at the time of retrieval; YouTube metadata and comments may change or become unavailable over time.

The project repository provides:
1. **Implementation:** Full modular implementation of the proposed framework in [`src/`](src/).
2. **Experimental Notebooks:** The primary experimental notebook [`notebooks/NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb`](notebooks/NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb) and supporting internal cohort record [`notebooks/NLP_REVISION_v16_FINAL_COMPLETE.ipynb`](notebooks/NLP_REVISION_v16_FINAL_COMPLETE.ipynb).
3. **Configuration Templates:** [`.env.example`](.env.example) and [`configs/config.yaml`](configs/config.yaml).
4. **Processed Data & Experimental Artifacts:** Evaluation results, ablation studies, and statistical significance analyses in [`results/`](results/).

Reproducing live data collection and LLM-assisted teaching-score generation may require valid API credentials and access to the relevant external services. The LAK benchmark and the project-collected YouTube data serve distinct roles in the study: the former provides expert relevance judgments for benchmark evaluation, while the latter supports experiments on the project-specific educational-video cohort.

* **Code Availability:** [https://github.com/NAYANESHREDDY/Semantic-Emotional-Hybrid-Video-Ranking-System-New](https://github.com/NAYANESHREDDY/Semantic-Emotional-Hybrid-Video-Ranking-System-New)

## 8. Provenance & Authorship
* **Author:** Chennareddy Nayanesh Reddy
* **Project:** Explainable Educational Video Ranking
* **Audit & Remediation:** Conducted with Google Antigravity (October 2026).
