# WellPulse Live Experiment HCI and Raw-Evidence Architecture

**Status:** WP2-P5 PASS / FROZEN  
**Closure record:** `docs/WP2_P5_HCI_RAW_EVIDENCE_CLOSURE_2026-08-27.md`  
**Purpose:** let the PI follow the experiment clearly in real time without contaminating the scientific run, while preserving complete raw evidence independently of the HCI.

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

`HCI_CONTROL_ACTIONS_ENABLED=false`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

Passing this design/implementation gate does not authorize Golden. A separate explicit user continuation is required before the advisory POWDER resource preflight or any reservation.

## 1. Separation of planes

The experiment uses two strictly separated planes.

### A. Scientific Raw-Data Plane

This is authoritative scientific evidence. It must remain lossless, append-only during acquisition where practical, and independent of the display layer.

At minimum preserve the exact files frozen in:

`experiments/WP-PWD01/evidence_inventory_golden_v1.txt`

The mandatory scientific/finalization inventory includes sender/receiver raw ledgers, RF timeline, LTE/core/eNB/UE chronology, runtime fingerprints, authoritative `gate_events.jsonl`, reconstruction outputs, SHA-256 manifests, persistent escrow markers and controller round-trip signals.

The HCI must never be the only location containing any scientific observation.

### B. Human-Computer Interaction / Display Plane

The HCI is a non-authoritative observer. It may display only status already owned by the orchestrator and frozen launch metadata.

It must not independently query, probe, restart, reconfigure, attenuate, teardown, or otherwise interact with POWDER during the protected scientific window.

`HCI_CONTROL_ACTIONS_ENABLED=false`

The implemented passive event emitter is:

`scripts/wp2_golden_hci_emit.py`

The Golden orchestrator invokes it only from its own gate state. HCI emission failure is explicitly degraded/non-authoritative and is swallowed by the observer wrapper; it cannot stop or change the scientific run.

## 2. HCI interaction rule

During G3-G10, the permitted architecture is:

`experiment processes -> orchestrator-owned gate/state -> passive hci event -> orchestrator stdout / GitHub Actions live log`

Not allowed:

`HCI -> SSH/API/tmcc/live probe -> experiment`

No HCI refresh action may create a new POWDER command.

## 3. Frozen minimal cockpit

The PI-facing live view is intentionally simple.

### Required identity/safety fields

When known from frozen launch/orchestrator state:

- experiment/run identity;
- NON-SCORED status for Golden;
- exact code commit;
- optional hard-expiry UTC supplied by launch metadata;
- compatibility gate = PASS;
- independent probes = DISABLED;
- `hci_control_actions_enabled=false`;
- evidence state;
- persistent-copy state;
- off-POWDER-copy state;
- teardown authorization state;
- fail-closed state.

### Progress fields

- G0-G10 gate;
- phase;
- PASS/FAIL/PENDING state;
- bounded progress percentage.

Current frozen phase mapping:

- G0-G1 -> PREP;
- G2 -> BASELINE;
- G3 -> RF_OUTAGE;
- G4-G5 -> RESTORE;
- G6 -> SERVICE_READY;
- G7 -> APPLICATION_HORIZON;
- G8 -> RECONSTRUCTION;
- G9-G10 controller handoff -> ESCROW.

The HCI does not inspect scientific application outcomes or raw payload contents.

## 4. Machine-readable event contract

Observer file:

`orchestration/hci_events.jsonl`

Schema identifier:

`wp2-hci-v1`

Each event contains only bounded non-secret fields:

- `schema_version`;
- `utc`;
- `run_id`;
- `experiment_id`;
- `gate`;
- `phase`;
- `status`;
- `progress_pct`;
- `scored_run`;
- `hci_control_actions_enabled`;
- `independent_probes`;
- `compatibility_gate`;
- `evidence_state`;
- `persistent_copy_state`;
- `off_powder_copy_state`;
- `teardown_authorized`;
- `fail_closed`;
- optional `code_commit`;
- optional `hard_expiry_utc`.

The event contract intentionally excludes arbitrary gate detail, credentials, private keys, tokens, private certificate material, TLS session secrets and raw payload contents.

Every successful HCI event is mirrored to orchestrator stdout as:

`HCI_EVENT=<json>`

Therefore GitHub Actions live output is the fallback cockpit without an independent testbed probe.

## 5. HCI is not scientific or teardown authority

`orchestration/hci_events.jsonl` is classified as `CONDITIONAL` in the Golden inventory.

Consequences:

1. if present, it is preserved and hashed with the bundle;
2. its absence/failure alone cannot invalidate a scientifically valid run;
3. it cannot substitute for raw files or authoritative `gate_events.jsonl`;
4. it cannot issue `EVIDENCE_ESCROW_GATE=PASS`;
5. it cannot issue `TEARDOWN_AUTHORIZED=YES`.

Only the qualified controller finalization chain may authorize teardown.

## 6. Raw-data preservation policy

### During protected acquisition G3-G7

- authoritative acquisition remains on the qualified experiment paths;
- no independent background sync is allowed;
- no `/proj` checkpoint is authorized on the current shortest path;
- HCI writes only its small local observer event file and stdout records from orchestrator-owned gate transitions.

No extra in-run checkpoint benchmark is required because no in-run checkpoint mechanism is being enabled.

### G8 reconstruction

The run must reconstruct from preserved raw evidence before escrow.

### G9 persistent escrow

After protected observation and reconstruction are complete:

1. freeze/inventory mandatory raw artifacts;
2. compute `escrow/SOURCE_SHA256SUMS.txt`;
3. copy complete evidence to `/proj/WellPulse/evidence-escrow/<experiment>/<run-id>/`;
4. verify persistent content against source hashes;
5. emit `PERSISTENT_ESCROW_GATE=PASS`;
6. emit/retain `CONTROLLER_OFFPOWDER_REQUIRED`;
7. keep `TEARDOWN_AUTHORIZED=NO`.

### Controller finalization

The mandatory qualified path is:

`/proj/WellPulse -> controller pull -> deterministic TAR -> GitHub Actions artifact -> independent controller download/read-back -> outer TAR SHA-256 + internal SOURCE_SHA256SUMS verification`

Required controller outputs:

- `CONTROLLER_PULL_GATE=PASS`;
- `CONTROLLER_BUNDLE_SHA256=<64hex>`;
- `CONTROLLER_OFFPOWDER_GATE=PASS`;
- `ROUNDTRIP_BUNDLE_SHA256=<same_64hex>`;
- `EVIDENCE_ESCROW_GATE=PASS`;
- only then `TEARDOWN_AUTHORIZED=YES`.

Google Drive/rclone is optional secondary mirroring only and has no teardown authority.

## 7. Exact mandatory raw-evidence contract

The authoritative filename/signal inventory is:

`experiments/WP-PWD01/evidence_inventory_golden_v1.txt` v1.5 or a later explicitly approved superseding version.

`RAW_EVIDENCE_COMPLETE=PASS` may be emitted only after:

- all `REQUIRED` inventory paths exist and satisfy non-empty rules;
- G8 reconstruction has passed;
- source evidence has been frozen for persistent escrow.

HCI material is not part of this scientific-completeness predicate.

## 8. WP2-P5 offline acceptance

The bounded P5 checks passed without POWDER or Drive contact. Accepted checks cover:

1. dependency-minimal passive HCI emitter with no SSH/API/network/probe/control implementation;
2. `HCI_CONTROL_ACTIONS_ENABLED=false` in the orchestrator;
3. observer failure explicitly non-fatal/non-authoritative;
4. valid `wp2-hci-v1` JSONL and stdout fallback from synthetic local state;
5. no arbitrary raw/gate detail in HCI events;
6. HCI classified conditional rather than required scientific evidence;
7. mandatory raw inventory complete independently of HCI;
8. reconstruction remains raw-evidence based;
9. persistent `/proj` escrow remains fail-closed with controller handoff required;
10. controller outer/internal hash round-trip contract remains intact;
11. teardown remains prohibited before controller verification.

Canonical closure evidence:

`docs/WP2_P5_HCI_RAW_EVIDENCE_CLOSURE_2026-08-27.md`

The active offline QA implementation is:

`scripts/wp2_golden_offline_qa.sh`

and workflow:

`.github/workflows/wp2-golden-offline-qa.yml`

## 9. Gate state and STOP

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

No POWDER contact, reservation, SSH, Golden or scored run was used to close WP2-P5.

The project stops here. Only after a **separate explicit user continuation** may the project perform the advisory `resinfo.php` preflight and attempt one clean non-scored Golden.
