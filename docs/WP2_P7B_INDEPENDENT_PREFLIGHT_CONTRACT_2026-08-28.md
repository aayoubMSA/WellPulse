# WP2-P7B Independent Preflight Contract

Status: OFFLINE DESIGN / NOT LIVE-AUTHORIZED

Purpose: provide an orthogonal, read-only target-environment preflight for an already-existing POWDER reservation. It must not reuse the R3 controller, the existing target-node preflight wrapper, Portal bootstrap helpers, project readiness parsers, RF mutation code, scientific cells, or teardown code.

## Required live inputs

A future explicitly authorized live invocation must receive only the already-resolved node access coordinates and credentials:

- CORE_HOST / CORE_USER / CORE_PORT
- UE_HOST / UE_USER / UE_PORT
- POWDER_SSH_PRIVATE_KEY / passphrase

The probe must not create, extend, modify, or terminate a reservation.

## Required observations

For each target node, directly through SSH and basic shell commands:

1. hostname, kernel, Bash version;
2. system Python version for provenance only;
3. exact pinned Python interpreter version, expected 3.11.13;
4. paho-mqtt import/version through the pinned interpreter;
5. Java major version on UE, expected 11;
6. Mosquitto daemon presence on CORE;
7. required shell preservation primitives;
8. /proj/WellPulse existence and writability;
9. direct route/interface observation;
10. syntax compilation of representative project Python with the exact pinned interpreter;
11. shell-only tar + SHA-256 preservation round-trip under /proj.

## Prohibited dependencies/actions

The independent probe must not execute or source:

- powder/wp2_p7b_r3_execute.sh
- scripts/wp2_p7b_target_node_preflight.sh
- scripts/wp2_portal_client_bootstrap.sh
- scripts/wp2_p7b_validate_readiness*
- scripts/wp2_p7b_r2_validate_controller.py

It must also contain no reservation create/terminate action, no RF attenuation mutation, and no B1/W1/B2 execution.

## Acceptance

Offline QA passes only if adversarial tests prove the probe remains syntactically valid, orthogonal to the existing control stack, read-only, single-process for SSH-agent lifetime, pinned-runtime aware, and independent of any workflow/trigger.

A later live probe requires separate explicit authorization and is not granted by this contract.
