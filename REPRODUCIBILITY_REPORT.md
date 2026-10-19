# Research Reproducibility & Verification Report

**Project Title:** Explainable Educational Video Ranking Using Hybrid Semantic Intelligence and LLM-Assisted Engagement Analysis  
**Author:** Chennareddy Nayanesh Reddy  
**Date of Audit:** October 2026  

---

## 1. Executive Summary

This report establishes the technical reproducibility, statistical validity, and data integrity of the Educational Video Ranking research project. The audit confirmed:
1. **Mathematical Consistency:** All scoring formulas (FES, IQS, Adaptive Alpha, Hybrid fusion) are implemented exactly according to their formal definitions and reproduced in both notebook and modular Python implementations.
2. **Cohort Integrity:** The internal cohort consists of exactly **98 unique videos** across 5 educational domains, and the external LAK 2026 benchmark evaluation consists of exactly **888 accessible topic-video pairs** across **54 topics** and **841 unique videos**.
3. **Metric & Baseline Verification:** The evaluation results against BM25, E5, DPR, and RankNet, as well as the 5-method component ablation and paired Wilcoxon significance tests, match the reported manuscript tables to 6 decimal places.

---

## 2. Environment & Dependency Specifications

The project was audited and validated under both the recorded reference environment and a modern Python environment:

| Component | Reference Colab Environment | Local Audit Environment | Status |
|:---|:---|:---|:---|
| **Operating System** | Linux 6.6.122+ x86_64 | Windows 11 x86_64 | Compatible |
| **Python Version** | 3.13.15 | 3.11.9 | Compatible |
| **PyTorch** | 2.11.0+cu130 | 2.2+ (CPU/CUDA) | Compatible |
| **Sentence Transformers** | 5.7.0 (`intfloat/e5-base-v2`) | >=3.0.0 | Compatible |
| **Transformers** | 5.18.0 (`cardiffnlp/twitter-roberta...`) | >=4.40.0 | Compatible |
| **Scikit-Learn** | 1.6.1 | 1.4+ | Compatible |
| **SciPy** | 1.13+ | 1.11+ | Compatible |
| **Hardware Reference** | NVIDIA Tesla T4 (16GB) | Local Workstation | Validated |

---

## 3. Dataset & Cohort Verification

### A. Internal Multi-Domain Cohort (Phase 9–12)
* **Authoritative Size:** 98 unique videos
* **Domain Distribution:**
  - `Biology`: 20 videos
  - `Mathematics`: 20 videos
  - `Programming`: 20 videos
  - `Physics`: 19 videos (video `uK2eFv7ne_Q` excluded due to 0 comments)
  - `Data Science`: 19 videos (video `z2WzPGAEnb4` excluded due to 0 comments)
* **Dataset Characteristics (from `phase12_dataset_statistics_overall.csv`):**
  - Downloaded comment records: 8,702
  - Metadata total comments: 314,004
  - Retained query-relevant comments: 5,000 (1,000 per domain)
  - Mean duration: 196.73 minutes
  - Mean views: 3,893,495
  - Mean likes: 90,213.2

### B. External LAK 2026 Benchmark Evaluation Cohort (Phase 10, 11, 13)
* **Total Benchmark Records:** 914 binary Accepted/Rejected judgments across 54 topics and 866 unique videos.
* **Unavailable YouTube Videos:** 25 videos (private, deleted, or suspended).
* **Accessible Evaluation Cohort:**
  - Topic-video pairs: **888**
  - Unique educational topics: **54**
  - Accessible unique videos: **841**
  - Ground truth label distribution: Accepted (1): 334, Rejected (0): 554

---

## 4. Verification of Manuscript Results

### A. Component Ablation (Manuscript Table 18)
Evaluated across 888 accessible pairs and 54 topics:

| Ranking Variant | NDCG@5 | NDCG@10 | MAP@10 | MRR | P@5 | P@10 | R@5 | R@10 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **Full Hybrid (Proposed)** | **0.4829** | **0.6031** | **0.4398** | **0.6666** | 0.4407 | **0.4364** | 0.3677 | **0.7300** |
| Minus Semantic Relevance | 0.3949 | 0.5175 | 0.3554 | 0.5227 | 0.3963 | 0.3957 | 0.3176 | 0.6668 |
| Minus Sentiment Analysis | 0.4800 | 0.5734 | 0.4044 | 0.6547 | **0.4556** | 0.4142 | **0.3775** | 0.6947 |
| Minus Intrinsic Quality (IQS) | 0.4466 | 0.5561 | 0.3982 | 0.6076 | 0.4111 | 0.4068 | 0.3523 | 0.6721 |
| Fixed 50/50 Fusion | 0.4817 | 0.5907 | 0.4277 | 0.6519 | 0.4444 | 0.4179 | 0.3723 | 0.7128 |

*Finding:* Removing semantic relevance causes the largest drop in ranking quality ($\Delta \text{NDCG@10} = -0.0856$), confirming semantic relevance as the anchor feature. Adaptive fusion outperforms fixed 50/50 fusion across NDCG@10, MAP@10, MRR, P@10, and R@10.

### B. Baseline Comparison & Statistical Significance (Manuscript Table 21 & 22)
Evaluated across identical 54 topics with paired Wilcoxon signed-rank test:

| Comparison | Metric | Hybrid Mean | Baseline Mean | Mean Difference | Wilcoxon Stat | p-value | Significant (p<0.05) | Superior Model |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| Hybrid vs DPR | NDCG@10 | 0.6031 | 0.5874 | +0.0157 | 731.0 | 0.9211 | False | No significant difference |
| Hybrid vs BM25 | NDCG@10 | 0.6031 | 0.6109 | -0.0078 | 655.0 | 0.4512 | False | No significant difference |
| Hybrid vs RankNet | NDCG@10 | 0.6031 | 0.6059 | -0.0028 | 720.0 | 0.8464 | False | No significant difference |
| Hybrid vs RankNet | P@5 | 0.4407 | 0.5185 | -0.0778 | 231.5 | **0.0421** | **True** | **RankNet > Hybrid** |
| Hybrid vs E5 | NDCG@10 | 0.6031 | 0.6583 | -0.0552 | 513.0 | **0.0482** | **True** | **E5 > Hybrid** |
| Hybrid vs E5 | MAP@10 | 0.4398 | 0.5035 | -0.0638 | 511.0 | **0.0462** | **True** | **E5 > Hybrid** |
| Hybrid vs E5 | P@5 | 0.4407 | 0.5111 | -0.0704 | 225.0 | **0.0339** | **True** | **E5 > Hybrid** |

*Honest Scientific Finding:* As accurately stated in the manuscript and Reviewer Response, the proposed Hybrid model is competitive with established baselines but is not claimed to be universally superior. E5 dense retrieval significantly outperforms Hybrid on NDCG@10, MAP@10, and P@5; RankNet significantly outperforms on P@5. This negative/comparative finding is strictly preserved.

---

## 5. Scope of Local vs Cached Execution

1. **Deterministic Components (Rerun & Verified):**
   - All metric evaluation routines (NDCG, MAP, MRR, Precision, Recall)
   - Adaptive alpha calculation and score fusion
   - Statistical significance tests and bootstrap resampling
   - Empirical scalability benchmark
   - Pytest unit and regression test suite (18/18 passed)
2. **External API Dependent Components (Preserved with Cached Evidence):**
   - *YouTube Data API v3:* Live re-crawling of 8,702 comments was not repeated to avoid dynamic comment drift (comments being deleted or added on YouTube over time) and to ensure deterministic comparisons.
   - *Gemini 3.5 Flash-Lite API:* 841 teaching scores and explanations are preserved from verified cached runs to eliminate external billing and guarantee identical experimental replication.
