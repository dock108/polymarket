from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings
from app.schemas.datagolf import DGTournament, DGPlayerPred, DGEventPreds


class DataGolfError(RuntimeError):
    pass


class DataGolfService:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.base_url = base_url or settings.datagolf_base_url
        self.api_key = api_key or settings.datagolf_api_key
        if not self.api_key:
            raise DataGolfError("DATAGOLF_API_KEY is required")
        self._client = httpx.AsyncClient(
            base_url=self.base_url, timeout=20.0, headers={"User-Agent": "polymarket-edge/0.1"}
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        p = params.copy() if params else {}
        p["key"] = self.api_key
        resp = await self._client.get(path, params=p)
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text
            raise DataGolfError(f"DataGolf error {exc.response.status_code}: {detail}") from exc
        return resp.json()

    async def fetch_schedule(self, tour: str = "pga") -> List[DGTournament]:
        data = await self._get("/get-schedule", params={"tour": tour})
        events: List[DGTournament] = []
        for ev in data.get("schedule", []):
            events.append(
                DGTournament(
                    tour=tour,
                    event_id=str(ev.get("event_id") or ev.get("dg_id") or ev.get("id") or ""),
                    name=str(ev.get("event_name") or ev.get("name") or ""),
                    start_date=str(ev.get("start_date") or ""),
                    end_date=str(ev.get("end_date") or ""),
                )
            )
        return events

    async def fetch_pre_tournament_preds(self, event_id: str) -> DGEventPreds:
        data = await self._get("/preds/pre-tournament", params={"event_id": event_id})
        tour = DGTournament(
            tour=str(data.get("tour") or "pga"),
            event_id=event_id,
            name=str(data.get("event_name") or data.get("event") or ""),
            start_date=str(data.get("start_date") or ""),
            end_date=str(data.get("end_date") or ""),
        )
        players: List[DGPlayerPred] = []
        for row in data.get("players", []):
            win = row.get("win")
            if win is None:
                continue
            try:
                win_prob = float(win)
            except Exception:
                continue
            players.append(
                DGPlayerPred(
                    player_id=str(row.get("player_id") or row.get("dg_id") or ""),
                    player_name=str(row.get("player_name") or row.get("name") or ""),
                    event_id=event_id,
                    win_prob=win_prob,
                )
            )
        return DGEventPreds(event_id=event_id, tournament=tour, players=players)


async def main_smoke() -> None:
    svc = DataGolfService()
    try:
        schedule = await svc.fetch_schedule("pga")
        print(f"Schedule events: {len(schedule)}")
        if schedule:
            preds = await svc.fetch_pre_tournament_preds(schedule[0].event_id)
            print(preds.model_dump())
    finally:
        await svc.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main_smoke())
