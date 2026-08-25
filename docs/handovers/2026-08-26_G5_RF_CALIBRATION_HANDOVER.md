# WellPulse — G5 / WP2 Clean Handover

Last updated: 2026-08-26, after RF-state freeze, Africa/Cairo

## Authoritative state

- GitHub: `aayoubMSA/WellPulse`.
- Canonical protocol remains `experiments/WP-PWD01/protocol.md` v0.4.
- `scored_runs_authorized = false`.
- Scientific weighted completion remains **20%** under gate-based credit: WP0 and WP1 design are complete; WP2 is **IN PROGRESS** and receives no scientific weight until its gate closes.
- POWDER G0–G4 remain PASS.
- **G5 RF impairment/control + numeric RF-state calibration is PASS.**
- WP2 overall is **not yet closed**: H/recovery-horizon calibration and the remaining pre-score measurement/evidence gates still require closure.
- Comparator sufficiency remains open: B1 is the matched Paho-Python primary comparator; candidate `B2_MQTT_DURABLE_CLIENT` still requires qualification/freeze before scoring.

## Current G5 experiment

Non-scored experiment:

- name: `WP-G5-RF-CAL`;
- UUID: `575d246e-8d01-4827-9a84-f4368d272cea`;
- profile: `srslte-controlled-rf`;
- profile revision: `a6da96560b6526dc6816761282722c996418fd8c`;
- live binding: `enb1 -> nuc1` (EPC/eNB), `rue1 -> nuc2` (UE);
- UE address after clean bearer reset: `172.16.0.2`;
- EPC SGi: `172.16.0.1`;
- controlled attenuation path IDs: `1 33 2 34`, always changed together;
- programmed attenuation uses integer dB values; matrix contributes roughly an additional fixed ~30 dB physical path loss.

At handover, all four attenuation IDs were restored to **0 dB** after the Q52 test. Last explicit Q0 user-plane health check was **3/3 replies, 0% packet loss**.

A timestamped ping logger was running on `nuc2` as PID `20134`, writing `/tmp/g5_q41_clean_ping.log`. Clean-stage logs created during the final boundary search include:

- `/tmp/g5_q41_clean_stage.log`
- `/tmp/g5_q42_clean_stage.log`
- `/tmp/g5_q49_clean_stage.log`
- `/tmp/g5_q52_clean_stage.log`

These `/tmp` files are ephemeral. If the live reservation is still active when work resumes, preserve a sanitized copy before teardown if useful; do not copy credentials, RPC tokens, private keys, passphrases, or certificate blocks.

A fallback reservation also exists for `nuc1+nuc2` on **2026-08-26 19:00–22:00 Africa/Cairo**. Do not spend it on further RF hunting.

## Frozen RF calibration

Canonical freeze artifact: `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`.
Canonical calibration ledger: `evidence/powder/g5-rf-calibration-ledger-2026-08-26.md`.

Frozen programmed attenuation values:

| State | Attenuation | Scientific meaning | Accepted evidence |
|---|---:|---|---|
| Q0 | **0 dB** | strong/stable reference | RSRP about -60 dBm, SNR ~40–45 dB, BLER 0; clean 5/5 and later 3/3 user-plane health |
| Q1 | **40 dB** | degraded but continuously connected | RSRP about -100 dBm, SNR ~18–19 dB, continuous ping, BLER 0 in accepted sweep |
| Q2 | **52 dB** | near-threshold/intermittent | clean isolated 20 s window: **6 replies / 12 misses**, followed by clean Q0 recovery |
| Q3 | **55 dB** | effective application-data outage | first isolated valid 20 s test: near-full-window user-plane outage with immediate recovery after reset to Q0 |

Boundary checks after clean bearer restoration showed:

- +41 dB: 20 replies / 0 misses;
- +42 dB: 20 replies / 0 misses;
- +49 dB: 21 replies / 0 misses;
- +52 dB: 6 replies / 12 misses.

Therefore Q2 is frozen at +52 dB; no further 1 dB sweep is justified.

## Critical invalidity discovered

Repeated severe RLF/re-attach testing eventually produced a **stale user-plane bearer** even though the UE remained attached and had an IP address. At Q0, UE->EPC and EPC->UE pings both failed. This was an infrastructure/calibration artifact, not an RF scientific outcome.

The following later classifications from that stale-bearer period must **not** be used as canonical RF-state evidence:

- the 48/50/52/54 sweep from the contaminated period;
- the 42/44/46/47 sweep from the contaminated period;
- the first +41 attempt.

The bearer was restored only after a bounded clean LTE reset: stop UE, restart EPC/eNB, restart UE, reattach, then verify Q0 user plane. Clean baseline restoration was 5/5 replies at `172.16.0.1` from `tun_srsue`.

### Frozen operational implication

Before every future scored run/block, Q0 must pass an explicit user-plane readiness gate. Attached state or an assigned UE IP alone is insufficient. If baseline Q0 user plane fails, the run is technically invalid and must not enter the scientific corpus.

## Evidence chain

Key commits from this G5 session:

- Q0 baseline: `9e4e8b0ee14f9919a8ca8b5a5e5f615fdb33e62d`
- +10 validation: `e7ebbbb1fbf348f64aaad152ae2e685a722a985d`
- +20/+30/+40 sweep: `7a4dc3891977b0e643850bfa713e6a0ae9c0a16c`
- +45/+50/+55 fine sweep: `a7fc11809fa9041041190fd52b947043dc8b8e99`
- threshold/RLF evidence: `2050395ebc48cb747fbb26bcd72d62049f332137`
- isolated +55 / Q3 evidence: `cf57bf8646f39c1be9443c4e08160a69697c7ba1`
- contaminated 48–54 evidence: `9fa053d9b38a69bd6655668a2fcbd148aef90b98`
- contaminated-boundary conclusion: `14845fd556fc7cb60aef9d70d68c7d2d393c7b4a`
- contaminated 42–47 boundary: `8df86670324756a276c81159c73e1cf7878a9fbb`
- invalid first +41 / stale-bearer diagnosis: `a67126b2fdbf30f69b1038e45d63e5d3547b8d67`
- clean Q0 recovery: `6f4cb5d01ceb2eb402f638534c24a7b04a3276da`
- clean +41: `ae2baa30065c606f54d819ff2c6610b10fe30bdc`
- clean +42: `41011cee93f5ab100061edfc2076d966e44824d9`
- clean +52 / Q2 freeze: `3b9d1992cfeb18ceb5be468b1fe751b0d2a40a9e`
- calibration ledger: `ae27b01311d84491120001d7bc308683515a87ba`
- RF calibration freeze artifact: `74e7eae3df8365693d01b627378dcd5a3f3f2860`

## Protocol relationship

`protocol.md` v0.4 deliberately left Q0–Q3 numeric values unfrozen pending WP2 calibration. The numeric authority is now `RF_CALIBRATION_FREEZE_v1.md`; do not rewrite protocol history retroactively. Consolidate into a later protocol revision only once the remaining WP2/pre-score gates and comparator amendment are closed.

Scored scenarios remain unchanged:

- S0 healthy;
- S1 `Q0 60 -> [Q2 20 / Q0 20] x3 -> Q0 H`;
- S2 `Q0 60 -> Q3 120 -> Q0 H`;
- S3 same Q3 outage with gateway-process restart 60 s into the Q3 interval.

## What is still open before scoring

Do **not** authorize scored runs yet. Remaining material gates include:

1. calibrate/freeze common recovery horizon `H` using valid non-scored W1 backlog-drain observations;
2. reproduce the frozen Paho session/runtime configuration on the remote path;
3. verify B1/W1 matched implementation and end-to-end identity/checksum preservation;
4. verify evidence capture + clock alignment for mandatory endpoints;
5. run the deterministic analysis pipeline on a non-scored pilot bundle without manual spreadsheet edits;
6. close the B2 durable-client comparator decision/amendment;
7. repair or bypass the known-bad automated `POWDER_SSH_PRIVATE_KEY` path before any scored automation is trusted.

## Exact next action

**First operational action:** if `WP-G5-RF-CAL` is still active, preserve any desired sanitized `/tmp` calibration logs, leave attenuation at 0, terminate the experiment cleanly, and verify zero active usage. Do not run any more attenuation sweep.

**Next scientific action after teardown:** remain in WP2 and calibrate/freeze `H` with the smallest valid non-scored W1 recovery pilot, then close the remaining pre-score measurement/evidence gates. Do not start WP3 and do not run B1/W1/B2 scored cells.

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

Never infer node roles from previous runs; verify live bindings. Never persist secrets or raw credential-bearing POWDER manifests.