# Benchmark Data Documentation & Access Note

This directory contains the ground truth and evaluation resources derived from the **LAK 2026 Educational Video Relevance Benchmark**.

---

## 1. Primary Evaluation Files

The complete evaluation pipeline executes directly from the structured CSVs included in this repository:

1. **`lak2026_benchmark_eval_all914.csv`**:
   - Total binary relevance judgments: **914**
   - Topics: **54**
   - Unique videos: **866**
   - Labels: `Accepted` (1: 349) / `Rejected` (0: 565)
2. **`lak2026_benchmark_eval_accessible_888.csv`**:
   - The authoritative accessible evaluation cohort used by the proposed Full Hybrid model and all baselines (BM25, E5, DPR, RankNet).
   - Filtered for YouTube accessibility (excludes 25 unavailable videos).
   - Topic-video pairs: **888**
   - Educational topics: **54**
   - Accessible unique videos: **841**
   - Ground truth distribution: Accepted (1: 334), Rejected (0: 554)
3. **`lak_unavailable_video_ids_25.csv`**:
   - List of the 25 YouTube video IDs that are no longer accessible on YouTube (deleted, private, or suspended).
4. **`lak_youtube_metadata_841.csv`**:
   - YouTube title, description, channel, duration, views, likes, and comment counts for all 841 accessible videos.
5. **`lak_youtube_comments.csv`**:
   - Reconstructed comment pool (31,603 usable comments) used for semantic relevance filtering and sentiment analysis.
6. **`lak_teaching_scores.csv`**:
   - Pre-computed LLM pedagogical teaching evaluation scores generated with Gemini 3.5 Flash-Lite under the structured prompt rubric.

---

## 2. Note on `db.sqlite3`

The original raw benchmark package included an uncompressed SQLite database (`db.sqlite3`, approximately 374 MB) containing historical web crawl metadata and database indexes.

Because GitHub enforces a strict 100 MB per-file upload limit, `db.sqlite3` is excluded from the Git repository via `.gitignore`. 

> **Important:** The pipeline **does not require** `db.sqlite3` for ranking execution or reproduction. All tabular data, queries, topic identifiers, video IDs, and expert ground-truth relevance annotations were extracted directly into `lak2026_benchmark_eval_all914.csv` and `lak2026_benchmark_eval_accessible_888.csv`.
