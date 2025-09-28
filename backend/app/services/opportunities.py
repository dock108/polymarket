from __future__ import annotations

from typing import List, Dict
from datetime import datetime, timezone

from app.schemas.opportunity import Opportunity
from app.services.polymarket import PolymarketService
from app.services.odds_api import OddsAPIService, OddsAPIError
from app.core.config import settings
from app.utils.canonical import canonical_event_key
from app.utils.sports_config import infer_league_from_fields, infer_team_keys


class OpportunityEngine:
    async def fetch_opportunities(self, include_non_sports: bool = False) -> List[Opportunity]:
        # Fetch PM
        pm = PolymarketService()
        try:
            events = await pm.fetch_events_with_binary_markets()
        finally:
            await pm.close()

        # Attempt sportsbook fair probs for configured sports if any
        sb_fair: Dict[str, Dict[str, float]] = {}
        try:
            sport_keys = sorted({(e.sport or "").lower() for e in events if e.sport})
            if sport_keys and settings.odds_api_key:
                sb = OddsAPIService()
                try:
                    for sk in sport_keys:
                        try:
                            lines = await sb.fetch_sport_odds(sk)
                        except OddsAPIError:
                            continue
                        for ev in lines:
                            if not ev.canonical_event_key:
                                ev.canonical_event_key = canonical_event_key(ev.sport, ev.title)
                            probs: Dict[str, float] = {}
                            for bl in ev.lines:
                                if bl.market == "h2h" and bl.fair_probability is not None:
                                    probs[bl.side] = bl.fair_probability
                            if len(probs) == 2:
                                sb_fair[ev.canonical_event_key] = probs
                finally:
                    await sb.close()
        except Exception:
            sb_fair = {}

        now_iso = datetime.now(timezone.utc).isoformat()
        opps: List[Opportunity] = []
        for ev in events:
            league_code = ev.sport
            if not league_code:
                league_code = infer_league_from_fields(
                    question=" ".join(m.question for m in ev.markets),
                    title=ev.title,
                    ticker=ev.ticker,
                )
            if not include_non_sports and not league_code:
                # Filter out if still not identified as sports
                continue

            for m in ev.markets:
                yes = next((o for o in m.outcomes if o.name.lower() == "yes"), None)
                no = next((o for o in m.outcomes if o.name.lower() == "no"), None)
                if not yes or not no:
                    continue
                p_true_pm = yes.price

                fee = max(0.0, min(settings.fee_cushion, 1.0))
                denom = (1.0 - fee) if (1.0 - fee) > 0 else 1.0
                raw_price = max(0.0, min(1.0, p_true_pm / denom))

                price = raw_price
                if price <= 0 or p_true_pm < 0 or p_true_pm > 1:
                    continue

                ce_key = canonical_event_key(league_code, ev.title)
                ev_usd = 0.0
                ev_percent = 0.0
                basis = "none"
                sources: List[str] = []
                inputs = {"pm_price": price, "pm_yes_probability": p_true_pm, "fee_cushion": fee}
                source_attr: Dict[str, str] = {}
                calc_notes = None

                probs = sb_fair.get(ce_key)
                if probs:
                    p_true = max(probs.values()) if probs else None
                    if p_true is not None and 0.0 < p_true < 1.0:
                        ev_usd = p_true * (1.0 - price) - (1.0 - p_true) * price
                        ev_percent = (ev_usd / price) * 100.0 if price > 0 else 0.0
                        basis = "sportsbook_fair"
                        sources = ["odds_api"]
                        inputs["sb_fair_probs"] = probs
                        calc_notes = "EV computed using sportsbook fair probability against PM price"

                opps.append(
                    Opportunity(
                        id=f"polymarket:{m.market_id}",
                        source="polymarket",
                        title=m.question,
                        sport=league_code,
                        event_id=ev.event_id,
                        market_id=m.market_id,
                        canonical_event_key=ce_key,
                        yes_probability=p_true_pm,
                        price=price,
                        ev_usd_per_share=ev_usd,
                        ev_percent=ev_percent,
                        comparison_basis=basis,
                        comparison_sources=sources,
                        source_attribution=source_attr,
                        inputs=inputs,
                        calc_notes=calc_notes,
                        updated_at=now_iso,
                    )
                )
        opps.sort(key=lambda o: (o.ev_percent or -1e9), reverse=True)
        return opps


async def main_smoke() -> None:
    eng = OpportunityEngine()
    opps = await eng.fetch_opportunities()
    print(f"Opportunities: {len(opps)}")
    if opps:
        print(opps[0].model_dump())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main_smoke())
