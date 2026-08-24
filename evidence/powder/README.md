# POWDER Evidence Index

This directory stores sanitized POWDER execution evidence for WellPulse.

## Admissibility rule

Every POWDER record must be classified as one of:

- **SCIENTIFIC** — admitted to a frozen WP-PWD01 analysis corpus;
- **INFRASTRUCTURE** — proves provisioning, access, orchestration, or teardown only;
- **CALIBRATION** — non-scored evidence used to freeze RF/runtime parameters;
- **TROUBLESHOOTING** — failed/exploratory attempt retained for provenance but excluded from claims.

No file is scientific merely because real POWDER hardware was allocated.

## Current canonical records

### INFRASTRUCTURE

- `manual-golden-path-2026-08-24.md` — **PASS**. Manual `srsLTE-SIM:9` provision -> explicit SSH -> metadata verification -> clean teardown.
- `api-smoke.md` — earlier read-only Portal API authentication evidence.
- `cleanup-latest.md` — cleanup evidence for the failed RF-matrix attempt.

### TROUBLESHOOTING / SUPERSEDED

- `lifecycle-latest.md` — failed `srs-rf-matrix` lifecycle attempt; hidden/unavailable `n310` dependency; not scientific evidence.
- `handover-feasibility-latest.md` — historical exploratory output only. It is not a currently accepted controlled-RF baseline unless a fresh manual verification explicitly promotes a new run.
- `profile-probe.md` and other profile/API probes — plumbing history; current POWDER UI/profile state takes precedence.

### SCIENTIFIC

**None yet.**

### CALIBRATION

**None yet.**

## Security/redaction rule

Do not commit:

- private SSH keys;
- SSH key passphrases;
- API tokens;
- experiment RPC tokens;
- raw PKCS7/certificate blocks;
- passwords or broker credentials;
- raw portal logs containing credential-like material when a sanitized extract is sufficient.

Prefer a sanitized record containing:

- experiment UUID/name;
- profile identity/revision;
- project;
- node/resource bindings;
- image/runtime identity;
- start/end/teardown state;
- SSH endpoint/auth mode where relevant;
- commands actually executed;
- acceptance verdict;
- explicit evidence boundary;
- hashes for external raw artifacts when such artifacts are retained outside Git.

## Reproducibility runbooks

Manual access baseline:

`../../powder/MANUAL_GOLDEN_PATH.md`

Scientific protocol:

`../../experiments/WP-PWD01/protocol.md`

The repository status file `../../docs/STATUS.md` is the current authority on which POWDER evidence has passed and what gate comes next.
