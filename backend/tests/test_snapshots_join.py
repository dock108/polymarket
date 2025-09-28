import json
import pathlib
import pytest
import httpx

from app.services import polymarket as pm_mod
from app.services import odds_api as odds_mod
from app.services.opportunities import OpportunityEngine

SNAP = pathlib.Path(__file__).resolve().parents[2] / "data" / "snapshots"


@pytest.mark.asyncio
async def test_snapshot_join_ev(monkeypatch):
    pm_data = json.loads((SNAP / "pm_markets.json").read_text())
    sb_data = json.loads((SNAP / "sb_odds.json").read_text())

    async def fake_pm_get(client, path, params=None, **kwargs):  # type: ignore[no-redef]
        return httpx.Response(200, json=pm_data)

    async def fake_odds_get(self, path, params=None):  # type: ignore[no-redef]
        return sb_data

    async def fake_fetch_sports_map(self):  # type: ignore[no-redef]
        return {"tag1": "basketball_nba"}

    # Ensure ODDS_API_KEY is present for service init
    monkeypatch.setattr(odds_mod.settings, "odds_api_key", "x", raising=False)

    monkeypatch.setattr(pm_mod, "http_get_with_retry", fake_pm_get)
    monkeypatch.setattr(odds_mod.OddsAPIService, "_get", fake_odds_get)
    monkeypatch.setattr(pm_mod.PolymarketService, "fetch_sports_map", fake_fetch_sports_map)

    eng = OpportunityEngine()
    opps = await eng.fetch_opportunities()
    assert opps and any(o.comparison_basis == "sportsbook_fair" for o in opps)
