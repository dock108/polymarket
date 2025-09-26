from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/api/golf")
async def get_golf() -> list:
    # DataGolf features are backlogged for later implementation
    return []
