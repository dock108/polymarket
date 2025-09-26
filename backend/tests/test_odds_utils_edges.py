import math
import pytest

from app.utils.odds import decimal_to_american, fair_odds_from_prob


def test_decimal_to_american_edges():
    with pytest.raises(ValueError):
        decimal_to_american(1.0)
    assert decimal_to_american(2.01) == pytest.approx(101)
    # negative odds branch
    assert decimal_to_american(1.25) == -400


def test_fair_odds_from_prob_zero_one():
    z = fair_odds_from_prob(0.0)
    assert z.probability == 0.0
    assert math.isinf(z.decimal_odds)
    o = fair_odds_from_prob(1.0)
    assert o.decimal_odds == 1.0
