# WP2-P7B-R3E — Target-Native EFCC Preflight Closure — 2026-08-28

## Verdict

`WP2_P7B_R3E=PASS_TARGET_NATIVE_EFCC_PREFLIGHT`

This is a **pre-RF compatibility/preflight PASS only**. It does not authorize RF mutation, B1/W1/B2 execution, a new reservation, teardown, scored work, or scored authorization.

## Existing reservation only

- Experiment UUID: `12b39276-af0f-4e34-8dfd-685b006dd6bd`
- Experiment name: `wp7brq19810043`
- CORE: `nuc1.emulab.net`
- UE: `nuc2.emulab.net`
- New reservation: `NO`
- RF mutation: `NO`
- Cells: `NO`
- Restart: `NO`
- Teardown: `NO`
- Scored: `NO`

## Authoritative target-runtime contract

- `experiments/WP-PWD01/p7b-target-runtime-contract-v2.json`
- schema: `wp2-p7b-target-runtime-contract-v2`
- EFCC target runtime is the compatibility baseline.
- Project Python must be pinned target Python, not system Python.
- Role-specific dependencies are enforced asymmetrically.
- Remote `jq` is prohibited as a dependency.
- Evidence preservation is shell/coreutils-only.
- Physical attenuation readback is not claimed where the observed tmcc interface does not expose a machine-readable readback.

## Live target-native PASS

Accepted run:

- GitHub Actions run: `33126350285`
- job: `98705325426`
- head/source SHA: `13b34c8dc4b515c010a5b531eaaaf40cfcd00c49`
- staged current-source TAR SHA-256: `95000267615168f7e58ee68206af38345684d1991ea64d50f4c3714dbc67f5dc`
- artifact ID: `9668505622`
- artifact ZIP SHA-256: `479b5667f02b9d0921969ca7b2047ac5fe37537d743188b82f9d9fae7daf4efd`
- artifact retention expiry: `2026-11-25T23:27:37Z`

Both nodes passed the same-image target-native checks against the current staged source:

- OS: Ubuntu `18.04`
- system Python observed: `3.6.9`
- system Python for project code: `PROHIBITED`
- pinned Python: `3.11.13`
- `paho-mqtt`: `2.1.0`
- current runtime sources syntax-compile under pinned Python
- `pkg_resources` is not required by runtime gate
- Bash target contract PASS
- CORE Mosquitto daemon contract PASS (`1.4.15`)
- UE Java contract PASS (major `11`)
- UE B2 Paho Java JAR exact SHA gate PASS (`59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185`)
- `/proj/WellPulse` presence/writeability PASS
- required shell preservation tools PASS
- remote `jq` dependency prohibited
- `ATTENUATOR_PREFLIGHT=FIXTURE_ONLY_NO_LIVE_TMCC_READBACK`
- `EFCC_RUNTIME_BINDING=PASS`
- `WP2_P7B_TARGET_NODE_PREFLIGHT=PASS` on CORE and UE

Final workflow marker:

`WP2_P7B_R3D_TARGET_NATIVE_PREFLIGHT=PASS`

## Retained failed preflight attempts

### Attempt 1 — run `33126193277`

Blocked on the GitHub controller before SSH because the workflow invented an `efcc` field instead of consuming the actual v2 contract schema (`efcc_gate` / `efcc_evidence`). POWDER was untouched.

### Attempt 2 — run `33126274200`

Reached CORE and confirmed Ubuntu 18.04 / system Python 3.6.9 / pinned Python 3.11.13 / Paho 2.1.0, then failed because `mosquitto -h` on the observed 1.4.15 build returns a non-zero diagnostic exit status despite printing usable version output. The preflight was hardened to treat diagnostic CLI output and semantic validation separately from command RC. No RF/cells occurred.

The accepted Attempt 3 then passed on both nodes.

## Authority-surface retirement

After evidence/artifact confirmation:

1. workflow removed first: commit `b35c8ccf4fd3f0bc6fb5d6053a3931ad9b7ad945`;
2. trigger removed second: commit `08046eb8a1d29e06b5fbd1f35d73dd514cc3dc8d`;
3. trigger-deletion commit produced `0` workflow runs.

This follows the trigger-retirement safety rule and leaves no active R3D preflight live surface on `main`.

## Claim boundary / next gate

`LIVE_AUTHORIZATION=NOT_GRANTED_BY_R3E`

`SCORED_AUTHORIZATION=BLOCKED`

A fresh explicit authorization is required before any same-reservation RF mutation or non-scored P7B cell execution.
