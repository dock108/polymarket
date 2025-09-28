from __future__ import annotations

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class Opportunity(BaseModel):
    id: str  # composite id like source:market_id or similar
    source: str  # polymarket | sportsbook | datagolf (when applicable)
    title: str
    sport: Optional[str] = None
    event_id: Optional[str] = None
    market_id: Optional[str] = None

    # Canonical keys for joining
    canonical_event_key: Optional[str] = None
    home_team_key: Optional[str] = None
    away_team_key: Optional[str] = None

    # Polymarket fields
    yes_probability: Optional[float] = None  # fee-adjusted probability
    price: Optional[float] = None  # current price (0..1)

    # EV
    ev_usd_per_share: Optional[float] = None  # EV in $ per 1 share (cost=price)
    ev_percent: Optional[float] = None  # EV / price if price>0

    # Comparison metadata
    comparison_basis: Optional[str] = None  # none | sportsbook_fair | datagolf | ...
    comparison_sources: Optional[List[str]] = None  # e.g., ["pinnacle", "betfair"]

    # Provenance and trace (compact)
    source_attribution: Optional[Dict[str, Any]] = None
    inputs: Optional[Dict[str, Any]] = None
    calc_notes: Optional[str] = None

    # Freshness
    updated_at: Optional[str] = None
    is_stale: Optional[bool] = None
