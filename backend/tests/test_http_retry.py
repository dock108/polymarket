import asyncio
import httpx
import pytest

from app.services._http import http_get_with_retry


@pytest.mark.asyncio
async def test_http_get_returns_4xx_without_retry():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(404, json={"error": "not found"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(
        transport=transport, base_url="https://example.com"
    ) as client:
        resp = await http_get_with_retry(client, "/x")
        assert resp.status_code == 404
        assert calls["n"] == 1


@pytest.mark.asyncio
async def test_http_get_retries_on_5xx_then_succeeds():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(502, json={"error": "bad gateway"})
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(
        transport=transport, base_url="https://example.com"
    ) as client:
        resp = await http_get_with_retry(client, "/x", retries=3, backoff_base=0.0)
        assert resp.status_code == 200
        assert calls["n"] == 3
