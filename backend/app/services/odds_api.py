from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings
from app.schemas.odds_api import BookLine, EventLines
from app.utils.odds import american_to_decimal


class OddsAPIError(RuntimeError):
    pass


def _vig_removed_pair(p1: float, p2: float) -> tuple[float, float]:
    total = p1 + p2
    if total <= 0:
        return 0.0, 0.0
    return p1 / total, p2 / total


class OddsAPIService:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.base_url = base_url or settings.odds_api_base_url
        self.api_key = api_key or settings.odds_api_key
        if not self.api_key:
            raise OddsAPIError("ODDS_API_KEY is required")
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=20.0, headers={"User-Agent": "polymarket-edge/0.1"})

    async def close(self) -> None:
        await self._client.aclose()

    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        p = params.copy() if params else {}
        p["apiKey"] = self.api_key
        resp = await self._client.get(path, params=p)
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text
            raise OddsAPIError(f"Odds API error {exc.response.status_code}: {detail}") from exc
        return resp.json()

    async def fetch_sport_odds(self, sport_key: str) -> List[EventLines]:
        params: Dict[str, Any] = {
            "regions": settings.odds_api_regions,
            "markets": settings.odds_api_markets,
            "oddsFormat": "american",
        }
        if settings.odds_api_bookmakers:
            params["bookmakers"] = settings.odds_api_bookmakers
        data = await self._get(f"/sports/{sport_key}/odds", params=params)
        if not isinstance(data, list):
            raise OddsAPIError("Unexpected odds response shape; expected list.")

        results: List[EventLines] = []
        for ev in data:
            eid = str(ev.get("id") or ev.get("event_id") or ev.get("commence_time") or "")
            title = str(ev.get("home_team") or ev.get("title") or "")
            lines: List[BookLine] = []
            bookmakers = ev.get("bookmakers") or []

            per_side_h2h: Dict[str, int] = {}

            for book in bookmakers:
                bkey = str(book.get("key") or book.get("title") or "")
                markets = book.get("markets") or []
                for mk in markets:
                    mk_key = str(mk.get("key") or "")
                    outcomes = mk.get("outcomes") or []
                    for o in outcomes:
                        side = str(o.get("name") or o.get("description") or "")
                        american = o.get("price")
                        point = None
                        if mk_key in ("spreads", "totals") and o.get("point") is not None:
                            try:
                                point = float(o.get("point"))
                            except Exception:
                                point = None
                        # Skip lines without odds to avoid decimal_odds=None in output
                        if american is None:
                            continue
                        try:
                            american = int(american)
                        except Exception:
                            continue
                        if mk_key == "h2h":
                            if side not in per_side_h2h:
                                per_side_h2h[side] = american
                            else:
                                current = per_side_h2h[side]
                                pick = american
                                if (american < 0 and current < 0 and american < current) or (american > 0 and current > 0 and american < current) or (american < 0 and current > 0):
                                    pick = american
                                per_side_h2h[side] = pick
                        lines.append(
                            BookLine(
                                bookmaker=bkey,
                                market=mk_key,
                                side=side,
                                american_odds=american,
                                decimal_odds=american_to_decimal(american),
                                point=point,
                            )
                        )

            if len(per_side_h2h) == 2:
                sides = list(per_side_h2h.keys())
                a_1, a_2 = per_side_h2h[sides[0]], per_side_h2h[sides[1]]

                def implied_from_american(a: int) -> float:
                    dec = american_to_decimal(a)
                    return 1.0 / dec

                p1 = implied_from_american(a_1)
                p2 = implied_from_american(a_2)
                f1, f2 = _vig_removed_pair(p1, p2)

                for bl in lines:
                    if bl.market != "h2h":
                        continue
                    if bl.side == sides[0]:
                        bl.fair_probability = f1
                        bl.fair_decimal_odds = (1.0 / f1) if f1 > 0 else None
                    elif bl.side == sides[1]:
                        bl.fair_probability = f2
                        bl.fair_decimal_odds = (1.0 / f2) if f2 > 0 else None

            results.append(EventLines(sport=sport_key, event_id=eid, title=title, lines=lines))
        return results


async def main_smoke() -> None:
    svc = OddsAPIService()
    try:
        events = await svc.fetch_sport_odds("basketball_nba")
        print(f"Fetched events: {len(events)}")
        if events:
            print(events[0].model_dump())
    finally:
        await svc.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main_smoke())
