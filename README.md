# WellPulse

**WellPulse: A Secure Offline-First Industrial IoT Edge Gateway for Read-Only Solar-Pump Monitoring**

This repository is the canonical code and reproducibility workspace for WellPulse.

## Current evidence state

- Research proposal: frozen/recovered.
- Student project: active.
- Remote-testbed validation: planned, not yet executed.
- No Siwa field-validation claim is made from remote-testbed work.
- No pump-mechanical, hydraulic, groundwater, crop, or local-environment claim is validated here unless a corresponding physical experiment is later added.

## Validation priority

1. `WP-RT01`: real embedded-hardware validation on FIT IoT-LAB under controlled connectivity interruption.
2. ARA Wireless Living Lab only after WP-RT01 passes, using the same workload where feasible.

## Repository map

- `src/wellpulse/` — small reusable resilience kernel.
- `scripts/` — local smoke and later remote execution wrappers.
- `tests/` — deterministic unit tests.
- `experiments/WP-RT01/` — frozen experiment contract and machine-readable configuration.
- `data/` — data policy only; raw large logs should not be casually committed.
- `results/` — derived result policy and manifests.
- `docs/` — architecture, decisions, evidence boundary, reproducibility rules.

## First local gate

```bash
python -m unittest discover -s tests -v
python scripts/run_local_smoke.py
```

The local smoke test is not publication evidence. It only verifies the record identity, durable queue, and reconciliation plumbing before remote hardware is booked.
