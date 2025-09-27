import pytest
import httpx

from app.services import odds_api as odds_mod
from app.services.odds_api import OddsAPIService


@pytest.mark.asyncio
async def test_h2h_fair_annotation(monkeypatch):
    # Two sides +150 and -170 -> implied p1 and p2, then vig removal
    payload = [
        {
            "id": "e1",
            "home_team": "X",
            "bookmakers": [
                {
                    "key": "bk",
                    "markets": [
                        {
                            "key": "h2h",
                            "outcomes": [
                                {"name": "A", "price": 150},
                                {"name": "B", "price": -170},
                            ],
                        }
                    ],
                }
            ],
        }
    ]

    async def fake_get(self, path, params=None):  # type: ignore[no-redef]
        return payload

    monkeypatch.setattr(odds_mod.OddsAPIService, "_get", fake_get)

    svc = OddsAPIService(base_url="https://mock", api_key="x")
    try:
        events = await svc.fetch_sport_odds("basketball_nba")
    finally:
        await svc.close()

    assert events and events[0].lines
    fair = [
        l
        for l in events[0].lines
        if l.market == "h2h" and l.fair_probability is not None
    ]
    assert len(fair) == 2
    assert 0.0 < fair[0].fair_probability < 1.0
