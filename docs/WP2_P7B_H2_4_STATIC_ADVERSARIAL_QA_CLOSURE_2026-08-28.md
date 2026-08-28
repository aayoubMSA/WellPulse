# WP2-P7B-H2.4 — Static + Adversarial QA Closure — 2026-08-28

## Terminal verdict

`H2_4_ADVERSARIAL_QA=PASS`

`POWDER_CONTACT=NO`

`NETWORK_CONTACT=NO`

`LIVE_SERVICE_MUTATION=NO`

`RF_MUTATION=NO`

`RETRY=NO`

`W1_B2=NO`

`SCORED=NO`

`TEARDOWN=NO`

H2.4 executed A7 only: offline static and synthetic adversarial QA of the prospective A1–A7 safety/observability controls. No live workflow, reservation, POWDER session, SSH to POWDER, RF mutation, service mutation, retry, scored execution, or teardown was authorized or performed.

## QA implementation

Reusable offline harness:

`scripts/wp2_p7b_h2_adversarial_qa.py`

Regression binding:

`tests/test_wp2_p7b_h2_adversarial_qa.py`

Machine-readable result:

`evidence/powder/wp2-p7b-h2-4-adversarial-qa.json`

The harness exercises the real prospective ownership functions, the real H2 restart-transition instrumentation, and the real H2 restore shell. The restore shell is executed only against a locally generated fake `ssh` executable so that faults can be injected without network contact.

## A7 required cases

All seven required cases passed:

1. `CONTROLLER_IN_TMUX_UE_REJECTED_BEFORE_RF=PASS`
2. `ALLOWED_CONTROLLER_SURVIVES_SERVICE_CLEANUP=PASS`
3. `SERVICE_OWNERSHIP_SELECTION_CANNOT_MATCH_CONTROLLER_PID_OR_SESSION=PASS`
4. `RESTART_TRANSITION_SURVIVES_SYNTHETIC_FAILURE_AFTER_GATEWAY_RESTART=PASS`
5. `EACH_RESTORE_PHASE_FAILURE_PRESERVES_LAST_FRONTIER=PASS`
6. `FROZEN_SCIENTIFIC_CONTROLS_UNCHANGED=PASS`
7. `AUTOMATIC_RETRY_NOT_INTRODUCED=PASS`

### Restore failure matrix

Synthetic failures were injected at:

- UE cleanup → last durable frontier `UE_CLEANUP_BEGIN`
- CORE cleanup → `CORE_CLEANUP_BEGIN`
- CORE start → `CORE_START_BEGIN`
- CORE stability → `CORE_START_END`
- UE start → `UE_START_BEGIN`
- UE readiness → `UE_START_END`
- service-ready probe → `SERVICE_READY_PROBE_END` with `status=FAIL`

This proves the diagnostic frontier remains available after each tested failure boundary.

### Restart-transition survival

The harness loads the actual `scripts/wp2_p7b_c_node_h2.py` instrumentation, supplies synthetic process objects, destroys the old gateway, starts a replacement with a distinct PID, passes the existing replacement-ready hook, verifies `restart_transition.json`, then injects a synthetic failure before any final `restart_proof.json`.

The transition file remains readable and unchanged after the synthetic failure. Therefore final-proof absence cannot erase the already-established incremental restart frontier.

## Preserved QA failure

Initial QA:

- implementation commit `410ee10c63b4caeb15d57507f6d6bd29fa0da1d6`
- run `33141172110`
- job `98752148529`
- suite: 163 tests
- result: FAIL
- adversarial harness itself: 7/7 required A7 cases PASS

Classification:

`TEST_HARNESS_FORBIDDEN_LITERAL_SELF_REFERENCE`

The failing test searched the QA source for forbidden text such as `portal-cli experiment create`; those literals were present only inside the QA harness's own forbidden-string detector. This was a test self-reference, not an executable authority surface and not an A1–A7 implementation failure.

The repair changed the check to inspect executable `_run(...)` subprocess arguments through the Python AST. No science, authority, or prospective experiment implementation was changed.

## Final QA

- final QA commit `a5854d30d83adcabd520f693b819cab9e59f7fa1`
- run `33141219303`
- job `98752288778`
- **163/163 tests PASS**
- H2.4-specific regression methods: 4/4 PASS
- A7 required adversarial cases: 7/7 PASS
- Python validation host: 3.12.14
- Paho MQTT: 2.1.0

## Scientific and authority preservation

No frozen scientific control changed. The H2.4 harness verifies science equivalence against `p7b-executable-contract-v2.json` and verifies automatic retry remains false.

H2.4 deliberately does not mutate the frozen base executable contract or the H2 delta implementation state. It is a QA-only patch. The separate machine-readable H2.4 result is the authority for this patch; H2.5 owns integrated contract/runtime regression and any subsequent offline promotion.

## Next patch

`WP2-P7B-H2.5 — CONTRACT/RUNTIME REGRESSION GATE`

H2.5 remains offline. It must integrate A1–A7 with the executable contract/runtime/EFCC and modular-pipeline assumptions, prove no scientific or interface regression, and issue PASS/BLOCKED. It must not contact POWDER or create live authority.

**STOP — H2.4 CLOSED. H2.5 NOT STARTED.**
