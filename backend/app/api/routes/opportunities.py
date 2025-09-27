from __future__ import annotations

from fastapi import APIRouter
from typing import List, Dict, Any
from datetime import datetime, timezone

from app.schemas.opportunity import Opportunity
from app.services.opportunities import OpportunityEngine
from app.core.config import settings

router = APIRouter()


@router.get("/api/opportunities", response_model=List[Opportunity])
async def get_opportunities() -> List[Opportunity]:
    eng = OpportunityEngine()
    items: List[Opportunity] = await eng.fetch_opportunities()

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
