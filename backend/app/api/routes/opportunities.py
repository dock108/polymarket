from __future__ import annotations

from fastapi import APIRouter
from typing import List

from app.schemas.opportunity import Opportunity
from app.services.opportunities import OpportunityEngine

router = APIRouter()


@router.get("/api/opportunities", response_model=List[Opportunity])
async def get_opportunities() -> List[Opportunity]:
    eng = OpportunityEngine()
    return await eng.fetch_opportunities()
