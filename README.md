# Environmental Constraint Gate

> **Deterministic local rule evaluation for synthetic weather observations and in-memory electric-field measurements.**

This is an independent GlacierEQ portfolio repository. It is **not affiliated with, endorsed by, or connected to SpaceX** and has no access to proprietary SpaceX, range-safety, launch-weather, pad-sensor, or mission-control systems.

Evidence state: `LOCAL_ENVIRONMENTAL_RULE_GATE_NOT_LAUNCH_SAFETY_AUTHORITY`

## Verified repository-owned scope

The admitted surface is intentionally narrower than a real launch-weather system:

- a five-rule Python evaluator for wind, shear, lightning distance, cloud ceiling, and visibility;
- finite/non-negative observation validation that fails closed on malformed inputs;
- deterministic violation ordering and a bounded **margin score** that is not a probability or forecast confidence;
- an in-memory Go electric-field sensor registry using caller-supplied synthetic readings;
- maximum absolute field aggregation and a configurable local threshold check;
- a separate illustrative Go constraint evaluator for caller-supplied values;
- repository-owned Python and Go tests plus cold-start local operability.

The numeric thresholds in this repository are **illustrative portfolio fixtures**, not official Launch Commit Criteria, range rules, safety limits, or vehicle-specific constraints.

## Core implementation

| Path | Verified role |
|---|---|
| `src/weather_gate.py` | Validated synthetic observation rule engine |
| `src/electric_field_monitor.go` | In-memory field-reading aggregation and illustrative constraint evaluation |
| `tests/test_weather_gate.py` | Python rule/validation tests |
| `src/electric_field_monitor_test.go` | Go sensor/constraint tests |
| `tests/test_public_truth.py` | Public and machine truth-boundary tests |
| `scripts/verify_public_surface.py` | Fail-closed claim verifier |

## Evidence boundary

This repository does **not** claim:

- SpaceX affiliation, endorsement, employment, or proprietary access;
- official Launch Commit Criteria or range-safety rules;
- real pad sensors, field mills, lightning networks, radar, weather stations, or telemetry;
- real-time data acquisition, concurrent external sensor polling, or safety-critical availability;
- ensemble numerical-weather-prediction fusion, probabilistic forecasting, or launch-window optimization;
- live MCP, provider, APEX, AKOS, Mastermind, or agent-mesh runtime integration;
- production launch GO/NO-GO authority, certification, deployment, or operational safety suitability.

Any future claim above this ceiling requires new source, deterministic tests, exact-head receipts, and a new governance admission.

## Reproduce the admitted surface

```bash
bash scripts/ci/verify.sh
```

The gate compiles and tests the Python surface, tests/vets the Go surface, runs the local operability probe, and verifies the public/machine truth boundary.
