from __future__ import annotations

from fastapi import APIRouter, Query
from typing import List, Dict, Any
from datetime import datetime, timezone

from app.schemas.opportunity import Opportunity
from app.services.opportunities import OpportunityEngine
from app.core.config import settings
from app.services.polymarket import PolymarketService

router = APIRouter()


@router.get("/api/opportunities", response_model=List[Opportunity])
async def get_opportunities(include_non_sports: bool = Query(False)) -> List[Opportunity]:
    eng = OpportunityEngine()
    try:
        items: List[Opportunity] = await eng.fetch_opportunities(include_non_sports=include_non_sports)
    except TypeError:
        # Backward-compat for test fakes without the kwarg
        items = await eng.fetch_opportunities()  # type: ignore[misc]

    # Compute staleness per item (additive field) without changing top-level shape
    as_of = datetime.now(timezone.utc)
    threshold_seconds = int(settings.refresh_interval_seconds)
    for o in items:
        is_stale = False
        try:
            if o.updated_at:
                updated = datetime.fromisoformat(o.updated_at)
                age = (as_of - updated).total_seconds()
                is_stale = age > threshold_seconds
        except Exception:
            is_stale = True
        # set attribute on model instance
        o.is_stale = is_stale  # type: ignore[attr-defined]
    return items


@router.get("/api/opportunities/meta")
async def get_opportunities_with_meta() -> Dict[str, Any]:
    eng = OpportunityEngine()
    items: List[Opportunity] = await eng.fetch_opportunities()

    as_of = datetime.now(timezone.utc)
    threshold_seconds = int(settings.refresh_interval_seconds)

    enriched: List[Dict[str, Any]] = []
    for o in items:
        is_stale = False
        try:
            if o.updated_at:
                updated = datetime.fromisoformat(o.updated_at)
                age = (as_of - updated).total_seconds()
                is_stale = age > threshold_seconds
        except Exception:
            is_stale = True
        od = o.model_dump()
        od["is_stale"] = is_stale
        enriched.append(od)

    return {
        "as_of": as_of.isoformat(),
        "staleness_seconds": threshold_seconds,
        "items": enriched,
    }


@router.get("/api/raw/polymarket")
async def get_raw_polymarket() -> Dict[str, Any]:
    svc = PolymarketService()
    try:
        raw_markets = await svc.fetch_markets_paginated()
    finally:
        await svc.close()
    return {"count": len(raw_markets), "markets": raw_markets}
