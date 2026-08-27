# WP2-P5 — HCI & Raw-Evidence Closure — 2026-08-27

## Verdict

`WP2_P5=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

`HCI_CONTROL_ACTIONS_ENABLED=false`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

`POWDER_CONTACT=NO`

`GOLDEN_EXECUTED=NO`

This closure is an offline implementation/contract/readiness result. It does not authorize a POWDER reservation, Golden rehearsal, H calibration, or scored B1/W1/B2 work.

Scientific weighted completion remains **20%** because WP2 is not scientifically closed. Under the revised internal WP2 management decomposition, P1-P5 are now closed and WP2 management/readiness progress is **80/100**; P6 Golden and P7 formal WP2 scientific closure remain open.

## Acceptance units

| Unit | Weight | Result | Closure basis |
|---|---:|---|---|
| P5.1 — passive HCI contract | 20% | PASS | `wp2-hci-v1` observer implemented; orchestrator-owned state only; no independent probe/control plane; observer failure is non-fatal/non-authoritative. |
| P5.2 — exact raw-evidence contract | 30% | PASS | Golden inventory v1.5 freezes exact required scientific evidence and controller signals; HCI file is conditional/non-authoritative and cannot substitute for raw evidence. |
| P5.3 — finalization/teardown contract | 25% | PASS | Protected science has no background `/proj` checkpoint; G9 persistent escrow occurs after G8 reconstruction; only controller artifact read-back plus outer/internal SHA-256 verification can authorize teardown. |
| P5.4 — bounded offline QA | 15% | PASS | Passive event generation/schema, HCI failure isolation, HCI/raw inventory separation, persistent/controller round-trip model, and fail-closed teardown semantics passed offline. Existing qualified controller/off-POWDER runtime path remains unchanged. |
| P5.5 — governance/canonical closure | 10% | PASS | Frozen HCI/raw contract, closure record, next-gate/status/workflow control and canonical handover reconciled; STOP retained before Golden. |

`WP2_P5_ACCEPTED_PROGRESS=100/100`

## 1. Passive HCI implementation

Implementation:

`scripts/wp2_golden_hci_emit.py`

Integration point:

`scripts/wp2_golden_orchestrator.sh`

The observer is strictly one-way:

`orchestrator-owned gate/state -> passive HCI JSONL/stdout`

It does not implement SSH, API, `tmcc`, network polling, RF observation, restart, reconfiguration or teardown behavior.

The machine-readable stream is:

`orchestration/hci_events.jsonl`

Schema:

`wp2-hci-v1`

Each successful event is also emitted to orchestrator stdout as `HCI_EVENT=<json>`, providing the PI a usable live GitHub Actions fallback view without a second testbed probe.

The observer wrapper is explicitly fail-independent. If HCI emission fails, the orchestrator records:

`HCI_OBSERVER=DEGRADED_NON_AUTHORITATIVE`

and continues scientific execution. HCI failure alone cannot invalidate a run.

## 2. Raw evidence remains authoritative

Frozen exact inventory:

`experiments/WP-PWD01/evidence_inventory_golden_v1.txt` v1.5

The authoritative gate chronology remains:

`orchestration/gate_events.jsonl`

The HCI stream is intentionally classified:

`CONDITIONAL|orchestration/hci_events.jsonl`

Therefore:

- HCI is preserved and hashed when present;
- absence/failure of HCI alone does not fail scientific evidence completeness;
- HCI cannot replace sender/receiver/RF/substrate/runtime/reconstruction evidence;
- HCI cannot issue evidence or teardown authority.

## 3. Protected-window I/O rule

No new in-run/background `/proj` checkpoint mechanism is enabled.

The shortest frozen sequence remains:

`G3-G7 protected acquisition/observation -> G8 reconstruction -> G9 freeze/hash/persistent escrow -> controller finalization`

This avoids adding unqualified I/O load during the protected scientific window. A future in-run checkpoint mechanism would require a separate non-perturbation qualification before authorization.

## 4. Final evidence and teardown authority

Mandatory path remains:

`POWDER raw -> /proj/WellPulse persistent escrow -> controller pull -> deterministic TAR -> GitHub Actions artifact -> independent controller download/read-back -> outer TAR SHA-256 + internal SOURCE_SHA256SUMS verification -> teardown authority`

Persistent/node-side closure may establish only:

- `RAW_EVIDENCE_COMPLETE=PASS`;
- `PERSISTENT_ESCROW_GATE=PASS`;
- `CONTROLLER_OFFPOWDER_REQUIRED`;
- `TEARDOWN_AUTHORIZED=NO`.

Only successful controller finalization may establish:

- `CONTROLLER_PULL_GATE=PASS`;
- `CONTROLLER_BUNDLE_SHA256=<64hex>`;
- `CONTROLLER_OFFPOWDER_GATE=PASS`;
- `ROUNDTRIP_BUNDLE_SHA256=<same_64hex>`;
- `EVIDENCE_ESCROW_GATE=PASS`;
- `TEARDOWN_AUTHORIZED=YES`.

Google Drive/rclone remains optional secondary mirroring only.

## 5. Bounded offline QA evidence

The P5 implementation was checked without POWDER or Drive contact.

Accepted checks include:

1. passive emitter syntax/behavior and `wp2-hci-v1` schema;
2. `hci_control_actions_enabled=false`;
3. `independent_probes=DISABLED`;
4. no arbitrary raw/gate detail in the HCI event;
5. forced observer failure remains non-fatal to its caller;
6. HCI inventory class is conditional rather than required;
7. mandatory scientific inventory can close without an HCI file;
8. persistent-copy/internal-hash model remains valid;
9. controller bundle/round-trip outer hash and internal hash model remains valid;
10. teardown remains `NO` before controller verification.

Deterministic local closure results:

- `EMITTER_QA=PASS`;
- `HCI_FAILURE_ISOLATION_QA=PASS`;
- `INVENTORY_HCI_SEPARATION_QA=PASS`;
- `PERSISTENT_CONTROLLER_ROUNDTRIP_MODEL_QA=PASS`;
- `TEARDOWN_PRE_CONTROLLER=NO`.

The active offline workflow was also extended to compile the HCI emitter and exercise these HCI/raw-evidence assertions:

`.github/workflows/wp2-golden-offline-qa.yml`

No new live workflow was added. The connector available during this closure did not expose a reliable private-repository listing of push-triggered Actions runs, so this closure does **not** claim a new GitHub Actions run ID. Existing accepted runtime evidence for the unchanged controller/artifact transport remains the AUDIT-R1 off-POWDER artifact QA run `33092849805`; current P5-specific HCI behavior is accepted by the bounded offline checks above.

## 6. Scientific state preserved

Unchanged:

- H1 = `VALID_W1_RECOVERY_FAILURE`, non-scored;
- original H1 node-local raw bundles remain unrecovered;
- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuator IDs `1 33 2 34` remain coupled;
- RF calibration remains PASS/FROZEN;
- K1-K8 remain PASS/CLOSED;
- `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`;
- primary cohort freezes at `t_rf_restore`;
- `H_app=300 s` from `t_service_ready`;
- primary endpoint remains `completeness_300`;
- `T_service`, `T_app`, `T_total` remain distinct;
- outcome-derived/W1-derived/Golden-derived/scored-result-derived H re-estimation remains prohibited.

## 7. Safe frontier after P5

P5 closes here and the project **STOPS before Golden**.

Current controls:

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

`HCI_CONTROL_ACTIONS_ENABLED=false`

Only after a **separate explicit user continuation** may the project:

1. perform the advisory `resinfo.php` resource-availability preflight immediately before booking and record `PASS|DEFER|UNKNOWN`;
2. preserve the frozen hardware/profile rather than chase availability;
3. book one clean non-scored Golden;
4. execute G0-G10;
5. complete controller artifact round-trip and obtain `TEARDOWN_AUTHORIZED=YES` before teardown;
6. decide formal WP2 scientific closure and scored authorization.

Do not start WP2-P6 from this closure record.
