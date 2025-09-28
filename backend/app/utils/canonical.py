from __future__ import annotations

import re
import unicodedata
from typing import Optional, Tuple


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
    sport_part = (sport or "").strip().lower().replace(" ", "_")
    title_part = _normalize_string(title).replace(" ", "_")
    if date_hint:
        date_part = _normalize_string(date_hint).replace(" ", "_")
        return f"{sport_part}:{title_part}:{date_part}"
    return f"{sport_part}:{title_part}"


def parse_event_title_teams(title: str) -> Optional[Tuple[str, str]]:
    # Try common separators: ' vs ', ' v ', ' @ ', ' at '
    candidates = [
        r"\s+vs\s+",
        r"\s+v\s+",
        r"\s+@\s+",
        r"\s+at\s+",
        r"\s+-\s+",
    ]
    for sep in candidates:
        parts = re.split(sep, title, flags=re.IGNORECASE)
        if len(parts) == 2:
            a = normalize_team_name(parts[0])
            b = normalize_team_name(parts[1])
            if a and b:
                return a, b
    return None


def normalize_free_text(value: str) -> str:
    return _normalize_string(value)
