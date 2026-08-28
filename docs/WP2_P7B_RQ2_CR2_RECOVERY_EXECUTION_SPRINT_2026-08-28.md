# WP2-P7B-RQ2 — CR2 Recovery Execution Sprint — 2026-08-28

## Sprint objective

Restore the current reservation `wp7brq2609012` to the known-good pre-RF environment contract by replaying the complete historical provisioning sequence, then run the authoritative frozen target-native preflight and STOP before any RF/cell action.

## Scope boundary

This sprint is pre-RF only.

Permitted only after separate explicit live authorization:
- bounded SSH to the existing reservation only;
- replay of the historical system bootstrap on CORE and UE;
- pinned Python/Paho runtime verification;
- exact B2 Eclipse Paho Java 1.2.5 JAR staging/hash verification on UE;
- authoritative `scripts/wp2_p7b_target_node_preflight.sh` execution on CORE and UE;
- evidence upload/readback;
- quiet periods and status checks.

Explicitly prohibited:
- new reservation;
- RF attenuation mutation;
- B1/W1/B2 cell execution;
- srsLTE service/profile restart;
- broker start/restart;
- scientific retry;
- scored run;
- teardown.

## Canonical recovered baseline

Known-good historical system bootstrap:

CORE:
`mosquitto mosquitto-clients rsync tmux curl unzip openssl`

UE:
`mosquitto-clients rsync tmux curl unzip openssl default-jdk-headless`

Then on both nodes:
- exact Python `3.11.13` via `scripts/wp2_a3_runtime_bootstrap.sh`;
- exact `paho-mqtt==2.1.0`;
- system Python remains provenance-only (`3.6.9`).

UE additionally requires:
- Java major 11;
- exact Eclipse Paho Java 1.2.5 JAR;
- JAR SHA-256 `59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185`.

CORE additionally requires:
- Mosquitto daemon binary version `1.4.15` present;
- daemon must NOT be started by this sprint.

Authoritative runtime contract:
`experiments/WP-PWD01/p7b-target-runtime-contract-v2.json`

Authoritative node preflight:
`scripts/wp2_p7b_target_node_preflight.sh`

The prior `.github/workflows/wp2-p7b-rq2-slow-target-preflight.yml` is non-authoritative and must not be used for final contract qualification.

## Patch plan

### CR2-P0 — Offline executable-contract freeze

Goal: build one bounded execution workflow from the recovered known-good sequence before any live contact.

Requirements:
- exact current reservation UUID/name pinned;
- exact profile/image/hardware identity gates retained;
- exact system package lists above, no additions;
- package versions must resolve to the Ubuntu 18.04 contract family; any version drift blocks;
- use `policy-rc.d` or equivalent only to prevent package auto-start where applicable;
- no broker/service start/restart command;
- exact source staging defined before authoritative preflight;
- exact B2 JAR download URL + SHA gate frozen;
- every live mutation named and finite;
- `RF=NO`, `CELLS=NO`, `RESTART=NO`, `TEARDOWN=NO`, `SCORED=NO` statically enforced.

Acceptance:
`CR2_P0=PASS_OFFLINE_EXECUTABLE_CONTRACT_FREEZE`

STOP if static contract contains any command outside the recovered baseline.

### CR2-P1 — Current-reservation identity/time gate

Goal: prove the reservation is still the intended usable target before mutation.

Checks:
- experiment UUID exactly `f6de95cb-a13a-421e-bd0e-766dfc1d3fb3`;
- name exactly `wp7brq2609012`;
- project `WellPulse`;
- status `ready`;
- profile revision exact;
- hardware `nuc5300`;
- image `U18LL-SRSLTE:1` / Ubuntu 18.04;
- CORE=`nuc1`, UE=`nuc2`;
- sufficient remaining reservation time for CR2 only.

Acceptance:
`CR2_P1=PASS_TARGET_IDENTITY_AND_TIME`

STOP on any mismatch or insufficient time. No replacement reservation automatically.

### CR2-P2 — Full known-good system bootstrap replay

Goal: restore the complete historical pre-RF system dependency set, not symptom-by-symptom repairs.

CORE exact target set:
- mosquitto
- mosquitto-clients
- rsync
- tmux
- curl
- unzip
- openssl

UE exact target set:
- mosquitto-clients
- rsync
- tmux
- curl
- unzip
- openssl
- default-jdk-headless

Rules:
- idempotent package convergence is allowed;
- already-present matching packages are not treated as an error;
- package auto-start must be prevented;
- no service/broker start/restart;
- no unrelated package installation;
- capture exact installed versions after convergence.

Acceptance:
`CR2_P2=PASS_KNOWN_GOOD_SYSTEM_BOOTSTRAP`

STOP on package/version drift, repository ambiguity that changes selected package versions, or any service auto-start that cannot be proven absent.

### CR2-P3 — Pinned project runtime and source staging

Goal: restore the exact execution interpreter and project runtime.

Actions:
- stage exact authorized source set to both nodes;
- execute the recovered `scripts/wp2_a3_runtime_bootstrap.sh`;
- verify Python `3.11.13`;
- verify `paho-mqtt==2.1.0` via `importlib.metadata`;
- verify system Python is not used for project code;
- verify source syntax under pinned interpreter.

Acceptance:
`CR2_P3=PASS_PINNED_PROJECT_RUNTIME`

STOP on any interpreter/dependency/source mismatch.

### CR2-P4 — Exact B2 Java dependency reconstruction

Goal: restore the dependency required by the frozen B2 arm before authoritative preflight.

Actions on UE only:
- verify Java major 11;
- acquire Eclipse Paho Java 1.2.5 JAR from the frozen Maven path;
- verify SHA-256 exactly `59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185`;
- stage it at one explicitly recorded path for `WP_B2_JAR_PATH`;
- do not execute B2.

Acceptance:
`CR2_P4=PASS_B2_DEPENDENCY_RECONSTRUCTION`

STOP on hash/version mismatch.

### CR2-P5 — Quiet period + authoritative target-native preflight

Goal: qualify the restored environment using the frozen contract, not the ad-hoc slow preflight.

Run on both nodes:
`scripts/wp2_p7b_target_node_preflight.sh`

Required outputs include on each node:
- target OS/image identity PASS;
- system Python provenance PASS;
- pinned Python PASS;
- Paho MQTT exact PASS;
- required command set PASS;
- Bash family PASS;
- role-specific Java/Mosquitto PASS;
- `/proj/WellPulse` writable PASS;
- source syntax PASS;
- no runtime `pkg_resources` dependency;
- no remote `jq` dependency;
- preservation helper checks PASS;
- UE B2 JAR exact SHA PASS;
- `EFCC_RUNTIME_BINDING=PASS`;
- `WP2_P7B_TARGET_NODE_PREFLIGHT=PASS`.

Acceptance:
- CORE `WP2_P7B_TARGET_NODE_PREFLIGHT=PASS`;
- UE `WP2_P7B_TARGET_NODE_PREFLIGHT=PASS`;
- overall `CR2_P5=PASS_AUTHORITATIVE_TARGET_NATIVE_PREFLIGHT`.

STOP on first named failure. No automatic repair loop and no automatic rerun.

### CR2-P6 — Evidence survival and independent verification

Goal: make CR2 independently auditable before any later RF authorization.

Required evidence:
- authority manifest;
- current reservation identity/time snapshot;
- exact package/version inventories after convergence;
- pinned runtime outputs;
- B2 JAR path/hash;
- CORE/UE authoritative preflight logs;
- source archive/hash;
- final reservation-ready status;
- GitHub artifact upload;
- independent artifact readback and SHA-256 verification.

Acceptance:
`CR2_P6=PASS_EVIDENCE_ROUNDTRIP`

## Sprint Definition of Done

CR2 is complete only if all six gates pass:

`P0 PASS -> P1 PASS -> P2 PASS -> P3 PASS -> P4 PASS -> P5 PASS -> P6 PASS`

Final sprint verdict must be exactly one of:

`WP2_P7B_RQ2_CR2=PASS_RECOVERED_PRE_RF_ENVIRONMENT`

or

`WP2_P7B_RQ2_CR2=BLOCKED:<first_named_reason>`

## Mandatory STOP

Even on full PASS:
- do not set attenuation;
- do not start B1/W1/B2;
- do not start/restart broker or srsLTE services;
- do not teardown;
- do not claim P7B scientific qualification;
- do not authorize scored execution.

A separate explicit user authorization is required for any subsequent physical qualification action.

## Progress model

- CR2-P0: 15%
- CR2-P1: 10%
- CR2-P2: 20%
- CR2-P3: 15%
- CR2-P4: 10%
- CR2-P5: 20%
- CR2-P6: 10%

Current state at sprint creation:
`CR2=PLANNED / 0% LIVE EXECUTION / WAITING FOR EXPLICIT AUTHORIZATION`
