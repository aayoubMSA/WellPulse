# Project Validation Status

## Current state — 2026-08-24

- Canonical GitHub repository: established.
- Canonical Drive validation workspace: established.
- FIT IoT-LAB WP-RT01: **COMPLETE / FINAL EVIDENCE PASS** on Grenoble A8 hardware; 18/18 final cells reconciled.
- POWDER project/access: **APPROVED**.
- Dedicated POWDER SSH automation key: configured.
- GitHub POWDER secrets: SSH username/private key and Portal API token configured.
- POWDER Portal API authentication: **PASS** via read-only `experiment list`.
- POWDER lifecycle automation: **IN PROGRESS**; create/get/manifests/terminate syntax verified from the official Portal API client, but exact `srs-rf-matrix` API profile resolution still needs closure before resource creation is automated.
- WP0 novelty/venue design: **PASS / LOCKED FOR CAMPAIGN DESIGN**.
- Primary venue-fit target: **Internet of Things (Elsevier)**; Computer Networks and Computer Communications retained as fit-dependent backups. Current Q1/indexing/APC status must be re-verified at submission.
- WP-PWD01 protocol: **v0.2 DESIGN FROZEN PENDING CALIBRATION AND BASELINE GATE**; scored runs remain unauthorized.
- Primary POWDER comparator upgraded from legacy publish-only B0 to **B1 standard MQTT QoS1 + automatic reconnect + volatile client state**, with W1 retaining durable application queue/reconciliation.
- Local B1/W1 semantics gate: **PASS — 9/9 tests** on Python 3.12.14; durable evidence at `evidence/local/unit-tests-latest.md`.
- Conducted POWDER scored design: **24–36 runs** under pre-frozen paired precision-based replication.
- Planned OTA replication: **12 runs** for intermittent and hard-outage scenarios only, kept separate from conducted inference.

## Current evidence state

### Existing scientific evidence

FIT WP-RT01 supports communications/durable-buffering/restart-recovery/reconciliation claims on real embedded hardware under controlled connectivity impairment. It does not support radio-propagation, field, pump, hydraulic, groundwater, or agronomic claims.

### POWDER evidence

Current POWDER files under `evidence/powder/` are **infrastructure/plumbing evidence only**. No POWDER run has yet been admitted to the scientific scored corpus.

### Next gates before any scored POWDER run

1. Finish API profile resolution and lifecycle automation with fail-safe termination.
2. Implement/freeze the actual Paho-based B1 remote comparator and document exact session/reconnect/queue semantics.
3. Run non-scored physical-RF calibration to freeze Q0–Q3 plus observed radio context.
4. Compute and freeze recovery horizon H.
5. Verify end-to-end evidence capture and one-command primary-endpoint reconstruction.
6. Only then set `scored_runs_authorized: true`.
