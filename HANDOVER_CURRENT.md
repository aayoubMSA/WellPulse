# WellPulse — Current Handover

Last updated: 2026-08-27 after read-only post-cleanup diagnosis of the first bounded WP2 K-fastlane compatibility provisioning failure.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5 infrastructure/RF qualification: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Recovery-semantics RS-2..RS-7: **PASS / FROZEN**.
- WP2: **ACTIVE — GOLDEN REHEARSAL NOT YET PASSED**.
- Scientific weighted completion: **20%**.
- Repository workflow cleanup: **CLOSED / 100% — C0..C4 PASS**.
- H1 GitHub salvage: **PASS as derived-evidence/provenance consolidation; raw recovery failed**.
- H1 PowerShell/local salvage: **CLOSED_NO_RECOVERY**.
- K1 supply-chain/runtime pin closure: **PASS**.
- K2 controller/off-POWDER transport: **OFFLINE PASS / LIVE CLOSURE OPEN**.
- K3 Portal contract: **STATIC PASS / LIVE BLOCKED ON UNRESOLVED RESERVATION PROVISIONING FAILURE**.
- Failed compatibility experiment cleanup: **VERIFIED PASS — experiment absent from `get` and `list`**.
- Provisioning root cause: **NOT RECOVERED from post-cleanup Portal state**.
- K4 receiver detach: **IMPLEMENTED / LIVE PROOF NOT RUN**.
- K5 time budget: **IMPLEMENTED / LIVE EXPIRY BINDING NOT RUN**.
- K6 `/proj/WellPulse` persistence + controller round-trip: **IMPLEMENTED / LIVE PROOF NOT RUN**.
- K7 observation policy: **POLICY FROZEN / STATIC ASSERTION NEEDS FIX**.
- K8 pre-integration compatibility gate: **BLOCKED**.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.

## Mission rule

K-fastlane is part of WP2 only. The user explicitly wants shortest path / highest ROI and does not want infrastructure work to drift away from the scientific WPs.

Do not continue K work beyond what is necessary to close the compatibility blocker. After K8, return immediately to the HCI/raw-evidence gate and then the clean non-scored Golden.

## Workstation independence

Home and work PCs are interchangeable operator terminals only.

No future Golden/scored execution may depend on workstation-local history, downloads, tokens, or unique filesystem state. Canonical authority is GitHub + frozen repository state + GitHub Actions/secrets + verified evidence stores.

## H1 experiment of record — frozen

- Experiment: `WP-HCAL-E`
- UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`
- Profile: `PowderProfiles/srslte-controlled-rf`
- Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- Mapping: `enb1 -> nuc1`, `rue1 -> nuc2`
- Exact deployed WellPulse source commit: `95ba9a57bef159450b00b8a439d393d22e1c0519`
- H1 run: `wp2h1-a1-20260826-001`
- Scored: **NO**
- Frozen classification: `VALID_W1_RECOVERY_FAILURE`

H1 must never be replaced, repaired retroactively, or reclassified.

Known H1 raw archive hash anchors:

- nuc1: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

Raw bundles were not recovered. GitHub salvage remains derived/provenance only. PowerShell/local salvage is `CLOSED_NO_RECOVERY`. Do not reopen salvage without a genuinely new evidence source.

## Frozen H1 scientific record

- Q0/Q1/Q2/Q3: `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled.
- Q3 full-state duration: `120.000117905 s`.
- RF restoration / primary-cohort cutoff: `2026-08-26T18:16:00.428045+00:00`.
- Generated records: `361`.
- Primary cohort records: `211`.
- Final pending: `270`.
- Application inflight: `20`.
- Publish calls: `111`.
- PUBACK callbacks: `91`.
- Q0 pre-readiness: `5/5` ping PASS through `tun_srsue`.
- Post-restoration health: `0/3` ping.
- Sender status: `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`.
- Sender rc: `20`.

These survive as derived/live-captured summaries, not record-level raw evidence.

## H1 failure localization / recovery

Preserved evidence localizes the dominant H1 non-recovery below the WellPulse application layer in LTE core/session-context/IP continuity behavior. This does not demonstrate a WellPulse durable-queue failure.

Recovery characterization remains:

- UE-only restart: **FAIL**.
- EPC/eNB reset with UE left running: reset PASS; Q0/user-plane recovery **FAIL**.
- Clean ordered recovery `stop UE -> EPC -> eNB -> fresh UE`: **PASS**.
- Post-recovery Q0: 10/10 packets, 0% loss.
- Full LTE/TLS/MQTT v3.1.1/QoS1 path: **3/3 fresh sessions PASS** with payload hash equality.

Operational recovery knowledge only; no retroactive H1 repair.

## K1 — PASS / closed

`K1=PASS`

Frozen controller/supply-chain facts:

- Portal API repo: `https://gitlab.flux.utah.edu/emulab/portal-api.git`
- Portal revision: `01be03b2f60c067815a7654437320dd981ca3617`
- Portal source capture SHA-256: `3e9f0073b2df6840801baa38333f1f04debd02a2eaa57997939b6f7ee678d4c8`
- uv `0.12.1`, SHA-256 `90b2f223fb69d19db49e117da601f64978593417988530aa733d456141b4bcbb`
- rclone `1.75.0`, SHA-256 `aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa`
- runner: `ubuntu-24.04`
- `actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09`
- `actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f`
- `actions/download-artifact@37930b1c2abaa49bbe596cd826c3c89aef350131`

Do not revert to moving tags.

## Evidence architecture after K-fastlane simplification

Critical path is now:

`POWDER raw -> /proj/WellPulse persistent escrow -> controller pull -> GitHub Actions artifact -> independent controller download/read-back -> outer + internal hash verification -> teardown authority`

Google Drive/rclone is no longer teardown-critical. Drive may later be an optional secondary mirror.

The Golden node phase must never authorize teardown by itself. It must leave:

- `CONTROLLER_OFFPOWDER_GATE=PENDING`
- `TEARDOWN_AUTHORIZED=NO`

Only verified controller round-trip may emit:

- `CONTROLLER_OFFPOWDER_GATE=PASS`
- `EVIDENCE_ESCROW_GATE=PASS`
- `TEARDOWN_AUTHORIZED=YES`

Relevant scripts:

- `scripts/wp2_controller_pull_persistent_escrow.sh`
- `scripts/wp2_controller_verify_artifact_roundtrip.sh`
- `scripts/wp2_golden_evidence_escrow.sh`
- `scripts/wp2_golden_orchestrator.sh`

## K2 — offline PASS / live closure open

Successful hardened controller artifact QA:

- workflow run `33082470592`: `success`
- source tar SHA-256 `1a5c78b3ff588cef38338d12b7891793aca8f436f312c501b5712bb74d423605`
- artifact ID `9650653376`
- artifact digest `b213b5a5170528c72f0cfa27780756796262c91234235bb2155a1f706e6b6a6b`
- internal hashes verified after download.

K2 final live closure remains open because the first actual compatibility reservation failed before `/proj` and controller artifact steps.

## K3 — static PASS / live blocked

Corrected offline CLI QA exists at:

`.github/workflows/wp2-k3-portal-cli-contract-qa.yml`

The frozen Portal client exposes the needed experiment lifecycle surface. An earlier expanded QA failure (`33082657617`) was caused by a bad nested help-tree assumption, not by the Portal pin.

Fail-closed real record guard:

`scripts/wp2_portal_record_guard.py`

### First live compatibility reservation

Workflow run: `33084240768`

Experiment UUID: `02bc305d-5d84-48f9-b518-dbebd1728ee6`

Observed sequence:

- reservation creation: PASS
- `PORTAL_POLL_1=provisioning`
- `PORTAL_POLL_2=failed`
- READY/expiry binding: NOT REACHED
- cleanup: `COMPAT_CLEANUP=TERMINATE_REQUESTED`

### Read-only post-cleanup diagnosis

Canonical artifact:

`evidence/powder/kfastlane-provision-failure-diagnosis-2026-08-27.md`

Diagnostic workflow:

`.github/workflows/wp2-kfastlane-provision-failure-diagnose.yml`

Diagnostic run: `33086065236` — **success**.

Authoritative observations from the frozen Portal client:

- `GET_RC=148`
- `ELABORATE_GET_RC=148`
- `LIST_RC=0`
- both `experiment get` calls return `No such experiment`;
- target is absent from `experiment list`.

Therefore:

- `COMPATIBILITY_CLEANUP_VERIFICATION=PASS`
- `FAILED_EXPERIMENT_RESOLUTION=ABSENT`
- `FAILED_EXPERIMENT_LIST_PRESENCE=NO`

However, the original failed-state JSON/error details were not frozen before cleanup. The post-cleanup Portal state cannot recover the detailed provisioning failure cause.

Therefore:

`PROVISION_FAILURE_ROOT_CAUSE=NOT_RECOVERED_FROM_POST_CLEANUP_PORTAL_STATE`

Do **not** infer hardware shortage, quota, site outage, profile failure, or any other cause without evidence.

Current K3 verdict:

`K3_LIVE_PORTAL_BINDING=BLOCKED_ON_UNRESOLVED_PROVISIONING_FAILURE`

## K4 — implementation PASS / live not run

The orchestrator has bounded detached SSH startup using `ssh -n`, remote `nohup ... </dev/null`, a 15 s default timeout, elapsed-time recording, and remote PID/readiness checks.

`K4_LIVE_DETACH_GATE=NOT_RUN`

## K5 — implementation PASS / live not run

`scripts/wp2_prelaunch_time_guard.py` passes offline boundary tests and blocks malformed/insufficient expiry.

The first compatibility experiment never reached READY, so authoritative expiry could not be fed into the time guard.

`K5_LIVE_TIME_BINDING=NOT_RUN`

## K6 — implementation ready / live not run

Required live chain remains cross-node `/proj/WellPulse` write/read/hash plus controller pull/artifact round-trip.

`K6_CROSS_NODE_PROJ_GATE=NOT_RUN`

## K7 — policy frozen / checker defect open

Frozen rule:

- `tmcc attenuator` is **not** a read-only observation command.
- no unqualified independent RF probe during protected science.
- protocol-prescribed RF mutation by the authoritative science process remains distinct and allowed.

Known QA defect: `.github/workflows/wp2-preintegration-static.yml` currently relies on a `! grep ...` K7 assertion while the checker itself contains the target phrase. Run `33083214108` printed a self-match yet still completed successfully. Therefore that run cannot be used as sufficient K7 proof.

`K7_STATIC_ASSERTION=NEEDS_FIX`

Shortest fix: exclude the checker or scan only execution workflows, capture match count explicitly, and fail with an explicit conditional.

## K8 / Golden state

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

Still required before K8 PASS:

- successful replacement compatibility reservation READY state;
- real Portal status/expiry binding;
- expiry -> time-budget PASS;
- manifest hardware/image/login identity;
- runtime/profile/SSH fingerprints;
- K4 live detach PASS;
- K6 cross-node `/proj` PASS;
- actual controller off-POWDER artifact round-trip PASS;
- cleanup verified;
- corrected K7 static assertion PASS.

Separate prerequisite remains:

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

No Golden reservation until **both** major gates pass.

## Frozen scientific state

- H1: `VALID_W1_RECOVERY_FAILURE`.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.
- Scientific weighted completion: **20%**.
- Primary cohort cutoff remains `t_rf_restore`.
- Application horizon remains 300 s from `t_service_ready`.
- No B1/W1/B2 scored run is authorized.

## Repository hygiene

C0..C4 remain PASS / closed. Do not reintroduce archived live workflows casually.

## Mandatory read order

1. `HANDOVER_CURRENT.md`
2. `evidence/powder/kfastlane-provision-failure-diagnosis-2026-08-27.md`
3. `docs/AGENT_HANDOVER_WP2_KFASTLANE_2026-08-27.md`
4. `.github/workflows/wp2-kfastlane-live-compat.yml`
5. `.github/workflows/wp2-kfastlane-provision-failure-diagnose.yml`
6. `.github/workflows/wp2-preintegration-static.yml`
7. `.github/workflows/wp2-k3-portal-cli-contract-qa.yml`
8. `scripts/wp2_portal_record_guard.py`
9. `scripts/wp2_prelaunch_time_guard.py`
10. `scripts/wp2_controller_pull_persistent_escrow.sh`
11. `scripts/wp2_controller_verify_artifact_roundtrip.sh`
12. `scripts/wp2_golden_orchestrator.sh`
13. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
14. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
15. `docs/GITHUB_POWDER_COMPATIBILITY_MATRIX_2026-08-27.md`
16. `docs/NEXT_GATE.md`
17. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
18. `experiments/WP-PWD01/protocol.md`
19. `experiments/WP-PWD01/evidence-schema.md`

## Exact next action

**STOP after provisioning-failure diagnosis. No replacement reservation is authorized in this patch.**

On explicit resume, execute one bounded **offline pre-retry hardening patch** only:

1. modify `.github/workflows/wp2-kfastlane-live-compat.yml` so any future `status=failed` freezes a sanitized failed-state Portal JSON/error artifact **before cleanup**;
2. rerun the corrected K3 offline CLI QA once;
3. fix the K7 static assertion and rerun static acceptance once;
4. update canonical compatibility status and STOP.

Only after that offline hardening PASS should one replacement compatibility-only reservation be considered to finish K3-K6 live proofs.

Shortest mission path:

`offline pre-retry hardening -> one replacement compatibility reservation -> remaining K3-K6 proofs -> K8 -> HCI/raw gate -> clean non-scored Golden -> freeze H -> WP2 close -> WP3 -> WP4 -> WP5`
