from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional


class PMOutcome(BaseModel):
    name: str
    price: float = Field(ge=0.0, le=1.0)


class PMMarket(BaseModel):
    market_id: str
    event_id: Optional[str] = None
    question: str
    slug: Optional[str] = None
    outcomes: List[PMOutcome]


class PMEvent(BaseModel):
    event_id: str
    sport: Optional[str] = None
    title: str
    ticker: Optional[str] = None
    slug: Optional[str] = None
    markets: List[PMMarket] = []
