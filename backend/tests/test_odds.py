import math
import pytest

from app.utils.odds import (
    american_to_decimal,
    decimal_to_american,
    implied_probability_from_decimal,
    implied_probability_from_american,
    remove_vig_two_outcomes,
    fair_odds_from_prob,
    expected_value_for_one_unit,
    edge_percentage,
    apply_fee_to_probability,
)


def test_american_decimal_roundtrip():
    assert american_to_decimal(+150) == pytest.approx(2.5)
    assert american_to_decimal(-200) == pytest.approx(1.5)
    assert decimal_to_american(2.5) == 150
    assert decimal_to_american(1.5) == -200


def test_implied_probability():
    assert implied_probability_from_decimal(2.0) == 0.5
    assert implied_probability_from_american(+100) == pytest.approx(0.5)


def test_remove_vig_two_outcomes():
    p1, p2 = remove_vig_two_outcomes(0.60, 0.50)
    assert p1 + p2 == pytest.approx(1.0)
    assert p1 == pytest.approx(0.5454545, rel=1e-6)


def test_fair_odds_from_prob():
    fo = fair_odds_from_prob(0.25)
    assert fo.probability == 0.25
    assert fo.decimal_odds == pytest.approx(4.0)


def test_expected_value_for_one_unit():
    # true 60%, odds 1.8 => payout .8 => EV = .6*.8 - .4*1 = .48 - .4 = .08
    ev = expected_value_for_one_unit(0.6, 1.8)
    assert ev == pytest.approx(0.08, abs=1e-6)


def test_edge_percentage():
    edge = edge_percentage(0.55, 0.50)
    assert edge == pytest.approx(10.0)


def test_apply_fee_to_probability():
    assert apply_fee_to_probability(0.5, 0.025) == pytest.approx(0.4875)
    assert apply_fee_to_probability(1.0, 0.10) == pytest.approx(0.9)


def test_error_conditions():
    with pytest.raises(ValueError):
        american_to_decimal(0)
    with pytest.raises(ValueError):
        decimal_to_american(1.0)
    with pytest.raises(ValueError):
        implied_probability_from_decimal(1.0)
    with pytest.raises(ValueError):
        remove_vig_two_outcomes(0.0, 0.0)
