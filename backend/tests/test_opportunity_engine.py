import pytest

from app.services.opportunities import OpportunityEngine
from app.schemas.polymarket import PMEvent, PMMarket, PMOutcome


class FakePMService:
    async def fetch_events_with_binary_markets(self):
        return [
            PMEvent(
                event_id="e1",
                title="A",
                sport=None,
                markets=[
                    PMMarket(
                        market_id="m1",
                        event_id="e1",
                        question="Q1",
                        outcomes=[
                            PMOutcome(name="Yes", price=0.60),  # fee-adjusted true prob
                            PMOutcome(name="No", price=0.40),
                        ],
                    )
                ],
            ),
            PMEvent(
                event_id="e2",
                title="B",
                sport=None,
                markets=[
                    PMMarket(
                        market_id="m2",
                        event_id="e2",
                        question="Q2",
                        outcomes=[
                            PMOutcome(name="Yes", price=0.30),
                            PMOutcome(name="No", price=0.70),
                        ],
                    )
                ],
            ),
        ]

    async def close(self):
        return None


@pytest.mark.asyncio
async def test_opportunity_engine_sorts_by_ev(monkeypatch):
    from app.services import opportunities as opp_mod

    # Monkeypatch the service constructor to our fake
    monkeypatch.setattr(opp_mod, "PolymarketService", lambda *a, **k: FakePMService())

    eng = OpportunityEngine()
    opps = await eng.fetch_opportunities()
    assert len(opps) == 2
    # Ensure sorted by EV desc
    assert (opps[0].ev_percent or 0) >= (opps[1].ev_percent or 0)


@pytest.mark.asyncio
async def test_baseline_ev_is_zero_and_basis_none(monkeypatch):
    from app.services import opportunities as opp_mod

    monkeypatch.setattr(opp_mod, "PolymarketService", lambda *a, **k: FakePMService())

    eng = OpportunityEngine()
    opps = await eng.fetch_opportunities()
    assert len(opps) == 2
    for o in opps:
        assert o.ev_usd_per_share == 0.0
        assert o.ev_percent == 0.0
        assert o.comparison_basis == "none"
        assert isinstance(o.comparison_sources, list)
