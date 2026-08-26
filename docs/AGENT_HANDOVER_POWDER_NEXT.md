# AGENT HANDOVER — WellPulse POWDER Validation Owner

**Handover timestamp:** 2026-08-26 post-H1 physical session and evidence closeout  
**Canonical repository:** `aayoubMSA/WellPulse`  
**Canonical branch:** `main`  
**Repository visibility:** private  
**Scientific completion:** **20%**  
**Current frontier:** **WP2 Recovery-Semantics Amendment Consortium / RS-1 offline reconstruction**  
**H:** `UNFROZEN`  
**Scored authorization:** `scored_runs_authorized = false`

## 1. Mandate

Own continuation of the WellPulse validation lane from the preserved H1 adverse result through the smallest defensible amendment, non-scored Golden E2E rehearsal, H requalification, and only then the scored campaign.

Optimize for:

`scientific value × reproducibility × reviewer defensibility ÷ execution risk × unnecessary scope × resource cost`

Do not reopen frozen RF science, do not broaden scope because POWDER exposes more capabilities, do not erase adverse evidence, and do not treat infrastructure activity as scientific completion.

## 2. Mandatory read order

Read before taking any action:

1. `HANDOVER_CURRENT.md`
2. `docs/NEXT_GATE.md`
3. `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`
4. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
5. `docs/RS1_OFFLINE_RECONSTRUCTION.md`
6. `scripts/wp2_rs1a_sender_reconstruct.py`
7. `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`
8. `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`
9. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
10. `experiments/WP-PWD01/PRE_SCORE_P1_AMENDMENT_2026-08-26.md`
11. `experiments/WP-PWD01/run-matrix.yaml`
12. `docs/MILESTONE_STATUS.md`
13. `docs/STATUS.md`
14. `docs/DECISIONS.md`
15. `experiments/WP-PWD01/protocol.md`
16. `experiments/WP-PWD01/analysis-plan.md`
17. `experiments/WP-PWD01/evidence-schema.md`

Do not use the prior “19:00 reservation / run H” instructions as current state.

## 3. Frozen project state

- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Q0/Q1/Q2/Q3: `0 / 40 / 52 / 55 dB`.
- attenuation IDs `1 33 2 34`, always coupled.
- WP0: **8/8 PASS**.
- WP1: **12/12 design complete**.
- B2 durable-client local semantics: **PASS 3/3**, compact S2/S3 sensitivity only.
- WP2: **ACTIVE / POST-H1**.
- WP3/WP4: **BLOCKED**.
- WP5: **not scientifically closed**.
- weighted scientific completion: **20%**.

## 4. Scientific question and claim boundary

The study asks when durable application-level record semantics add measurable value beyond correctly configured MQTT QoS1, rather than assuming WellPulse wins every outage.

- S0: healthy integrity equivalence/overhead sanity.
- S1: intermittent network-only integrity; recovery/overhead secondary.
- S2: hard network outage while volatile client-process state survives.
- S3: primary process-state durability/integrity stress.

Primary endpoint remains unique primary-cohort completeness at one common prospectively frozen H. Do not claim a separately powered confirmatory recovery-time advantage. Use cross-testbed consistency/triangulation, not broad transportability. Claim is bounded to the frozen 1 Hz low-rate regime.

## 5. Physical experiment of record

Experiment: `WP-HCAL-E`  
UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`  
Profile: `PowderProfiles/srslte-controlled-rf`  
Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`  
Binding: `enb1 -> nuc1`, `rue1 -> nuc2`.

Exact deployed WellPulse H code commit:

`95ba9a57bef159450b00b8a439d393d22e1c0519`

Pre-H physical/runtime gates passed: Q0 user plane, `tun_srsue` route, Python 3.11.16, Paho 2.1.0, TLS MQTT endpoint 172.16.0.1:8883, MQTTv3.1.1/QoS1/clean_session=false, fresh `session_present=false` isolation.

## 6. H1 Trial #1 — DO NOT RECLASSIFY

Run ID: `wp2h1-a1-20260826-001`  
Classification: **`VALID_W1_RECOVERY_FAILURE`**  
Scored: false.

Key observed data:

- Q3 full-state duration: `120.000117905 s`.
- RF restoration/cutoff: `2026-08-26T18:16:00.428045+00:00`.
- generated records: `361`.
- pre-restoration cohort: `211`.
- final pending: `270`.
- app inflight: `20`.
- published calls: `111`.
- PUBACK callbacks: `91`.
- Q0 pre-readiness: `5/5` ping PASS.
- post-restoration health: `0/3` ping.
- queue pending zero: not reached.
- status: `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`.

Consequences:

- preserve Trial #1 permanently;
- no replacement H2/H3 under the old plan;
- H remains unfrozen;
- scored work remains prohibited.

## 7. Failure diagnosis

The dominant failure was below the application layer:

- UE/tunnel remained present but user-plane packets did not traverse;
- eNB later showed recovered uplink CRC/SNR, so radio recovery occurred;
- EPC/MME/SPGW showed stale/context/IP churn, repeated attach requests, existing UE/GTP-C conflicts, failed old-tunnel deletion, and successive IP allocations while UE retained its old tunnel address.

Do not interpret H1 as proof that WellPulse durable queueing failed.

## 8. Recovery characterization

- UE-only restart: **FAIL** after 96 s.
- EPC/eNB reset while UE remains running: reset **PASS**, user-plane recovery **FAIL** after 61 s.
- coordinated clean-order `stop UE -> EPC -> eNB -> fresh UE`: **PASS**, returning `172.16.0.2`, `tun_srsue`, and 10/10 Q0 ping.

The clean-order sequence is a **qualified testbed recovery primitive only**. It is not yet a scientifically approved in-trial action.

After clean-order recovery, exact application transport qualification passed **3/3** independent fresh sessions:

`LTE -> TLS -> MQTTv3.1.1 -> QoS1 -> SUBACK/PUBACK -> round-trip receive -> matching SHA-256`

All fresh sessions had `session_present=false`.

## 9. Evidence preservation

Original H1 raw archives:

- nuc1 SHA-256 `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2 SHA-256 `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

Recovery-characterization archives:

- nuc1 `71aaea25a50ad955fa797a358b14cce4efc0e76ec0861468b3b99dd224c7dd55`
- nuc2 `431855c8662fa46a82f7baca60b5f3deeda4fd849cf4d90bfc4889800be3e71d`

Reproducibility archives:

- nuc1 `af601716237082be410be3680f1e33b36240beae77e7b644f0f5bef811c1b647`
- nuc2 `ada35310a2dd46dba6c28a26604d41f28884799e0fc27c0846a7bf66421935bc`

Node-local chain-of-custody manifests:

- nuc1: 22 files, SHA-256 `9596f23f4e9359d3395f29f6e0081d5acdec05dc6a986c0e0b0f19ac5fa35811`
- nuc2: 34 files, SHA-256 `343a9deb1e432c0f5d30cbf55def3d133726a214a595d9f7f0723a5e87d8ec2e`

Canonical session closeout commit: `74722415dc6e6f0fff6af023d8e7efffd998be3b`.

Core raw sender artifacts include `sender_summary.json`, `calibration_manifest.json`, `attenuation_timeline.csv`, `telemetry_generated.csv`, `queue_timeline.csv`, `mqtt_events.jsonl`, and `w1_queue.sqlite`. Receiver and LTE/EPC/eNB/UE logs are preserved in the node bundles.

Hashes are integrity anchors; the raw files contain the actual scientific tables/timestamps/record identities.

## 10. Current Recovery-Semantics Consortium gate

Authority: `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`.

Question: how should network-service recovery be represented so that srsLTE/testbed pathology does not contaminate B1-vs-W1 application-level inference?

Candidate event clocks:

- `t_rf_restore`
- `t_service_ready`
- `t_app_complete`

Candidate strategies:

- A: repair/qualify autonomous LTE recovery — preferred if bounded fix exists;
- B: prospectively standardize service restoration and separate clocks — strong fallback;
- C: reopen RF outage design — presumptive KILL;
- D: ad-hoc restart when recovery stalls — KILL.

Work packages:

`RS-1 -> RS-2 -> RS-3 -> RS-4 -> RS-5 -> RS-6 -> RS-7`

## 11. RS-1 offline evidence reconstruction

Canonical guide: `docs/RS1_OFFLINE_RECONSTRUCTION.md`.

Canonical sender tool: `scripts/wp2_rs1a_sender_reconstruct.py`.

RS-1 requires no live reservation. Work only from copied/extracted preserved evidence.

Sequence:

- RS-1A sender/RF/queue timeline;
- RS-1B receiver/identity/checksum timeline;
- RS-1C LTE/EPC/RAN chronology;
- RS-1D generated-received-durable reconciliation;
- RS-1E paper-grade tables/figures.

## 12. Exact next actions for the new agent

1. Do **not** instantiate POWDER or rerun H.
2. Obtain/copy the preserved H1 node archives into a local offline analysis workspace.
3. Verify their SHA-256 values against this handover.
4. Execute RS-1A through RS-1E and preserve derived outputs/hashes.
5. Run RS-2 bounded LTE recovery-mechanism review using H1 logs and current srsLTE configuration/runtime fingerprints.
6. RS-3 chooses `t_rf_restore`/`t_service_ready`/`t_app_complete` estimands and H semantics.
7. RS-4 adversarially attacks the proposal for bias/confounding/censoring.
8. Only after RS-1..RS-4 PASS, draft a prospective amendment (RS-5).
9. Freeze Golden E2E non-scored rehearsal specification (RS-6).
10. `GO_REOPEN_H` only after RS-1..RS-6 PASS.

No WP3, no scored B1/W1/B2, no RF recalibration before that.

## 13. Security boundary

Never expose or commit private SSH keys, passphrases, POWDER API tokens, RPC credentials, certificate private keys, or raw credential-bearing portal manifests. Preserve only sanitized topology/runtime/evidence metadata and public integrity hashes.

## 14. Handover acceptance test

A replacement agent may take ownership only if it can correctly state:

1. H1 is valid adverse evidence, not technical invalidity.
2. H is still unfrozen.
3. Clean-order LTE recovery is not yet an approved scientific treatment.
4. The raw evidence bundles, not their hashes alone, contain the data required for analysis.
5. The immediate work is offline RS-1 reconstruction, not another reservation.
6. RS-1..RS-7 govern the recovery amendment.
7. `scored_runs_authorized=false` remains mandatory.
