from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional


class BookLine(BaseModel):
    bookmaker: str
    market: str  # h2h, spreads, totals, outrights
    side: str  # team/player name or descriptor
    american_odds: Optional[int] = None
    decimal_odds: Optional[float] = None
    point: Optional[float] = None  # spread/total number when applicable
    fair_probability: Optional[float] = None  # vig-removed probability for this side
    fair_decimal_odds: Optional[float] = None  # 1 / fair_probability


class EventLines(BaseModel):
    sport: str
    event_id: str
    title: str
    lines: List[BookLine]
    # Join helpers and attribution
    canonical_event_key: Optional[str] = None
    home_team_key: Optional[str] = None
    away_team_key: Optional[str] = None
    selected_bookmaker: Optional[str] = None  # chosen for conservative H2H
