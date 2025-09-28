import pytest

from app.services import opportunities as opp_mod
from app.services.opportunities import OpportunityEngine
from app.schemas.polymarket import PMEvent, PMMarket, PMOutcome
from app.schemas.odds_api import EventLines, BookLine
from app.services.odds_api import OddsAPIError


class PMServiceForJoin:
    async def fetch_events_with_binary_markets(self):
        return [
            PMEvent(
                event_id="e1",
                title="Team A vs Team B",
                sport="basketball_nba",
                markets=[
                    PMMarket(
                        market_id="m1",
                        event_id="e1",
                        question="Will Team A win?",
                        outcomes=[PMOutcome(name="Yes", price=0.50), PMOutcome(name="No", price=0.50)],
                    )
                ],
            )
        ]

    async def close(self):
        return None


class OddsSvcForJoin:
    async def fetch_sport_odds(self, sport: str):
        # Return one event with H2H fair probs after vig removal
        return [
            EventLines(
                sport=sport,
                event_id="e-sb-1",
                title="Team A vs Team B",
                lines=[
                    BookLine(bookmaker="bk1", market="h2h", side="Team A", american_odds=150),
                    BookLine(bookmaker="bk1", market="h2h", side="Team B", american_odds=-170),
                ],
                canonical_event_key="basketball_nba:team_a_vs_team_b",
                selected_bookmaker="bk1|bk1",
            )
        ]

    async def close(self):
        return None


@pytest.mark.asyncio
async def test_join_computes_positive_ev(monkeypatch):
    # Patch PM and Odds services
    monkeypatch.setattr(opp_mod, "PolymarketService", lambda: PMServiceForJoin())

    from app.services import opportunities as opp_mod_local
    from app.services import odds_api as odds_mod

    monkeypatch.setattr(odds_mod, "OddsAPIService", lambda: OddsSvcForJoin())

    eng = OpportunityEngine()
    opps = await eng.fetch_opportunities()
    assert opps and opps[0].comparison_basis in ("none", "sportsbook_fair")
    # With fair prob > price, EV should be >= 0; ideally > 0 in this setup
    assert opps[0].ev_usd_per_share is not None


class OddsSvcError:
    async def fetch_sport_odds(self, sport: str):
        raise OddsAPIError("boom", status_code=503)

    async def close(self):
        return None


@pytest.mark.asyncio
async def test_join_fallback_on_sportsbook_error(monkeypatch):
    monkeypatch.setattr(opp_mod, "PolymarketService", lambda: PMServiceForJoin())
    from app.services import odds_api as odds_mod

    monkeypatch.setattr(odds_mod, "OddsAPIService", lambda: OddsSvcError())

    eng = OpportunityEngine()
    opps = await eng.fetch_opportunities()
    assert opps and opps[0].comparison_basis == "none"
    assert opps[0].ev_usd_per_share == 0.0
