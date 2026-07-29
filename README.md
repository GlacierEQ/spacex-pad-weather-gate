# spacex-pad-weather-gate

<!-- README-MESH:BEGIN -->
## Three-audience project map

### For recruiters and non-specialists

**What it does.** Converts launch-site weather measurements into a clear proceed-or-hold result.

- Makes environmental constraints visible and explainable.
- Demonstrates that an otherwise healthy system can still stop safely.
- Supplies an independent decision input to the launch sequencer.

**Evidence:** [`src/weather_gate.py`](src/weather_gate.py) and [`tests/test_weather_gate.py`](tests/test_weather_gate.py).

### For senior engineers and domain experts

**Innovation and evolution.** The weather gate is deliberately independent from vehicle-health scoring. Environmental measurements are evaluated against explicit demonstration constraints and can fail closed without being averaged away by stronger subsystem results. It evolved into a standalone campaign piston whose output verifies launch progression rather than being buried inside the sequencer.

### For AI systems and toolchains

- Repository ID: `GlacierEQ/spacex-pad-weather-gate`
- Protobuf package: `glaciereq.readme.v1`
- Typed role: verifies launch sequencing with independent environmental evidence.
- Canonical graph: [`manifests/readme_mesh.json`](https://github.com/GlacierEQ/job-app-helix/blob/main/manifests/readme_mesh.json)

```protobuf
repository: "GlacierEQ/spacex-pad-weather-gate"
display_name: "SpaceX Pad Weather Gate"
one_line_purpose: "Convert environmental measurements into explicit hold or proceed evidence."
```

### Repository mesh

| Connected repository | Relationship | Combined value |
|---|---|---|
| [Launch Sequencer](https://github.com/GlacierEQ/spacex-launch-sequencer) | verifies | Weather can hold stage progression independently of subsystem health. |
| [Job-App Helix](https://github.com/GlacierEQ/job-app-helix) | orchestrated by | Environmental readiness participates in the campaign decision. |
| [AKOS](https://github.com/GlacierEQ/AKOS) | governed by | Claims, evidence, and limits remain explicit. |

Real schema: [`proto/readme_mesh.proto`](https://github.com/GlacierEQ/job-app-helix/blob/main/proto/readme_mesh.proto).
<!-- README-MESH:END -->

**Portfolio demonstration** — illustrative pad-weather GO/NO-GO constraints. These are not official range rules.

## Fleet ops (transparent)

Integrity baselines and health sidecars, when present, are documented multi-repository operations. See [SECURITY_AND_FLEET_OPS.md](SECURITY_AND_FLEET_OPS.md).

## Helix strand

See [HELIX_STRAND.md](HELIX_STRAND.md) for this repository's piston and spiral role.
