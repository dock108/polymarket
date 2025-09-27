from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.api.routes import odds as odds_route_mod
from app.api.routes import opportunities as opp_route_mod
from app.schemas.odds_api import EventLines, BookLine
from app.schemas.opportunity import Opportunity
from app.services.odds_api import OddsAPIError


client = TestClient(app)


def test_golf_route_returns_empty():
    r = client.get("/api/golf")
    assert r.status_code == 200
    assert r.json() == []


def test_opportunities_route_ok(monkeypatch):
    class FakeEngine:
        async def fetch_opportunities(self):
            return [
                Opportunity(
                    id="polymarket:x",
                    source="polymarket",
                    title="t",
                    ev_usd_per_share=0.1,
                )
            ]

    monkeypatch.setattr(opp_route_mod, "OpportunityEngine", lambda: FakeEngine())
    r = client.get("/api/opportunities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and len(data) == 1
    # is_stale should be present (additive field)
    assert "is_stale" in data[0]


def test_opportunities_meta_route_ok(monkeypatch):
    class FakeEngine:
        async def fetch_opportunities(self):
            return [
                Opportunity(
                    id="polymarket:y",
                    source="polymarket",
                    title="t2",
                    ev_usd_per_share=0.0,
                )
            ]

    monkeypatch.setattr(opp_route_mod, "OpportunityEngine", lambda: FakeEngine())
    r = client.get("/api/opportunities/meta")
    assert r.status_code == 200
    payload = r.json()
    assert set(payload.keys()) >= {"as_of", "staleness_seconds", "items"}
    assert isinstance(payload["items"], list) and len(payload["items"]) == 1
    assert "is_stale" in payload["items"][0]


def test_odds_route_404_propagates(monkeypatch):
    class FakeOddsSvc:
        async def fetch_sport_odds(self, sport: str):
            raise OddsAPIError("not found", status_code=404)

        async def close(self):
            return None

    monkeypatch.setattr(odds_route_mod, "OddsAPIService", lambda: FakeOddsSvc())
    r = client.get("/api/odds/bad_sport")
    assert r.status_code == 404


def test_odds_route_ok(monkeypatch):
    class FakeOddsSvc:
        async def fetch_sport_odds(self, sport: str):
            return [
                EventLines(
                    sport=sport,
                    event_id="e",
                    title="t",
                    lines=[
                        BookLine(
                            bookmaker="a", market="h2h", side="b", american_odds=100
                        )
                    ],
                )
            ]

        async def close(self):
            return None

    monkeypatch.setattr(odds_route_mod, "OddsAPIService", lambda: FakeOddsSvc())
    r = client.get("/api/odds/sport_x")
    assert r.status_code == 200
    payload = r.json()
    assert isinstance(payload, list) and payload and payload[0]["sport"] == "sport_x"
