"""
Preprocessing and lexical analysis module.
Implements text normalization and Type-Token Ratio (TTR) lexical diversity.
"""

import re
from typing import List, Set


def clean_text(text: str) -> str:
    """
    Standard text normalization: strips HTML tags, replaces extra whitespace,
    and removes non-printable characters.
    """
    if not isinstance(text, str):
        return ""
    # Remove HTML tags
    cleaned = re.sub(r"<[^>]+>", " ", text)
    # Remove URL links
    cleaned = re.sub(r"http\S+|www\.\S+", " ", cleaned)
    # Normalize whitespaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def tokenize_words(text: str) -> List[str]:
    """
    Tokenizes text into lowercase alphabetic/alphanumeric words.
    """
    cleaned = clean_text(text).lower()
    tokens = re.findall(r"\b[a-z0-9_]+\b", cleaned)
    return tokens


def compute_ttr(text: str) -> float:
    """
    Computes Type-Token Ratio (TTR) = UniqueWords / TotalWords.
    Aligned with conventional lexical diversity definition.
    Returns 0.0 if total words is 0.
    """
    tokens = tokenize_words(text)
    if not tokens:
        return 0.0
    unique_tokens: Set[str] = set(tokens)
    return float(len(unique_tokens) / len(tokens))
