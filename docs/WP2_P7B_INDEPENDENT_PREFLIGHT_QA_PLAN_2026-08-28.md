# WP2-P7B Independent Preflight QA Plan

This QA plan is offline-only.

## Static gates

- bash syntax validation of scripts/wp2_p7b_independent_preflight.sh
- no reservation create/terminate commands
- no attenuation mutation commands
- no invocation/source of the R3 controller, current target preflight, Portal bootstrap helper, readiness parser, or controller validator
- SSH agent creation and ssh-add occur in the same process that performs both node probes
- exact pinned Python version gate is present
- paho-mqtt is queried through the pinned interpreter
- representative project Python is compiled by the pinned interpreter
- shell-only /proj tar + SHA-256 round-trip is present
- no independent-preflight workflow or trigger exists

## Adversarial gates

The probe must fail closed when any of these are absent or mismatched at runtime:

- SSH key cannot be loaded
- CORE/UE coordinates missing
- pinned Python absent or not 3.11.13
- paho-mqtt import unavailable
- Java major on UE is not 11
- Mosquitto daemon absent on CORE
- /proj/WellPulse missing or not writable
- required shell tool missing
- representative source cannot compile under pinned Python
- preservation round-trip hash verification fails

## Live authority

No live execution is authorized by this QA plan. A future live invocation must be separately authorized after offline QA passes.
