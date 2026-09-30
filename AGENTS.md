# AGENTS.md — spacex-pad-weather-gate

**Company:** SpaceX
**Domain:** Telemetry Processing & Mission Sequencing

## Quick Rules
- **Test command:** `PYTHONPATH=src pytest tests/ -v`
- **Lint:** `ruff check src/ tests/`
- **No drive-by edits** — load the skill first.

## Architecture
- `src/spacex_pad_weather_gate/core.py` — Domain logic (Telemetry Processing & Mission Sequencing)
- `tests/` — Verified test suite
- `.github/workflows/ci.yml` — Enforced CI pipeline
