import numpy as np
import pandas as pd
import json
from scipy.spatial.distance import cdist
from typing import Dict


def _split_status(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return data.query("status == 'Accepted'"), data.query("status == 'Rejected'")


def _load_embeddings(series: pd.Series) -> np.ndarray:
    return np.vstack(series.map(json.loads))


def compute_baseline(data: pd.DataFrame) -> Dict[str, int]:
    accepted, rejected = _split_status(data)
    if accepted.empty or rejected.empty:
        return {"baseline_ok": 0, "baseline_nok": 0}

    accepted_orders = accepted["resource_order"].values
    rejected_orders = rejected["resource_order"].values
    comparisons = accepted_orders[:, None] < rejected_orders

    ok = int(comparisons.sum())
    nok = int(comparisons.size - ok)
    return {"baseline_ok": ok, "baseline_nok": nok}


def compute_embedding_performance(data: pd.DataFrame) -> Dict[str, int]:
    accepted, rejected = _split_status(data)

    if accepted.empty or rejected.empty:
        return {"ok": 0, "not_ok": 0}

    A = _load_embeddings(accepted["value"])
    R = _load_embeddings(rejected["value"])

    AA_dist = cdist(A, A, "cosine")
    AR_dist = cdist(A, R, "cosine")

    ok = 0
    not_ok = 0

    for i in range(len(A)):
        # Remove self from intra-accepted distances
        intra_accepted = np.delete(AA_dist[i], i)
        comparisons = intra_accepted[:, np.newaxis] < AR_dist[i]
        ok += np.sum(comparisons)
        not_ok += comparisons.size - np.sum(comparisons)

    return {"ok": int(ok), "not_ok": int(not_ok)}


def agg_function(data: pd.DataFrame) -> Dict[str, int]:
    return compute_embedding_performance(data)


def compute_embedding_precision(data: pd.DataFrame, at_n: int = 5) -> Dict[str, float]:
    accepted, rejected = _split_status(data)
    num_accepted = len(accepted)
    total = num_accepted + len(rejected)

    if num_accepted == 0 or total <= 1:
        return {
            "precision_at_n": np.nan,
            # "num_accepted": num_accepted,
            # "num_rejected": len(rejected),
        }

    all_data = pd.concat([accepted, rejected])
    all_emb = _load_embeddings(all_data["value"])
    labels = all_data["status"].values
    accepted_idx = accepted.index

    precision_scores = []
    for i, idx in enumerate(accepted_idx):
        emb = all_emb[i]
        sims = 1 - cdist([emb], all_emb, "cosine")[0]
        sims[i] = -np.inf  # exclude self
        top_n = np.argpartition(sims, -min(num_accepted, at_n - 1))[-(at_n - 1) :]
        hits = (labels[top_n] == "Accepted").sum()
        precision_scores.append(hits / (at_n - 1))

    return {
        "precision_at_n": float(np.mean(precision_scores)),
        # "num_accepted": num_accepted,
        # "num_rejected": len(rejected),
    }


def compute_baseline_precision(data: pd.DataFrame, at_n: int = 5) -> Dict[str, float]:
    if "resource_order" not in data.columns:
        return {"baseline_precision": np.nan}

    accepted = data.query("status == 'Accepted'")
    if accepted.empty or len(data) <= 1:
        return {"baseline_precision": np.nan}

    effective_n = min(at_n, len(accepted))
    top_n = data.sort_values("resource_order").head(effective_n)
    precision = (top_n["status"] == "Accepted").sum() / effective_n
    return {"baseline_precision": float(precision)}


def top_agg_function(data: pd.DataFrame, at_n: int = 5) -> Dict[str, float]:
    return {
        **compute_embedding_precision(data, at_n),
        # **compute_baseline_precision(data, at_n),
    }
