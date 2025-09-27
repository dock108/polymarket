from __future__ import annotations

import re
import unicodedata
from typing import Optional


_ALIAS_MAP = {
    # basketball
    "la clippers": "los angeles clippers",
    "ny knicks": "new york knicks",
    "okc thunder": "oklahoma city thunder",
    # baseball
    "ny yankees": "new york yankees",
}


def _normalize_string(value: str) -> str:
    s = value.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip()
    return s


def normalize_team_name(name: str) -> str:
    base = _normalize_string(name)
    return _ALIAS_MAP.get(base, base)


def canonical_team_key(name: str) -> str:
    return normalize_team_name(name).replace(" ", "_")


def canonical_event_key(sport: Optional[str], title: str, date_hint: Optional[str] = None) -> str:
    # Simple canonicalization: sport + normalized title (date hint optional)
    sport_part = (sport or "").strip().lower().replace(" ", "_")
    title_part = _normalize_string(title).replace(" ", "_")
    if date_hint:
        date_part = _normalize_string(date_hint).replace(" ", "_")
        return f"{sport_part}:{title_part}:{date_part}"
    return f"{sport_part}:{title_part}"
