# Next Gate — WP2 HCI and Raw-Evidence Closure

**Current frontier:** K1–K8 pre-integration compatibility is closed  
**Scientific completion:** 20%  
**Pre-integration compatibility:** `PASS`  
**Live HCI/raw-evidence gate:** `BLOCKED`  
**Scored authorization:** `false`  
**Golden rebook authorization:** `false`

## Compatibility closure

Canonical K8 record:

`docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`

Decisive bounded live compatibility run:

- workflow: `.github/workflows/wp2-kfastlane-live-compat-v2.yml`;
- run: `33085406598` — success;
- experiment: `fc7c2187-2376-4a92-8de1-4665a06ea943`;
- classification: `INFRASTRUCTURE_ONLY_NON_SCORED`.

Validated live evidence includes:

- Portal `ready` state + exact experiment ID + authoritative expiry;
- `PRELAUNCH_TIME_GATE=PASS` with 3283 s remaining against 2700 s minimum;
- exact `enb1 -> nuc1`, `rue1 -> nuc2` bindings;
- `nuc5300` hardware and frozen image/profile revision;
- controller SSH and runtime/profile fingerprints;
- K4 detached-process return in 1 s under the 15 s bound;
- cross-node `/proj/WellPulse` write/read/hash PASS;
- controller pull -> GitHub artifact -> independent read-back/hash PASS;
- `EVIDENCE_ESCROW_GATE=PASS` and `TEARDOWN_AUTHORIZED=YES` after verified controller round-trip;
- no unsafe independent RF observation command;
- mandatory termination requested.

Post-live offline revalidation:

- K3 Portal CLI QA run `33087174307`: success;
- K7 semantic observation guard run `33087181821`: success;
- integrated K2–K7 static acceptance run `33087199247`: success.

Therefore:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

## Current blocker

The K-series is no longer the blocker.

The separate prerequisite remains:

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`

This gate exists to ensure that the next scientific run has complete, non-perturbing observability and raw evidence preservation independent of dashboards or summaries.

## Exact next bounded work

Execute only the HCI/raw-evidence closure patch:

1. reconcile `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md` with the now-qualified `/proj -> controller -> GitHub artifact -> independent read-back/hash` evidence path;
2. freeze a passive, one-way HCI contract with `HCI_CONTROL_ACTIONS_ENABLED=false` and no independent unqualified pull/probe during the protected scientific window;
3. freeze the complete raw-evidence inventory required for Golden: sender records/state, receiver records/state, queue/database state, MQTT events/acks, RF transition chronology, LTE/service-ready/recovery events, runtime/profile fingerprints, gate chronology, hashes/manifests;
4. ensure raw freeze/hash reaches `/proj/WellPulse` before node-local state can be destroyed;
5. ensure teardown authority remains controller-side and requires verified off-POWDER round-trip;
6. close as `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS` only from bounded evidence;
7. STOP before creating the Golden reservation unless explicitly authorized by the user.

No new automation feature should be added unless required to obtain or protect the next scientific result.

## After HCI/raw gate PASS

Scientific path resumes immediately:

1. authorize one fresh non-scored Golden reservation;
2. run one clean G0–G10 Golden rehearsal;
3. preserve and independently verify complete raw evidence before teardown;
4. only after Golden PASS, requalify/freeze H;
5. close WP2 scientifically and issue explicit scored authorization;
6. execute WP3 conducted-RF B1/W1 + fixed B2 sensitivity;
7. execute WP4 compact OTA replication;
8. execute WP5 analysis, reproducibility artifact, figures, and manuscript closure.

## Frozen scientific controls

- H1 remains `VALID_W1_RECOVERY_FAILURE`.
- H1 node-local raw bundles were not recovered; do not claim raw recovery.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB` with attenuation IDs `1 33 2 34` coupled.
- primary cohort cutoff remains `t_rf_restore`.
- application horizon remains 300 s from `t_service_ready`.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false` until the HCI/raw-evidence gate passes.

## Read first

1. `HANDOVER_CURRENT.md`
2. `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`
3. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
4. this file
5. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
6. `experiments/WP-PWD01/protocol.md`
7. `experiments/WP-PWD01/evidence-schema.md`

Shortest mission path:

`HCI/raw gate -> clean non-scored Golden -> freeze H -> WP2 close -> WP3 -> WP4 -> WP5`
