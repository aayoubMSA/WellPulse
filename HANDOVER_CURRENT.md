# WellPulse — Current Handover

Last updated: 2026-08-26, after G5 RF-state freeze, Africa/Cairo

## Standing handover rule

No material project state may exist only in chat. Decisions, results, artifacts, blockers, evidence boundaries, milestone percentages and the exact next action must be recoverable from GitHub and/or Drive.

## Executive state

- FIT IoT-LAB scientific evidence layer: **FINAL PASS**.
- POWDER G0–G4: **PASS**.
- POWDER **G5 RF impairment/control + numeric RF-state calibration: PASS**.
- WP0 Novelty & Venue Lock: **8/8 complete**.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 design complete**, comparator sufficiency still open pre-score.
- WP2 RF Calibration & Measurement Validation: **IN PROGRESS**. RF-state calibration sub-gate is closed; H/recovery-horizon and remaining measurement/evidence pre-score gates are still open.
- WP3: **0/30 — BLOCKED** by WP2 + comparator freeze + explicit scored authorization.
- WP4: **0/15 — BLOCKED** by WP3.
- WP5: **0/20 scientific closure**.
- Gate-based scientific weighted completion remains **20%** until WP2 closes.
- `scored_runs_authorized = false`.

No G5 calibration observation is a scored B1/W1 scientific result.

## Canonical repositories and workspaces

- GitHub: `aayoubMSA/WellPulse`.
- Drive project root `P12_WellPulse`: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`.
- Drive validation workspace `00_Validation_Workspace`: `1SydHCA2jlkatxdGgUtJ1P8atgyi8_ta3`.
- Drive raw evidence `02_RAW_EVIDENCE`: `11xaitxG0vkV6fCzK_JgLAacrdhjz7GBf`.
- Drive handover folder `WellPulse Handover`: `1Du4j_YkMLvQjWJCxV5zqxxK6OGG2Q0hA`.
- Clean G5 snapshot: `docs/handovers/2026-08-26_G5_RF_CALIBRATION_HANDOVER.md`.

## Frozen scientific design

Canonical protocol remains `experiments/WP-PWD01/protocol.md` v0.4. It intentionally left numeric Q0–Q3 values open pending WP2 calibration.

Primary comparison remains:

- `B1_MQTT_QOS1`: Paho Python MQTT v3.1.1, QoS1, TLS on scored path, automatic reconnect, `clean_session=False`, volatile client state, no application-level disk durability/reconciliation.
- `W1_OFFLINE_FIRST`: same low-level Paho session plus SQLite durable application queue, stable record identity/checksum, replay, idempotent receiver and reconciliation.

Frozen low-level parameters: `paho-mqtt==2.1.0`, keepalive 60 s, reconnect 1–8 s, outgoing queue 4096, inflight 20.

Comparator caveat remains open: B1 is the clean matched same-implementation comparator but not the strongest durable MQTT client generally. Candidate `B2_MQTT_DURABLE_CLIENT` must be qualified/frozen before scoring if retained.

## G5 accepted experiment state

Non-scored experiment:

- `WP-G5-RF-CAL`;
- UUID `575d246e-8d01-4827-9a84-f4368d272cea`;
- profile `srslte-controlled-rf`;
- profile revision `a6da96560b6526dc6816761282722c996418fd8c`;
- live binding `enb1 -> nuc1` (EPC/eNB), `rue1 -> nuc2` (UE);
- UE `172.16.0.2`, EPC SGi `172.16.0.1` after clean bearer restoration;
- attenuation path IDs `1 33 2 34`, always changed together.

At this handover the last commanded RF state was restored to **0 dB** after Q52, and the last explicit Q0 user-plane health test was **3/3 replies, 0% loss**.

A timestamped ping logger was running on `nuc2` as PID `20134`, file `/tmp/g5_q41_clean_ping.log`. Final clean stage logs include `/tmp/g5_q41_clean_stage.log`, `/tmp/g5_q42_clean_stage.log`, `/tmp/g5_q49_clean_stage.log`, `/tmp/g5_q52_clean_stage.log`. These files are ephemeral and may be sanitized/preserved before teardown if still available.

Fallback reservation remains available for `nuc1+nuc2` on **2026-08-26 19:00–22:00 Africa/Cairo**. Do not spend it on further RF hunting.

## RF calibration — FROZEN

Numeric authority: `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`.
Calibration ledger: `evidence/powder/g5-rf-calibration-ledger-2026-08-26.md`.

| State | Programmed attenuation | Meaning | Accepted observation |
|---|---:|---|---|
| Q0 | **0 dB** | strong/stable | ~-60 dBm RSRP, SNR ~40–45 dB, BLER 0; clean user-plane PASS |
| Q1 | **40 dB** | degraded but continuously connected | ~-100 dBm RSRP, SNR ~18–19 dB; continuous ping |
| Q2 | **52 dB** | near-threshold/intermittent | clean isolated 20 s window: **6 replies / 12 misses**; clean Q0 recovery |
| Q3 | **55 dB** | effective application-data outage | first isolated valid 20 s outage with immediate recovery after Q0 reset |

Clean boundary checks after bearer restoration:

- +41 dB: 20 replies / 0 misses;
- +42 dB: 20 replies / 0 misses;
- +49 dB: 21 replies / 0 misses;
- +52 dB: 6 replies / 12 misses.

**No more attenuation sweep is authorized or scientifically useful.**

## Critical invalidity and safeguard

Repeated severe RLF/re-attach testing eventually produced a stale user-plane bearer while the UE still appeared attached and had an IP. Q0 then failed in both directions. This is infrastructure/calibration invalidity, not an RF scientific result.

The contaminated-period 48/50/52/54 sweep, 42/44/46/47 sweep, and first +41 attempt are retained for provenance but excluded from canonical RF classification.

The bearer was restored by a bounded clean LTE reset: stop UE, restart EPC/eNB, restart UE, reattach, then verify Q0 user plane. Clean restoration passed 5/5.

**Frozen safeguard:** every future scored run/block must begin with an explicit Q0 user-plane readiness gate. Attached state or assigned IP alone is insufficient. If Q0 user-plane health fails, the run is technically invalid and must not enter the scientific corpus.

## Key G5 evidence

- Q0 baseline `9e4e8b0ee14f9919a8ca8b5a5e5f615fdb33e62d`
- +20/+30/+40 sweep `7a4dc3891977b0e643850bfa713e6a0ae9c0a16c`
- isolated +55 / Q3 `cf57bf8646f39c1be9443c4e08160a69697c7ba1`
- invalid first +41 / stale bearer `a67126b2fdbf30f69b1038e45d63e5d3547b8d67`
- clean Q0 recovery `6f4cb5d01ceb2eb402f638534c24a7b04a3276da`
- clean +41 `ae2baa30065c606f54d819ff2c6610b10fe30bdc`
- clean +42 `41011cee93f5ab100061edfc2076d966e44824d9`
- clean +52 / Q2 `3b9d1992cfeb18ceb5be468b1fe751b0d2a40a9e`
- calibration ledger `ae27b01311d84491120001d7bc308683515a87ba`
- RF freeze artifact `74e7eae3df8365693d01b627378dcd5a3f3f2860`

## Remaining pre-score work

Do not authorize scored runs yet. Material open gates:

1. calibrate/freeze common recovery horizon `H` from valid non-scored W1 backlog-drain observations;
2. reproduce frozen Paho/runtime configuration on the remote path;
3. verify B1/W1 implementation matching and end-to-end identity/checksum preservation;
4. verify evidence capture and clock alignment for mandatory endpoints;
5. run deterministic analysis on a non-scored pilot bundle without manual spreadsheet edits;
6. close the B2 durable-client comparator decision/amendment;
7. repair or bypass the known-bad automated `POWDER_SSH_PRIVATE_KEY` path before scored automation is trusted.

## Exact next action

**Operationally:** if `WP-G5-RF-CAL` is still active, preserve any desired sanitized `/tmp` calibration logs, leave attenuation at 0, terminate the experiment cleanly, and verify zero active usage. Do not run more RF calibration.

**Scientifically after teardown:** stay in WP2. Run the smallest valid non-scored W1 recovery pilot needed to calibrate/freeze `H`, then close the remaining pre-score measurement/evidence gates. Do not start WP3 and do not execute B1/W1/B2 scored cells.

## Reproducibility read order

1. `HANDOVER_CURRENT.md`
2. `docs/handovers/2026-08-26_G5_RF_CALIBRATION_HANDOVER.md`
3. `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`
4. `evidence/powder/g5-rf-calibration-ledger-2026-08-26.md`
5. `docs/MILESTONE_STATUS.md`
6. `docs/STATUS.md`
7. `docs/DECISIONS.md`
8. `experiments/WP-PWD01/protocol.md`
9. `docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`
10. `experiments/WP-PWD01/analysis-plan.md`
11. `experiments/WP-PWD01/evidence-schema.md`
12. `experiments/WP-PWD01/randomization-plan.csv`
13. `experiments/WP-PWD01/run-matrix.yaml`
14. `powder/MANUAL_GOLDEN_PATH.md`

Never infer node roles from prior runs. Never persist secrets, private keys, passphrases, RPC tokens, credential blocks, or raw credential-bearing manifests.