# WP2 POWDER Runtime Compatibility Matrix — 2026-08-28

## Evidence

- Workflow: `WP2 POWDER SSH Environment Inventory`
- Run: `33124645486`
- Head SHA: `6ed30e09e2c43deca870bf185947369934d89377`
- Experiment: `12b39276-af0f-4e34-8dfd-685b006dd6bd` / `wp7brq19810043`
- Artifact ID: `9667857505`
- Artifact ZIP SHA-256: `e0a1923af8ff1ffbbdf5bb20641f01ec9f81e5d96c67b0328260063f14848245`
- Inner inventory TAR SHA-256: `b94c958a0b23bf812892680372485e6710b8f74b8368ea1c5c109e9f34d5541d`
- Collection verdict: `WP2_POWDER_SSH_ENV_INVENTORY_WORKFLOW=PASS_COLLECTION_COMPLETE`
- New reservation: `NO`
- RF mutation: `NO`
- Cells: `NO`
- Restart: `NO`
- Teardown: `NO`
- Scored: `NO`

## Observed target reality

| Capability | CORE `nuc1` | UE `nuc2` | Contract consequence |
|---|---|---|---|
| OS | Ubuntu 18.04 | Ubuntu 18.04 | Target QA must test against this image, not GitHub Ubuntu 24.04 |
| System Python | 3.6.9 | 3.6.9 | Repo/project code MUST NOT use unqualified `python3` |
| Pinned Python | 3.11.13 | 3.11.13 | Required interpreter for project Python |
| Pinned Paho MQTT | 2.1.0 | 2.1.0 | Exact runtime dependency is available |
| Pinned packaging | 26.3 | 26.3 | Available |
| `pkg_resources` in pinned venv | absent | absent | Runtime QA MUST NOT depend on `pkg_resources` |
| Java | absent | OpenJDK 11.0.19 | Java requirement is UE-only |
| Mosquitto daemon | 1.4.15 | absent | Broker daemon requirement is CORE-only |
| Mosquitto clients | present | present | Client tools available on both |
| `jq` | absent | absent | Remote node code MUST NOT require `jq` |
| Bash | 4.4.19 | 4.4.19 | Bash 4.4 floor is supported |
| GNU tar | 1.29 | 1.29 | Shell-only evidence preservation supported |
| rsync | 3.1.2 | 3.1.2 | Shell-only evidence preservation supported |
| SHA256/coreutils | 8.28 | 8.28 | Hash evidence supported |
| `/proj/WellPulse` | present/writable | present/writable | Persistent escrow available |
| B2 Paho Java JAR | not observed | SHA `59914287...8185` observed | Exact frozen JAR evidence remains UE-side |

## QA findings

1. `SYSTEM_PYTHON_COMPATIBILITY`: **FAIL for project code**. Python 3.6.9 caused the prior `from __future__ import annotations` failure. Project scripts must use `$HOME/.wp2-golden-venv/bin/python` only.
2. `PINNED_PROJECT_RUNTIME`: **PASS**. Python 3.11.13 exists on both nodes and the observed staged Python source set has no syntax failures under that interpreter.
3. `ROLE_SPECIFIC_RUNTIME`: **PASS with explicit role rules**. Java belongs on UE; Mosquitto daemon belongs on CORE. Their absence on the opposite node is not a defect.
4. `REMOTE_JQ_DEPENDENCY`: **PROHIBITED**. `jq` is absent on both nodes.
5. `PRESERVATION_RUNTIME`: **PASS CONDITIONALLY**. `bash/find/sort/xargs/sha256sum/tar/rsync` are available, so preservation can be shell-only and independent of Python.
6. `PINNED_ENV_METADATA`: `paho-mqtt==2.1.0` is verified through `pip freeze`; `pkg_resources` is absent, therefore `importlib.metadata` is the supported metadata interface.
7. `INVENTORY_V1_REPORTING`: **QA DEFECT**. The v1 probe could report `REPO_PRESENT=no` because of quoting while later compiling source successfully; it also treated local imports as third-party import failures. These reporting defects do not invalidate the observed OS/interpreter/tool versions. They are repaired prospectively by `scripts/wp2_powder_ssh_environment_inventory_v2.sh`.

## Mandatory future pre-RF gate

A live qualification may not begin RF/cell work until a same-image target check proves:

- exact pinned Python `3.11.13` on CORE and UE;
- exact `paho-mqtt==2.1.0` in that interpreter;
- exact authorized source set staged before syntax/import checks;
- all required project sources syntax-compile under the pinned interpreter;
- no remote project/preservation command uses system `python3`;
- no remote runtime path requires `jq`;
- Java 11 requirement checked only on UE;
- Mosquitto daemon requirement checked only on CORE;
- shell preservation commands present on both nodes;
- B2 JAR exact SHA verified on UE;
- `/proj/WellPulse` visible and writable;
- SSH identity is initialized and used in the same CI step.

## Verdict

`POWDER_RUNTIME_REALITY_CAPTURE=PASS`

`TARGET_RUNTIME_COMPATIBILITY=PASS_CONDITIONAL_ON_PINNED_INTERPRETER_AND_ROLE_SPECIFIC_GATES`

`SYSTEM_PYTHON_FOR_PROJECT_CODE=PROHIBITED`

`REMOTE_JQ_DEPENDENCY=PROHIBITED`

`LIVE_AUTHORIZATION=BLOCKED`

`SCORED_AUTHORIZATION=BLOCKED`
