# WellPulse — Current Handover

Last updated: 2026-08-27 after H1-GitHub Salvage Patch.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5 infrastructure/RF qualification: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Recovery-semantics RS-2..RS-7: **PASS / FROZEN**.
- WP2: **ACTIVE — GOLDEN REHEARSAL NOT YET PASSED**.
- Scientific weighted completion: **20%**.
- Repository workflow cleanup: **CLOSED / 100% — C0..C4 PASS**.
- H1 GitHub salvage: **PASS as derived-evidence consolidation; raw recovery failed**.
- `H = UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.

## Mandatory patch discipline

All work remains bounded:

`execute exactly one declared patch -> PASS/BLOCKED -> update canonical handover/status -> STOP -> resume only on explicit user instruction`

Never start the next patch before the user explicitly resumes, even when it is obvious or offline-only.

## Current scientific frontier

### H1 experiment of record

- Experiment: `WP-HCAL-E`
- UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`
- Profile: `PowderProfiles/srslte-controlled-rf`
- Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- Mapping: `enb1 -> nuc1`, `rue1 -> nuc2`
- Exact deployed WellPulse source commit: `95ba9a57bef159450b00b8a439d393d22e1c0519`
- H1 run: `wp2h1-a1-20260826-001`
- Scored: **NO**
- Frozen classification: `VALID_W1_RECOVERY_FAILURE`

H1 must never be replaced or reclassified.

### H1 preserved high-level result

- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled.
- Q3 full-state duration: `120.000117905 s`.
- RF restoration / primary-cohort cutoff: `2026-08-26T18:16:00.428045+00:00`.
- Generated records: `361`.
- Primary cohort: `211`.
- Final pending: `270`.
- Application inflight: `20`.
- Publish calls: `111`.
- PUBACK callbacks: `91`.
- Q0 pre-readiness: `5/5` ping PASS through `tun_srsue`.
- Post-restoration health: `0/3` ping.
- Sender status: `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`.
- Sender rc: `20`.

These counts/timestamps survive as Git-native derived/live-captured summaries; they are not a substitute for the missing record-level corpus.

### H1 failure localization

The preserved evidence shows radio/eNB recovery sufficient for later uplink CRC-OK traffic while the user-plane remained unusable. EPC/MME/SPGW logs recorded attach/session-context churn, including stale UE context/GTP-C behavior and successive UE IP allocations while the UE tunnel retained its prior address.

The dominant failure is therefore localized below the WellPulse application layer in LTE core/session-context/IP continuity. This does **not** demonstrate a WellPulse durable-queue failure. H1 nevertheless remains a valid W1 recovery failure because the required user-plane recovery did not occur inside the frozen bound.

### Recovery characterization

- UE-only restart: **FAIL**.
- EPC/eNB reset with UE left running: core/RAN reset PASS, Q0/user-plane recovery **FAIL**.
- Clean ordered recovery `stop UE -> EPC -> eNB -> fresh UE`: **PASS**.
- After clean-order recovery, Q0 returned with 10/10 packets and 0% loss.
- Exact WellPulse application path was then requalified through LTE/TLS/MQTT v3.1.1/QoS1 and passed **3/3 fresh sessions**, including payload SHA-256 equality.

This is operational recovery knowledge only; it does not retroactively repair H1 or authorize scored runs.

## H1-GitHub Salvage — CLOSED

### Verdict

`H1_GITHUB_SALVAGE=PASS`

`H1_FULL_RAW_FROM_GITHUB=NOT_RECOVERED`

`H1_DERIVED_LOG_EVIDENCE=AVAILABLE`

`H1_RECORD_LEVEL_RECONSTRUCTION_FROM_GITHUB=BLOCKED`

`RS1_RAW_RECONSTRUCTION=BLOCKED_ON_RAW_BUNDLES`

### Canonical salvage artifacts

- `evidence/powder/h1-github-salvage-2026-08-27.md`
  - creation commit: `a3cccf1cb6999e213ac47da681ecc31c0cd4fc6e`
  - evidence class: `DERIVED_GIT_GITHUB_SALVAGE`
- `evidence/powder/h1-github-salvage-manifest-2026-08-27.json`
  - creation commit: `e438e910a80495bc76351def6c6080fb6aa2cb60`
  - schema: `wellpulse.h1-github-salvage.v1`

### GitHub negative-recovery evidence

Re-verified during salvage:

- H1 classification commit `9cd7789a8960fd396ba35806127c16251ea8574a` has **0 associated Actions workflow runs**.
- H1 archive-hash commit `375f767bae237729458f558b1c64c60633c00673` has **0 associated Actions workflow runs**.
- Relevant pre-H live SSH workflow run `32993568290` has **0 uploaded Actions artifacts**.
- `data/raw/` contains only `.gitkeep`.
- `results/runs/` contains only `.gitkeep`.

Therefore GitHub cannot yield the missing H1 raw CSV/JSONL/SQLite/log/tar bytes.

### Storage correction

Historical 2026-08-26 evidence files described `/users/aayoub/wellpulse-powder-evidence/...` as persistent POWDER home storage. Later lifecycle review established that this location was node-local/non-durable for the relevant teardown lifecycle.

The current handover and salvage package supersede that historical **storage characterization**. Historical files remain unchanged as provenance.

The node archive/hash records survive only as integrity anchors; their original bytes are unavailable because they were not copied to `/proj/WellPulse` or off POWDER before teardown.

### Historical hash anchors retained

Original H1 archives:

- nuc1: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

Recovery-characterization archives:

- nuc1: `71aaea25a50ad955fa797a358b14cce4efc0e76ec0861468b3b99dd224c7dd55`
- nuc2: `431855c8662fa46a82f7baca60b5f3deeda4fd849cf4d90bfc4889800be3e71d`

Reproducibility fingerprints:

- nuc1 runtime record: `1ef8b04a8d3a634c1cc3ded2b84c80a7140d877758a0d63010411971eab8607f`
- nuc1 archive: `af601716237082be410be3680f1e33b36240beae77e7b644f0f5bef811c1b647`
- nuc2 runtime record: `fc1c131602c49b8376733ad8e190c4fc5d8d1976b62fe59c1e5becbe41cf8d5a`
- nuc2 archive: `ada35310a2dd46dba6c28a26604d41f28884799e0fc27c0846a7bf66421935bc`

Node-local chain-of-custody manifests:

- nuc1: 22 files; `9596f23f4e9359d3395f29f6e0081d5acdec05dc6a986c0e0b0f19ac5fa35811`
- nuc2: 34 files; `343a9deb1e432c0f5d30cbf55def3d133726a214a595d9f7f0723a5e87d8ec2e`

### RS-1 limitation

`docs/RS1_OFFLINE_RECONSTRUCTION.md` remains a valid raw-reconstruction method, but it requires unavailable raw artifacts including:

- `sender_summary.json`
- `calibration_manifest.json`
- `attenuation_timeline.csv`
- `telemetry_generated.csv`
- `queue_timeline.csv`
- `mqtt_events.jsonl`
- `w1_queue.sqlite`
- receiver raw events/record identities
- full UE/eNB/EPC/SPGW logs

RS-1A..RS-1E therefore cannot be closed from GitHub alone. Do not infer record-level duplicate/missing counts, queue trajectory, exact event ordering, or receiver reconciliation from the derived summaries.

No scientific completion credit was added by salvage.

## Golden A3 state

Experiment `WP-GOLDEN-A3`, UUID `357f3275-403d-491a-906f-99677bdf454f`, is expired/removed and must not be reused.

### Attempt 6

- Workflow run `33067316888`.
- G0..G6 PASS.
- G7 `DIAGNOSTIC_NONCANONICAL` because a supposedly read-only workflow invoked `tmcc attenuator <id>` and POWDER reported `changing attenuation`.
- G8/G9/G10 not reached.
- Scored: NO.

### Attempt 7

- Workflow run `33069500256`.
- Static/no-create/no-scored and encrypted Drive pre-mutation gates passed.
- Stopped before science when the Portal API returned `404 No such experiment` for A3.
- Scored: NO.

`REBOOK_GOLDEN=false` remains mandatory.

## Repository hygiene program — CLOSED / 100%

- C0 inventory/classification: PASS.
- C1 archived 12 expired A3 workflows + 12 A3 request/trigger files; key commit `169b5632d2db20a9cda0ac7cc2633f68b2316024`.
- C2 archived 16 FIT-specific workflows after FIT FINAL PASS; key commit `4d10df3bc6de3492d661d34dee51599452d6eed1`.
- C3 archived 22 historical/live POWDER workflows + 20 stale POWDER trigger/request files; key commit `1cde375d07504567afe78383db3f3eb6a69e46b5`.
- C4 created `docs/WORKFLOW_REGISTRY.md` and `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md`; PASS.
- Total workflows removed from active Actions path: **50**.
- Exactly six local/offline/static workflows remain active; none contacts live POWDER.
- Historical workflow names/runs may remain visible in GitHub Actions as audit history. Do not manually re-run archived live-testbed workflows.

## Mandatory integration and raw-evidence gates

Before any future GitHub Actions <-> POWDER live integration:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

and

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

are both mandatory.

Current compatibility status remains **BLOCKED**.

Material remaining compatibility items include:

- immutable supply-chain/runtime pinning for future live workflows;
- Portal API exact pinned upstream revision plus lifecycle/status/error semantics;
- `uv` pinning;
- rclone exact version/checksum and dedicated Drive OAuth/write-read-hash validation;
- exact OpenSSL/Mosquitto live runtime fingerprints;
- receiver-start SSH/detach semantics;
- prelaunch reservation-time budget guard;
- `/proj/WellPulse` write/read/hash persistence validation on the next reservation;
- authoritative `tmcc attenuator` command/observation semantics;
- prohibition of independent unqualified probes during G3–G10;
- passive HCI runtime acceptance.

No live integration is allowed while this gate is BLOCKED.

## HCI and evidence doctrine

Scientific Raw-Data Plane and HCI/display plane remain separate.

- Raw scientific records are authoritative.
- HCI is derived/passive/non-authoritative.
- HCI consumes orchestrator/process-emitted events only during G3–G10.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.
- No independent SSH/API/tmcc/poll/probe/restart/reconfiguration during the protected scientific window unless separately proven safe and prospectively admitted.

Before teardown of every future rehearsal/calibration/scored run require:

`RAW_EVIDENCE_COMPLETE=PASS`

`EVIDENCE_ESCROW_GATE=PASS`

`TEARDOWN_AUTHORIZED=YES`

Required evidence sequence:

`freeze writers -> inventory mandatory raw -> hash -> /proj/WellPulse/evidence-escrow/... -> verify -> off-POWDER copy -> read-back/hash verify -> provenance record -> teardown`

## Frozen scientific state

- H1 remains `VALID_W1_RECOVERY_FAILURE`.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`.
- Attenuation IDs `1 33 2 34` remain coupled.
- Recovery-semantics amendment v1 and protocol v0.6 remain frozen.
- Primary cohort cutoff remains `t_rf_restore`.
- Application horizon remains 300 s from `t_service_ready`.
- No scored B1/W1/B2 run is authorized.
- H1 raw record-level bundles remain unavailable from user-accessible persistent storage.
- Scientific weighted completion remains **20%**.

## Mandatory current read order

1. `HANDOVER_CURRENT.md`
2. `docs/NEXT_GATE.md`
3. `evidence/powder/h1-github-salvage-2026-08-27.md`
4. `evidence/powder/h1-github-salvage-manifest-2026-08-27.json`
5. `docs/WORKFLOW_REGISTRY.md`
6. `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md`
7. `AGENTS.md`
8. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
9. `docs/GITHUB_POWDER_COMPATIBILITY_MATRIX_2026-08-27.md`
10. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
11. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
12. `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`
13. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
14. `experiments/WP-PWD01/protocol.md`
15. `experiments/WP-PWD01/evidence-schema.md`

## Exact next action

**STOP after H1-GitHub Salvage handover closure.**

On the next explicit user resume, execute exactly one bounded patch:

### K1 — Offline supply-chain/runtime pin closure

Scope: close only the compatibility blockers that can be solved without contacting or reserving POWDER. At minimum:

1. inventory all moving references in the future Golden/integration path;
2. replace or freeze GitHub Actions used by the future live path to immutable SHAs where applicable;
3. freeze the exact Portal API client upstream revision instead of cloning moving HEAD;
4. freeze `uv` and any remaining bootstrap tool versions/checksums;
5. verify the existing rclone exact-version/checksum contract consistently across the intended future path;
6. extend static acceptance so moving/unpinned references fail closed;
7. update the compatibility matrix with only evidence actually closed offline.

K1 must not contact POWDER, create a reservation, run a live probe, or claim the entire Pre-Integration Compatibility Gate has passed.

Close K1 with PASS/BLOCKED, update this handover, and STOP again.

## Handover acceptance test

A replacement agent is ready only if it can state:

- scientific completion is 20%;
- H1 is permanently `VALID_W1_RECOVERY_FAILURE` and H remains unfrozen;
- H1 raw record-level data were **not** recovered from GitHub;
- H1 GitHub salvage is PASS only as derived-evidence/provenance consolidation;
- the two canonical salvage artifacts and their evidence boundary;
- RS-1 raw reconstruction remains blocked by missing raw bundle bytes;
- the `/users/aayoub` historical persistence characterization is superseded by the later lifecycle audit;
- A3 is expired/removed and must not be reused;
- repository cleanup C0–C4 is complete and active Actions are local/offline/static only;
- Pre-Integration Compatibility and Live-HCI/Raw-Evidence gates remain mandatory and not passed;
- `scored_runs_authorized=false` and `REBOOK_GOLDEN=false`;
- the next patch is K1 offline pin closure;
- every patch must end with a handover update and STOP before the next patch.