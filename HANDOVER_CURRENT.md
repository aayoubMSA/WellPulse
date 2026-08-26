# WellPulse — Current Handover

Last updated: 2026-08-26 after the 19:00–22:00 POWDER physical session, H1 valid recovery failure, bounded recovery characterization, application-path repeatability, reproducibility/evidence closeout, and creation of the WP2 Recovery-Semantics Amendment Consortium.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- Repository visibility: **private** (verified after the temporary deployment-public window was closed).
- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5 infrastructure/RF qualification: **PASS**.
- RF calibration: **PASS / FROZEN**.
- WP0: **8/8 PASS**.
- WP1: **12/12 design complete; P0/P1 frozen; B2 local semantics PASS**.
- WP2: **ACTIVE — POST-H1 / PRE-AMENDMENT / PRE-SCORE**.
- WP3: **0/30 — BLOCKED**.
- WP4: **0/15 — BLOCKED**.
- WP5: **0/20 scientific closure**.
- Scientific weighted completion: **20%**.
- `H = UNFROZEN`.
- `scored_runs_authorized = false`.

The current scientific frontier is no longer “run H again.” It is the **WP2 Recovery-Semantics Amendment Consortium**.

## Mandatory current read order

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

Do not reconstruct current state from old reservation instructions or chat history.

## Frozen scientific interpretation

The study asks:

> **When does application-level durable record semantics add measurable value beyond a correctly configured standard MQTT QoS1 client, and what reliability/overhead price is paid for that value?**

- `S0_HEALTHY`: integrity equivalence + overhead sanity.
- `S1_INTERMITTENT`: network-only integrity primary; recovery/overhead secondary.
- `S2_HARD_OUTAGE`: network-only integrity primary while volatile process state survives; recovery/overhead secondary.
- `S3_OUTAGE_RESTART`: primary process-state durability/integrity stress.

Primary inferential endpoint remains unique primary-cohort completeness at one prospectively frozen common H. Do not claim a separately powered confirmatory recovery-time advantage. Use `cross-testbed consistency/triangulation`, not broad transportability. Claim remains bounded to the 1 Hz low-rate telemetry regime.

## Frozen RF state — DO NOT REOPEN

- Q0 = **0 dB**.
- Q1 = **40 dB**.
- Q2 = **52 dB**.
- Q3 = **55 dB**.
- attenuation IDs = `1 33 2 34`, always changed together.

Every physical run requires explicit Q0 end-to-end LTE user-plane PASS. Attach/IP alone is insufficient.

## 2026-08-26 physical experiment of record

Experiment: `WP-HCAL-E`  
UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`  
Profile: `PowderProfiles/srslte-controlled-rf`  
Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`  
Mapping: `enb1 -> nuc1`, `rue1 -> nuc2`  
Image: `PowderProfiles:U18LL-SRSLTE:1`

Exact H runner source was deployed at WellPulse commit:

`95ba9a57bef159450b00b8a439d393d22e1c0519`

Key runner blobs:

- `scripts/wp_pwd01_h_sender.py`: `6b680c5b671aa836b9a0f8c090ac44ee03957cd1`
- `scripts/wp_pwd01_h_receiver.py`: `cbdad9e7188ae956caa36d3c7e33754b07017642`
- `scripts/finalize_wp_pwd01_h_calibration.py`: `9a065649c92166f9bd7da52c3471551faf9c9b8f`

Runtime qualification before H1:

- Q0 user plane through `tun_srsue`: PASS.
- UE source IP: `172.16.0.2`.
- broker/EPC endpoint: `172.16.0.1`.
- Python 3.11.16.
- `paho-mqtt==2.1.0`.
- TLS MQTT listener: 8883.
- MQTT v3.1.1, QoS1, `clean_session=false`.
- fresh session isolation: PASS (`session_present=false`).

## H1 Trial #1 — preserved adverse result

Run ID: `wp2h1-a1-20260826-001`  
Classification: **`VALID_W1_RECOVERY_FAILURE`**  
Scored: false.

Observed frozen schedule:

- Q0 before readiness: PASS.
- Q3: 55 dB on all four attenuators.
- Q3 full-state duration: **120.000117905 s**.
- RF/Q0 restoration cutoff: `2026-08-26T18:16:00.428045+00:00`.
- generated records: **361**.
- pre-restoration cohort: **211**.
- final pending: **270**.
- final app inflight: **20**.
- published calls: **111**.
- PUBACK callbacks: **91**.
- Q0 pre-readiness ping: **5/5**.
- post-restoration health ping: **0/3**.
- queue pending zero: **not reached**.
- sender status: `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`.

Frozen consequence:

- preserve Trial #1;
- do not replace it as invalid;
- H remains unfrozen;
- H2/H3 under the old plan are not authorized;
- scored B1/W1/B2 remains prohibited.

## Failure diagnosis

The post-Q3 failure is dominated by LTE substrate/session continuity rather than WellPulse durability logic.

Evidence:

- UE process and `tun_srsue` remained present but traffic did not traverse.
- eNB later showed recovered uplink decoding with CRC OK and ~33 dB SNR.
- EPC/MME/SPGW showed repeated attach/context churn, including `UE Context already exists`, active GTP-C connection conflicts, failed tunnel deletion, and successive IP allocations while the UE tunnel retained the old address.

Therefore H1 is a valid end-to-end recovery failure under the frozen protocol, but it cannot be interpreted as a WellPulse application-layer failure.

## Bounded recovery characterization

1. **UE-only restart:** FAIL after 96 s. Cell discovery/RRC connection occurred, but usable attach/user plane did not return.
2. **EPC/eNB reset with UE left running:** core/RAN reset PASS, automatic user-plane recovery FAIL after 61 s.
3. **Coordinated clean-order recovery:** `stop UE -> EPC -> eNB -> fresh UE` — PASS. Q0 returned with `172.16.0.2`, route through `tun_srsue`, and 10/10 ping success.

This sequence is a **qualified testbed recovery primitive only**. It is not yet an approved scientific treatment and must not be silently inserted into H.

## Post-recovery application qualification

After clean-order LTE recovery, the exact application path passed in **3/3 independent fresh sessions**:

`LTE/tun_srsue -> TLS -> MQTT v3.1.1 -> QoS1 -> SUBACK/PUBACK -> broker round-trip -> SHA-256 payload integrity`

All three sessions used fresh run-unique client/topic identities and reported `session_present=false`.

This demonstrates that the recovered substrate supports the exact WellPulse transport path; it does not alter H1 classification.

## Preserved evidence and hashes

### Original H1 raw archives

- nuc1: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

### Recovery-characterization archives

- nuc1: `71aaea25a50ad955fa797a358b14cce4efc0e76ec0861468b3b99dd224c7dd55`
- nuc2: `431855c8662fa46a82f7baca60b5f3deeda4fd849cf4d90bfc4889800be3e71d`

### Runtime/config reproducibility fingerprints

- nuc1 record: `1ef8b04a8d3a634c1cc3ded2b84c80a7140d877758a0d63010411971eab8607f`
- nuc1 archive: `af601716237082be410be3680f1e33b36240beae77e7b644f0f5bef811c1b647`
- nuc2 record: `fc1c131602c49b8376733ad8e190c4fc5d8d1976b62fe59c1e5becbe41cf8d5a`
- nuc2 archive: `ada35310a2dd46dba6c28a26604d41f28884799e0fc27c0846a7bf66421935bc`

### Node-local chain-of-custody manifests

- nuc1: 22 files; manifest SHA-256 `9596f23f4e9359d3395f29f6e0081d5acdec05dc6a986c0e0b0f19ac5fa35811`
- nuc2: 34 files; manifest SHA-256 `343a9deb1e432c0f5d30cbf55def3d133726a214a595d9f7f0723a5e87d8ec2e`

Canonical session-level closeout commit: `74722415dc6e6f0fff6af023d8e7efffd998be3b`.

Never expose raw credential-bearing manifests, SSH private keys, certificate private keys, POWDER API tokens, passphrases, or RPC credentials.

## Raw scientific artifacts available for offline analysis

Core sender-side artifacts include:

- `sender_summary.json`
- `calibration_manifest.json`
- `attenuation_timeline.csv`
- `telemetry_generated.csv`
- `queue_timeline.csv`
- `mqtt_events.jsonl`
- `w1_queue.sqlite`

Receiver-side artifacts/logs and EPC/eNB/UE diagnostic logs are also preserved in the node archives.

These contain the actual timestamps, record IDs, checksums, queue states, publish/PUBACK evolution, receive evidence, RF timeline, and LTE failure chronology needed for paper-grade tables/figures. The SHA values are integrity anchors, not substitutes for the raw data.

## Current consortium gate

Authority:

`docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`

Mission: determine how network-service recovery should be represented without allowing srsLTE testbed pathology to contaminate the B1-vs-W1 scientific comparison.

Work packages:

`RS-1 evidence reconstruction -> RS-2 LTE recovery review -> RS-3 estimand/H review -> RS-4 adversarial reviewer attack -> RS-5 prospective amendment -> RS-6 Golden E2E rehearsal design -> RS-7 GO/KILL`

Candidate recovery clocks:

- `t_rf_restore`
- `t_service_ready`
- `t_app_complete`

No protocol amendment is frozen yet.

## RS-1 offline reconstruction state

Canonical doctrine:

`docs/RS1_OFFLINE_RECONSTRUCTION.md`

Canonical sender-side tool:

`scripts/wp2_rs1a_sender_reconstruct.py`

The RS-1 tools are offline/read-only. They do not require an active POWDER reservation and must reconstruct evidence from copied/extracted preserved artifacts.

Planned sequence:

- RS-1A sender timeline/queue/RF reconstruction;
- RS-1B receiver receive/checksum reconstruction;
- RS-1C LTE/EPC/RAN chronology;
- RS-1D generated-vs-received-vs-durable-state reconciliation;
- RS-1E paper-grade tables and figures.

## Exact next action

Do **not** book or run another H trial yet.

1. Copy/extract the preserved H1 node archives to an offline analysis workspace when convenient.
2. Execute RS-1A through RS-1E and preserve derived artifacts with hashes.
3. Consortium RS-2 determines whether bounded LTE configuration/runtime repair can restore autonomous post-Q3 recovery without changing the RF protocol.
4. Consortium RS-3 decides recovery clocks and H semantics.
5. RS-4 adversarially reviews the proposal for confounding/censoring/fairness.
6. Only then draft/freeze a prospective protocol amendment (RS-5).
7. Freeze a non-scored Golden E2E rehearsal (RS-6).
8. `GO_REOPEN_H` only after RS-1..RS-6 PASS.

No scored run, WP3, or RF recalibration before that gate.

## Handover acceptance test for another agent

A replacement agent is ready only if it can state, without chat history:

- why H1 is valid adverse evidence rather than technical invalidity;
- why H is still unfrozen;
- why the clean-order LTE restart is not yet an approved in-trial action;
- where the raw evidence and integrity hashes are documented;
- what RS-1..RS-7 mean;
- that the immediate next work is offline reconstruction, not another reservation;
- that `scored_runs_authorized=false` remains mandatory.
