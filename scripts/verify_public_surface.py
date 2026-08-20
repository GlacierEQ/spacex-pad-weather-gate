from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = "LOCAL_ENVIRONMENTAL_RULE_GATE_NOT_LAUNCH_SAFETY_AUTHORITY"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    readme = read("README.md")
    python_source = read("src/weather_gate.py")
    go_source = read("src/electric_field_monitor.go")
    capabilities = json.loads(read("machine/capabilities.json"))
    target = json.loads(read("machine/target-contract.json"))
    planes = json.loads(read("machine/capability-planes.json"))
    excellence = json.loads(read("machine/excellence-state.json"))

    assert TOKEN in readme
    assert TOKEN in python_source
    assert TOKEN in go_source
    assert capabilities["evidence_token"] == TOKEN
    assert "not affiliated with, endorsed by, or connected to SpaceX" in readme
    assert "illustrative portfolio fixtures" in readme
    assert "official Launch Commit Criteria" in readme
    assert "Fully connected to APEX Highway mesh" not in readme
    assert "weather_check()" not in readme
    assert "EvaluateLCC" not in go_source
    assert "IsTriggeredLightningRisk" not in go_source
    assert "hyper-scaling" not in capabilities["capabilities"]

    evidence = target["evidence_checkpoint"]
    assert evidence["evidence_token"] == TOKEN
    assert evidence["verified_capability"] == "deterministic-local-environmental-constraint-evaluation"
    assert evidence["verified_checkpoint_head"] == "7f8ca0a9d4e346b7350b30e2a9263a10b3baae26"
    assert target["implementation_checkpoint"]["deployed"] is False
    assert target["target_architecture"]["status"] == "ACTIVE_FRONTIER"
    assert target["apex"]["selection_mode"] == "CURRENT_BEST_REVISABLE"
    assert len(target["target_architecture"]["objectives"]) >= 6

    assert planes["schema"] == "glaciereq.repository-capability-evolution.v2"
    assert planes["apex"]["selection_mode"] == "CURRENT_BEST_REVISABLE"
    assert planes["apex"]["capability_donor_preservation"] is True
    assert planes["selection"]["challengeable"] is True
    assert len(planes["selection"]["capabilities"]) >= 3
    assert len(planes["capability_donors"]) >= 2
    assert planes["projection"]["projection_may_overwrite_intent_or_target"] is False
    assert planes["target"]["status"] == "ACTIVE_FRONTIER"
    assert len(planes["target"]["items"]) >= 6

    target_names = {item["capability"] for item in planes["target"]["items"]}
    assert "probabilistic environmental forecasting with ensemble-model integration" in target_names
    assert "time-window optimization for favorable operating conditions" in target_names
    assert "programmatic environmental-status query service" in target_names

    assert excellence["schema"] == "glaciereq.repo-excellence-state.v3"
    assert excellence["product_state"] == "FUNCTIONAL_LOCAL_ENVIRONMENTAL_RULE_ENGINE"
    assert excellence["evidence_state"] == "EXACT_HEAD_VERIFIED"
    assert excellence["projection_state"] == TOKEN
    assert excellence["target_state"] == "ACTIVE_FRONTIER"
    assert excellence["selection_state"] == "CURRENT_BEST_REVISABLE"
    assert excellence["selection_challengeable"] is True
    assert excellence["capability_donor_preservation"] is True
    assert excellence["evidence_checkpoint"]["head_sha"] == "7f8ca0a9d4e346b7350b30e2a9263a10b3baae26"
    assert "HYPER_VALIDATED" not in json.dumps(excellence, sort_keys=True)

    print(TOKEN)


if __name__ == "__main__":
    main()
