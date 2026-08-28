# WP2-P7B Modular Semi-Automatic Execution Architecture — 2026-08-28

## Status and authority

`STATUS=DESIGN_ONLY_OFFLINE`

`LIVE_POWDER_AUTHORIZATION=NO`

`NEW_RESERVATION_AUTHORIZATION=NO`

`RF_AUTHORIZATION=NO`

`B1_RETRY_AUTHORIZATION=NO`

`W1_B2_AUTHORIZATION=NO`

`TEARDOWN_AUTHORIZATION=NO`

`SCORED_AUTHORIZATION=NO`

This document defines the shortest-path/highest-ROI GitHub Actions architecture for the current P7B qualification lane. It does not itself create a live workflow, contact POWDER, create a reservation, SSH to nodes, mutate RF, restart services, retry B1, execute W1/B2, or teardown anything.

The current executable frontier remains `WP2-P7B-H2` and H2 must pass offline before any future live workflow is created.

## Design decision

Use **one short-lived parent GitHub Actions workflow with sequential jobs**, not a collection of independently-triggerable live workflows.

Each job is one experiment module. Jobs are chained with `needs:` so the next module starts automatically only when its predecessor has produced the required gate. The GitHub Actions run graph becomes the operator HCI.

Do **not** use:

- path-trigger sentinel files for live execution;
- `workflow_run` chains across many detached runs;
- separate live workflows for every small step;
- hidden cross-step process state;
- automatic retry or automatic replacement reservation;
- performance thresholds as execution gates.

Why this is the preferred architecture:

1. one live entry surface is easier to audit and retire;
2. no trigger-file retirement side effect;
3. one run graph exposes progress and blockers clearly;
4. each module re-establishes its own CI/SSH process state;
5. module inputs/outputs can be machine-readable and hashable;
6. a failed module stops scientific progression while a dedicated evidence module can still run with `if: always()`;
7. the experiment remains one causal session rather than a collection of loosely coupled Actions runs.

## Ledger rules converted into architecture constraints

The current Research & Grants Lessons Learned Ledger was read through LL-001–LL-029. The following entries directly govern this design:

- LL-001: canonical state must be recoverable outside chat;
- LL-002: evidence class is explicit at creation;
- LL-004: scientific controls are frozen before live execution;
- LL-007: failed attempts are preserved and classified before any retry;
- LL-009: CI retention is not durable provenance;
- LL-015: generated-vs-received reconciliation is primary evidence;
- LL-019: use an explicit dependency DAG and one integration authority;
- LL-020: exact target runtime is a pre-live gate;
- LL-021: ssh-agent/process state is step-local and must not be assumed to persist;
- LL-022: CLI success and parser/schema compatibility are separate gates;
- LL-023: Portal/API transport error is not scientific/testbed failure;
- LL-024: machine-readable evidence paths must be absolute and fully resolved;
- LL-025: one executable contract is the authority-bearing source;
- LL-026: evidence survival must be simpler than the scientific/application path;
- LL-027: workflow retirement must not depend on deleting a path trigger;
- LL-028: EFCC is a standing pre-live gate;
- LL-029: diagnostic command exit code is not automatically a semantic failure.

## Manual versus automatic boundary

### Manual step R0 — POWDER reservation

**Manual by design.**

After H2 PASS and a separate explicit live authorization, the user creates/selects the POWDER reservation in the Portal using the frozen profile/hardware bindings, then supplies only:

- `experiment_id`;
- `experiment_name`.

Rationale: reservation creation and Portal readiness polling have already shown control-plane brittleness; the Portal is faster for the human and removes an unnecessary mutation/API failure domain from the scientific workflow.

The live workflow must never create a reservation.

### Automatic session — GitHub Actions

After R0, one manually-dispatched, short-lived workflow performs the bounded session from identity validation through the non-scored P7B qualification verdict.

### Manual step T0 — teardown

**Manual by design.**

The automatic workflow stops after immutable evidence/read-back and emits `TEARDOWN_READY=YES`. The user then terminates the reservation in the POWDER Portal.

Rationale: teardown is destructive, Portal termination is simple, and keeping it outside the automated scientific runner prevents evidence-path failure from destroying the experiment.

## Phase A — current H2 offline chain

The current patch remains completely offline and should itself be executed as finite modules:

| Module | Purpose | Gate |
|---|---|---|
| H2.1 | executable contract delta for A1–A7 | `H2_1_CONTRACT_DELTA=PASS` |
| H2.2 | controller/session/process ownership repair | `H2_2_SESSION_OWNERSHIP=PASS` |
| H2.3 | incremental restart/restoration frontier evidence | `H2_3_FRONTIER_EVIDENCE=PASS` |
| H2.4 | static + adversarial failure injection QA | `H2_4_ADVERSARIAL_QA=PASS` |
| H2.5 | contract/runtime/full regression | `H2_5_REGRESSION=PASS` |
| H2.6 | future non-scored requalification authority decision | `WP2_P7B_H2=PASS` or `BLOCKED:<reason>` |

No live workflow may be created before H2.6 PASS plus separate user authorization.

## Phase B — future live P7B session DAG

```text
MANUAL R0: create/select POWDER reservation
        |
        v
M0 SESSION FREEZE
        |
        v
M1 RESERVATION + EFCC DELTA (READ-ONLY)
        |
        v
M2 CONTROLLER DISJOINTNESS + TARGET PREFLIGHT
        |
        v
M3 Q0 KNOWN-GOOD BASELINE PREPARATION
        |
        v
M4 B1 CELL
        |
        v
M5 B1 EVIDENCE FREEZE + READBACK
        |
        v
M6 W1 CELL
        |
        v
M7 W1 EVIDENCE FREEZE + READBACK
        |
        v
M8 B2 CELL
        |
        v
M9 B2 EVIDENCE FREEZE + READBACK
        |
        v
M10 RECONSTRUCTION + NON-SCORED QUALIFICATION VERDICT
        |
        v
STOP: TEARDOWN_READY=YES
        |
        v
MANUAL T0: terminate in POWDER Portal
```

## Module contracts

### M0 — Session freeze

Contact: **no POWDER**.

Responsibilities:

- verify one-shot authority identity;
- require first run/first attempt only;
- verify exact authorized scientific source SHA and executable-contract digest;
- freeze evidence class `NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION`;
- verify `scored=false` and automatic retry disabled;
- derive deterministic session `run_id` from GitHub run identity;
- emit immutable `session_contract.json`.

Required gate:

`M0_SESSION_FREEZE=PASS`

One-shot guards for the future ephemeral workflow:

- `GITHUB_RUN_NUMBER == 1`;
- `GITHUB_RUN_ATTEMPT == 1`;
- exact authority ID match;
- exact scientific source SHA match;
- exact executable-contract SHA-256 match.

Any failure is terminal for that authority instance.

### M1 — Reservation identity + EFCC delta

Contact: **POWDER read-only only**.

Responsibilities:

- verify supplied UUID/name/project/profile identity;
- acquire manifest with bounded retry;
- classify Portal transport errors separately from semantic state;
- verify CORE=`nuc1`, UE=`nuc2`, `nuc5300`, exact image/profile revision;
- resolve current SSH endpoints;
- read-only inventory only the EFCC deltas that can materially drift;
- capture exact CLI/API outputs used by parsers;
- write `target_delta_inventory.json` and digest.

No package installation, service mutation, RF mutation, cell execution, or teardown.

Required gate:

`M1_EFCC_DELTA=PASS`

### M2 — Controller disjointness + target-native preflight

Contact: read-only target inspection; no scientific RF impairment.

Responsibilities:

- prove controller is not hosted in `ue`, `srs-ue`, `enb`, `srs-enb`, `srs-epc`, or any cleanup-owned namespace;
- prove cleanup target selection cannot match controller PID/session;
- validate absolute evidence paths;
- validate exact interpreters/runtime/tool versions;
- validate parser fixtures against observed target output;
- validate required persistent escrow path;
- validate B2 JAR digest and role-specific dependencies;
- use controlled diagnostic RC tolerance where semantic output is valid.

Required gate:

`CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS`

and

`M2_TARGET_PREFLIGHT=PASS`

### M3 — Q0 known-good baseline preparation

Contact: live substrate/service preparation after explicit authority; no scientific impairment yet.

Responsibilities:

- establish service ownership explicitly;
- restore exact Q0 state using the H2-safe restore implementation;
- use PID/ownership-scoped termination rather than unsafe generic service-session destruction;
- establish CORE, UE, route, TLS/MQTT, receiver readiness;
- record Q0 command acknowledgements and independent Q0 path evidence;
- preserve controller outside restore failure domain.

Required gate:

`M3_Q0_BASELINE=PASS`

Failure here occurs before the scientific treatment and is preserved/classified; it does not authorize an automatic retry.

### M4 — B1 cell

Scientific controls are frozen and unchanged.

Responsibilities:

- execute only `P7B-B1-S3`;
- preserve generator outside restart domain;
- write `restart_transition.json` immediately after gateway replacement is proven started;
- write incremental restoration frontier markers before/after destructive restore phases;
- preserve UTC + monotonic clocks;
- finish the cell without applying any performance pass threshold.

Required execution gate:

`M4_B1_MECHANICS=PASS`

A poor/negative `completeness_300` is **not** a workflow failure if the mechanics and evidence are valid. Scientific outcome must not control whether W1 is attempted.

### M5 — B1 evidence freeze + independent readback

Runs with `if: always()` after M4.

Evidence path must be shell/coreutils-first and must initialize its own SSH state inside this job.

Minimum chain:

`node raw -> /proj persistent escrow -> controller pull -> GitHub artifact -> independent readback -> outer/internal SHA-256`

Required gate to continue:

`M5_B1_EVIDENCE=PASS`

If M4 blocked after treatment or M5 cannot prove evidence survival, **stop** and leave the experiment live. No W1 and no retry.

### M6 — W1 cell

Starts only when M4 mechanics and M5 evidence gates passed.

Execute only `P7B-W1-S3` under the same frozen controls. The only intended B1/W1 difference remains application-level SQLite durability/reconciliation.

Required gate:

`M6_W1_MECHANICS=PASS`

Again, scientific performance is evidence, not an orchestration gate.

### M7 — W1 evidence freeze + independent readback

Same evidence-survival contract as M5.

Required gate:

`M7_W1_EVIDENCE=PASS`

### M8 — B2 cell

Starts only after M7 PASS.

Execute only `P7B-B2-S3` using the exact Eclipse Paho Java 1.2.5 artifact and frozen B2 semantics.

Required gate:

`M8_B2_MECHANICS=PASS`

### M9 — B2 evidence freeze + independent readback

Same evidence-survival contract as M5/M7.

Required gate:

`M9_B2_EVIDENCE=PASS`

### M10 — reconstruction + non-scored qualification verdict

Contact: no new scientific mutation.

Responsibilities:

- reconstruct from the executable contract and immutable per-cell artifacts;
- independently reconcile generated versus received IDs;
- verify missing/duplicate counts from sets;
- validate all required evidence inventory entries;
- verify restart-transition/final proof consistency;
- preserve cell outcomes even if unfavourable;
- issue only a **qualification-mechanics** verdict.

Allowed terminal verdicts:

- `WP2_P7B_REQUALIFICATION=PASS_NON_SCORED_PHYSICAL_QUALIFICATION`
- `WP2_P7B_REQUALIFICATION=BLOCKED:<first-cause>`

On PASS:

`TEARDOWN_READY=YES`

`SCORED_AUTHORIZATION=NO`

`WP3_AUTHORIZATION=NO`

## Workflow implementation shape

When later explicitly authorized, create exactly one short-lived workflow file, proposed name:

`.github/workflows/wp2-p7b-rq2-session.yml`

Trigger:

`workflow_dispatch` **only**.

Inputs:

- `experiment_id` — required UUID;
- `experiment_name` — required exact reservation name;
- `authority_id` — required exact frozen authority string.

Do not accept scientific controls as dispatch inputs. Scientific controls come only from the executable contract.

Recommended controls:

- `permissions: contents: read` plus only the minimum Actions permissions actually required;
- `concurrency.group = wp2-p7b-${experiment_id}`;
- `cancel-in-progress: false`;
- bounded `timeout-minutes` per module;
- no scheduled trigger;
- no `push` trigger;
- no path trigger;
- no automatic rerun;
- no automatic reservation creation/extension;
- no automatic teardown.

After terminal closure, retire this one live workflow definition. Because it is manual-dispatch-only, retirement does not trigger another run.

## CI process-state rule

Every job that uses SSH must perform all of the following **inside that same job**:

1. materialize the key;
2. initialize `ssh-agent`;
3. `ssh-add`;
4. perform all SSH/SCP/rsync work required by that module;
5. destroy/allow runner teardown of the agent.

No module may depend on `SSH_AUTH_SOCK`, an agent process, shell exports, or `/tmp` content created in a previous job.

Cross-module controller state must move only through explicit GitHub job outputs and/or immutable artifacts.

## State and evidence handoff

Every module writes a small machine-readable result:

`module_result.json`

Required fields:

- schema version;
- module ID;
- session/run ID;
- experiment UUID/name where applicable;
- scientific source SHA;
- executable-contract SHA-256;
- UTC start/end;
- `PASS` or `BLOCKED`;
- exact first-cause code;
- input artifact digests;
- output artifact digests;
- evidence class;
- `scored=false`.

No prose log is sufficient as an inter-module contract.

## Fail-closed transition rules

1. M0 failure -> stop; no POWDER contact.
2. M1/M2 failure -> stop; no scientific mutation.
3. M3 failure -> stop; preserve diagnostics; no treatment.
4. M4/M6/M8 failure -> run its paired evidence module, then stop.
5. M5/M7/M9 evidence failure -> leave experiment live and stop.
6. A negative/null/unfavourable scientific result with valid mechanics/evidence -> continue to the next planned cell.
7. No module may invoke automatic retry.
8. No module may create a second reservation.
9. No teardown before all required evidence/readback gates pass.
10. No scored or WP3 action from this workflow.

## Operator HCI

Use the GitHub Actions job graph as the primary live HCI. Job display names should be short and ordered:

- `00 Freeze`
- `10 EFCC`
- `20 Preflight`
- `30 Q0 Baseline`
- `40 B1`
- `45 B1 Evidence`
- `60 W1`
- `65 W1 Evidence`
- `80 B2`
- `85 B2 Evidence`
- `95 Reconstruct`
- `99 Session Summary`

Each job writes a compact `$GITHUB_STEP_SUMMARY` containing only:

- current module;
- PASS/BLOCKED;
- first cause;
- current reservation identity;
- evidence status;
- next authorized module;
- explicit `SCORED=NO`.

Raw scientific data remain authoritative and separate from this HCI.

## Frozen science

This architecture changes no scientific control. It inherits from the canonical P7B executable contract:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuators `[1,33,2,34]`;
- pre-Q0 `60 s`;
- Q3 `120 s`;
- gateway restart at `60 s` into Q3;
- cell order `B1 -> W1 -> B2`;
- generator outside restart domain;
- cohort cutoff `t_rf_restore`;
- `H_app=300 s` from `t_service_ready`;
- separate `t_rf_restore`, `t_service_ready`, `t_app_complete`;
- no automatic scientific retry;
- negative/null evidence retained.

## Implementation sequence

Shortest implementation path:

1. finish H2.1–H2.6 offline;
2. update the executable contract with the promoted A1–A7 operational controls;
3. implement module scripts/tests offline, with no POWDER workflow;
4. run local/adversarial regression to PASS;
5. STOP for explicit live authority;
6. user manually creates/selects the reservation;
7. create the single short-lived manual-dispatch live workflow;
8. execute exactly one run;
9. stop at `TEARDOWN_READY=YES`;
10. user tears down manually;
11. retire the live workflow and update canonical handover.

`MODULAR_PIPELINE_DESIGN=PASS_OFFLINE_DESIGN_ONLY`
