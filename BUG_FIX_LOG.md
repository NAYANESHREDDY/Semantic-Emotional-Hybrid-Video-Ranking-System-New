# Bug Fix & Technical Remediation Log

**Project Title:** Explainable Educational Video Ranking Using Hybrid Semantic Intelligence and LLM-Assisted Engagement Analysis  
**Auditor:** Antigravity Engineering Agent  
**Date:** October 2026  

---

## Issue 1: Hardcoded Frozen Cohort Size Assertion Crash in Phase 12D-B

* **Affected Component:** `NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb` (Cell 75, Phase 12D-B)
* **Severity:** High (blocked Phase 12 execution and caused downstream completeness check failure in Cell 76)
* **Root Cause Analysis:**
  1. In Phase 9A, YouTube API collection retrieved 20 candidate videos per domain across 5 domains (100 total).
  2. However, two videos had comments disabled or zero comments on YouTube:
     - `z2WzPGAEnb4` (Domain: Data Science / Machine Learning Course) — `comment_count = 0`
     - `uK2eFv7ne_Q` (Domain: Physics / Quantum Mechanics Lecture) — `comment_count = 0`
  3. Because the Feature-based Engagement Score (FES) requires audience comment sentiment and semantic relevance, videos lacking any comments cannot participate in engagement modeling and were legitimately filtered out.
  4. This left exactly:
     - Biology: 20
     - Mathematics: 20
     - Programming: 20
     - Physics: 19
     - Data Science: 19
     - **Total: 98 unique videos**
  5. In `phase9_cohort_manifest.json`, the authoritative cohort size was explicitly recorded and hashed as **98**. This 98-video count was also documented in the manuscript (Section 3.2, Table 1, Table 20) and the Reviewer Response Letter.
  6. However, notebook v17 inherited legacy code from v16 (where an earlier run had 20 Data Science videos for a total of 99). Cell 75 contained an obsolete hardcoded check:
     ```python
     if frozen_n < 99:
         raise ValueError(f"Frozen Phase-9F cohort contains only {frozen_n} rows; expected frozen cohort size is 99.")
     cohort_sizes = [20, 40, 60, 80, 99]
     ```
  7. When executed with the true 98-video cohort, this assertion raised `ValueError`, crashing Cell 75 and failing to produce `phase12_empirical_scalability.csv` and `phase12_scalability_summary.csv`. Consequently, Cell 76 reported missing required artifacts.
* **Remediation Implemented:**
  1. Updated Cell 75 to validate against the authoritative cohort size (`EXPECTED_INTERNAL_COHORT_SIZE = 98`), matching `phase9_cohort_manifest.json`.
  2. Set scalability evaluation points dynamically: `cohort_sizes = [20, 40, 60, 80, frozen_n]`.
  3. Executed the deterministic scalability ranking sort ($O(N \log N)$) across all sizes up to 98 videos and saved `phase12_empirical_scalability.csv` and `phase12_scalability_summary.csv`.
* **Validation:**
  - Scalability analysis executed cleanly.
  - Phase 12J completeness check (`test_phase12_completeness`) ran and confirmed **16 out of 16 required files present (0 missing)**.
  - Automated regression test `test_internal_cohort_count_and_domains` in `tests/test_cohort_and_data_integrity.py` passed with 100% compliance.

---

## Issue 2: Missing Typing Import in `src/hybrid_ranking.py`

* **Affected Component:** `src/hybrid_ranking.py`
* **Severity:** Medium (prevented module import during unit testing)
* **Root Cause Analysis:** Function signature `rank_items(..., group_by: Optional[str] = None)` used `Optional` without importing it from `typing`.
* **Remediation Implemented:** Added `Optional` to `from typing import Union, Optional`.
* **Validation:** Pytest test suite re-executed; all 18 test cases collected and passed.

---

## Issue 3: Windows Shell CP-1252 Encoding Exceptions

* **Affected Component:** Console scripts and logging utilities
* **Severity:** Low (prevented console output containing arrows or Unicode characters)
* **Root Cause Analysis:** Default Windows PowerShell / CMD terminal environment uses Windows-1252 codepage, which cannot encode mathematical arrows (`\u2192`) or checkmarks.
* **Remediation Implemented:** Added `sys.stdout.reconfigure(encoding='utf-8')` to all audit scripts and Python entry points.
* **Validation:** Scripts executed without `UnicodeEncodeError`.

---

## Issue 4: Identification of Authoritative Master Notebook

* **Affected Component:** Experimental archive
* **Severity:** Critical (risk of utilizing stale, unexecuted notebook versions)
* **Investigation:**
  - The loose notebook `NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb` in `Downloads` had 203 cells, of which Phase 13 cells (195–200) had cleared outputs (`outputs=False`).
  - The uploaded zip file `media_1792380011728_fc303b7d.zip` contained an 86-cell version of `NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb` where all Phase 13 cells (78–83) were fully executed and contained all saved verification outputs.
* **Remediation Implemented:**
  - Archived the original notebooks in `archive/original_notebooks/`.
  - Used the complete 86-cell v17 as the authoritative base for `notebooks/NLP_REVISION_v17_LAK_HYBRID_COMPLETE.ipynb`.
  - Documented complete version lineage in `NOTEBOOK_VERSION_MAP.md`.
