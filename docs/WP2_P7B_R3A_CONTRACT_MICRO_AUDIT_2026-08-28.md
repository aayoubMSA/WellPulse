# WP2-P7B-R3A — Contract Micro-Audit

**Date:** 2026-08-28  
**Verdict:** `WP2_P7B_R3A=BLOCKED_CONTRACT_DRIFT_REPAIR_REQUIRED`  
**Live R3 state:** `PAUSED_BEFORE_POWDER_CONTACT`  
**POWDER contact / reservation / SSH / mutation during R3A:** NO / NO / NO / NO  
**Scored authorization:** BLOCKED

## Why this audit was opened

After the user explicitly authorized `P7B-R3`, execution was deliberately paused before any POWDER contact because the repeated operational failures suggested that the contracts themselves might be contributing to error creation or error concealment. This audit therefore treats the contracts, plans, evidence inventory, runtime implementation, reconstruction logic, and R2 authority layer as one executable system and checks whether they actually agree.

The answer is **no**. The current stack contains material contract drift. A live replacement run must not proceed until the drift is repaired and regression-protected.

## Executive finding

The central problem is not a single bad shell quote. The deeper problem is that the current P7B design has several competing sources of truth:

1. `experiments/WP-PWD01/P7B_PHYSICAL_QUALIFICATION_PLAN_v1.md`;
2. `experiments/WP-PWD01/p7b-qualification-contract.json`;
3. `experiments/WP-PWD01/evidence_inventory_p7b_v1.txt`;
4. `src/wellpulse/p7b.py`;
5. `scripts/wp2_p7b_c_node.py` + the R1 wrapper;
6. `scripts/reconstruct_wp2_p7b.py`;
7. `experiments/WP-PWD01/p7b-requalification-r2-contract.json`;
8. `scripts/wp2_p7b_r2_validate_controller.py`;
9. tests that check selected invariants but do not prove the whole chain is contract-complete.

These layers overlap but are not generated from one canonical executable schema. That allows documentation, inventory paths, runtime writers, reconstruction readers, and authority gates to drift independently.

## Critical findings

### C1 — Evidence inventory paths do not match runtime writer paths

**Severity:** CRITICAL  
**Class:** contract/runtime drift

Examples:

- inventory requires `cells/<cell>/readiness.json`, while runtime writes `readiness_observation.json` and `readiness_verdict.json`;
- inventory requires `generator/telemetry_generated.csv`, while generator writes `telemetry_generated.csv` directly under the cell root;
- inventory requires `generator/generator_events.jsonl`, while generator writes `generator_events.jsonl` at cell root;
- inventory requires `gateway/gateway_process_events.jsonl`, while gateway writes `gateway_process_events.jsonl` at cell root;
- inventory requires `gateway/mqtt_events.jsonl`, while gateway writes `mqtt_events.jsonl` at cell root;
- inventory requires `gateway/w1_queue.sqlite`, while W1 queue is cell-root `w1_queue.sqlite`;
- inventory requires `gateway/queue_timeline.csv`; no canonical writer for that exact artifact was identified;
- inventory requires `substrate/attenuation_timeline.csv`, while the live runner writes separate Q0/Q3/read-back/restore files rather than that exact timeline artifact;
- inventory requires `substrate/service_ready_probe.txt`, while the runner writes `service_ready_probe.txt` at cell root;
- B2 inventory names `gateway/persistence_inventory_before.json` and `...after.json`, while runtime writes `b2_pre_restart_persistence_inventory.json` and `b2_post_restart_persistence_inventory.json`.

This means an evidence bundle can be operationally rich yet fail the declared inventory, or a reconstruction can pass without proving the declared inventory existed.

### C2 — Reconstruction PASS does not prove complete contract evidence

**Severity:** CRITICAL  
**Class:** acceptance-gap

`scripts/reconstruct_wp2_p7b.py` validates readiness observations, restart proof, runtime manifests, B1 accepted/unacked semantics, W1 durability proof, B2 durability proof, and B1/W1 manifest match. It does **not** enforce the full evidence inventory, reservation-level evidence, complete receiver evidence, complete generated/received ledgers, raw SHA inventory, or all declared substrate files.

Therefore:

`WP2_P7B_RECONSTRUCTION=PASS`

is currently weaker than:

`P7B_CONTRACT_COMPLETE=PASS`.

The two must not be treated as synonyms.

### C3 — The JSON contract is not the true execution source of values

**Severity:** CRITICAL  
**Class:** duplicate-source-of-truth

The live node runner hard-codes key contract values such as:

- attenuator IDs;
- Q0/Q3 values;
- pre-Q0 duration;
- Q3 duration;
- restart offset;
- H_app;
- broker host/port;
- B2 JAR SHA.

The runner does not derive all of these values from the JSON contract at runtime. As a result, the contract can say one thing while code executes another unless a separate regression happens to catch the mismatch.

A contract is not a source of truth if execution can ignore it.

### C4 — Contract loader validates only a narrow subset of invariants

**Severity:** HIGH  
**Class:** schema weakness

`load_contract()` verifies schema version and non-scored authority, but does not validate the full internal consistency of the contract: required keys, evidence inventory, runtime lock equivalence, authority precedence, path-location mapping, complete acceptance criteria, or binding between contract values and execution values.

### C5 — Evidence location ownership is ambiguous across UE/core/controller

**Severity:** CRITICAL  
**Class:** location contract ambiguity

The evidence inventory is written as one logical tree, while actual evidence is split between:

- UE/local cell evidence;
- core receiver/broker evidence;
- controller reservation/manifest evidence;
- `/proj` escrow;
- GitHub artifact/read-back evidence.

The original contract does not encode, per evidence item, which host owns the writer, the exact absolute source path, how it is merged into the canonical bundle, and which reader validates it. This ambiguity directly contributed to the earlier receiver-ledger loss.

### C6 — R1 fixes receiver path execution but base status still emits unresolved `$HOME`

**Severity:** HIGH  
**Class:** repaired-runtime/status drift

The R1 wrapper resolves receiver paths correctly, but the base runner still records `core_evidence_root` using literal `$HOME/...` in its status object. R2 explicitly prohibits literal `$HOME`/`~` in evidence-survival paths.

A future R3 controller must not consume this status field as a trusted absolute path until the status schema is repaired.

### C7 — Original teardown authority and R2 teardown authority differ

**Severity:** HIGH  
**Class:** supersession ambiguity

Original P7B contract/plan allows teardown after `EVIDENCE_ESCROW_GATE=PASS`. R2 strengthens this to require both persistent escrow and independent off-POWDER verification before teardown.

The stronger R2 rule is scientifically safer and should govern the replacement, but the precedence is not represented through one executable supersession mechanism shared by all code paths.

### C8 — R2 controller validator is lexical, not semantic

**Severity:** HIGH  
**Class:** authority-gate weakness

`scripts/wp2_p7b_r2_validate_controller.py` checks literal token counts and textual ordering. It can establish that required strings exist, but it cannot prove shell control-flow semantics, that a marker is reached only after a real verified gate, or that comments/unused branches do not satisfy the lexical requirement.

This is useful as a static smoke gate, not sufficient as the final authority proof.

### C9 — Live authorization is not yet a separate machine-readable authority object

**Severity:** HIGH  
**Class:** authority provenance

R2 correctly freezes an offline contract with `live_authorized=false`. The user later explicitly authorized R3. That approval should not be represented by mutating the immutable R2 contract; however, there is currently no separate canonical one-shot live-authorization artifact that binds:

- user authorization state;
- authority ID `P7B-RQ1`;
- exact controller hash;
- exact execution artifact hashes;
- reservation count = 1;
- no retry/second replacement;
- expiry/consumption semantics.

Without such an object, authority is split between conversation state, trigger content, and code.

### C10 — R2 execution lock records exact artifact blobs, but future controller validation does not prove them

**Severity:** CRITICAL  
**Class:** implementation-lock gap

R2 freezes exact blob SHAs for the R1 node entrypoint, path contract, and preservation helper. The current static validator checks that expected path names appear in controller text, but does not require the future live controller to verify the checked-out files against the frozen blob/content hashes before mutation.

A docs-only commit after the tested implementation is acceptable only if the live gate proves the frozen implementation artifacts are byte-identical.

### C11 — Tests prove selected invariants but not contract closure

**Severity:** HIGH  
**Class:** QA coverage gap

Current tests successfully protect many important semantics, including the R1 path repair and R2 one-replacement rules. However, they do not instantiate the declared evidence inventory and prove that every REQUIRED item has exactly one writer, exact path, exact host/location, and exact validator.

The evidence inventory test is therefore currently weaker than an executable evidence-schema test.

### C12 — Workflow/runtime dependencies are not fully version-locked

**Severity:** MEDIUM  
**Class:** reproducibility risk

Python Paho and the Java JAR are strongly pinned, but system packages such as Mosquitto and other apt-installed runtime components are obtained from the node repository at execution time. The contract requests runtime fingerprinting but does not define a hard acceptance policy for these versions.

This was not the identified cause of the receiver-path failure, but it is a latent reproducibility risk and should be explicitly classified as either pinned-required or observed-only.

## Root-cause interpretation

The first live P7B failure was triggered by a quoting/path bug, but the contract system made that class of bug easier to create and harder to detect because:

- the evidence path was conceptual rather than a typed host/path object;
- writer and watcher paths were not generated from one canonical schema;
- the inventory and runtime layout had already drifted;
- reconstruction did not prove evidence completeness;
- live authority, execution lock, evidence completeness, and teardown were validated by separate layers rather than one composed state machine.

The user's hypothesis is therefore supported:

`CONTRACT_SYSTEM_IS_A_MATERIAL_SOURCE_OF_OPERATIONAL_ERROR_RISK=true`.

## R3A decision

`WP2_P7B_R3A=BLOCKED_CONTRACT_DRIFT_REPAIR_REQUIRED`

The prior user authorization for R3 is acknowledged, but execution is placed on an administrative safety hold because material contract defects were discovered before POWDER contact.

No live reservation has been created under `P7B-RQ1` during R3/R3A.

## Mandatory repair before live R3

The next patch must be offline only and must build a **single executable contract model** rather than add another prose amendment.

Minimum acceptance criteria:

1. define one canonical machine-readable R3 contract/schema;
2. encode every frozen scientific/runtime value once and make runtime read it rather than duplicate it;
3. define every required evidence item with exact logical ID, writer, host/location, absolute-path template, required/conditional status, and validator;
4. generate or validate the evidence inventory from that schema;
5. make reconstruction fail if any REQUIRED evidence item is missing/empty/wrong-location;
6. repair the status schema so no unresolved `$HOME`/`~` evidence path is emitted;
7. define explicit supersession/precedence: R2 replacement rules override original teardown semantics without rewriting historical evidence;
8. create a separate one-shot machine-readable live-authorization object rather than mutating R2;
9. require byte/hash verification of all frozen implementation artifacts before reservation creation or mutation;
10. replace lexical-only controller acceptance with semantic/runtime premutation assertions where feasible;
11. classify all system-package versions as either hard-pinned or observed-only and test that policy;
12. add an end-to-end synthetic contract test proving `contract -> writer paths -> reconstructed bundle -> evidence completeness -> teardown gate` without POWDER.

## Exact next bounded patch

`WP2-P7B-R3B — EXECUTABLE CONTRACT UNIFICATION + END-TO-END OFFLINE CONTRACT QA`

Status: **NOT STARTED / OFFLINE ONLY**.

R3 live execution remains paused. After R3B PASS, a fresh explicit resume decision is required because the authority-bearing contract/controller will have materially changed from the state originally approved.

**STOP — CONTRACT AUDIT COMPLETE; NO POWDER CONTACT.**
