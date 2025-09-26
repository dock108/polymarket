from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set

import httpx

from app.core.config import settings
from app.schemas.polymarket import PMEvent, PMMarket, PMOutcome
from app.utils.odds import apply_fee_to_probability, clamp


class PolymarketAPIError(RuntimeError):
    pass


class PolymarketService:
    def __init__(self, base_url: Optional[str] = None, fee_cushion: Optional[float] = None) -> None:
        self.base_url = base_url or settings.polymarket_base_url
        self.fee_cushion = fee_cushion if fee_cushion is not None else settings.fee_cushion
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=20.0,
            headers={"User-Agent": "polymarket-edge/0.1"},
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        resp = await self._client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    def _extract_markets_array(self, data: Any) -> List[Dict[str, Any]]:
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("markets"), list):
            return data["markets"]  # type: ignore[index]
        raise PolymarketAPIError("Unexpected /markets response format; expected list or {\"markets\": [...]}.")

    async def fetch_markets_paginated(self, page_limit: int = 500, max_pages: int = 5) -> List[Dict[str, Any]]:
        all_markets: List[Dict[str, Any]] = []
        seen_ids: Set[str] = set()
        offset = 0
        for _ in range(max_pages):
            params: Dict[str, Any] = {"limit": str(page_limit), "closed": "false"}
            if offset:
                params["offset"] = str(offset)
            data = await self._get("/markets", params=params)
            batch = self._extract_markets_array(data)
            if not batch:
                break
            new_count = 0
            for m in batch:
                mid = str(m.get("id") or m.get("marketId") or m.get("slug") or "")
                if mid and mid not in seen_ids:
                    seen_ids.add(mid)
                    all_markets.append(m)
                    new_count += 1
            if len(batch) < page_limit or new_count == 0:
                # no more pages, or offset param ignored and no new items
                break
            offset += page_limit
        if not all_markets:
            raise PolymarketAPIError("No markets returned from /markets (closed=false). Check API availability.")
        return all_markets

    def _extract_event_info(self, m: Dict[str, Any]) -> tuple[str, str]:
        ev_list = m.get("events")
        if not isinstance(ev_list, list) or not ev_list:
            raise PolymarketAPIError("Market missing embedded 'events' array; cannot determine event grouping.")
        ev0 = ev_list[0] or {}
        eid = str(ev0.get("id") or ev0.get("slug") or ev0.get("eventId") or "").strip()
        title = str(ev0.get("title") or ev0.get("name") or m.get("eventName") or m.get("title") or m.get("question") or "").strip()
        if not eid:
            raise PolymarketAPIError("Embedded event does not contain an 'id' or 'slug'.")
        return eid, title

    def _yes_probability_from_outcomes(self, outcomes_data: Any) -> Optional[float]:
        if not (isinstance(outcomes_data, list) and len(outcomes_data) == 2):
            return None
        candidates: List[Optional[float]] = []
        names_lower: List[str] = []
        for o in outcomes_data:
            names_lower.append(str(o.get("name") or o.get("label") or o.get("outcome") or "").lower())
            val = None
            for price_key in ("price", "lastPrice", "yesPrice", "probability"):
                if o.get(price_key) is not None:
                    try:
                        val = float(o[price_key])
                        break
                    except Exception:
                        pass
            candidates.append(val)
        if "yes" in names_lower:
            idx = names_lower.index("yes")
            return candidates[idx]
        for v in candidates:
            if v is not None:
                return v
        return None

    def _market_level_yes_probability(self, m: Dict[str, Any]) -> Optional[float]:
        for k in ("lastTradePrice", "bestBid", "bestAsk"):
            if m.get(k) is not None:
                try:
                    return float(m[k])
                except Exception:
                    continue
        return None

    def _normalize_market(self, m: Dict[str, Any], event_id: str) -> Optional[PMMarket]:
        # Use explicit outcome prices if present; otherwise derive from market-level price fields
        yes_prob = self._yes_probability_from_outcomes(m.get("outcomes"))
        if yes_prob is None:
            yes_prob = self._market_level_yes_probability(m)
        if yes_prob is None:
            return None
        yes_prob = clamp(yes_prob, 0.0, 1.0)
        yes_prob = apply_fee_to_probability(yes_prob, self.fee_cushion)
        no_prob = apply_fee_to_probability(1.0 - yes_prob, self.fee_cushion)
        outcomes = [
            PMOutcome(name="Yes", price=yes_prob),
            PMOutcome(name="No", price=no_prob),
        ]
        return PMMarket(
            market_id=str(m.get("id") or m.get("marketId") or m.get("slug") or ""),
            event_id=event_id,
            question=str(m.get("question") or m.get("title") or m.get("name") or ""),
            outcomes=outcomes,
        )

    async def fetch_events_with_binary_markets(self) -> List[PMEvent]:
        markets_raw = await self.fetch_markets_paginated()
        grouped: Dict[str, List[PMMarket]] = defaultdict(list)
        titles: Dict[str, str] = {}

        total = len(markets_raw)
        examined = 0
        kept = 0

        for m in markets_raw:
            examined += 1
            try:
                eid, etitle = self._extract_event_info(m)
            except PolymarketAPIError:
                continue
            nm = self._normalize_market(m, eid)
            if nm:
                grouped[eid].append(nm)
                titles.setdefault(eid, etitle)
                kept += 1

        if kept == 0:
            sample_keys = list(markets_raw[0].keys()) if markets_raw else []
            raise PolymarketAPIError(
                f"No usable binary markets found after pagination (examined={examined}, total={total}). "
                f"Sample market keys: {sample_keys}"
            )

        events: List[PMEvent] = []
        for eid, mkts in grouped.items():
            if not mkts:
                continue
            events.append(PMEvent(event_id=eid, title=titles.get(eid, ""), sport=None, markets=mkts))
        return events


async def main_smoke() -> None:
    svc = PolymarketService()
    try:
        events = await svc.fetch_events_with_binary_markets()
        print(f"Events with binary markets: {len(events)}")
        print(events[0].model_dump() if events else {})
    finally:
        await svc.close()


if __name__ == "__main__":
    asyncio.run(main_smoke())
