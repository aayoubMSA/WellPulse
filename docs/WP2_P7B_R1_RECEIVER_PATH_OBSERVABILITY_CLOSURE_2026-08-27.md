# WP2-P7B-R1 — Receiver-Path Repair + Observability Regression QA Closure

**Date:** 2026-08-27  
**Verdict:** `WP2_P7B_R1=PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA`  
**Evidence class:** OFFLINE / NON-SCORED / PRE-SCORE OPERATIONAL QUALIFICATION  
**POWDER contact:** NO  
**Reservation / SSH / testbed mutation:** NO / NO / NO  
**Scientific run / scored run:** NO / NO  
**Scored authorization:** BLOCKED  

## Scope and claim ceiling

R1 repairs and regression-protects the operational defect exposed by the single authorized P7B-C reservation. It does not reinterpret the blocked P7B-C result, reconstruct missing evidence, create a replacement reservation, contact POWDER, change RF/timing/scientific controls, authorize scored work, or start WP3.

The retained live results remain:

- `WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`;
- completed cells: NONE;
- scientific measurement started: NO;
- `WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`;
- teardown complete;
- P7B successful qualification credit remains 40/100 from A+B only.

Canonical provenance:

- `docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`;
- `evidence/powder/wp2-p7b-c-live-status.md`;
- `evidence/powder/wp2-p7b-d-live-status.md`.

## Root cause retained

The P7B-C B1 receiver was not demonstrated to have failed at MQTT or LTE. The live broker proved that receiver client `wp-hcrx-885b10cacb1c`:

- connected to the broker;
- received CONNACK;
- subscribed to the exact B1 topic;
- remained alive through repeated MQTT PINGREQ/PINGRESP exchanges.

At the same time, the controller could not observe the expected `receiver_events.jsonl` and emitted `RECEIVER_CONNECT_TIMEOUT`.

The old live runner built the core cell directory as a string containing literal `$HOME`, then passed receiver `--output-dir` through single quotes while the console redirect/readiness watcher used a shell-expanded path. This creates a writer/watcher path disagreement. The same class of path/quoting defect also caused the first P7B-D preservation attempt to fail closed before persistent copy.

R1 therefore treats the defect as an orchestration/path-contract failure, not a scientific or LTE/MQTT failure.

## R1 implementation

### 1. Absolute remote-path contract

Created:

`scripts/wp2_p7b_path_contract.py`

Implementation commit:

`576354a84be46683b5ff94ce6f6b4ced883b2402`

The contract:

- accepts only already-resolved absolute POSIX paths;
- rejects literal `$` and `~` shell-expansion tokens;
- rejects relative/empty/control-character paths;
- derives receiver output, event-writer, event-watcher and console paths from one canonical absolute cell path;
- explicitly proves `receiver_event_writer_path == receiver_event_watcher_path`;
- exposes a fail-closed CLI for validation and path joining.

### 2. Repaired receiver launcher + bounded failure observability

Created:

`scripts/wp2_p7b_c_node_r1.py`

Implementation commit:

`f6a709508db46e8b99448abdf05ec37964aa3f4e`

Design choice: do not rewrite the large frozen P7B-C scientific runner. R1 loads `scripts/wp2_p7b_c_node.py` as the frozen base and monkey-patches only the operational receiver/path/diagnostic surface, then delegates to the unchanged base cell schedule and reconstruction logic.

R1 receiver behavior:

- resolves the remote core `$HOME` once through the already-authorized SSH abstraction at execution time;
- validates the resolved home as an absolute remote path;
- converts the historical literal `$HOME/...` cell path into one absolute path;
- creates a machine-readable `receiver_path_contract.json`;
- uses shell-safe quoting only after all receiver paths are absolute;
- gives receiver writer and readiness watcher the identical event-ledger path;
- tests receiver PID liveness while waiting for `receiver_connect`;
- emits `RECEIVER_EXITED_BEFORE_CONNECT` immediately if the process exits;
- retains `RECEIVER_CONNECT_TIMEOUT` only when the process remains alive but the event does not appear;
- emits bounded diagnostics before either failure verdict.

The bounded diagnostics include:

- receiver PID/process state;
- receiver console tail;
- receiver event-ledger tail;
- broker log tail;
- experimental route evidence;
- Q0 user-plane probes;
- TLS/MQTT probe;
- Q0 radio capture;
- runtime manifest and readiness records when present;
- Python version;
- `paho-mqtt` version;
- Java version;
- Eclipse Paho Java JAR SHA-256 when present;
- broker certificate fingerprint when present.

They are grouped in GitHub-compatible log groups and are intentionally bounded rather than dumping an unbounded raw tree or credentials.

### 3. Preservation-path helpers

Created:

`scripts/wp2_p7b_preservation_helpers.sh`

Implementation commit:

`544c0b9b40c6d845bf20bf7627f546ddbdceb55b`

These helpers contain no POWDER or SSH authority. They:

- require callers to supply already-resolved absolute paths;
- reject literal `$HOME`/`~` paths before copying;
- can assert the same receiver writer/watcher path contract;
- preserve a tree with a source SHA-256 manifest;
- use `rsync` only after source/destination path validation;
- verify the copied raw files against `SOURCE_SHA256SUMS`.

A future evidence-survival controller must use or equivalently satisfy this resolved-path contract before any copy/teardown chain is authorized.

## Regression QA

Updated:

`tests/test_wp2_p7b_c_premutation.py`

Regression commit:

`695b31cba6c0256b3637223abdfef4f4b11bf6ca`

New executable regressions prove:

1. the historical P7B live workflow is retired and R1 creates no live authority;
2. literal `$HOME` remote paths are rejected;
3. receiver writer and watcher event paths are exactly equal;
4. receiver startup checks PID liveness and has a specific early-exit verdict;
5. timeout/early-exit paths contain the bounded diagnostic sections required by R1;
6. preservation helper shell syntax is valid and its path gate rejects unresolved shell tokens;
7. R1 itself does not define or alter Q0/Q3/H_app or invoke Portal/scored authority;
8. the frozen base still contains Q0=0, Q3=55, pre-Q0=60 s, Q3=120 s, restart offset=60 s and H_app=300 s.

Accepted GitHub Actions Local Unit Tests:

- run `33116073295`;
- job `98670934415`;
- tested SHA `695b31cba6c0256b3637223abdfef4f4b11bf6ca`;
- Python `3.12.14`;
- `paho-mqtt==2.1.0`;
- **65/65 tests PASS**;
- result: SUCCESS.

All prior P7B contract, readiness, reconstruction, B1/W1 matching, B2 durability, restart-domain and no-reservation-authority regressions remained PASS in the same run.

## Frozen science / authority audit

R1 changes no scientific control. In particular:

- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`;
- attenuation IDs `1 33 2 34` remain coupled;
- pre-impairment Q0 remains 60 s;
- Q3 remains 120 s;
- gateway restart remains 60 s into Q3;
- `t_rf_restore`, `t_service_ready`, `t_app_complete` remain distinct;
- `H_app=300 s` from `t_service_ready` remains frozen;
- primary cohort cutoff remains `t_rf_restore`;
- no outcome-derived H re-estimation is permitted;
- H1 remains valid adverse non-scored evidence;
- no scientific measurement or scored execution occurred in R1.

No R1 file creates a POWDER reservation, terminates an experiment, or sets `scored_runs_authorized=true`.

## Historical controller integration status

The retired historical controller `powder/wp2_p7b_c_execute.sh` still invokes the old entrypoint `scripts/wp2_p7b_c_node.py`. This controller currently has **no live workflow/trigger authority** and must not be reused directly.

Any future requalification authority contract must explicitly freeze the repaired entrypoint:

`scripts/wp2_p7b_c_node_r1.py`

and must regression-check that the authority-bearing controller invokes that exact repaired entrypoint before any live workflow is created.

R1 intentionally does not reactivate or modify live authority surfaces.

## R1 verdict

`WP2_P7B_R1=PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA`

The observed P7B-C operational defect is now concretely repaired and regression-protected offline. The repair is scientifically neutral and the prior failed attempt remains preserved without relabelling.

## Requalification recommendation

`FUTURE_PHYSICAL_REQUALIFICATION_RECOMMENDATION=GO_CONDITIONAL`

Rationale:

- the first P7B-C attempt stopped before scientific measurement;
- the physical LTE path, Q0 probes and TLS/MQTT readiness had passed;
- broker evidence proves the receiver was connected/subscribed/alive;
- the blocking contradiction maps to a specific path-contract defect;
- that defect now has a fail-closed absolute-path contract, fail-fast receiver monitoring and executable regression coverage;
- the scientific protocol has not been changed to chase an outcome.

This is a **recommendation only**, not reservation authority.

The frozen original P7B contract has `reservation_limit=1`, `automatic_retry=false` and `automatic_new_reservation=false`; that one reservation was consumed. Therefore a new live reservation cannot be inferred from the old P7B-C authorization.

## Exact next bounded patch

`WP2-P7B-R2 — REQUALIFICATION AUTHORITY + CONTRACT FREEZE`

Status: **OFFLINE ONLY / NOT STARTED**.

R2 may only decide and freeze whether one replacement non-scored qualification reservation is justified after the pre-measurement operational defect. If GO, R2 must at minimum:

1. preserve the original blocked P7B-C/D evidence unchanged;
2. explicitly amend reservation authority from the consumed original limit to at most one named replacement qualification reservation;
3. prohibit automatic retries or a second replacement;
4. freeze `scripts/wp2_p7b_c_node_r1.py` as the only permitted node entrypoint;
5. freeze resolved absolute-path preservation mechanics before live execution;
6. require the same three-cell order and unchanged scientific controls;
7. require GitHub Action failure logs to expose the bounded raw diagnostics before the final generic exit code;
8. retire any temporary live workflow immediately after terminal evidence/teardown;
9. stop again for separate explicit live authorization.

R2 itself must not contact POWDER.

## Progress and stop boundary

- successful P7B physical-qualification credit: **40/100** from A+B only;
- WP2 management/readiness: **95/100**;
- scientific weighted completion: **20%**;
- `SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`;
- `scored_runs_authorized=false`;
- `WP3=BLOCKED`.

**STOP — R1 PASS OFFLINE. No replacement reservation, POWDER contact, SSH, scored execution, or WP3 execution is authorized.**
