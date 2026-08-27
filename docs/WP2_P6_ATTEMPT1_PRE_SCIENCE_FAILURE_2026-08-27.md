# WP2-P6 Attempt 1 — Pre-Science G0 Infrastructure Failure — 2026-08-27

## Classification

`P6_ATTEMPT1=PRE_SCIENCE_G0_INFRASTRUCTURE_FAILURE`

`SCIENTIFIC_GOLDEN_EXECUTED=NO`

`RF_TREATMENT_EXECUTED=NO`

`SCORED_RUN=NO`

`TEARDOWN_AUTHORIZED=NO`

`EXPERIMENT_LEFT_LIVE=5579cf25-dbb1-4d04-87e3-ff558e3be2af`

This attempt is preserved as infrastructure/provenance evidence only. It is not a scientific Golden outcome and must not be interpreted as an application failure.

## Evidence

GitHub Actions run: `33097498036`  
Job: `98606121049`  
Authorized source SHA: `bd1b5e12f3d2eca27ec81ccadbeec5afaa2f2159`  
Experiment ID: `5579cf25-dbb1-4d04-87e3-ff558e3be2af`  
Experiment name: `wpg7498036`  
Portal hard expiry: `2026-08-27T18:16:26Z`  
Initial Golden run ID: `wp2-p6-33097498036-20260827T172441Z`

Resource advisory preflight was fetched successfully but intentionally classified:

`RESOURCE_AVAILABILITY_PREFLIGHT=UNKNOWN`

Reason:

`AMBIGUOUS_UNPARSED_ADVISORY_PAGE`

The authoritative Portal path then passed:

- no active Golden conflict;
- one reservation created;
- lifecycle `provisioning -> provisioned -> ready`;
- exact experiment ID and expiry bound;
- `PRELAUNCH_TIME_GATE=PASS`, with 3283 s remaining at the gate;
- exact manifest hardware/image/logical-to-physical mapping PASS;
- both controller-to-node SSH paths PASS;
- exact profile repository revision `a6da96560b6526dc6816761282722c996418fd8c` on both nodes;
- `/proj/WellPulse` writable on both nodes;
- frozen runtime bootstrap completed;
- clean Q0 baseline passed 5/5 over `tun_srsue`.

## Exact failure

The orchestrator was invoked after the Q0 pre-science gate. At G0 environment identity it attempted the frozen internal management alias:

`ssh aayoub@enb1 ...`

from the UE/application node. The current reservation did not resolve that alias:

`ssh: Could not resolve hostname enb1: Name or service not known`

The orchestrator immediately emitted:

`GOLDEN_E2E=FAIL_G0:CORE_IDENTITY`

No G1/G2/G3 was reached. Therefore:

- no sender workload was launched;
- no receiver was launched;
- no Q3 attenuation treatment occurred;
- no primary cohort exists;
- no scientific application outcome exists;
- no persistent scientific raw bundle is required for this pre-science abort.

The P6 controller's `SCIENCE_STARTED=1` marker was set immediately before invoking the orchestrator and therefore overstates this attempt's scientific stage. The authoritative gate chronology shows failure inside G0 before workload/treatment. Future controller logic must distinguish `ORCHESTRATOR_INVOKED` from actual protected-science start at G3.

## Fail-closed effect

Because the controller conservatively treated the orchestrator invocation as science-started, it did not auto-terminate. This protected evidence and left the reservation live:

`AUTOMATIC_TERMINATION=PROHIBITED`

`TEARDOWN_AUTHORIZED=NO`

Artifact upload/download/finalization were correctly skipped because no verified persistent Golden bundle existed.

## Recovery decision

Use **the same existing reservation only**. Do not create a second reservation.

A bounded pre-science recovery may proceed only if:

1. Portal still reports the exact experiment READY with sufficient remaining time;
2. exact profile/hardware/image/bindings remain unchanged;
3. controller-to-node SSH remains valid;
4. the UE can resolve and SSH to the exact core management endpoint through an explicitly frozen alias repair derived from the Portal manifest;
5. Q0 5/5 is re-established before any workload;
6. no scientific state from Attempt 1 is reused.

The repair is management-plane-only. It must not change RF settings, profile, application protocol, recovery semantics, evidence contract, or `H_app=300 s`.

If these pre-science gates pass, the same reservation may host the first scientifically valid P6 Golden attempt. If they do not pass, preserve the reservation/evidence state and stop rather than opening a second reservation.
