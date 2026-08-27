# WellPulse — Current Handover

Last updated: 2026-08-27 after **WP2-P5 HCI & Raw-Evidence Closure PASS**.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- Last accepted checkpoint: **WP2-P5 PASS / CLOSED / STOPPED BEFORE GOLDEN**.
- Scientific weighted completion: **20%**.
- WP2 management/readiness progress: **80/100**; this creates no partial scientific credit.
- WP0: **PASS**, 8/8.
- WP1: **PASS / FROZEN**, 12/12.
- WP2: **ACTIVE** — P1-P5 closed; P6 Golden + P7 formal closure remain.
- WP3: **BLOCKED ON WP2**, 0/30.
- WP4: **BLOCKED**, 0/15.
- WP5: **PREPARED / NOT EXECUTED**, 0/20.
- FIT IoT-LAB layer: **FINAL PASS**.
- POWDER G0-G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- K1-K8 compatibility series: **PASS / CLOSED**.
- `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`.
- `AUDIT_R1=PASS`.
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.
- `REBOOK_GOLDEN=false`.
- `scored_runs_authorized=false`.

**STOP.** Do not perform the POWDER resource preflight, contact POWDER, create/modify/terminate a reservation, SSH to POWDER, execute Golden, run H calibration, execute B1/W1/B2 scored work, reopen K1-K8, reopen RF calibration, or reopen H1 salvage until a separate explicit user continuation.

## Canonical closure/control records

Current P5 closure:

`docs/WP2_P5_HCI_RAW_EVIDENCE_CLOSURE_2026-08-27.md`

Frozen HCI/raw-evidence contract:

`docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`

Audit + AUDIT-R1 closure:

`docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`

Canonical supersession map:

`docs/AUDIT_R1_SUPERSESSION_MAP_2026-08-27.md`

Workflow deactivation provenance:

`docs/AUDIT_R1_WORKFLOW_DEACTIVATION_2026-08-27.md`

Current next-gate record:

`docs/NEXT_GATE.md`

Current milestone state:

`docs/MILESTONE_STATUS.md`

## Revised WP2 management decomposition

| Patch | Scope | Internal share | Status |
|---|---|---:|---|
| WP2-P1 | RF Foundation | 20% | PASS / FROZEN |
| WP2-P2 | Recovery Semantics | 15% | PASS / FROZEN |
| WP2-P3 | Platform Compatibility | 20% | PASS / CLOSED |
| WP2-P4 | Pre-Golden Reconciliation / AUDIT-R1 | 15% | PASS / CLOSED |
| WP2-P5 | HCI & Raw-Evidence Closure | 10% | **PASS / CLOSED** |
| WP2-P6 | One clean non-scored Golden | 15% | **BLOCKED / NOT STARTED** |
| WP2-P7 | Formal WP2 scientific closure + scored authorization decision | 5% | **BLOCKED / NOT STARTED** |

`WP2_MANAGEMENT_READINESS_PROGRESS=80/100`

Scientific weighted completion remains **20%** until WP2-P7 closes WP2 scientifically.

## WP2-P5 closure summary

`WP2_P5=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

P5 acceptance: **100/100**.

### P5.1 — passive HCI contract — PASS — 20/20

Implemented:

`scripts/wp2_golden_hci_emit.py`

Integrated only through:

`scripts/wp2_golden_orchestrator.sh`

Frozen one-way architecture:

`orchestrator-owned gate/state -> passive wp2-hci-v1 JSONL/stdout`

Prohibited:

`HCI -> SSH/API/tmcc/live probe/control -> experiment`

The observer emits `orchestration/hci_events.jsonl` and `HCI_EVENT=<json>` stdout. It contains bounded identity/gate/phase/progress/safety state only; no raw payloads, credentials, TLS secrets or arbitrary gate detail.

HCI failure is explicitly non-authoritative/non-fatal:

`HCI_OBSERVER=DEGRADED_NON_AUTHORITATIVE`

and cannot stop or invalidate scientific execution.

### P5.2 — exact raw-evidence contract — PASS — 30/30

Frozen inventory:

`experiments/WP-PWD01/evidence_inventory_golden_v1.txt` v1.5.

Authoritative scientific gate chronology remains:

`orchestration/gate_events.jsonl`

HCI is intentionally:

`CONDITIONAL|orchestration/hci_events.jsonl`

It is preserved/hashed when present but is **not** mandatory scientific evidence and cannot replace raw sender/receiver/RF/substrate/runtime/reconstruction artifacts.

### P5.3 — finalization/teardown contract — PASS — 25/25

No background/in-run `/proj` checkpoint is enabled during protected G3-G7 science.

Frozen sequence:

`G3-G7 protected acquisition/observation -> G8 reconstruction -> G9 freeze/hash/persistent /proj escrow -> controller finalization`

Node/persistent side may emit only:

- `RAW_EVIDENCE_COMPLETE=PASS`;
- `PERSISTENT_ESCROW_GATE=PASS`;
- `CONTROLLER_OFFPOWDER_REQUIRED`;
- `TEARDOWN_AUTHORIZED=NO`.

Only successful independent controller artifact round-trip may emit:

- `CONTROLLER_PULL_GATE=PASS`;
- `CONTROLLER_BUNDLE_SHA256=<64hex>`;
- `CONTROLLER_OFFPOWDER_GATE=PASS`;
- `ROUNDTRIP_BUNDLE_SHA256=<same_64hex>`;
- `EVIDENCE_ESCROW_GATE=PASS`;
- `TEARDOWN_AUTHORIZED=YES`.

Mandatory path:

`POWDER raw -> /proj/WellPulse persistent escrow -> controller pull -> GitHub Actions artifact -> independent controller download/read-back -> outer + internal SHA-256 verification -> teardown authority`

Google Drive/rclone is optional secondary mirroring only.

### P5.4 — bounded offline QA — PASS — 15/15

No POWDER or Drive contact was used.

Accepted P5-specific checks:

- `EMITTER_QA=PASS`;
- `HCI_FAILURE_ISOLATION_QA=PASS`;
- `INVENTORY_HCI_SEPARATION_QA=PASS`;
- `PERSISTENT_CONTROLLER_ROUNDTRIP_MODEL_QA=PASS`;
- `TEARDOWN_PRE_CONTROLLER=NO`.

The existing offline workflow `.github/workflows/wp2-golden-offline-qa.yml` was extended to compile/test the passive HCI contract and retained reconstruction/escrow/interlock checks. No new live workflow was added.

The connector available during P5 did not expose a reliable private-repository listing of push-triggered Actions runs, therefore **no new Actions run ID is claimed for P5**. Existing accepted runtime evidence for the unchanged off-POWDER transport remains AUDIT-R1 run `33092849805`.

### P5.5 — governance/canonical closure — PASS — 10/10

Current status, workflow registry, supersession map, next gate and this handover were reconciled. P5 does not authorize P6.

No POWDER contact, reservation, SSH, Golden, H calibration, scored execution, RF recalibration, K reopening or H1 salvage occurred during P5.

## Governing scientific state — frozen

Recovery Semantics Amendment v1 remains scientific authority:

- `t_rf_restore`, `t_service_ready`, `t_app_complete` are distinct;
- primary cohort = valid records generated at or before `t_rf_restore`;
- **`H_app=300 s from t_service_ready`** is prospectively frozen;
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`;
- preserve `T_service`, `T_app`, `T_total`;
- S2/S3 clean ordered restore = `stop UE -> EPC -> eNB -> fresh UE -> architecture-blind service-ready probe`;
- Golden G6 qualification bound = 120 s;
- negative/null outcomes remain valid scientific evidence;
- W1/Golden/scored outcome-driven H changes are prohibited.

Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled. Do not reopen RF calibration.

There is **no future H-calibration/freeze step**.

## H1 — frozen adverse experiment of record

- experiment `WP-HCAL-E`;
- UUID `9153e16a-1eb1-45f5-88bf-303636a9d1ec`;
- run `wp2h1-a1-20260826-001`;
- profile revision `a6da96560b6526dc6816761282722c996418fd8c`;
- mapping `enb1 -> nuc1`, `rue1 -> nuc2`;
- exact deployed WellPulse commit `95ba9a57bef159450b00b8a439d393d22e1c0519`;
- classification **`VALID_W1_RECOVERY_FAILURE`**;
- scored: **NO**.

Original H1 node-local raw bundles were **not recovered** after teardown. GitHub/local salvage is derived/provenance only. POWDER support confirmed the node-local disks were reloaded after termination while `/proj` persists across experiments. Do not reopen H1 salvage, rerun H1 to select H, or relabel the adverse result.

## K1-K8 — closed

Canonical record:

`docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`

Decisive compatibility evidence:

- historical workflow `wp2-kfastlane-live-compat-v2.yml`;
- Actions run `33085406598` — success;
- experiment `fc7c2187-2376-4a92-8de1-4665a06ea943`;
- classification `INFRASTRUCTURE_ONLY_NON_SCORED`.

K1-K8 remain PASS/CLOSED absent a material interface change.

## Workflow/governance surface

Exactly **6** active offline/static workflows remain:

1. `local-gate-once.yml`
2. `local-unit-tests.yml`
3. `wp2-b2-semantics.yml`
4. `wp2-golden-offline-qa.yml`
5. `wp2-offpowder-artifact-qa.yml`
6. `wp2-preintegration-static.yml`

Exactly **4** root sentinels remain:

- `.local-gate-trigger`
- `.wp2-b2-semantics-trigger`
- `.wp2-offpowder-artifact-qa-trigger`
- `.wp2-preintegration-static-trigger`

No active workflow is currently authorized to contact/mutate POWDER or launch Golden/scored work.

## Current exact frontier — STOPPED before WP2-P6

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

`HCI_CONTROL_ACTIONS_ENABLED=false`

The next bounded patch is:

`WP2-P6 — ONE CLEAN NON-SCORED GOLDEN REHEARSAL`

**Status: BLOCKED / NOT STARTED.**

Do not begin P6 until the user separately and explicitly continues.

When separately authorized, the shortest path is:

1. immediately before booking, perform protocol v0.6.1 advisory resource-availability preflight at `https://www.powderwireless.net/resinfo.php`;
2. record `RESOURCE_AVAILABILITY_PREFLIGHT=PASS|DEFER|UNKNOWN`;
3. never silently change frozen hardware/profile/bindings to chase capacity;
4. use Portal lifecycle/READY/manifest as authoritative;
5. book exactly one clean non-scored Golden;
6. execute frozen G0-G10 using passive HCI only;
7. reconstruct from raw evidence;
8. complete G9 persistent escrow and independent controller artifact round-trip;
9. require `EVIDENCE_ESCROW_GATE=PASS` and `TEARDOWN_AUTHORIZED=YES` before teardown;
10. STOP and perform WP2-P7 formal scientific closure/scored authorization decision separately.

## Shortest mission path

`AUDIT-R1 PASS -> WP2-P5 PASS -> STOP -> separate explicit user resume -> resinfo advisory preflight -> one clean non-scored Golden -> WP2-P7 closure/scored authorization -> WP3 -> WP4 -> WP5`

## Mandatory read order for the next agent

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P5_HCI_RAW_EVIDENCE_CLOSURE_2026-08-27.md`
3. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
4. `docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`
5. `docs/AUDIT_R1_SUPERSESSION_MAP_2026-08-27.md`
6. `docs/AUDIT_R1_WORKFLOW_DEACTIVATION_2026-08-27.md`
7. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
8. `experiments/WP-PWD01/protocol.md`
9. `docs/NEXT_GATE.md`
10. `docs/MILESTONE_STATUS.md`
11. `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`
12. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
13. `experiments/WP-PWD01/evidence_inventory_golden_v1.txt`
14. `experiments/WP-PWD01/evidence-schema.md`
15. `experiments/WP-PWD01/analysis-plan.md`
16. `experiments/WP-PWD01/run-matrix.yaml`
17. `scripts/wp2_golden_hci_emit.py`
18. `scripts/wp2_golden_orchestrator.sh`
19. `scripts/wp2_golden_evidence_escrow.sh`
20. `scripts/wp2_controller_pull_persistent_escrow.sh`
21. `scripts/wp2_controller_verify_artifact_roundtrip.sh`
22. `scripts/wp2_golden_offline_qa.sh`
23. `scripts/reconstruct_wp2_golden.py`
24. `src/wellpulse/powder_analysis.py`
25. `docs/WORKFLOW_REGISTRY.md`
26. `AGENTS.md`

**STOP / HANDOVER READY.**
