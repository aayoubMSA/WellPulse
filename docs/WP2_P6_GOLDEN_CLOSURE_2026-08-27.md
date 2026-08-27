# WP2-P6 — Golden Rehearsal Closure — 2026-08-27

## Verdict

`WP2_P6=PASS_RECOVERED_SINGLE_RUN`

`SCIENTIFIC_MEASUREMENT_GATE=PASS`

`RAW_EVIDENCE_COMPLETE=PASS`

`EVIDENCE_ESCROW_GATE=PASS`

`TEARDOWN_AUTHORIZED=YES`

`TEARDOWN_CONFIRMED=YES`

`SCIENTIFIC_RERUN=NO`

`SECOND_RESERVATION=NO`

`scored_runs_authorized=false`

This is **not** represented as an uninterrupted clean G0-G10 automation pass. The protected non-scored Golden measurement completed through G7 on one reservation and one scientific run; deterministic post-run evidence-pipeline defects were recovered on that same immutable run without repeating RF treatment or measurement. All raw evidence was persisted, pulled off POWDER, artifact-read-back verified and hashed before teardown.

P6 therefore closes as a successful **recovered single-run qualification rehearsal**, while P7 remains responsible for deciding scored authorization after canonical hardening/QA of the defects revealed by the rehearsal.

## Experiment identity

- Reservation UUID: `5579cf25-dbb1-4d04-87e3-ff558e3be2af`
- Reservation name: `wpg7498036`
- Frozen profile: `PowderProfiles/srslte-controlled-rf`
- Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- Bindings: `enb_node=nuc1`, `ue_node=nuc2`, `ue_type=srsue`
- Hardware: `nuc5300`
- Image: `urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1`
- Scientific source SHA: `bd1b5e12f3d2eca27ec81ccadbeec5afaa2f2159`
- Scientific run ID: `wp2-p6r-33099648133-20260827T174149Z`
- Scored: **NO**

## Execution chronology

### Attempt 1 — pre-science G0 infrastructure failure

Actions run `33097498036`.

The reservation reached READY and passed profile/hardware/image/runtime/Q0 gates, but the first orchestrator invocation failed at G0 because UE could not resolve management alias `enb1`.

Classification:

`P6_ATTEMPT1=PRE_SCIENCE_G0_INFRASTRUCTURE_FAILURE`

No G3 workload, Q3 treatment, primary cohort or application outcome existed. The experiment was deliberately left live.

Canonical record:

`docs/WP2_P6_ATTEMPT1_PRE_SCIENCE_FAILURE_2026-08-27.md`

### Same-reservation recovery — protected measurement completed

Actions run `33099648133`.

Using the same UUID only, the controller derived exact management endpoints from the manifest, repaired aliases, reverified frozen source/profile/runtime/Q0, and executed the first scientifically material run.

Passed:

- G0 identity;
- G1 clean run path;
- G2 TLS/broker and detached receiver;
- G3 workload start;
- G4 Q3->Q0 restoration;
- G5 clean ordered LTE restoration;
- G6 architecture-blind service readiness;
- G7 fixed 300 s application observation.

Observed service-ready timestamp:

`t_service_ready = 2026-08-27T17:45:32.001525Z`

G8 then failed only in receiver-file collection because OpenSSH rejected the source form `.../receiver/.` with `unexpected filename: .`.

This occurred **after G7 completed**. The scientific run was not repeated.

### Post-run evidence recovery

The same immutable run was retained and recovered according to the experience-ledger rule `evidence survival before teardown`.

- Run `33100744938`: salvage v1 failed before data movement due a quoting defect in the recovery check.
- Run `33100989983`: receiver raw evidence was successfully transferred with a tar stream (`P6_RECEIVER_TAR_SALVAGE=PASS`); reconstruction then exposed a clock-authority defect.
- Run `33101403867`: corrected reconstruction succeeded on the immutable raw evidence; the node checkout lacked the current escrow helper, so final persistence remained pending.
- Run `33101564419`: final same-run persistence/controller/artifact/read-back/hash/teardown chain **PASS**.

No salvage workflow launched sender/receiver science, changed RF, created a second reservation, or edited the raw measurement.

## Reconstruction correction and provenance

The prior reconstruction implementation inferred `t_rf_restore` from the **last Q0 command** in `attenuation_timeline.csv`. The sender also emits a fail-safe cleanup Q0 in `finally` after the 300 s horizon, so that inference can select the cleanup command and falsely place RF restoration after service readiness.

Corrected authority:

`sender/rf_restore.ready`

The marker is emitted prospectively at the actual treatment-ending Q3->Q0 command and is now cross-checked against exactly one matching Q0 `command_end_utc` row in the immutable attenuation timeline.

Canonical analysis-fix commit:

`b7389f5e38276673333a44ba2f5cf013cb60cc2f`

Reconstruction script SHA-256 used on the live raw evidence:

`3163516253e60a5a5850ae31ef4c45d626173753ba2dcb369c216f569ef3ead1`

The evidence bundle contains `analysis/reconstruction_provenance.txt` recording:

- original scientific source SHA;
- reconstruction-fix commit;
- reconstruction-script SHA-256;
- `raw_measurement_modified=NO`;
- `scientific_rerun=NO`.

A regression test was added at:

`tests/test_golden_reconstruction_clock_authority.py`

to ensure a trailing cleanup Q0 cannot replace `rf_restore.ready` as the treatment clock.

## Verified non-scored endpoint reconstruction

Independent artifact read-back verified:

- `t_rf_restore = 2026-08-27T17:45:06.913285Z`
- `t_service_ready = 2026-08-27T17:45:32.001525Z`
- `T_service = 25.088240 s`
- `t_app_complete = 2026-08-27T17:45:37.295360Z`
- `T_app = 5.293835 s`
- `T_total = 30.382075 s`
- primary cohort = `181`
- valid primary-cohort records received by horizon = `181`
- `completeness_300 = 1.0`
- missing by horizon = `0`
- checksum mismatch attempts = `0`
- duplicate valid attempts = `0`
- late valid attempts = `0`

These are **non-scored qualification observations** and do not enter the confirmatory WP3 corpus.

The reconstruction currently reports `unexpected_attempts=325`. Because post-`t_rf_restore` generation intentionally continues as realistic load and is excluded only from the primary denominator, P7 must review whether this counter is conflating valid post-cohort traffic with truly unexpected IDs before scored authorization. This does not change the reconstructed primary endpoint above.

## Evidence survival and off-platform proof

Final Actions run:

`33101564419`

Persistent path before teardown:

`/proj/WellPulse/evidence-escrow/5579cf25-dbb1-4d04-87e3-ff558e3be2af/wp2-p6r-33099648133-20260827T174149Z`

Controller deterministic TAR SHA-256:

`ff72a50fd11db1d308f4049b49fffa317c8220c9290845434dbadc8dbef847cf`

GitHub Actions artifact:

- ID: `9658678808`
- name: `wp2-p6-final-33101564419`
- bytes: `1,157,340`
- artifact ZIP SHA-256: `69bd6927c66008be66d919bd2ec4d635b6f704a02834cee2801ef5de59e183dc`
- retention expiry: `2026-11-25T18:03:32Z`

Independent download/read-back established:

`CONTROLLER_OFFPOWDER_GATE=PASS`

`ROUNDTRIP_BUNDLE_SHA256=ff72a50fd11db1d308f4049b49fffa317c8220c9290845434dbadc8dbef847cf`

`EVIDENCE_ESCROW_GATE=PASS`

`TEARDOWN_AUTHORIZED=YES`

Only after those states were reached was the exact experiment terminated; termination was confirmed at `2026-08-27T18:04:31Z`.

This directly validates the critical Drive experience-ledger lesson learned from H1: node-local home is not archival storage and teardown must wait for persistent plus independently verified off-platform evidence.

## P7 entry conditions / mandatory hardening before scored authorization

P7 may begin only after explicit user continuation. It must **not** authorize scored work merely because P6 evidence is valid.

Mandatory P7 checks include:

1. replace the orchestrator G8 `scp .../receiver/.` transport with the live-validated tar/stream or equivalently qualified exact-file transfer;
2. verify the corrected `rf_restore.ready` reconstruction authority by regression QA;
3. review/fix `unexpected_attempts` semantics so planned post-cohort load is not mislabeled as unexpected scientific traffic;
4. verify future controller preparation always installs/validates exact manifest-derived `enb1/rue1` management aliases before G0;
5. retire P6 one-off live/recovery/salvage workflow and trigger surfaces from active Actions;
6. rerun bounded offline/static QA only; no new Golden is authorized by this closure;
7. then issue the explicit P7 decision: `SCORED_AUTHORIZATION=PASS|BLOCKED`.

## Final P6 state

`WP2_P6=PASS_RECOVERED_SINGLE_RUN`

`P6_CLEAN_UNINTERRUPTED_ORCHESTRATOR_E2E=NO`

`P6_SCIENTIFIC_RERUN_REQUIRED=NO`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

`WP2_MANAGEMENT_READINESS_PROGRESS=95/100`

Scientific weighted completion remains **20%** until P7 closes WP2 scientifically.

**STOP BEFORE WP2-P7.**
