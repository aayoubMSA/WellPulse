# WP2-P7B-B — Offline Implementation + Premutation QA Closure

**Date:** 2026-08-27  
**Verdict:** `WP2_P7B_B=PASS_OFFLINE_IMPLEMENTATION_PREMUTATION_QA`  
**Evidence class:** OFFLINE / NON-SCORED / PRE-SCORE QUALIFICATION  
**POWDER contact:** NO  
**Reservation / SSH / testbed mutation:** NO / NO / NO  
**Scientific run / scored run:** NO / NO  
**Scored authorization:** BLOCKED  

## Scope and claim ceiling

This patch implements and verifies only the frozen P7B-A physical-qualification contract. It does not execute P7B-C, create a POWDER reservation, qualify the real remote LTE/MQTT path, change any frozen scientific parameter, or authorize scored work.

Canonical contract authority remains:

- `docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`;
- `experiments/WP-PWD01/P7B_PHYSICAL_QUALIFICATION_PLAN_v1.md`;
- `experiments/WP-PWD01/p7b-qualification-contract.json`.

## Accepted implementation chain

1. `03a7f424e92ef8c2a207e8888b06b406e1e8f3f6` — separated generator/gateway runtime and fail-closed gates.
2. `dcefc42bc4474bce07bd29a40e014b6e2408227d` — remote-capable B2 adapter plus deterministic P7B reconstruction/evidence inventory.
3. `6892ad26810d598965dfbe85ecb38f53b1097a5c` — one-line compatibility correction for the Eclipse Paho Java 1.2.5 API.
4. `ccd4c3aa635e9ad513ba4c6851a2de39a27c5d50` — sanitized B2 local semantics evidence only; no implementation change.

## Acceptance matrix

| Requirement | Evidence | Verdict |
|---|---|---|
| Generator outside gateway restart domain | `scripts/wp2_p7b_generator.py`; generator ledger/process events; runtime tests | PASS |
| Separate B1/W1 gateway/client process | `scripts/wp2_p7b_python_gateway.py`; explicit B1 FIFO vs W1 queue paths | PASS |
| B1 accepted/unacknowledged MID reconstruction | `src/wellpulse/p7b.py`; publish/PUBACK event reconstruction and pre-restart snapshot tests | PASS |
| Exact B1/W1 low-level manifest comparison | `scripts/wp2_p7b_compare_manifests.py`; mismatch regression tests | PASS |
| W1 durable restart-survival/replay mechanics | `DurableQueue` + `DurablePahoReplay`; synthetic durability proof and existing queue/replay regressions | PASS |
| Eclipse Paho Java 1.2.5 B2 adapter + exact lock | `P7BRemoteB2Gateway.java`; exact 1.2.5 build and three restart semantics trials | PASS |
| Per-cell washout/readiness | `wp2_p7b_validate_readiness.py`; Q0/route/session/residue/runtime/clock/radio/evidence fail-closed tests | PASS |
| Deterministic evidence reconstruction | `reconstruct_wp2_p7b.py`; complete synthetic bundle PASS; corrupted readiness/B2 hash/durability FAIL | PASS |
| Evidence inventory + stop/interlocks | `evidence_inventory_p7b_v1.txt`; cell-order and no-reservation-authority regressions | PASS |
| Scored authority remains false | reconstruction tests assert `scored=false` and `scored_runs_authorized=false` | PASS |

## Offline QA evidence

### Runtime implementation gate

GitHub Actions Local Unit Tests:

- run `33108584032`;
- job `98645029922`;
- tested SHA `03a7f424e92ef8c2a207e8888b06b406e1e8f3f6`;
- Python `3.12.14`;
- `paho-mqtt==2.1.0`;
- **51/51 tests PASS**.

This gate included P7B runtime-contract tests for B1 event reconstruction, B1/W1 matching, generator/gateway separation, readiness fail-closed behavior, restart-domain proof and cell sequencing.

### Full P7B reconstruction gate

GitHub Actions Local Unit Tests:

- run `33108767123`;
- job `98645668213`;
- tested SHA `dcefc42bc4474bce07bd29a40e014b6e2408227d`;
- Python `3.12.14`;
- `paho-mqtt==2.1.0`;
- **56/56 tests PASS**.

This gate added deterministic three-cell reconstruction, W1 durability proof, B2 JAR/config/durability validation, corruption fail-closed tests, evidence-inventory checks, and an explicit regression that no new P7B script contains reservation authority.

### B2 compatibility provenance and accepted gate

The first B2 semantics run after adding the remote adapter, run `33108767171` at SHA `dcefc42...`, **FAILED** because the Java adapter used an API form incompatible with the pinned Eclipse Paho Java 1.2.5 artifact. This negative QA result is retained as provenance and was not relabelled.

Commit `6892ad26810d598965dfbe85ecb38f53b1097a5c` changed one line in `P7BRemoteB2Gateway.java` to match the actual Paho Java 1.2.5 API.

Accepted B2 semantics gate:

- run `33108848011`;
- job `98645950042`;
- tested SHA `6892ad26810d598965dfbe85ecb38f53b1097a5c`;
- exact Eclipse Paho Java `1.2.5` downloaded and both Java probes compiled;
- `P7B_B2_REMOTE_ADAPTER_COMPILE=PASS`;
- three independent local broker-outage + client-process-destruction + recovery trials;
- every trial: buffered `5`, received `5`, unique `5`, missing `0`, duplicates `0`, post-recovery buffer `0`;
- gate **PASS**;
- `POWDER interaction=NONE`;
- `Scored run interaction=NONE`.

The workflow then committed only `evidence/local/wp2-b2-semantics-latest.md` as `ccd4c3aa635e9ad513ba4c6851a2de39a27c5d50`; no implementation file changed in that evidence-only commit.

## Scientific invariants preserved

No frozen RF, timing, endpoint, comparator, or horizon rule changed. In particular:

- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB` with attenuation IDs `1 33 2 34` coupled;
- primary cohort cutoff remains `t_rf_restore`;
- `H_app=300 s` from `t_service_ready`;
- outcome-derived/W1-derived/Golden-derived/scored-derived H re-estimation remains prohibited;
- H1 remains adverse non-scored evidence;
- P7B remains qualification mechanics only.

## Closure decision

All P7B-B offline implementation, compatibility, readiness, reconstruction and fail-closed acceptance gates have evidence-backed PASS status.

`WP2_P7B_B=PASS_OFFLINE_IMPLEMENTATION_PREMUTATION_QA`

`WP2_P7B_PROGRESS=40/100`

`WP2_MANAGEMENT_READINESS_PROGRESS=95/100`

`SCIENTIFIC_WEIGHTED_COMPLETION=20%`

`SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`

`scored_runs_authorized=false`

## Stop boundary

**STOP before P7B-C.** P7B-C is one live, non-scored POWDER reservation containing exactly the frozen sequential cells `P7B-B1-S3 -> P7B-W1-S3 -> P7B-B2-S3`. It requires separate explicit live authorization.

Until that authorization exists: no POWDER contact, reservation, SSH, testbed mutation, physical cell, Golden/H/RF recalibration, scored work, OTA replication or WP3 execution.
