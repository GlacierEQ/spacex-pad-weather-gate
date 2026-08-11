from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from weather_gate import EVIDENCE_STATE, Weather, evaluate


def test_pass_fixture() -> None:
    result = evaluate(Weather(10, 5, 30, 10000, 10))
    assert result["decision"] == "PASS"
    assert result["violations"] == []
    assert 0 <= result["margin_score"] <= 1
    assert result["evidence_state"] == EVIDENCE_STATE


def test_lightning_fixture_blocks() -> None:
    result = evaluate(Weather(10, 5, 2, 10000, 10))
    assert result["decision"] == "BLOCK"
    assert "lightning" in result["violations"]
    assert result["margin_score"] == 0


def test_violation_order_is_deterministic() -> None:
    result = evaluate(Weather(40, 20, 2, 1000, 2))
    assert result["violations"] == [
        "wind",
        "shear",
        "lightning",
        "ceiling",
        "visibility",
    ]


@pytest.mark.parametrize(
    "weather",
    [
        Weather(-1, 5, 30, 10000, 10),
        Weather(10, -1, 30, 10000, 10),
        Weather(10, 5, -1, 10000, 10),
        Weather(10, 5, 30, -1, 10),
        Weather(10, 5, 30, 10000, -1),
        Weather(math.nan, 5, 30, 10000, 10),
        Weather(10, math.inf, 30, 10000, 10),
    ],
)
def test_invalid_observations_fail_closed(weather: Weather) -> None:
    with pytest.raises(ValueError):
        evaluate(weather)
