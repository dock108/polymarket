from __future__ import annotations

from pydantic import BaseModel
from typing import Optional


class Opportunity(BaseModel):
    id: str  # composite id like source:market_id or similar
    source: str  # polymarket | sportsbook | datagolf (when applicable)
    title: str
    sport: Optional[str] = None
    event_id: Optional[str] = None
    market_id: Optional[str] = None

    # Polymarket fields
    yes_probability: Optional[float] = None  # fee-adjusted probability
    price: Optional[float] = None  # current price (0..1)

    # EV
    ev_usd_per_share: Optional[float] = None  # EV in $ per 1 share (cost=price)
    ev_percent: Optional[float] = None  # EV / price if price>0

    # Freshness
    updated_at: Optional[str] = None
