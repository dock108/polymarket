from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional


class DGTournament(BaseModel):
    tour: str
    event_id: str
    name: str
    start_date: str
    end_date: str


class DGPlayerPred(BaseModel):
    player_id: str
    player_name: str
    event_id: str
    win_prob: float  # 0..1


class DGEventPreds(BaseModel):
    event_id: str
    tournament: DGTournament
    players: List[DGPlayerPred]
