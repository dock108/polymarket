import asyncio
import math
import pytest

from app.services.opportunities import OpportunityEngine


@pytest.mark.asyncio
async def test_first_nonzero_and_positive_ev(capsys):
    eng = OpportunityEngine()
    opps = await eng.fetch_opportunities()

    first_nonzero = next(
        (
            o
            for o in opps
            if o.ev_usd_per_share is not None
            and not math.isclose(o.ev_usd_per_share, 0.0, abs_tol=1e-9)
        ),
        None,
    )
    first_positive = next((o for o in opps if (o.ev_usd_per_share or 0.0) > 0.0), None)

    print("First non-zero EV:", first_nonzero.model_dump() if first_nonzero else None)
    print("First positive EV:", first_positive.model_dump() if first_positive else None)

    # Ensure shape
    assert isinstance(opps, list)
    if opps:
        assert opps[0].canonical_event_key is not None
