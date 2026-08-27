# Agent Handover — WellPulse WP2 K-Fastlane

**Date:** 2026-08-27  
**Canonical repo:** `aayoubMSA/WellPulse`  
**Branch:** `main`  
**Purpose:** exact continuation point after the first bounded K-fastlane live compatibility reservation completed and failed before READY.

## 0. Exact retrieval point

Do **not** create another POWDER reservation immediately on resume.

First read the final result of the already-completed compatibility-only run:

- Workflow: `WP2 K-Fastlane Live Compatibility Gate`
- Run ID: `33084240768`
- Trigger commit: `dd275a3f7dbc75a7096b587ae3f01d61ff801411`
- Created experiment UUID: `02bc305d-5d84-48f9-b518-dbebd1728ee6`
- Classification: `INFRASTRUCTURE_ONLY_NON_SCORED`
- Authorized reservations: exactly `1`
- Duration requested: `1 hour`
- Golden workload: `false`
- H calibration: `false`
- Scored run: `false`

Final workflow result: **FAILURE at Portal readiness gate**.

Observed Portal lifecycle:

`provisioning -> failed`

Specifically:

- `PORTAL_POLL_1=provisioning`
- `PORTAL_POLL_2=failed`
- workflow exited step 6 with rc `21`

Because the reservation never reached READY, all later live checks were skipped:

- manifest hardware/image/login identity;
- runtime/profile fingerprints;
- K4 live detach proof;
- K6 cross-node `/proj` proof;
- actual controller off-POWDER artifact round-trip.

Mandatory cleanup did run and returned:

`COMPAT_CLEANUP=TERMINATE_REQUESTED`

This proves the terminate request was accepted by the client, but the next agent should still verify the failed compatibility experiment no longer resolves before authorizing another live reservation.

## 1. Mission boundary

K-fastlane is **inside WP2**. It is not a separate automation project.

The user wants shortest path / highest ROI and explicitly does not want infrastructure drift.

Scientific state remains frozen:

- WP2: **ACTIVE — Golden rehearsal not yet passed**.
- Scientific weighted completion: **20%**.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.

No K result changes scientific completion by itself.

## 2. Frozen H1 state — do not reopen

Experiment of record:

- Experiment: `WP-HCAL-E`
- UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`
- Profile: `PowderProfiles/srslte-controlled-rf`
- Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- Mapping: `enb1 -> nuc1`, `rue1 -> nuc2`
- Deployed WellPulse commit: `95ba9a57bef159450b00b8a439d393d22e1c0519`
- Run: `wp2h1-a1-20260826-001`
- Scored: **NO**
- Frozen classification: `VALID_W1_RECOVERY_FAILURE`

H1 must never be replaced, retroactively repaired, or reclassified.

Known raw archive hash anchors:

- nuc1: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

Raw bundles were not recovered. GitHub salvage is derived/provenance only. Home-PC PowerShell salvage is `CLOSED_NO_RECOVERY`. Do not reopen salvage without a genuinely new evidence source.

## 3. K1 — PASS / closed

`K1=PASS`

Frozen supply-chain/runtime facts:

- Portal API repo: `https://gitlab.flux.utah.edu/emulab/portal-api.git`
- Portal revision: `01be03b2f60c067815a7654437320dd981ca3617`
- Portal source capture SHA-256: `3e9f0073b2df6840801baa38333f1f04debd02a2eaa57997939b6f7ee678d4c8`
- Portal capture size: `1003520` bytes
- Portal bootstrap: `scripts/wp2_portal_client_bootstrap.sh`
- uv: `0.12.1`, SHA-256 `90b2f223fb69d19db49e117da601f64978593417988530aa733d456141b4bcbb`
- rclone: `1.75.0`, SHA-256 `aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa`
- runner major image: `ubuntu-24.04`

Current immutable Node24-native controller actions:

- `actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09`
- `actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f`
- `actions/download-artifact@37930b1c2abaa49bbe596cd826c3c89aef350131`

Do not revert to moving tags.

## 4. Workstation-independent architecture

Normal operation must not depend on the home PC or work PC.

Current control/evidence design:

`home/work PC -> GitHub -> GitHub Actions controller -> POWDER -> /proj/WellPulse -> controller pull -> GitHub Actions artifact round-trip verification`

Home/work PCs are interchangeable operator terminals only.

### Evidence authority simplification

Google Drive/rclone was removed from the teardown-critical path during K-fastlane to shorten and harden WP2:

- `/proj/WellPulse` = mandatory node-side persistent safety boundary.
- GitHub Actions controller = mandatory verified off-POWDER copy and teardown authority.
- GitHub Actions artifact round-trip = mandatory off-POWDER read-back mechanism.
- Drive may later be an optional secondary mirror, not a prerequisite for teardown.

## 5. K2 — partial PASS / live closure open

Offline controller artifact transport is proven.

Successful hardened QA run:

- Run: `33082470592`
- Result: `success`
- deterministic synthetic escrow tar SHA-256: `1a5c78b3ff588cef38338d12b7891793aca8f436f312c501b5712bb74d423605`
- artifact ID: `9650653376`
- artifact ZIP digest: `b213b5a5170528c72f0cfa27780756796262c91234235bb2155a1f706e6b6a6b`
- internal hashes passed after download.

Relevant scripts:

- `scripts/wp2_controller_pull_persistent_escrow.sh`
- `scripts/wp2_controller_verify_artifact_roundtrip.sh`

Golden node phase no longer authorizes teardown by itself. After `/proj` escrow it must keep:

- `CONTROLLER_OFFPOWDER_GATE=PENDING`
- `TEARDOWN_AUTHORIZED=NO`

Only verified controller round-trip may emit:

- `CONTROLLER_OFFPOWDER_GATE=PASS`
- `EVIDENCE_ESCROW_GATE=PASS`
- `TEARDOWN_AUTHORIZED=YES`

Final live K2 closure is still open because the first compatibility reservation failed before `/proj` and controller round-trip steps.

## 6. K3 — static contract PASS / live readiness BLOCKED

Frozen client basic CLI surface was captured successfully in run `33082535948`, including experiment create/get/extend/modify/terminate and experiment-related groups.

The client defaults to SSL verification and raises on unexpected HTTP status.

A later expanded QA run `33082657617` failed because the QA harness assumed a nested `manifests get --help` structure. This was a QA-introspection assumption, not a Portal-client failure.

Current corrected workflow:

`.github/workflows/wp2-k3-portal-cli-contract-qa.yml`

At handover, the corrected version existed but had not yet been re-triggered.

Fail-closed real-record validator:

`scripts/wp2_portal_record_guard.py`

It requires exact ready status, expected experiment-ID binding, and exactly one timezone-aware expiry field; missing/ambiguous expiry blocks.

The first live K-fastlane run did not reach this validator because the actual reservation status moved from `provisioning` to `failed`.

Therefore:

`K3_LIVE_PORTAL_BINDING=BLOCKED_ON_RESERVATION_PROVISIONING_FAILURE`

Do not weaken the ready-state requirement.

## 7. K4 — implementation PASS / live proof not reached

Golden orchestrator contains bounded detached SSH launch:

- `ssh -n`;
- remote `nohup ... </dev/null`;
- default 15 s launch timeout;
- elapsed launch time recorded;
- remote PID/ready evidence checked.

Static implementation checks passed.

The live K4 smoke step was skipped because the compatibility reservation failed before READY.

`K4_LIVE_DETACH_GATE=NOT_RUN`

## 8. K5 — implementation PASS / live expiry binding not reached

Fail-closed guard:

`scripts/wp2_prelaunch_time_guard.py`

Offline boundary tests passed:

- 2700 s remaining => PASS;
- 2699 s => BLOCKED;
- malformed/unknown expiry => BLOCKED.

The live run failed before a READY record and authoritative expiry could be extracted.

`K5_LIVE_TIME_BINDING=NOT_RUN`

## 9. K6 — implementation ready / live proof not reached

Persistent escrow implementation:

`scripts/wp2_golden_evidence_escrow.sh`

Required live chain remains:

1. `/proj/WellPulse` writable;
2. cross-node visibility;
3. source manifest verifies;
4. controller pulls exact bundle;
5. GitHub artifact upload;
6. independent download;
7. outer SHA and internal raw hashes verify;
8. only controller may authorize teardown.

The first compatibility reservation failed before these steps.

`K6_CROSS_NODE_PROJ_GATE=NOT_RUN`

## 10. K7 — static-QA defect open

Policy is frozen:

- `tmcc attenuator` must never be used as a read-only observation/status mechanism.
- no independent unqualified RF probe during protected science.
- authoritative protocol-prescribed RF mutation is distinct and remains allowed.

However, the K7 assertion in `.github/workflows/wp2-preintegration-static.yml` is not trustworthy yet. It currently relies on a `! grep ...` construct while the checker itself contains the target phrase. In run `33083214108`, the matching checker line was printed yet the workflow still completed successfully because `!`/`set -e` behavior does not give the intended fail-close guarantee.

Therefore:

`K7_STATIC_ASSERTION=NEEDS_FIX`

Shortest fix: scan only intended execution workflows or exclude the checker itself, capture match count explicitly, and fail with an explicit conditional if the count is non-zero.

Do not expand K7 into new RF-probing research.

## 11. K8 — BLOCKED

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

Do not mark K8 PASS until evidence exists for:

- successful live reservation READY state and real Portal status/expiry binding;
- real expiry -> time guard PASS;
- manifest hardware/image/login identity;
- controller SSH/runtime/profile fingerprints;
- K4 live detach timing;
- K6 cross-node `/proj` persistence;
- actual off-POWDER controller artifact round-trip;
- confirmed compatibility experiment cleanup;
- corrected K7 static assertion PASS.

Even after K8, Golden remains blocked until:

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

## 12. First live K-fastlane run — final record

Workflow: `.github/workflows/wp2-kfastlane-live-compat.yml`  
Run: `33084240768`  
Trigger commit: `dd275a3f7dbc75a7096b587ae3f01d61ff801411`  
Experiment UUID: `02bc305d-5d84-48f9-b518-dbebd1728ee6`

Final step record:

- setup: PASS
- checkout: PASS
- bounded authorization: PASS
- frozen Portal client + SSH identity: PASS
- exactly one reservation create: PASS
- Portal poll 1: `provisioning`
- Portal poll 2: `failed`
- READY/expiry binding: FAIL, rc 21
- manifest identity: SKIPPED
- runtime/SSH fingerprint: SKIPPED
- K4 live detach: SKIPPED
- K6 `/proj`: SKIPPED
- artifact upload/download/verify: SKIPPED
- mandatory cleanup: PASS as `COMPAT_CLEANUP=TERMINATE_REQUESTED`

No Golden workload, H calibration, or scored science ran.

## 13. Exact resume procedure

1. Read `HANDOVER_CURRENT.md` and this file first.
2. Verify experiment `02bc305d-5d84-48f9-b518-dbebd1728ee6` is absent/terminated before any new reservation.
3. Inspect why POWDER provisioning returned `failed`; use the smallest authoritative failure evidence available. Do **not** launch another reservation until the provisioning cause is understood or clearly classified transient and bounded.
4. Re-run the corrected K3 offline CLI QA once; do not broaden it.
5. Fix the K7 static checker and rerun static acceptance once.
6. Only then decide whether one replacement compatibility-only reservation is justified. If so, it must remain one bounded non-scored reservation and must not run Golden/H/scored work.
7. On a successful READY reservation, finish K3/K5 -> manifest/runtime -> K4 -> K6 -> controller artifact round-trip -> cleanup.
8. Reconcile the compatibility matrix and set K8 only from evidence.
9. Return immediately to `LIVE_HCI_AND_RAW_EVIDENCE_GATE`; do not linger in infrastructure work.
10. Golden remains unauthorized until both major gates pass.

## 14. Frozen prohibitions

Until both major gates pass:

- `REBOOK_GOLDEN=false`
- `scored_runs_authorized=false`
- no H requalification;
- no B1/W1/B2 scored campaign;
- no reuse of expired `WP-GOLDEN-A3`;
- no unqualified independent scientific-window probes;
- `HCI_CONTROL_ACTIONS_ENABLED=false`.

## 15. Future scientific teardown requirement

Required chain:

`freeze writers -> mandatory raw inventory -> SHA-256 -> /proj/WellPulse persistent escrow -> verify -> controller pull -> off-POWDER artifact -> independent download/read-back -> outer + internal hash verification -> provenance -> teardown`

Required markers:

- `RAW_EVIDENCE_COMPLETE=PASS`
- `EVIDENCE_ESCROW_GATE=PASS`
- `TEARDOWN_AUTHORIZED=YES`

## 16. Mandatory read order

1. `HANDOVER_CURRENT.md`
2. `docs/AGENT_HANDOVER_WP2_KFASTLANE_2026-08-27.md`
3. `.github/workflows/wp2-kfastlane-live-compat.yml`
4. `.github/workflows/wp2-preintegration-static.yml`
5. `.github/workflows/wp2-k3-portal-cli-contract-qa.yml`
6. `scripts/wp2_portal_record_guard.py`
7. `scripts/wp2_prelaunch_time_guard.py`
8. `scripts/wp2_controller_pull_persistent_escrow.sh`
9. `scripts/wp2_controller_verify_artifact_roundtrip.sh`
10. `scripts/wp2_golden_orchestrator.sh`
11. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
12. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
13. `docs/GITHUB_POWDER_COMPATIBILITY_MATRIX_2026-08-27.md`
14. `docs/NEXT_GATE.md`
15. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
16. `experiments/WP-PWD01/protocol.md`
17. `experiments/WP-PWD01/evidence-schema.md`

## 17. Mission after K-fastlane

Shortest scientific path:

`understand provisioning failure -> finish remaining live K evidence -> fix K7 -> K8 decision -> HCI/raw-evidence gate -> one clean non-scored Golden -> freeze H -> close WP2 -> WP3 scored campaign -> WP4 OTA replication -> WP5 analysis/manuscript`
