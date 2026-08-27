# WP2-P7B-R3D — EFCC Contract Delta Closure — 2026-08-28

## Verdict

`WP2_P7B_R3D=PASS_EFCC_CONTRACT_DELTA_QA`

`EFCC_CONTRACT_DELTA=PASS`

`TARGET_RUNTIME_COMPATIBILITY=PASS_CONDITIONAL_ON_SAME_IMAGE_PREFLIGHT`

`LIVE_AUTHORIZATION=BLOCKED`

`SCORED_AUTHORIZATION=BLOCKED`

## Scope

Offline contract/runtime repair only. No POWDER reservation creation, no RF mutation, no cell execution, no restart, no teardown, and no scored work were performed by this patch.

## EFCC evidence authority

The prospective runtime contract is now bound to the independent read-only POWDER census:

- standard: `EFCC — Environment-First Compatibility Census Gate`
- workflow: `WP2 POWDER SSH Environment Inventory`
- GitHub run: `33124645486`
- experiment: `12b39276-af0f-4e34-8dfd-685b006dd6bd` / `wp7brq19810043`
- artifact: `9667857505`
- artifact ZIP SHA-256: `e0a1923af8ff1ffbbdf5bb20641f01ec9f81e5d96c67b0328260063f14848245`
- inner inventory TAR SHA-256: `b94c958a0b23bf812892680372485e6710b8f74b8368ea1c5c109e9f34d5541d`
- compatibility matrix: `docs/WP2_POWDER_RUNTIME_COMPATIBILITY_MATRIX_2026-08-28.md`

## Contract delta repaired

1. Added `experiments/WP-PWD01/p7b-target-runtime-contract-v2.json` as the prospective runtime contract. Historical v1 is retained for provenance only.
2. Bound `scripts/wp2_p7b_c_node_r2.py` to runtime-contract v2 rather than v1.
3. R2 now verifies the actual execution interpreter and exact `paho-mqtt==2.1.0` using `importlib.metadata` before entering the inherited qualification runner.
4. Target preflight now enforces the observed POWDER image/runtime facts: Ubuntu 18.04, system Python 3.6.9 as provenance-only, pinned Python 3.11.13, Paho MQTT 2.1.0, Bash 4.4.19 family, role-specific Java/Mosquitto, writable `/proj/WellPulse`, and exact UE-side B2 JAR SHA before RF.
5. Remote runtime/preservation dependency on `jq` is prohibited; `pkg_resources` is not accepted as the runtime metadata interface.
6. Preservation remains Bash/coreutils-only and does not depend on target Python.
7. Attenuator verification remains `SET_COMMAND_ACK_PLUS_INDEPENDENT_Q0_PATH_EVIDENCE`; no physical readback capability is claimed.
8. Portal `GET_ERROR` remains `UNKNOWN_CONTROL_PLANE_STATE`, not `NOT_READY` or `NOT_FOUND`.
9. SSH-agent/background-process state is explicitly step-local and may not be assumed across CI steps.
10. EFCC blocks live execution on any required dependency classified `MISSING`, `UNKNOWN`, `VERSION_INCOMPATIBLE`, `ROLE_MISMATCH`, or `UNTESTED`.

## Change provenance

- `ea331eb8d52e563e4fd8a474deedbd687bb6a4c8` — add EFCC-bound runtime contract v2
- `9a5486dc7fd9abb256c45f299516068c15d15c68` — bind authoritative R2 entrypoint to v2 and exact Paho metadata gate
- `f23eca1af95bd734933e06e1a4fad229e26122b4` — enforce EFCC target-runtime delta in node preflight
- `50b221c955ada1bd006578b82fa7fd522bed888a` — make static target-runtime QA enforce EFCC v2
- `acc37965c3d166daa4a3d5bc0633a99eae5d9194` — update R3C regression tests for EFCC v2

## QA evidence

- workflow: `Local Unit Tests`
- run: `33125917174`
- job: `98703917225`
- tested SHA: `acc37965c3d166daa4a3d5bc0633a99eae5d9194`
- Python: `3.12.14`
- Paho MQTT: `2.1.0`
- result: `119 tests`, `OK`
- static runtime QA emitted `WP2_P7B_TARGET_RUNTIME_QA=PASS` and `EFCC_CONTRACT_DELTA=PASS` through the regression suite.

## Required next gate

Before any future RF/cell execution, run the target-native preflight on the same image and exact staged source/dependency set. For UE, `WP_B2_JAR_PATH` must point to the staged Eclipse Paho Java 1.2.5 JAR and its SHA-256 must equal `59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185`.

A target-native preflight PASS is compatibility evidence only. It does not itself authorize a live qualification, replacement reservation, retry, or scored run.
