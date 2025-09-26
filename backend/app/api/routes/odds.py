from __future__ import annotations

from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.odds_api import EventLines
from app.services.odds_api import OddsAPIService, OddsAPIError

router = APIRouter()


@router.get("/api/odds/{sport}", response_model=List[EventLines])
async def get_odds(sport: str) -> List[EventLines]:
    svc = OddsAPIService()
    try:
        return await svc.fetch_sport_odds(sport)
    except OddsAPIError as e:
        status = e.status_code or 503
        raise HTTPException(status_code=status, detail=str(e))
    finally:
        await svc.close()
