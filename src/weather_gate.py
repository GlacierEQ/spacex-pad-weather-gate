#!/usr/bin/env python3
"""Repository-local environmental constraint evaluator.

The thresholds are illustrative portfolio fixtures. This module is not an
implementation of SpaceX Launch Commit Criteria or launch-safety authority.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

EVIDENCE_STATE = "LOCAL_ENVIRONMENTAL_RULE_GATE_NOT_LAUNCH_SAFETY_AUTHORITY"
MARGIN_FLOOR = 0.0


@dataclass(frozen=True)
class Weather:
    wind_knots: float
    shear_knots: float
    lightning_nm: float
    ceiling_ft: float
    visibility_sm: float


LIMITS = {
    "wind_knots_max": 30.0,
    "shear_knots_max": 15.0,
    "lightning_nm_min": 10.0,
    "ceiling_ft_min": 3000.0,
    "visibility_sm_min": 5.0,
}


def _validated(w: Weather) -> Weather:
    values = {
        "wind_knots": w.wind_knots,
        "shear_knots": w.shear_knots,
        "lightning_nm": w.lightning_nm,
        "ceiling_ft": w.ceiling_ft,
        "visibility_sm": w.visibility_sm,
    }
    for name, value in values.items():
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be finite and non-negative")
    return w


def evaluate(w: Weather) -> dict:
    """Evaluate synthetic observations against illustrative local constraints."""
    w = _validated(w)
    violations: list[str] = []
    if w.wind_knots > LIMITS["wind_knots_max"]:
        violations.append("wind")
    if w.shear_knots > LIMITS["shear_knots_max"]:
        violations.append("shear")
    if w.lightning_nm < LIMITS["lightning_nm_min"]:
        violations.append("lightning")
    if w.ceiling_ft < LIMITS["ceiling_ft_min"]:
        violations.append("ceiling")
    if w.visibility_sm < LIMITS["visibility_sm_min"]:
        violations.append("visibility")

    margins = [
        (LIMITS["wind_knots_max"] - w.wind_knots) / LIMITS["wind_knots_max"],
        (LIMITS["shear_knots_max"] - w.shear_knots) / LIMITS["shear_knots_max"],
        (w.lightning_nm - LIMITS["lightning_nm_min"]) / LIMITS["lightning_nm_min"],
        (w.ceiling_ft - LIMITS["ceiling_ft_min"]) / LIMITS["ceiling_ft_min"],
        (w.visibility_sm - LIMITS["visibility_sm_min"]) / LIMITS["visibility_sm_min"],
    ]
    margin_score = max(MARGIN_FLOOR, min(1.0, min(margins)))
    return {
        "decision": "PASS" if not violations else "BLOCK",
        "violations": violations,
        "margin_score": round(margin_score, 4),
        "evidence_state": EVIDENCE_STATE,
    }


if __name__ == "__main__":
    print(evaluate(Weather(18, 8, 25, 8000, 10)))
    print(evaluate(Weather(40, 5, 5, 2000, 3)))
