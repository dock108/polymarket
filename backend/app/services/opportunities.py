from __future__ import annotations

from typing import List
from datetime import datetime, timezone

from app.schemas.opportunity import Opportunity
from app.services.polymarket import PolymarketService
from app.core.config import settings


class OpportunityEngine:
    async def fetch_opportunities(self) -> List[Opportunity]:
        # v1: Polymarket-only opportunities (binary)
        svc = PolymarketService()
        try:
            events = await svc.fetch_events_with_binary_markets()
        finally:
            await svc.close()

        now_iso = datetime.now(timezone.utc).isoformat()
        opps: List[Opportunity] = []
        for ev in events:
            for m in ev.markets:
                yes = next((o for o in m.outcomes if o.name.lower() == "yes"), None)
                no = next((o for o in m.outcomes if o.name.lower() == "no"), None)
                if not yes or not no:
                    continue
                # Fee-adjusted true probability comes from normalized outcome price
                p_true = yes.price
                # Reconstruct raw (pre-fee) market price from fee-adjusted probability
                fee = max(0.0, min(settings.fee_cushion, 1.0))
                denom = (1.0 - fee) if (1.0 - fee) > 0 else 1.0
                raw_price = max(0.0, min(1.0, p_true / denom))

                price = raw_price
                if price <= 0 or p_true < 0 or p_true > 1:
                    continue
                # Baseline policy: Polymarket-only -> EV = 0, annotate basis
                ev_usd = 0.0
                ev_percent = 0.0
                opps.append(
                    Opportunity(
                        id=f"polymarket:{m.market_id}",
                        source="polymarket",
                        title=m.question,
                        sport=ev.sport,
                        event_id=ev.event_id,
                        market_id=m.market_id,
                        yes_probability=p_true,
                        price=price,
                        ev_usd_per_share=ev_usd,
                        ev_percent=ev_percent,
                        comparison_basis="none",
                        comparison_sources=[],
                        updated_at=now_iso,
                    )
                )
        # Sort by EV% desc
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
