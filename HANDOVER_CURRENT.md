# WellPulse — Current Handover

Last updated: 2026-08-27 after validated K1–K8 pre-integration compatibility closure.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5 infrastructure/RF qualification: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Recovery-semantics RS-2..RS-7: **PASS / FROZEN**.
- WP2: **ACTIVE — GOLDEN REHEARSAL NOT YET PASSED**.
- Scientific weighted completion: **20%**.
- K1–K8 compatibility series: **PASS / CLOSED**.
- `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`.
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false` until the HCI/raw-evidence gate passes.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.

## Mission rule

The K-series is finished. Do **not** continue building automation for its own sake.

From this point, add infrastructure only when it is required to obtain or protect the next scientific result. Return immediately to the WP2 scientific path:

`HCI/raw-evidence gate -> clean non-scored Golden -> freeze H -> WP2 close -> WP3 -> WP4 -> WP5`.

## Workstation independence

Home and work PCs are interchangeable operator terminals only.

No future Golden/scored execution may depend on workstation-local history, downloads, tokens, or unique filesystem state. Canonical authority is GitHub + frozen repository state + GitHub Actions/secrets + verified evidence stores.

## H1 experiment of record — frozen

- Experiment: `WP-HCAL-E`
- UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`
- Profile: `PowderProfiles/srslte-controlled-rf`
- Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- Mapping: `enb1 -> nuc1`, `rue1 -> nuc2`
- Exact deployed WellPulse source commit: `95ba9a57bef159450b00b8a439d393d22e1c0519`
- H1 run: `wp2h1-a1-20260826-001`
- Scored: **NO**
- Frozen classification: `VALID_W1_RECOVERY_FAILURE`

H1 must never be replaced, repaired retroactively, or reclassified.

Known H1 raw archive hash anchors:

- nuc1: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

The original node-local raw bundles were not recovered after teardown. GitHub salvage is derived/provenance evidence only. PowerShell/local salvage is `CLOSED_NO_RECOVERY`. Do not claim record-level H1 raw recovery and do not reopen salvage without a genuinely new evidence source.

## Frozen H1 scientific record

- Q0/Q1/Q2/Q3: `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled.
- Q3 full-state duration: `120.000117905 s`.
- RF restoration / primary-cohort cutoff: `2026-08-26T18:16:00.428045+00:00`.
- Generated records: `361`.
- Primary cohort records: `211`.
- Final pending: `270`.
- Application inflight: `20`.
- Publish calls: `111`.
- PUBACK callbacks: `91`.
- Q0 pre-readiness: `5/5` ping PASS through `tun_srsue`.
- Post-restoration health: `0/3` ping.
- Sender status: `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`.
- Sender rc: `20`.

These survive as derived/live-captured summaries, not record-level raw evidence.

## H1 failure localization / recovery

Preserved evidence localizes the dominant H1 non-recovery below the WellPulse application layer in LTE core/session-context/IP continuity behavior. This does not demonstrate a WellPulse durable-queue failure.

Recovery characterization remains:

- UE-only restart: **FAIL**.
- EPC/eNB reset with UE left running: reset PASS; Q0/user-plane recovery **FAIL**.
- Clean ordered recovery `stop UE -> EPC -> eNB -> fresh UE`: **PASS**.
- Post-recovery Q0: 10/10 packets, 0% loss.
- Full LTE/TLS/MQTT v3.1.1/QoS1 path: **3/3 fresh sessions PASS** with payload hash equality.

Operational recovery knowledge only; no retroactive H1 repair.

## K1–K8 compatibility closure

Canonical record:

`docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`

Final status:

- `K1=PASS`
- `K2=PASS`
- `K3=PASS`
- `K4=PASS`
- `K5=PASS`
- `K6=PASS`
- `K7=PASS`
- `K8=PASS`

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

### Decisive bounded live compatibility run

Workflow:

`.github/workflows/wp2-kfastlane-live-compat-v2.yml`

Run:

`33085406598` — **success**

Experiment:

`fc7c2187-2376-4a92-8de1-4665a06ea943`

Classification:

`INFRASTRUCTURE_ONLY_NON_SCORED`

Observed/verified:

- Portal client pin PASS at revision `01be03b2f60c067815a7654437320dd981ca3617`;
- status `provisioning -> provisioned -> ready`;
- exact experiment-ID binding;
- unique authoritative expiry `2026-08-27T16:00:53Z`;
- time gate PASS: 3283 s remaining vs 2700 s required;
- bindings `enb1 -> nuc1`, `rue1 -> nuc2`, UE type `srsue`;
- hardware `nuc5300` on both nodes;
- image `urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1`;
- profile revision `a6da96560b6526dc6816761282722c996418fd8c` on both nodes;
- controller SSH PASS;
- `/proj/WellPulse` writable on both nodes;
- K4 detached-process return: 1 s under 15 s bound;
- K6 cross-node `/proj/WellPulse` write/read/hash PASS;
- controller bundle SHA-256 `f5464e08b41e2bcb81facd26daa2ee11ad115fa06554d40eea9bc01e0b0e6616`;
- GitHub artifact ID `9652138428`, artifact ZIP digest `7d0333519e4446ed216672e86962d59973a947b0392680e6249028a604292cc2`;
- independent artifact download/read-back and internal hashes PASS;
- `CONTROLLER_OFFPOWDER_GATE=PASS`;
- `EVIDENCE_ESCROW_GATE=PASS`;
- `TEARDOWN_AUTHORIZED=YES` only after verified controller round-trip;
- no independent RF observation command executed;
- mandatory termination requested.

### Offline closure after live run

- K3 Portal CLI QA run `33087174307`: **success**.
- K7 semantic observation guard run `33087181821`: **success**.
- Integrated K2–K7 static acceptance run `33087199247`: **success**.

The previous false-confidence `! grep` K7 assertion has been replaced in the integrated gate by `scripts/wp2_k7_active_workflow_guard.py`, which ignores comments/search assertions and fails on executable-looking unsafe RF invocations.

### Frozen controller/supply-chain facts

- Portal repo: `https://gitlab.flux.utah.edu/emulab/portal-api.git`
- Portal revision: `01be03b2f60c067815a7654437320dd981ca3617`
- Portal source capture SHA-256: `3e9f0073b2df6840801baa38333f1f04debd02a2eaa57997939b6f7ee678d4c8`
- uv `0.12.1`, SHA-256 `90b2f223fb69d19db49e117da601f64978593417988530aa733d456141b4bcbb`
- isolated scientific Python `3.11.13`
- `paho-mqtt=2.1.0`
- rclone `1.75.0`, SHA-256 `aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa`
- runner label `ubuntu-24.04`; observed successful live image `20260823.283.1`
- checkout `fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09`
- upload-artifact `b7c566a772e6b6bfb58ed0dc250532a479d7789f`
- download-artifact `37930b1c2abaa49bbe596cd826c3c89aef350131`

Do not revert to moving tags.

## Evidence architecture — frozen critical path

`POWDER raw -> /proj/WellPulse persistent escrow -> controller pull -> GitHub Actions artifact -> independent controller download/read-back -> outer + internal hash verification -> teardown authority`

Google Drive/rclone is not teardown-critical. Drive may be an optional secondary mirror later.

The Golden node phase must never authorize teardown by itself. It must leave:

- `CONTROLLER_OFFPOWDER_GATE=PENDING`
- `TEARDOWN_AUTHORIZED=NO`

Only verified controller round-trip may emit:

- `CONTROLLER_OFFPOWDER_GATE=PASS`
- `EVIDENCE_ESCROW_GATE=PASS`
- `TEARDOWN_AUTHORIZED=YES`

## Historical first compatibility failure — retain as provenance only

The first compatibility run `33084240768`, experiment `02bc305d-5d84-48f9-b518-dbebd1728ee6`, entered `provisioning -> failed`. It ran no science. Cleanup was requested; later read-only diagnosis run `33086065236` verified `No such experiment` and absence from `experiment list`.

The exact original provisioning root cause was not recoverable post-cleanup. Do not infer one. The subsequent v2 compatibility run succeeded with the known-good binding contract and is the decisive K2–K8 acceptance evidence.

## Current WP2 frontier

The K-series is no longer the blocker.

The next and only active prerequisite is:

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`

It must close before any Golden rebooking.

Required outcome:

1. passive, one-way HCI only;
2. `HCI_CONTROL_ACTIONS_ENABLED=false`;
3. no independent unqualified pull/probe during protected science;
4. complete raw-evidence inventory independent of HCI summaries;
5. raw freeze/hash to `/proj/WellPulse` before destructive teardown;
6. controller off-POWDER artifact read-back/hash verification before teardown authority.

Do not add automation beyond what is necessary for these scientific-evidence requirements.

After this gate passes:

`one clean non-scored Golden G0–G10 -> verified raw evidence -> requalify/freeze H -> WP2 scientific close -> explicit scored authorization -> WP3`.

## Scientific WP state

- WP0 — Novelty & Venue Lock: **PASS**, 8/8.
- WP1 — Confirmatory Protocol & Statistics Freeze: **PASS/FROZEN**, 12/12.
- WP2 — RF Calibration & Measurement Validation: **ACTIVE**, compatibility closed; HCI/raw gate + Golden + H remain.
- WP3 — Conducted-RF Confirmatory Campaign: **BLOCKED ON WP2**, 0/30.
- WP4 — OTA External Replication: **BLOCKED**, 0/15.
- WP5 — Analysis + Artifact + Paper Closure: **PREPARED, NOT EXECUTED**, 0/20.

Scientific weighted completion remains **20%** until WP2 closes.

## Frozen scientific controls

- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false` until HCI/raw gate PASS.
- primary cohort cutoff remains `t_rf_restore`.
- application horizon remains 300 s from `t_service_ready`.
- no B1/W1/B2 scored work is authorized.

## Repository hygiene

C0..C4 remain PASS / closed. Do not reintroduce archived live workflows casually.

## Mandatory read order

1. `HANDOVER_CURRENT.md`
2. `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`
3. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
4. `docs/NEXT_GATE.md`
5. `docs/GITHUB_POWDER_COMPATIBILITY_MATRIX_2026-08-27.md`
6. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
7. `experiments/WP-PWD01/protocol.md`
8. `experiments/WP-PWD01/evidence-schema.md`
9. `scripts/wp2_golden_orchestrator.sh`
10. `scripts/wp2_controller_pull_persistent_escrow.sh`
11. `scripts/wp2_controller_verify_artifact_roundtrip.sh`

## Exact next action

**STOP after K8 reconciliation. Do not create a Golden reservation in this patch.**

On explicit resume, execute one bounded HCI/raw-evidence closure patch only. Close `LIVE_HCI_AND_RAW_EVIDENCE_GATE` from actual contract/evidence, then STOP before Golden unless separately authorized.

Shortest mission path:

`HCI/raw gate -> clean non-scored Golden -> freeze H -> WP2 close -> WP3 -> WP4 -> WP5`
