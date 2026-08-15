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


def load(path: str) -> dict:
    return json.loads(read(path))


def test_public_surface_is_non_affiliated_and_non_authoritative() -> None:
    readme = read("README.md")
    assert TOKEN in readme
    assert "not affiliated with, endorsed by, or connected to SpaceX" in readme
    assert "illustrative portfolio fixtures" in readme
    assert "official Launch Commit Criteria" in readme
    assert "ensemble numerical-weather-prediction fusion" in readme
    assert "Fully connected to APEX Highway mesh" not in readme
    assert "weather_check()" not in readme


def test_machine_projection_matches_evidence_without_erasing_target() -> None:
    capabilities = load("machine/capabilities.json")
    target = load("machine/target-contract.json")
    planes = load("machine/capability-planes.json")
    excellence = load("machine/excellence-state.json")

    assert "hyper-scaling" not in capabilities["capabilities"]
    assert capabilities["evidence_token"] == TOKEN

    evidence = target["evidence_checkpoint"]
    assert evidence["evidence_token"] == TOKEN
    assert evidence["verified_capability"] == (
        "deterministic-local-environmental-constraint-evaluation"
    )
    assert evidence["canonical_proof_head"] == (
        "7f8ca0a9d4e346b7350b30e2a9263a10b3baae26"
    )
    assert target["implementation_checkpoint"]["deployed"] is False
    assert target["target_architecture"]["status"] == (
        "PRESERVED_UNVERIFIED_TARGET_ARCHITECTURE"
    )
    assert len(target["target_architecture"]["objectives"]) >= 6

    assert planes["projection"]["projection_may_overwrite_canonical_or_target"] is False
    assert planes["target"]["status"] == "PRESERVED_UNVERIFIED_TARGET_ARCHITECTURE"
    target_states = {item["state"] for item in planes["target"]["items"]}
    assert "UNVERIFIED_TARGET" in target_states
    assert "PARTIALLY_IMPLEMENTED_TARGET" in target_states

    assert excellence["product_state"] == "FUNCTIONAL_LOCAL_ENVIRONMENTAL_RULE_ENGINE"
    assert excellence["evidence_state"] == "EXACT_HEAD_VERIFIED"
    assert excellence["projection_state"] == TOKEN
    assert excellence["target_state"] == "PRESERVED_UNVERIFIED_TARGET_ARCHITECTURE"
    assert excellence["evidence_checkpoint"]["head_sha"] == (
        "7f8ca0a9d4e346b7350b30e2a9263a10b3baae26"
    )
    assert "HYPER_VALIDATED" not in json.dumps(excellence, sort_keys=True)


def test_historical_weather_ambition_survives_only_as_target_state() -> None:
    readme = read("README.md")
    planes = load("machine/capability-planes.json")
    targets = {item["capability"]: item for item in planes["target"]["items"]}

    assert "probabilistic environmental forecasting with ensemble-model integration" in targets
    assert targets[
        "probabilistic environmental forecasting with ensemble-model integration"
    ]["state"] == "UNVERIFIED_TARGET"
    assert "time-window optimization for favorable operating conditions" in targets
    assert targets[
        "time-window optimization for favorable operating conditions"
    ]["state"] == "UNVERIFIED_TARGET"
    assert "programmatic environmental-status query service" in targets
    assert "environmental-event publication into a governed orchestration mesh" in targets

    assert "weather_check()" not in readme
    assert "probabilistic forecasting with ensemble weather model integration" not in readme
    assert "finding the best launch opportunity" not in readme


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
