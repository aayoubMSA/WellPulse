# Project Validation Status

## Current state — 2026-08-24 23:56 Africa/Cairo

- Canonical GitHub repository: established.
- Canonical Drive validation workspace: established.
- FIT IoT-LAB WP-RT01: **COMPLETE / FINAL EVIDENCE PASS** on Grenoble A8 hardware; 18/18 final cells reconciled.
- POWDER project/access: **APPROVED**.
- POWDER Portal API authentication: **PASS** via earlier read-only `experiment list`.
- Resource-creating POWDER automation: **FROZEN by owner mandate**. G3 PASS does not authorize automatic creation of G4 resources or any scored run.
- Manual POWDER golden path G0/G1/G2: **PASS** on 2026-08-24 using `srsLTE-SIM:9` on one `d430` node.
- Canonical successful G1/G2 experiment: `WP-G1-SIM`, UUID `0dc233d7-44a0-4e6c-9734-6d4c8ea0e2ad`, node `pc734`.
- Manual G3 simulated stack/data path: **PASS** on 2026-08-24.
- Canonical G3 experiment: `WP-G3-SIMSTACK`, UUID `3484b01d-7eca-48e7-9e34-866680057b0d`, profile `srsLTE-SIM:9`, one `d430`, live node `pc757`.
- G3 SSH: **PASS** with explicit local key `WellPulse-POWDER-Golden`.
- G3 simulated path: **PASS** for `pdsch_enodeb -> IQ file -> pdsch_ue`; MIB/PDCCH/PDSCH decoded, multiple `TB decoded OK`, `RX_RC=0`.
- G3 waveform evidence: `2304000` bytes; SHA-256 `103de59d52e75252e916d7ed62c5c9b76401e817ffec3178363879e0bed71678`.
- G3 temporary waveform cleanup: **PASS**.
- G3 portal teardown: **PASS**; POWDER dashboard returned to `Current Usage: 0 Node Hours` with no active experiments.
- Canonical G3 evidence: `evidence/powder/g3-simstack-2026-08-24.md`.
- `srsLTE-SIM:9` remains compute/file-based simulation only: **no SDR, no physical RF, no scientific result**.

## POWDER infrastructure gates

- G0 account/project: **PASS**.
- G1 compute provisioning: **PASS**.
- G2 explicit-key SSH + teardown: **PASS**.
- G3 simulated stack/data path: **PASS**.
- G4 controlled physical-RF lifecycle: **NEXT**.
- G5 RF impairment plumbing: **PENDING**.

G0–G3 are infrastructure only and add **0%** to scientific completion.

## Scientific programme state

- WP0 novelty/venue design: **PASS / 8 of 8**.
- WP1 confirmatory protocol/statistics freeze: **PASS / 12 of 12**.
- WP2 RF Calibration & Measurement Validation: **0 of 15 — NEXT SCIENTIFIC WP**, but blocked until G4 establishes a valid controlled physical-RF lifecycle/user-plane.
- WP3 Conducted-RF Confirmatory Campaign: **0 of 30 — BLOCKED BY WP2**.
- WP4 OTA External Replication: **0 of 15 — BLOCKED BY WP3**.
- WP5 Analysis + Artifact + Paper Closure: **0 of 20 scientific closure**; scaffolding exists but is not counted yet.
- Scientific weighted completion: **20%**.
- `scored_runs_authorized = false`.
- No POWDER run has been admitted to the scored scientific corpus.

## Frozen scientific design

- Primary comparator `B1_MQTT_QOS1`: MQTT v3.1.1, QoS1, TLS scored path, automatic reconnect, volatile client state, no application-level disk durability/reconciliation.
- WellPulse `W1_OFFLINE_FIRST`: same low-level Paho session plus SQLite durable queue, stable record identity/checksum, replay, idempotent receiver and reconciliation.
- Frozen low-level session: `paho-mqtt==2.1.0`, `clean_session=False`, keepalive 60 s, reconnect 1–8 s, outgoing queue 4096, inflight 20.
- Scenarios: S0 healthy, S1 intermittent, S2 hard outage, S3 outage + gateway-process restart.
- Run is the statistical unit.
- Conducted campaign: 24–36 scored runs under the frozen precision rule.
- OTA replication: 12 scored runs for S1/S2 only.

## Automation state and troubleshooting boundary

The safe attach-only G3 workflow exists at `.github/workflows/powder-g3-attach.yml`, but its current repository SSH credential must not be trusted yet. Sanitized diagnosis established that `POWDER_SSH_PRIVATE_KEY` contains a public key rather than an usable private key. Earlier CI attempts failed before target validation; they did not execute the G3 workload or terminate the experiment.

The accepted G3 result was therefore completed manually with the validated Golden key. Preserve the failed CI records as troubleshooting only. Do not rerun CI merely to obtain a prettier G3 result.

The full resource-creating workflow `.github/workflows/powder-g3-simstack.yml` remains **UNAPPROVED / DO NOT RUN** under the owner mandate.

## Failed/exploratory POWDER history — quarantined

- `PowderTeam/srs-rf-matrix` attempt `wpplmb6787317`: failed because topology requested an `n310` while WellPulse entitlement was 0; **do not resubmit unchanged**.
- `srsran-handover` attempt `wphnd8201533`: exploratory/invalid feasibility attempt; **not** an accepted current controlled-RF baseline.
- Earlier pre-Golden G1 and failed G3 CI attempts are troubleshooting provenance only.

## Current exact next gate — G4

**Controlled physical-RF lifecycle discovery and qualification.**

1. Use the live authenticated POWDER UI to identify current controlled physical-RF example/profile candidates.
2. Verify exact profile name, owner/project, revision, requested hardware/radio resources, entitlement and current availability live.
3. Do not infer profile compatibility from stale repository code or prior memory.
4. Do not reuse `srsran-handover` as a baseline without fresh verification.
5. Do not resubmit `srs-rf-matrix` unchanged.
6. Select the smallest suitable current controlled-RF profile.
7. Manually prove one lifecycle first: provision -> READY -> manifest/resource binding -> explicit-key SSH -> clean terminate -> zero active usage.
8. Only then establish the experimental cellular user-plane and proceed to G5/WP2 RF calibration.

## Evidence boundary

Current POWDER evidence supports only infrastructure/plumbing/feasibility claims through a file-based simulated LTE path. It does not support physical-RF propagation, attenuation, OTA, WellPulse/MQTT resilience, pump/hydraulic/groundwater/agronomic/Siwa-field, or rural-generalization claims.