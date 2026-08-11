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
    excellence = json.loads(read("machine/excellence-state.json"))

    assert TOKEN in readme
    assert TOKEN in python_source
    assert TOKEN in go_source
    assert capabilities["evidence_token"] == TOKEN
    assert target["evidence_token"] == TOKEN
    assert excellence["evidence_token"] == TOKEN
    assert "not affiliated with, endorsed by, or connected to SpaceX" in readme
    assert "illustrative portfolio fixtures" in readme
    assert "official Launch Commit Criteria" in readme
    assert "Fully connected to APEX Highway mesh" not in readme
    assert "weather_check()" not in readme
    assert "EvaluateLCC" not in go_source
    assert "IsTriggeredLightningRisk" not in go_source
    assert "hyper-scaling" not in capabilities["capabilities"]
    assert target["current"]["deployed"] is False
    assert target["verified_capability"] == (
        "deterministic-local-environmental-constraint-evaluation"
    )
    assert excellence["principal_state"] == "TESTED"
    assert "HYPER_VALIDATED" not in json.dumps(excellence, sort_keys=True)

    print(TOKEN)


if __name__ == "__main__":
    main()
