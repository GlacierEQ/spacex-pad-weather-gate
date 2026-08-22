from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_secret_bound_promotion_artifacts_are_retired() -> None:
    retired = (
        ROOT / "src" / "promotion_authority.py",
        ROOT / "machine" / "promotion_authority.json",
        ROOT / "tests" / "test_promotion_authority.py",
        ROOT / "scripts" / "verify_promotion_grant.py",
    )
    assert all(not path.exists() for path in retired)


def test_local_environmental_rule_evidence_remains_keyless() -> None:
    proof = json.loads((ROOT / "machine" / "proof_receipt.json").read_text())
    state = json.loads((ROOT / "machine" / "excellence-state.json").read_text())

    assert proof["repository"] == "GlacierEQ/spacex-pad-weather-gate"
    assert proof["source_sha"]
    assert state["promotion_authority"]["status"] == "RETIRED_KEYLESS"
    assert "no production launch authority, deployment, certification, or safety suitability" in state["nonclaims"]
