import json
import pytest
import httpx

from app.services import polymarket as pm_mod
from app.services.polymarket import PolymarketService


@pytest.mark.asyncio
async def test_polymarket_normalizes_binary_markets(monkeypatch):
    # Mock /markets to return two markets, one valid binary, one invalid (3 outcomes)
    markets_payload = [
        {
            "id": "m1",
            "question": "Will Team A win?",
            "closed": False,
            "events": [{"id": "e1", "title": "Match A"}],
            "outcomes": [
                {"name": "Yes", "price": 0.6},
                {"name": "No", "price": 0.4},
            ],
        },
        {
            "id": "m2",
            "question": "Too many outcomes?",
            "closed": False,
            "events": [{"id": "e2", "title": "Match B"}],
            "outcomes": [
                {"name": "A", "price": 0.4},
                {"name": "B", "price": 0.3},
                {"name": "C", "price": 0.3},
            ],
        },
    ]

    async def fake_get(client, path, params=None, **kwargs):  # type: ignore[no-redef]
        # Return the markets payload regardless of path
        return httpx.Response(200, json=markets_payload)

    monkeypatch.setattr(pm_mod, "http_get_with_retry", fake_get)

    svc = PolymarketService(base_url="https://mock")
    try:
        events = await svc.fetch_events_with_binary_markets()
    finally:
        await svc.close()

    # We should have one event with one normalized market
    assert any(e.event_id == "e1" for e in events)
    e1 = next(e for e in events if e.event_id == "e1")
    assert len(e1.markets) == 1
    m = e1.markets[0]
    names = [o.name for o in m.outcomes]
    assert "Yes" in names and "No" in names


@pytest.mark.asyncio
async def test_polymarket_filters_closed_and_past(monkeypatch):
    # Closed market and past endDate should be filtered out
    markets_payload = [
        {
            "id": "m3",
            "question": "Closed market",
            "closed": True,
            "events": [{"id": "e3", "title": "Past"}],
            "outcomes": [
                {"name": "Yes", "price": 0.5},
                {"name": "No", "price": 0.5},
            ],
        },
        {
            "id": "m4",
            "question": "Past end",
            "closed": False,
            "endDate": "2020-01-01T00:00:00Z",
            "events": [{"id": "e4", "title": "Old"}],
            "outcomes": [
                {"name": "Yes", "price": 0.5},
                {"name": "No", "price": 0.5},
            ],
        },
    ]

    async def fake_get(client, path, params=None, **kwargs):  # type: ignore[no-redef]
        return httpx.Response(200, json=markets_payload)

    monkeypatch.setattr(pm_mod, "http_get_with_retry", fake_get)

    svc = PolymarketService(base_url="https://mock")
    try:
        events = await svc.fetch_events_with_binary_markets()
    finally:
        await svc.close()

    # Should filter out all, leaving no events
    assert len(events) == 0
