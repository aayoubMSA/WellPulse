# WP2-P7B-RQ2 — Contract Recovery Sprint — 2026-08-28

## Verdict

`CONTRACT_RECOVERY_SPRINT=PASS`

`ROOT_CAUSE=RQ2_PROVISIONING_SEQUENCE_INCOMPLETE_AND_PREFLIGHT_DRIFTED_FROM_AUTHORITATIVE_EFCC_CONTRACT`

`CURRENT_RESERVATION_RECOVERABLE=YES_CONDITIONAL`

`CURRENT_RESERVATION_CONTAMINATED_REPLACE_REQUIRED=NO`

`LIVE_ACTION_AUTHORIZED_BY_THIS_RECORD=NO`

`RF_AUTHORIZED=NO`

`CELLS_AUTHORIZED=NO`

`RESTART_AUTHORIZED=NO`

`TEARDOWN_AUTHORIZED=NO`

`SCORED_AUTHORIZED=NO`

## Scope

Offline/read-only recovery of the known-good provisioning and preflight path. No POWDER contact, SSH, package installation, RF mutation, cell execution, restart, teardown, or scored work was performed by this sprint.

## Canonical contract recovered

The prospective runtime contract is `experiments/WP-PWD01/p7b-target-runtime-contract-v2.json` and the authoritative target-native gate is `scripts/wp2_p7b_target_node_preflight.sh`.

The v2 contract requires, among other things:

- Ubuntu 18.04 / `nuc5300` / frozen profile image;
- pinned Python `3.11.13` and `paho-mqtt==2.1.0` on both nodes;
- `mosquitto_pub` on both nodes;
- Mosquitto daemon `1.4.15` on CORE only;
- Java major 11 on UE only;
- exact Eclipse Paho Java 1.2.5 JAR SHA-256 `59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185` on UE before RF;
- Bash/coreutils preservation dependencies and writable `/proj/WellPulse`;
- remote `jq` dependency prohibited;
- authoritative source staging and target-Python syntax checks before RF.

Therefore the earlier CORE Mosquitto and UE Mosquitto-client installations did **not** change the scientific MQTT contract. They restored dependencies already present in the frozen v2 runtime baseline. The mistake was operational: they were repaired symptom-by-symptom rather than replaying the known-good provisioning sequence.

## Known-good provisioning sequence recovered

The historical P7B-C controller at source `a582b95ceef5705c7c1204df2c9dd637717dcef1` performed the following before any scientific cell:

1. freeze profile/hardware/image identity;
2. copy exact authorized source to both nodes;
3. perform complete role-specific system bootstrap;
4. perform pinned A3 Python runtime bootstrap on both nodes;
5. establish Q0 only after runtime bootstrap;
6. compile/download and hash-lock the exact B2 Java runtime before B1/W1/B2 execution.

Exact historical system bootstrap:

```text
CORE:
  apt install mosquitto mosquitto-clients rsync tmux curl unzip openssl

UE:
  apt install mosquitto-clients rsync tmux curl unzip openssl default-jdk-headless
```

Then both nodes ran `scripts/wp2_a3_runtime_bootstrap.sh`, producing Python 3.11.13 and Paho MQTT 2.1.0.

The B2 runtime downloaded Eclipse Paho Java 1.2.5 from Maven, verified the exact frozen SHA-256, and compiled `experiments/WP-PWD01/b2-semantics/P7BRemoteB2Gateway.java` with `javac` into the evidence runtime tree.

## Accepted R3E preflight recovered

Accepted run `33126350285`, job `98705325426`, source `13b34c8dc4b515c010a5b531eaaaf40cfcd00c49`:

- staged the exact source set into a temporary directory on both nodes;
- invoked the authoritative `scripts/wp2_p7b_target_node_preflight.sh` rather than reproducing checks inline;
- supplied the exact UE B2 JAR through `WP_B2_JAR_PATH`;
- required `WP2_P7B_TARGET_NODE_PREFLIGHT=PASS` and `EFCC_RUNTIME_BINDING=PASS` on both nodes;
- produced artifact `9668505622`, ZIP SHA-256 `479b5667f02b9d0921969ca7b2047ac5fe37537d743188b82f9d9fae7daf4efd`;
- performed no RF/cells/restart/teardown/scored work.

## RQ2 drift identified

### D1 — incomplete bootstrap

`.github/workflows/wp2-p7b-rq2-slow-runtime-bootstrap.yml` stages the scientific source and runs only `scripts/wp2_a3_runtime_bootstrap.sh` on CORE/UE. It omits the historical role-specific **system bootstrap** entirely.

This explains the fresh-reservation sequence:

- CORE initially lacked `mosquitto`;
- UE initially lacked `mosquitto_pub`;
- further UE checks could still fail because the complete historical UE package set, especially `default-jdk-headless`, was never replayed as a unit.

### D2 — preflight implementation drift

`.github/workflows/wp2-p7b-rq2-slow-target-preflight.yml` does not invoke the authoritative target preflight. It duplicates a reduced set of inline shell checks.

Material differences from the frozen gate include:

- no exact source staging for the authoritative source set;
- no call to `scripts/wp2_p7b_target_node_preflight.sh`;
- no target-Python syntax compilation of the frozen runtime sources;
- no Bash 4.4.19 family gate;
- no CORE Mosquitto exact-version gate;
- no mandatory `WP_B2_JAR_PATH` supply and exact UE JAR gate;
- no authoritative `EFCC_RUNTIME_BINDING=PASS` marker;
- UE Java is checked against an ad-hoc exact text match `11.0.19`, whereas the authoritative prospective preflight gates Java major 11 and the compatibility evidence separately records 11.0.19 as the observed baseline.

Therefore `RQ2_SLOW_PREFLIGHT=BLOCKED:UE` from this workflow is **not a valid substitute for the frozen EFCC target-native preflight verdict**.

## Current-reservation delta audit

The two package repairs already made on `wp7brq2609012` are aligned with the historical package versions:

- CORE Mosquitto installed as Ubuntu package `1.4.15-2ubuntu0.18.04.3`; CLI reported Mosquitto `1.4.15`; daemon was explicitly not started and remained not running after the quiet period.
- UE `mosquitto-clients` installed as `1.4.15-2ubuntu0.18.04.3`; `mosquitto_pub` and `mosquitto_sub` became present; no Mosquitto daemon was running after the quiet period.

These are contract-aligned runtime dependencies, not scientific-protocol changes. No RF/cells/restart/teardown occurred during either repair.

The current reservation is therefore not invalidated merely by those package installations. It remains **conditionally recoverable**, provided recovery re-enters the known-good contract path and passes the authoritative target-native gate before any RF mutation.

## Bounded recovery patch to own next

`RQ2-CR2 — REPLAY KNOWN-GOOD PRE-RF PROVISIONING AND AUTHORITATIVE PREFLIGHT`

Only after fresh explicit live authorization, execute exactly:

1. confirm same reservation/profile/hardware/image identity and adequate remaining time;
2. stage exact frozen source set;
3. apply the complete historical role-specific system bootstrap idempotently:
   - CORE package set exactly as recovered above;
   - UE package set exactly as recovered above;
4. run the byte-identical pinned A3 runtime bootstrap on both nodes;
5. stage/build the exact B2 Paho Java 1.2.5 runtime and verify frozen JAR SHA;
6. quiet period;
7. run the authoritative `scripts/wp2_p7b_target_node_preflight.sh` on CORE and UE using the staged source and explicit `WP_B2_JAR_PATH`;
8. require both `WP2_P7B_TARGET_NODE_PREFLIGHT=PASS` and `EFCC_RUNTIME_BINDING=PASS`;
9. upload immutable evidence;
10. STOP.

No RF, cells, restart, teardown, or scored execution belongs to CR2.

## STOP conditions

Stop before RF if any of the following occurs:

- profile/hardware/image mismatch;
- missing or incompatible required package/runtime;
- pinned Python/Paho mismatch;
- Java major mismatch on UE;
- Mosquitto version mismatch on CORE;
- B2 JAR missing/hash mismatch;
- source staging or target-Python syntax failure;
- `/proj/WellPulse` not writable;
- authoritative preflight does not emit PASS on both nodes;
- remaining reservation time is insufficient for the later bounded qualification.

No symptom-by-symptom package repair is permitted after such a block. Return to the recovered provisioning contract and diagnose the exact delta first.

## Doctrine recovered

`Never repair a frozen-contract environment symptom-by-symptom. Reconstruct and replay the known-good provisioning contract, then invoke the authoritative preflight implementation.`
