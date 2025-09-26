from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

import httpx


async def http_get_with_retry(
    client: httpx.AsyncClient,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    *,
    retries: int = 3,
    backoff_base: float = 0.5,
) -> httpx.Response:
    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            resp = await client.get(path, params=params)
            # Retry on 5xx; return otherwise (including 4xx) so caller can handle
            if 500 <= resp.status_code < 600:
                if attempt == retries - 1:
                    return resp
                await asyncio.sleep(backoff_base * (2 ** attempt))
                continue
            return resp
        except Exception as exc:  # network/transport errors
            last_exc = exc
            if attempt == retries - 1:
                raise
            await asyncio.sleep(backoff_base * (2 ** attempt))
    assert last_exc is not None
    raise last_exc
