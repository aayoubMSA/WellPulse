# Agent Handover — WellPulse WP2 K-Fastlane

**Date:** 2026-08-27  
**Canonical repo:** `aayoubMSA/WellPulse`  
**Branch:** `main`  
**Purpose:** exact continuation point after user requested handover while the single bounded K-fastlane live compatibility run is already in progress.

## 0. Absolute operating rule

Do **not** create another POWDER reservation when resuming this handover.

First inspect the already-running GitHub Actions workflow:

- Workflow: `WP2 K-Fastlane Live Compatibility Gate`
- Run ID: `33084240768`
- Trigger commit: `dd275a3f7dbc75a7096b587ae3f01d61ff801411`
- Trigger classification: `INFRASTRUCTURE_ONLY_NON_SCORED`
- Reservation count authorized: `1`
- Duration: `1 hour`
- Golden workload: `false`
- H calibration: `false`
- Scored run: `false`

At handover capture time, the job was **IN PROGRESS**. Completed steps were setup, checkout, bounded authorization, frozen Portal-client install/SSH identity, and creation of exactly one one-hour compatibility reservation. The active step was:

`Wait READY and bind exact Portal status/expiry`

All later live checks were still pending.

If the run has completed by the time the next agent resumes, inspect the final job result/logs/artifacts before taking any action. If the run is still active, observe the GitHub Actions state only; do not start a duplicate run or manually alter the experiment unless the cleanup path itself has failed and a bounded recovery is explicitly required.

## 1. Mission boundary

This K-fastlane is **inside WP2**. It is not a separate automation project.

The user explicitly wants the shortest path / highest ROI while avoiding mission drift.

Scientific state remains:

- WP2: **ACTIVE — Golden rehearsal not yet passed**.
- Scientific weighted completion: **20%**.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.

No K result by itself changes scientific completion.

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

H1 must never be replaced, repaired retroactively, or reclassified.

Known H1 raw archive hash anchors:

- nuc1: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

Raw bundles were not recovered. GitHub salvage is closed as derived/provenance only. Home-PC PowerShell salvage is `CLOSED_NO_RECOVERY`. Do not expand into forensic recovery unless a genuinely new evidence source appears.

## 3. K1 — PASS / closed

`K1=PASS`

Frozen supply-chain/runtime facts:

- Portal API authoritative repo: `https://gitlab.flux.utah.edu/emulab/portal-api.git`
- Portal API revision: `01be03b2f60c067815a7654437320dd981ca3617`
- Portal source capture SHA-256: `3e9f0073b2df6840801baa38333f1f04debd02a2eaa57997939b6f7ee678d4c8`
- Portal source capture size: `1003520` bytes
- Portal bootstrap: `scripts/wp2_portal_client_bootstrap.sh`
- uv: `0.12.1`, SHA-256 `90b2f223fb69d19db49e117da601f64978593417988530aa733d456141b4bcbb`
- rclone: `1.75.0`, SHA-256 `aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa`
- GitHub runner major image: `ubuntu-24.04`

Controller actions were subsequently hardened to current Node24-native immutable SHAs:

- `actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09`
- `actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f`
- `actions/download-artifact@37930b1c2abaa49bbe596cd826c3c89aef350131`

Do not revert to moving tags.

## 4. K-fastlane rationale and architecture

User authorized grouping the remaining K work into one shortest-path/highest-ROI fastlane.

Architecture was simplified so normal operation is workstation-independent:

`home/work PC -> GitHub -> GitHub Actions controller -> POWDER -> /proj/WellPulse -> controller pull -> GitHub Actions artifact round-trip verification`

Home/work PCs are operator terminals only. No experiment-critical authority may live only on a workstation.

### Evidence authority change

The earlier design made Google Drive/rclone part of the teardown-critical evidence chain. During K-fastlane this was simplified:

- `/proj/WellPulse` = node-side persistent safety boundary before teardown.
- GitHub Actions controller = mandatory verified off-POWDER copy and teardown authority.
- GitHub Actions artifact round-trip = current mandatory off-POWDER verification mechanism.
- Google Drive may be added later as an optional secondary mirror, but is **not** required for teardown authority in the current fastlane architecture.

This removes dedicated Drive OAuth from the WP2 critical path.

## 5. K2 — current status

### Offline proof already PASS

Workflow: `WP2 Off-POWDER Artifact Transport QA`

Successful hardened run:

- Run ID: `33082470592`
- Result: `success`
- Runner image observed: Ubuntu 24.04.4, image `20260823.283.1`
- Synthetic deterministic escrow tar SHA-256: `1a5c78b3ff588cef38338d12b7891793aca8f436f312c501b5712bb74d423605`
- GitHub artifact ID: `9650653376`
- Artifact ZIP digest: `b213b5a5170528c72f0cfa27780756796262c91234235bb2155a1f706e6b6a6b`
- Internal raw hashes verified after download.

Relevant controller scripts:

- `scripts/wp2_controller_pull_persistent_escrow.sh`
- `scripts/wp2_controller_verify_artifact_roundtrip.sh`

Golden node orchestrator was changed so the node phase cannot authorize teardown by itself. After `/proj` escrow it must emit/retain controller handoff state and keep:

- `CONTROLLER_OFFPOWDER_GATE=PENDING`
- `TEARDOWN_AUTHORIZED=NO`

Only verified controller round-trip may emit:

- `CONTROLLER_OFFPOWDER_GATE=PASS`
- `EVIDENCE_ESCROW_GATE=PASS`
- `TEARDOWN_AUTHORIZED=YES`

### K2 final live closure

K2 is not fully closed until the current live compatibility run proves the same chain using an actual `/proj/WellPulse` compatibility bundle and controller artifact round-trip.

## 6. K3 — current status

Frozen client basic CLI surface was successfully captured offline in run `33082535948`:

- `experiment create`
- `experiment get`
- `experiment extend`
- `experiment modify`
- `experiment terminate`
- `experiment manifests`
- `experiment nodes`
- related experiment groups

The frozen client defaults to SSL verification and raising on unexpected HTTP status.

A later expanded QA run `33082657617` failed because the QA harness assumed a nested `portal-cli experiment manifests get --help` shape. This is a **QA introspection assumption failure**, not evidence that the pinned Portal client itself failed.

The current corrected K3 workflow is:

`.github/workflows/wp2-k3-portal-cli-contract-qa.yml`

It now captures only stable top-level experiment lifecycle help (`experiment`, `create`, `get`, `terminate`). The correction existed at handover but had not yet been re-triggered after the edit.

Fail-closed live record validator:

`scripts/wp2_portal_record_guard.py`

It requires:

- exact ready status;
- expected experiment ID bound in the record;
- exactly one recognized timezone-aware expiry field;
- unknown/ambiguous expiry => BLOCKED.

The current live compatibility run is the authoritative test of real Portal status/expiry binding.

## 7. K4 — current status

Implementation is present in the Golden orchestrator:

- detached SSH launch uses `ssh -n`;
- remote process uses `nohup ... </dev/null`;
- launch is bounded by `RECEIVER_LAUNCH_TIMEOUT_S` (default 15 s);
- elapsed launch time is recorded;
- receiver process/ready evidence is checked.

Static implementation checks passed.

Final K4 closure requires the current live compatibility run step:

`K4 prove bounded detached SSH process return`

This live test is intentionally a harmless compatibility process, not the Golden receiver workload.

## 8. K5 — current status

Fail-closed time-budget guard:

`scripts/wp2_prelaunch_time_guard.py`

Offline tests passed:

- exactly 2700 s remaining => PASS;
- 2699 s => BLOCKED;
- malformed/unknown expiry => BLOCKED.

Final K5 closure requires real Portal expiry from the current live reservation to be accepted by `wp2_portal_record_guard.py` and then fed to the time guard with at least 2700 s remaining.

## 9. K6 — current status

Persistent escrow implementation already exists:

`scripts/wp2_golden_evidence_escrow.sh`

The current live compatibility workflow is designed to prove:

1. `/proj/WellPulse` exists and is writable on both relevant nodes;
2. a probe written from one node is visible and hash-verifiable from the other;
3. `/proj` escrow manifest passes;
4. controller pulls the exact bundle;
5. controller uploads it as a GitHub Actions artifact;
6. artifact is downloaded to an independent controller path;
7. outer bundle SHA and internal raw hashes match;
8. only then may the controller print `TEARDOWN_AUTHORIZED=YES`.

This is the critical anti-H1-loss chain.

## 10. K7 — IMPORTANT static-QA defect still open

Policy intent is correct:

- `tmcc attenuator` must never be used as a read-only status/observation mechanism.
- During protected science, no unqualified independent RF probe is allowed.
- Experimental RF mutation by the authoritative science runner is distinct from observation and remains allowed where prescribed by the frozen protocol.

However, the current `.github/workflows/wp2-preintegration-static.yml` K7 assertion is **not scientifically trustworthy yet**.

Current code uses a construct of the form:

`! grep -R -E 'tmcc[[:space:]]+attenuator' .github/workflows ...`

The checker file itself contains the phrase in its own comment/check, and Bash `set -e` behavior around `!` makes this a false-confidence risk. In the successful static run `33083214108`, the log visibly printed a matching line from the checker itself yet the job still completed successfully.

Therefore:

`K7_STATIC_ASSERTION=NEEDS_FIX`

Do not cite run `33083214108` alone as proof that active workflows are free from RF observation calls.

Shortest correction on resume: make K7 scanning exclude the checker itself or inspect only the intended active execution workflows, and assert the result explicitly with a captured match count / test condition rather than relying on `! grep` under `set -e`.

No need to broaden into new RF probing research. The preferred scientific policy remains: **do not independently query RF state during the protected window**.

## 11. K8 — current status

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

Do not mark K8 PASS until all of the following have evidence:

- current live K3 Portal record/status/expiry binding PASS;
- current live K5 expiry-to-time-budget binding PASS;
- hardware/image/login identity from actual manifest PASS;
- controller SSH topology/runtime/profile fingerprints PASS;
- live K4 detach timing PASS;
- live K6 cross-node `/proj` persistence PASS;
- actual controller off-POWDER artifact round-trip PASS;
- mandatory compatibility reservation cleanup confirmed;
- K7 static assertion defect fixed and rerun successfully.

The separate gate remains mandatory before any new Golden:

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

Thus even a complete K1-K8 PASS does not by itself authorize Golden unless the HCI/raw-evidence gate is also closed.

## 12. Current live run — exact retrieval point

Workflow:

`.github/workflows/wp2-kfastlane-live-compat.yml`

Run ID:

`33084240768`

Trigger:

`.wp2-kfastlane-live-compat-trigger`

Trigger commit:

`dd275a3f7dbc75a7096b587ae3f01d61ff801411`

At handover capture time:

- Set up job: PASS
- Checkout audited controller state: PASS
- Validate bounded compatibility authorization: PASS
- Install frozen Portal client and prepare SSH identity: PASS
- Create exactly one one-hour compatibility reservation: PASS
- Wait READY and bind exact Portal status/expiry: **IN PROGRESS**
- Manifest identity: PENDING
- Runtime/SSH fingerprints: PENDING
- K4 live detach proof: PENDING
- K6 `/proj` proof/controller bundle: PENDING
- Off-POWDER upload/download/round-trip: PENDING
- Mandatory cleanup: PENDING

The run is compatibility-only and MUST NOT execute Golden workload, H calibration, or scored science.

## 13. Exact resume procedure

When resuming:

1. Read this file and `HANDOVER_CURRENT.md` first.
2. Inspect GitHub Actions run `33084240768`.
3. **Do not create another reservation.**
4. If run completed, retrieve job logs and any artifact metadata. Classify each K gate separately; do not convert workflow success into scientific PASS automatically.
5. Confirm mandatory cleanup/termination of the compatibility reservation even if earlier steps failed.
6. Fix the K7 static assertion defect only; rerun static acceptance once.
7. Reconcile `docs/GITHUB_POWDER_COMPATIBILITY_MATRIX_2026-08-27.md` and `HANDOVER_CURRENT.md`.
8. If and only if all K1-K8 material compatibility items pass, set `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`.
9. Then return to the remaining WP2 prerequisite: `LIVE_HCI_AND_RAW_EVIDENCE_GATE`.
10. Do not create a Golden reservation until **both** major gates pass.

## 14. Frozen prohibitions

Until both major gates pass:

- `REBOOK_GOLDEN=false`
- `scored_runs_authorized=false`
- no H requalification;
- no B1/W1/B2 scored campaign;
- no reuse of expired `WP-GOLDEN-A3`;
- no independent unqualified live probes during the scientific window;
- `HCI_CONTROL_ACTIONS_ENABLED=false`.

## 15. Required evidence before teardown of future science

For every future scientific experiment:

`freeze writers -> mandatory raw inventory -> SHA-256 -> /proj/WellPulse persistent escrow -> verify -> controller pull -> off-POWDER artifact -> independent download/read-back -> outer + internal hash verification -> provenance -> teardown`

Required final markers:

- `RAW_EVIDENCE_COMPLETE=PASS`
- `EVIDENCE_ESCROW_GATE=PASS`
- `TEARDOWN_AUTHORIZED=YES`

## 16. Mandatory read order for next agent

1. `HANDOVER_CURRENT.md`
2. `docs/AGENT_HANDOVER_WP2_KFASTLANE_2026-08-27.md`
3. `.github/workflows/wp2-kfastlane-live-compat.yml`
4. `scripts/wp2_portal_record_guard.py`
5. `scripts/wp2_prelaunch_time_guard.py`
6. `scripts/wp2_controller_pull_persistent_escrow.sh`
7. `scripts/wp2_controller_verify_artifact_roundtrip.sh`
8. `scripts/wp2_golden_orchestrator.sh`
9. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
10. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
11. `docs/GITHUB_POWDER_COMPATIBILITY_MATRIX_2026-08-27.md`
12. `docs/NEXT_GATE.md`
13. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
14. `experiments/WP-PWD01/protocol.md`
15. `experiments/WP-PWD01/evidence-schema.md`
16. H1 evidence records only if historical provenance is needed; do not reopen salvage.

## 17. Mission after K-fastlane

Do not stay in infrastructure work longer than necessary.

Shortest scientific path remains:

`finish K live compatibility evidence -> fix K7 checker -> K8 decision -> close HCI/raw-evidence gate -> one clean non-scored Golden -> freeze H -> close WP2 -> WP3 scored campaign -> WP4 OTA replication -> WP5 analysis/manuscript`
