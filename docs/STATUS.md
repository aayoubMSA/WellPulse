# Project Validation Status

## Current state — 2026-08-25 01:42 Africa/Cairo

- Canonical GitHub repository and Drive validation workspace: established.
- FIT IoT-LAB WP-RT01: **COMPLETE / FINAL EVIDENCE PASS**; Grenoble A8; 18/18 final cells reconciled.
- POWDER G0 account/project: **PASS**.
- POWDER G1 compute provisioning: **PASS**.
- POWDER G2 explicit-key SSH + teardown: **PASS**.
- POWDER G3 simulated LTE stack/data path: **PASS**; file-based only, no SDR/RF/scientific result.
- POWDER G4 profile discovery: **PASS** for `PowderProfiles/srslte-controlled-rf`, repo hash `a6da9656`, UE `srsLTE UE (B210)`.
- Required NUC5300/B210 reservation under `WellPulse`: **APPROVED** for 2026-08-25 19:00–22:00 Africa/Cairo.
- Scheduled G4 experiment: `WP-G4-CTRL-RF`, state **scheduled** pending the 19:00 window.
- Resource-creating POWDER automation: **FROZEN** until the current G4 lifecycle is manually qualified.
- Scientific weighted completion: **20%**.
- `scored_runs_authorized = false`.

## POWDER infrastructure gates

- G0 account/project: **PASS**.
- G1 compute provisioning: **PASS**.
- G2 explicit-key SSH + teardown: **PASS**.
- G3 simulated stack/data path: **PASS**.
- G4 controlled physical-RF lifecycle: **SCHEDULED / LIFECYCLE PENDING**.
- G5 RF impairment plumbing: **PENDING**.

G0–G4 are infrastructure qualification and add **0%** to scientific completion.

## Scientific programme state

- WP0 Novelty & Venue Lock: **8/8 complete**, augmented by the 2026-08-25 serious related-work benchmark and comparator audit.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 design work complete**, but comparator sufficiency is **OPEN FOR PRE-SCORE REVIEW**; v0.4 remains the working infrastructure/calibration protocol.
- WP2 RF Calibration & Measurement Validation: **0/15 — NEXT SCIENTIFIC WP after valid G4/user-plane**.
- WP3 Conducted-RF Confirmatory Campaign: **0/30 — BLOCKED BY WP2 + comparator freeze + scored authorization**.
- WP4 OTA External Replication: **0/15 — BLOCKED BY WP3**.
- WP5 Analysis + Artifact + Paper Closure: **0/20 scientific closure**.

## Working scientific design

Primary matched comparison remains:

- `B1_MQTT_QOS1`: Paho Python MQTT v3.1.1, QoS1, TLS scored path, automatic reconnect, volatile client state, no application-level disk durability/reconciliation.
- `W1_OFFLINE_FIRST`: same Paho Python low-level session plus SQLite durable application queue, stable record identity/checksum, replay, idempotent receiver and reconciliation.

Frozen low-level session for B1/W1:

- `paho-mqtt==2.1.0`;
- `clean_session=False`;
- keepalive 60 s;
- reconnect 1–8 s;
- outgoing queue 4096;
- inflight 20.

Scenarios: S0 healthy, S1 intermittent, S2 hard outage, S3 outage + gateway-process restart. Run is the statistical unit. Working conducted campaign remains 24–36 B1/W1 scored runs under the precision rule; OTA remains 12 scored S1/S2 runs if the conducted gate passes.

## 2026-08-25 serious related-work/comparator audit

Canonical artifacts:

- `docs/WP0_RELATED_WORK_BENCHMARK_2026-08-25.md`
- `docs/WP0_RELATED_WORK_MATRIX_2026-08-25.csv`
- `docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`
- updated `docs/WP0_NOVELTY_VENUE_LOCK_2026-08-24.md`

The survey confirmed that standalone novelty cannot rest on MQTT resilience, buffering/store-and-forward, SQLite/database retransmission, offline-first operation, identifiers/checksums/idempotence in isolation, reconciliation, cellular/5G agricultural IoT, or testbed usage.

### Material finding

Official Eclipse Paho Python documentation confirms the current Python client session is not durably persisted across process restart. Deeper review of official Eclipse Paho Java documentation/source shows file-backed persistence and configurable persistent disconnected buffering exist in the standard MQTT client ecosystem.

Therefore:

- B1 remains the cleanest **same-implementation matched causal comparator** for B1/W1.
- B1 must **not** be described as the strongest durable MQTT client configuration available generally.
- A candidate `B2_MQTT_DURABLE_CLIENT` sensitivity comparator is under review.
- Preferred provisional route: locally prove B2 semantics first; if valid, use only a compact S2/S3 sensitivity matrix rather than turn the whole study into a three-arm campaign.
- Exact B2 version/options/replication/analysis remain **UNFROZEN**.
- No scored run may begin until this comparator review is explicitly closed.

The high-priority direct competitor still requiring full-text recovery before final manuscript novelty freeze is:

`The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications`, IEEE Internet of Things Magazine (2026), DOI `10.1109/MIOT.2026.3681190`.

## G4 exact next action

At 2026-08-25 19:00 Africa/Cairo:

1. Open existing `WP-G4-CTRL-RF`.
2. Refresh and wait for `READY`.
3. Capture actual manifest/resource/radio bindings.
4. Verify B210 controlled-RF topology and live endpoints.
5. SSH with the explicit canonical Golden key.
6. Validate the controlled LTE physical-RF lifecycle/data path.
7. Preserve sanitized evidence only.
8. Terminate manually.
9. Verify zero active usage / `0 Node Hours`.
10. Record G4 PASS/FAIL.

G4 contains no B1/W1/B2 scored science and is **not blocked** by the comparator review.

## Automation/security boundary

- Canonical manual key: `WellPulse-POWDER-Golden`, fingerprint `SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`.
- Never expose/commit/copy its private key or passphrase.
- GitHub secret `POWDER_SSH_PRIVATE_KEY` is known-bad: it contains a public key rather than usable private-key material.
- Repair the automation credential path before trusting automated scored execution.
- After G4 PASS, automation may clone the proven lifecycle. Each new infrastructure/RF-control layer still gets one manual qualification before repetitive automation.

## Evidence boundary

Current accepted POWDER evidence through G3 supports infrastructure/plumbing and file-based LTE-stack feasibility only. G4, if it passes, will establish a controlled physical-RF lifecycle but still no WellPulse scientific effect. Remote-testbed work does not validate pump mechanics, hydraulics, groundwater, agronomy, Siwa field performance, or generic rural generalization.
