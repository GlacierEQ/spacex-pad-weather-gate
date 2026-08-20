#!/usr/bin/env python3
"""Execute the selected local environmental-rule capability and emit a receipt."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from weather_gate import EVIDENCE_STATE, Weather, evaluate  # noqa: E402


def _stable(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def build_receipt() -> dict:
    pass_case = evaluate(Weather(18.0, 8.0, 25.0, 8000.0, 10.0))
    block_case = evaluate(Weather(40.0, 5.0, 5.0, 2000.0, 3.0))
    body = {
        "schema": "glaciereq.weather-operate-receipt.v1",
        "selection_mode": "CURRENT_BEST_REVISABLE",
        "capability": "deterministic-local-environmental-constraint-evaluation",
        "evidence_state": EVIDENCE_STATE,
        "pass_case": pass_case,
        "block_case": block_case,
        "external_actions_executed": 0,
    }
    return {**body, "receipt_sha256": hashlib.sha256(_stable(body)).hexdigest()}


def main() -> int:
    receipt = build_receipt()
    print(json.dumps(receipt, indent=2, sort_keys=True))
    valid = (
        receipt["evidence_state"] == EVIDENCE_STATE
        and receipt["selection_mode"] == "CURRENT_BEST_REVISABLE"
        and receipt["pass_case"]["decision"] == "PASS"
        and receipt["pass_case"]["violations"] == []
        and receipt["block_case"]["decision"] == "BLOCK"
        and {"wind", "lightning", "ceiling", "visibility"} <= set(receipt["block_case"]["violations"])
        and receipt["external_actions_executed"] == 0
        and len(receipt["receipt_sha256"]) == 64
    )
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
