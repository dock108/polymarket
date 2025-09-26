from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class FairOdds:
    probability: float
    decimal_odds: float


def clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(value, max_value))


def american_to_decimal(american: int) -> float:
    if american == 0:
        raise ValueError("American odds cannot be 0")
    if american > 0:
        return 1.0 + (american / 100.0)
    return 1.0 + (100.0 / abs(american))


def decimal_to_american(decimal_odds: float) -> int:
    if decimal_odds <= 1.0:
        raise ValueError("Decimal odds must be > 1.0")
    if decimal_odds >= 2.0:
        return int(round((decimal_odds - 1.0) * 100))
    else:
        return int(round(-100.0 / (decimal_odds - 1.0)))


def implied_probability_from_decimal(decimal_odds: float) -> float:
    if decimal_odds <= 1.0:
        raise ValueError("Decimal odds must be > 1.0")
    return 1.0 / decimal_odds


def implied_probability_from_american(american: int) -> float:
    return 1.0 / american_to_decimal(american)


def remove_vig_two_outcomes(prob_a: float, prob_b: float) -> Tuple[float, float]:
    total = prob_a + prob_b
    if total <= 0:
        raise ValueError("Sum of implied probabilities must be > 0")
    return prob_a / total, prob_b / total


def fair_odds_from_prob(prob: float) -> FairOdds:
    p = clamp(prob)
    if p == 0.0:
        return FairOdds(probability=0.0, decimal_odds=float("inf"))
    return FairOdds(probability=p, decimal_odds=1.0 / p)


def expected_value_for_one_unit(true_prob: float, decimal_odds: float) -> float:
    p = clamp(true_prob)
    if decimal_odds <= 1.0:
        raise ValueError("Decimal odds must be > 1.0")
    payout = decimal_odds - 1.0
    return p * payout - (1.0 - p) * 1.0


def edge_percentage(p_true: float, p_market: float) -> float:
    p_m = max(1e-9, p_market)
    return (p_true - p_m) / p_m * 100.0


def apply_fee_to_probability(implied_prob: float, fee: float) -> float:
    return clamp(implied_prob * (1.0 - max(0.0, min(fee, 1.0))))
