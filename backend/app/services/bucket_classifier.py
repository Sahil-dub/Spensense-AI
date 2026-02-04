from __future__ import annotations

import re
from typing import Literal

Bucket = Literal["necessary", "controllable", "unnecessary"]


# Category → bucket mapping (MVP)
CATEGORY_BUCKET_MAP: dict[str, Bucket] = {
    # necessary
    "rent": "necessary",
    "utilities": "necessary",
    "health_insurance": "necessary",
    "groceries": "necessary",
    "transport": "necessary",
    "phone_internet": "necessary",
    "education": "necessary",
    "medical": "necessary",
    # controllable
    "dining_out": "controllable",
    "shopping": "controllable",
    "subscriptions": "controllable",
    "gym": "controllable",
    "travel": "controllable",
    # unnecessary
    "entertainment": "unnecessary",
}

# Keyword fallback (note/description) → bucket
KEYWORD_BUCKET_RULES: list[tuple[re.Pattern[str], Bucket]] = [
    (
        re.compile(
            r"\b(rent|insurance|grocer(?:y|ies)?|electric(?:ity)?|water|internet|phone)\b",
            re.I,
        ),
        "necessary",
    ),
    (
        re.compile(
            r"\b(restaurant|dinner|lunch|coffee|uber|taxi|shopping|amazon|subscr)\b",
            re.I,
        ),
        "controllable",
    ),
    (
        re.compile(
            r"\b(movie|cinema|netflix|spotify|game|gaming|club|bar)\b",
            re.I,
        ),
        "unnecessary",
    ),
]


def infer_bucket(*, category: str | None, note: str | None) -> Bucket | None:
    """
    Infer bucket from category/note.
    Returns None if not confident.
    """
    if category:
        c = category.strip().lower()
        if c in CATEGORY_BUCKET_MAP:
            return CATEGORY_BUCKET_MAP[c]

    if note:
        n = note.strip()
        for pattern, bucket in KEYWORD_BUCKET_RULES:
            if pattern.search(n):
                return bucket

    return None
