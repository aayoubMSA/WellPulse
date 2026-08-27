# WP2-P6 — Same-Reservation G0 Recovery Amendment — 2026-08-27

## Status

`P6_RECOVERY_AMENDMENT=FROZEN_PRE_RETRY`

`SECOND_RESERVATION_AUTHORIZED=NO`

`SCIENTIFIC_GOLDEN_ATTEMPT1=NOT_EXECUTED`

`SCORED_RUNS_AUTHORIZED=false`

Existing reservation only:

- experiment UUID: `5579cf25-dbb1-4d04-87e3-ff558e3be2af`;
- experiment name: `wpg7498036`;
- hard expiry: `2026-08-27T18:16:26Z`;
- original authorized node-source SHA: `bd1b5e12f3d2eca27ec81ccadbeec5afaa2f2159`.

## Why recovery is scientifically legitimate

Attempt 1 failed inside orchestrator G0 before G1/G2/G3. No sender/receiver workload, Q3 treatment, primary cohort or application outcome existed. The failure was solely the UE node being unable to resolve the internal management alias `enb1`.

Therefore a same-reservation management-plane repair is a technical pre-science recovery, not an outcome-driven repeat. Attempt 1 remains immutable infrastructure/provenance evidence.

## Exact repair

The recovery controller may only:

1. re-read the exact existing Portal experiment and require READY;
2. re-freeze exact manifest hardware/image/bindings and controller login endpoints;
3. derive the current core/UE management IPs from those exact manifested endpoints;
4. install explicit `enb1` and `rue1` aliases in the UE `/etc/hosts`;
5. prove UE->core and UE->UE SSH using those aliases;
6. reverify original node source SHA, profile revision, runtime and writable `/proj/WellPulse`;
7. restore Q0 and require 5/5 user-plane PASS;
8. then invoke the unchanged original Golden orchestrator from source SHA `bd1b5e12...`.

No profile, RF value, attenuation ID, application protocol, endpoint, recovery clock, H_app, evidence schema or claim is changed.

## Recovery-specific time gate

The original `2700 s` prelaunch bound included first-time provisioning, runtime bootstrap and Q0 preparation. Those stages have already completed on this exact live reservation and are reverified rather than rebuilt.

For same-reservation recovery, freeze:

`P6_RECOVERY_MIN_REMAINING_S=1800`

Rationale from already frozen timing rather than observed scientific outcome:

- protected application/RF schedule: `60 + 120 + 300 = 480 s`;
- architecture-blind service-ready gate remains bounded by `120 s`;
- 1800 s leaves approximately twice the frozen science/service-ready duration for management repair, evidence reconstruction, `/proj` escrow, controller pull, artifact upload/download/hash verification and teardown confirmation.

This is an operational lifecycle bound only. It does **not** change `H_app=300 s`, any endpoint, or any scientific inclusion/censoring rule.

## Experience-ledger controls

From the Drive Physical Validation Asset Ledger and Research Operating Doctrine v2.1:

- evidence survival has priority over cleanup convenience;
- node-local home is transient, `/proj` persistence plus off-platform read-back is mandatory before scientific teardown;
- capability catalog is not live availability evidence;
- preserve exact failure identity and repair the earliest actionable failure;
- do not regenerate or silently repair missing measurements;
- remote POWDER evidence supports wireless/network/edge claims only.

## Teardown

If the scientifically valid recovery run reaches protected G3 and then fails before verified evidence closure:

`AUTOMATIC_TERMINATION=PROHIBITED`

If it succeeds through persistent escrow, controller pull, GitHub artifact upload/download and outer+internal SHA-256 verification, only then may:

`EVIDENCE_ESCROW_GATE=PASS`

`TEARDOWN_AUTHORIZED=YES`

be issued and the same experiment terminated.

## Terminal rule

No second reservation may be created under this amendment. If this existing reservation cannot satisfy the frozen recovery gates, stop and preserve the failure record for a later explicit decision.
