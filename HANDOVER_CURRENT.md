# WellPulse — Current Handover

Last updated: 2026-08-27 after **WP2-P6 short QA PASS and explicit one-shot Golden authorization**.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- Last accepted checkpoint: **WP2-P5 PASS / P6 SHORT QA PASS / P6 ACTIVE**.
- Scientific weighted completion: **20%**.
- WP2 management/readiness before P6 result: **80/100**; no partial scientific credit.
- WP0: **PASS**, 8/8.
- WP1: **PASS / FROZEN**, 12/12.
- WP2: **ACTIVE** — P1-P5 closed; P6 authorized/active; P7 remains blocked.
- WP3: **BLOCKED ON WP2**, 0/30.
- WP4: **BLOCKED**, 0/15.
- WP5: **PREPARED / NOT EXECUTED**, 0/20.
- FIT IoT-LAB layer: **FINAL PASS**.
- POWDER G0-G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- K1-K8 compatibility: **PASS / CLOSED**.
- `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`.
- `AUDIT_R1=PASS`.
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`.
- `P6_SHORT_QA=PASS`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.
- `REBOOK_GOLDEN=true` **for exactly one non-scored WP2-P6 reservation/run only**.
- `scored_runs_authorized=false`.

## Current bounded work package

`WP2-P6 — ONE CLEAN NON-SCORED GOLDEN REHEARSAL`

The user's explicit continuation on 2026-08-27 authorizes P6 after a short QA cycle. P6 is the only live work authorized by this handover.

Canonical P6 QA:

`docs/WP2_P6_SHORT_QA_2026-08-27.md`

Live workflow:

`.github/workflows/wp2-p6-golden.yml`

Execution controller:

`powder/wp2_p6_golden_execute.sh`

Current live/status evidence path:

`evidence/powder/wp2-p6-live-status.md`

## P6 execution contract

1. Premutation offline QA must PASS in the same workflow.
2. Immediately before booking, perform advisory `https://www.powderwireless.net/resinfo.php` check and record `PASS|DEFER|UNKNOWN`. If the page is ambiguous/unparseable, record `UNKNOWN` and rely on authoritative Portal gates; never infer availability or change the frozen design.
3. Create exactly one reservation using:
   - project `WellPulse`;
   - profile `PowderProfiles/srslte-controlled-rf`;
   - exact profile repository revision target `a6da96560b6526dc6816761282722c996418fd8c`;
   - bindings `enb_node=nuc1`, `ue_node=nuc2`, `ue_type=srsue`;
   - expected hardware `nuc5300`;
   - expected image `urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1`.
4. Require authoritative Portal READY/identity/expiry/time gate, exact manifest identity, SSH reachability, profile revision and writable `/proj/WellPulse` before science.
5. Establish clean Q0 5/5 user-plane baseline before protected science.
6. Execute exactly one non-scored Golden G0-G10 using the frozen orchestrator and passive HCI only.
7. Frozen science remains:
   - Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
   - attenuation IDs `1 33 2 34` coupled;
   - `t_rf_restore`, `t_service_ready`, `t_app_complete` distinct;
   - primary cohort cutoff `t_rf_restore`;
   - `H_app=300 s from t_service_ready`;
   - primary endpoint `completeness_300`;
   - `T_service`, `T_app`, `T_total` preserved;
   - no outcome-derived H changes.
8. Protected G3-G7 science has no background `/proj` checkpoint. After G8 reconstruction, G9 freezes/hashes/copies to `/proj/WellPulse`.
9. Node/persistent phase must end with `RAW_EVIDENCE_COMPLETE=PASS`, `PERSISTENT_ESCROW_GATE=PASS`, controller handoff required, and `TEARDOWN_AUTHORIZED=NO`.
10. Controller pulls the verified persistent evidence, builds deterministic TAR and SHA-256, uploads via pinned GitHub artifact action, independently downloads/read-backs, and verifies outer + internal SHA-256.
11. Only controller finalization may emit `CONTROLLER_OFFPOWDER_GATE=PASS`, `EVIDENCE_ESCROW_GATE=PASS`, `TEARDOWN_AUTHORIZED=YES`.
12. Only after that may Portal teardown be requested and confirmed.
13. STOP after P6. WP2-P7 formal scientific closure/scored authorization is a separate decision.

## Fail-closed rules

- Failure before protected science begins: bounded reservation cleanup is allowed.
- Failure after protected science begins without verified final evidence closure: automatic teardown is prohibited; preserve the experiment live for evidence recovery.
- HCI failure alone is non-authoritative/non-fatal.
- Negative/null/unfavorable application outcome remains valid scientific evidence and never justifies rerun/protocol drift.
- P6 does not authorize B1/W1/B2 scored work.

## Frozen prior evidence

### H1

- experiment `WP-HCAL-E`;
- UUID `9153e16a-1eb1-45f5-88bf-303636a9d1ec`;
- run `wp2h1-a1-20260826-001`;
- profile revision `a6da96560b6526dc6816761282722c996418fd8c`;
- mapping `enb1 -> nuc1`, `rue1 -> nuc2`;
- deployed WellPulse commit `95ba9a57bef159450b00b8a439d393d22e1c0519`;
- classification `VALID_W1_RECOVERY_FAILURE`;
- scored: NO;
- original node-local raw bundles were not recovered after teardown.

Do not reopen H1 salvage or use H1 to select/re-estimate H.

### K1-K8

K1-K8 remain PASS/CLOSED. Decisive compatibility evidence:

- Actions run `33085406598`;
- experiment `fc7c2187-2376-4a92-8de1-4665a06ea943`;
- classification `INFRASTRUCTURE_ONLY_NON_SCORED`.

Do not reopen K1-K8 absent a material interface change.

## Workflow governance during P6

The active workflow surface is temporarily **7 workflows**: the six P5-era offline/static workflows plus one bounded live workflow `wp2-p6-golden.yml`. Its only authorized trigger is `.wp2-p6-golden-trigger`, and that trigger is single-use for this P6 run. Historical K/A3 workflows remain retired.

After P6 reaches a terminal verdict, remove live P6 authority during canonical closure.

## Mandatory read order

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P6_SHORT_QA_2026-08-27.md`
3. `docs/WP2_P5_HCI_RAW_EVIDENCE_CLOSURE_2026-08-27.md`
4. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
5. `docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`
6. `docs/AUDIT_R1_SUPERSESSION_MAP_2026-08-27.md`
7. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
8. `experiments/WP-PWD01/protocol.md`
9. `docs/NEXT_GATE.md`
10. `docs/MILESTONE_STATUS.md`
11. `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`
12. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
13. `experiments/WP-PWD01/evidence_inventory_golden_v1.txt`
14. `scripts/wp2_golden_hci_emit.py`
15. `scripts/wp2_golden_orchestrator.sh`
16. `scripts/wp2_golden_evidence_escrow.sh`
17. `scripts/wp2_controller_pull_persistent_escrow.sh`
18. `scripts/wp2_controller_verify_artifact_roundtrip.sh`
19. `powder/wp2_p6_golden_execute.sh`
20. `.github/workflows/wp2-p6-golden.yml`
21. `docs/WORKFLOW_REGISTRY.md`
22. `AGENTS.md`

**CURRENT ACTION: execute the single-use P6 trigger, then follow the fail-closed terminal verdict.**
