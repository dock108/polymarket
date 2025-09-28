from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import re


@dataclass(frozen=True)
class Team:
    key: str
    names: List[str]
    abbrs: List[str]


@dataclass(frozen=True)
class League:
    code: str  # e.g., basketball_nba
    names: List[str]
    team_map: Dict[str, Team]


NBA_TEAMS: Dict[str, Team] = {
    "boston_celtics": Team(
        key="boston_celtics",
        names=["boston celtics", "celtics"],
        abbrs=["bos", "bkn-celtics"],
    ),
    "los_angeles_lakers": Team(
        key="los_angeles_lakers",
        names=["los angeles lakers", "la lakers", "lakers"],
        abbrs=["lal"],
    ),
    # ... add more teams as needed
}

LEAGUES: Dict[str, League] = {
    "basketball_nba": League(
        code="basketball_nba",
        names=["nba", "national basketball association"],
        team_map=NBA_TEAMS,
    )
}


def normalize_text(value: str) -> str:
    v = value.lower().strip()
    v = re.sub(r"[^a-z0-9\s]", " ", v)
    v = re.sub(r"\s+", " ", v)
    return v


def infer_league_from_fields(question: str, title: str, ticker: Optional[str]) -> Optional[str]:
    hay = " ".join(filter(None, [question, title, ticker]))
    hay_n = normalize_text(hay)
    for code, lg in LEAGUES.items():
        for nm in lg.names:
            if nm in hay_n:
                return code
    return None


def infer_team_keys(league_code: str, question: str, title: str) -> List[str]:
    keys: List[str] = []
    hay = normalize_text(" ".join([question, title]))
    league = LEAGUES.get(league_code)
    if not league:
        return keys
    for key, team in league.team_map.items():
        if any(nm in hay for nm in team.names) or any(ab in hay for ab in team.abbrs):
            keys.append(key)
    return keys
