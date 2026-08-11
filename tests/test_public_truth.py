from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from weather_gate import EVIDENCE_STATE, LIMITS, Weather, evaluate

TOKEN = "LOCAL_ENVIRONMENTAL_RULE_GATE_NOT_LAUNCH_SAFETY_AUTHORITY"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_public_surface_is_non_affiliated_and_non_authoritative() -> None:
    readme = read("README.md")
    assert TOKEN in readme
    assert "not affiliated with, endorsed by, or connected to SpaceX" in readme
    assert "illustrative portfolio fixtures" in readme
    assert "official Launch Commit Criteria" in readme
    assert "ensemble numerical-weather-prediction fusion" in readme
    assert "Fully connected to APEX Highway mesh" not in readme
    assert "weather_check()" not in readme


def test_machine_truth_matches_current_scope() -> None:
    capabilities = json.loads(read("machine/capabilities.json"))
    target = json.loads(read("machine/target-contract.json"))
    excellence = json.loads(read("machine/excellence-state.json"))
    assert "hyper-scaling" not in capabilities["capabilities"]
    assert capabilities["evidence_token"] == TOKEN
    assert target["evidence_token"] == TOKEN
    assert target["verified_capability"] == (
        "deterministic-local-environmental-constraint-evaluation"
    )
    assert target["current"]["deployed"] is False
    assert excellence["principal_state"] == "TESTED"
    assert excellence["evidence_token"] == TOKEN
    assert "HYPER_VALIDATED" not in json.dumps(excellence, sort_keys=True)


def test_margin_score_is_bounded_fixture_metric_not_probability() -> None:
    result = evaluate(
        Weather(
            wind_knots=LIMITS["wind_knots_max"] * 0.5,
            shear_knots=LIMITS["shear_knots_max"] * 0.5,
            lightning_nm=LIMITS["lightning_nm_min"] * 2,
            ceiling_ft=LIMITS["ceiling_ft_min"] * 2,
            visibility_sm=LIMITS["visibility_sm_min"] * 2,
        )
    )
    assert result["decision"] == "PASS"
    assert 0 <= result["margin_score"] <= 1
    assert "confidence" not in result
    assert result["evidence_state"] == EVIDENCE_STATE


def test_go_source_has_no_real_time_polling_claim() -> None:
    source = read("src/electric_field_monitor.go")
    assert TOKEN in source
    assert "caller-supplied synthetic" in source
    assert "EvaluateLCC" not in source
    assert "IsTriggeredLightningRisk" not in source
