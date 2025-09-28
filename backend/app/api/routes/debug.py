from __future__ import annotations

from fastapi import APIRouter, HTTPException
from typing import Any, Dict

from app.services.opportunities import OpportunityEngine

router = APIRouter()


@router.get("/api/debug/opportunity/{opportunity_id}")
async def debug_opportunity(opportunity_id: str) -> Dict[str, Any]:
    eng = OpportunityEngine()
    items = await eng.fetch_opportunities()
    found = next((o for o in items if o.id == opportunity_id), None)
    if not found:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    trace: Dict[str, Any] = found.model_dump()
    # Note: In this v1, we include compact provenance if present.
    trace.setdefault("trace_info", {
        "note": "Detailed intermediate sportsbook/PM inputs can be expanded in a later iteration.",
    })
    return trace
