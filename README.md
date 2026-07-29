# SpaceX Pad Weather Gate — Launch Commit Criteria Meteorological Engine ⛈️

> **Automated weather assessment against Launch Commit Criteria (LCC) with go/no-go meteorological gating.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue)]()
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8)]()
[![Domain](https://img.shields.io/badge/Domain-Launch%20Weather-red)]()

---

## 🎯 For Recruiters & Hiring Managers

This repository implements a **weather gate decision engine** — the system that evaluates real-time meteorological data against formal Launch Commit Criteria to determine if conditions are safe for launch. It demonstrates:

- **Rule engine** evaluating 11+ weather criteria simultaneously (wind, lightning, cloud ceiling, precipitation, etc.)
- **Triggered Lightning Rule**: Range safety constraint preventing launch through charged clouds
- **Probabilistic forecasting** with ensemble weather model integration
- **Time-window optimization** finding the best launch opportunity within a window

**Why this matters**: Weather gating is a **real-time decision engine with formal safety constraints** — identical in structure to compliance engines, risk management platforms, and automated trading circuit breakers.

---

## 🔬 For Engineers & Technical Reviewers

### Launch Commit Criteria (LCC)

| Rule | Threshold | Constraint |
|---|---|---|
| Surface winds | ≤30 kt sustained | Structural loads |
| Upper-level winds | ≤140 kt | Max-Q shear |
| Lightning (0-10 nmi) | 0 strikes / 30 min | Triggered lightning |
| Cumulus cloud | No Cb within 10 nmi | Field mill criteria |
| Temperature | ≥40°F | O-ring / seal integrity |
| Precipitation | None at pad | Ice formation |
| Visibility | ≥4 statute miles | Range tracking |

### Core Components

| Component | Language | Purpose |
|---|---|---|
| `src/weather_gate.py` | Python | LCC rule engine, criteria evaluation, window optimization |
| `src/field_mill.go` | Go | Real-time electric field monitoring with concurrent sensor polling |
| `tests/` | Python | Historical weather scenario replay for rule validation |

---

## 🤖 ML/AI & Programmatic Mesh Integration

- **MCP Tool**: `weather_check()` — LCC status queryable by launch sequencer agents
- **Mastermind Sidecar**: Publishes weather violations to APEX Highway mesh
- **AI Extension**: Ensemble NWP model fusion for probabilistic launch window prediction

```python
gate = await mcp_client.call_tool("pad-weather-gate", "evaluate_lcc")
# Returns: {"status": "GO", "violations": [], "confidence": 0.92, "window_minutes": 120}
```

---

## ⚡ Quick Start

```bash
python3 src/weather_gate.py
python3 tests/test_weather_gate.py
```
