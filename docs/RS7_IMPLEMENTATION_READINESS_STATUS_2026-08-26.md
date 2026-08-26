# WellPulse WP2 — RS-7 Implementation & Reservation Readiness Status

Date: 2026-08-26
Owner: Pre-Reservation Consortium
Stage: PRE-RESERVATION / PRE-SCORE

## Executive verdict

**REPAIR_OFFLINE_FIRST — ONE MATERIAL BLOCKER REMAINS.**

The Golden E2E implementation package now exists and has passed offline static/functional QA. A new POWDER reservation is not yet authorized because the required second verified evidence copy must terminate on a real destination outside POWDER, and that destination has not yet been frozen and exercised.

## Work-package status

### WP7.1 — Existing implementation recovery — PASS — 15/100

Recovered and reconciled the actual H1 implementation and exact code blobs, including:

- `scripts/wp_pwd01_h_sender.py`
- `scripts/wp_pwd01_h_receiver.py`
- `scripts/finalize_wp_pwd01_h_calibration.py`
- `powder/wp2_h_epc_broker.sh`
- profile-authoritative `/local/repository/bin/start.sh` evidence

No implementation dependency remains conceptually unknown.

### WP7.2 — Golden orchestration package — PASS — 30/100

Implemented:

- `scripts/wp_pwd01_golden_sender.py`
- `scripts/wp2_golden_orchestrator.sh`
- `scripts/wp2_golden_service_restore.sh`
- `scripts/wp2_golden_service_ready_probe.sh`
- exact G0-G10 machine-readable state progression
- shell-visible progress bars
- fixed Q3=55 dB / 120 s outage and fixed `H_app=300 s`
- deterministic clean-order LTE restoration
- architecture-blind 120 s service-ready bound
- no application-state inspection before service-ready classification

The Golden sender intentionally differs from the obsolete H-calibration runner: it does not stop early on queue-zero and does not retain the old 150 s post-restoration stop rule. It observes exactly 300 s from `t_service_ready`.

### WP7.3 — Evidence, reconstruction, and fail-closed teardown — TECHNICAL PASS / DEPLOYMENT BLOCKED — 30/100 withheld until live destination exists

Implemented:

- `experiments/WP-PWD01/evidence_inventory_golden_v1.txt` v1.2
- `scripts/reconstruct_wp2_golden.py`
- `scripts/wp2_golden_evidence_escrow.sh`
- `scripts/wp2_golden_teardown_guard.sh`
- `scripts/wp2_golden_offline_qa.sh`
- `.github/workflows/wp2-golden-offline-qa.yml`

Offline QA exposed and corrected a real shell defect in the progress-bar implementation under `set -u`. After correction, GitHub Actions run `33013616916`, job `98326004030`, completed **SUCCESS**.

The successful QA proved:

1. bash syntax for the Golden orchestration/restore/readiness/escrow/guard scripts;
2. Python compilation for Golden sender and reconstruction code;
3. synthetic raw-record reconstruction;
4. fixed 300 s cohort computation logic;
5. source SHA-256 manifest creation;
6. persistent-copy verification;
7. second-copy verification;
8. teardown authorization only after both copies verify;
9. deliberate corruption of the second copy causes the teardown guard to fail and does not emit `TEARDOWN_AUTHORIZED=YES`.

This is a valid functional simulation of the evidence chain, not proof of a real off-POWDER destination.

## Remaining material blocker

`WP_OFF_POWDER_ROOT` must resolve during the live run to a **real, durable filesystem endpoint outside POWDER** that the UE/controller node can write and later re-read for SHA-256 verification.

The current code deliberately rejects `/proj`, `/users`, and `/share` as the second-copy destination.

A reservation must not be made until one off-POWDER transport/destination is selected and verified. Candidate mechanisms include:

- a user-controlled external host reachable by SSH/rsync;
- an authenticated rclone-backed external repository (for example Google Drive) exposed through a controlled local staging/mount workflow;
- another approved durable external evidence endpoint with read-after-write verification.

The destination must not be a public repository or an unverified transient copy.

## WP7.4 — Reservation readiness QA — ACTIVE

### Resource requirement

Reuse the frozen POWDER profile and RF mapping used for the H-calibration lane:

- profile family: `PowderProfiles/srslte-controlled-rf`
- physical roles: `nuc1` core/eNB/broker/receiver, `nuc2` UE/sender/controller
- attenuator IDs: `1 33 2 34`
- no GPU or additional radio resources required

### Golden time budget

Deterministic scientific window, worst case:

- pre-Q0 workload: 60 s
- Q3 outage: 120 s
- service restoration qualification: <=120 s
- application observation: 300 s
- subtotal live scientific sequence: <=600 s (10 min)

Operational allowance recommended:

- provisioning/login/code/runtime/broker preflight: 20–25 min
- Golden execution: <=10 min
- raw collection/reconstruction: 10 min
- persistent + off-POWDER escrow and verification: 10–15 min
- one bounded infrastructure retry/contingency: 20 min
- safe closeout margin: 15 min

**Recommended reservation duration: 90 minutes minimum; 120 minutes preferred.**

The reservation is for executing a frozen rehearsal, not developing scripts interactively.

## Readiness matrix

| Gate | Implementation | Offline QA | Live dependency |
|---|---|---|---|
| G0 environment identity | orchestrator | syntax PASS | POWDER hosts |
| G1 clean state | orchestrator | syntax PASS | POWDER hosts |
| G2 Q0 + TLS/MQTT readiness | broker/receiver/orchestrator | compile/syntax PASS | real LTE path |
| G3 workload/RF | Golden sender | compile PASS | attenuator control |
| G4 `t_rf_restore` | Golden sender/orchestrator | logic frozen | real RF |
| G5 service restoration | restore script | syntax PASS | srsLTE runtime |
| G6 service-ready | readiness probe | syntax PASS | real LTE/TLS |
| G7 300 s horizon | Golden sender | compile PASS | live run |
| G8 reconstruction | reconstruction script | functional PASS | live raw data |
| G9 evidence escrow | escrow + guard | functional PASS incl. corruption test | **real off-POWDER target BLOCKED** |
| G10 Golden verdict | orchestrator | syntax PASS | G0-G9 live PASS |

## Current decision

`RS7_CURRENT_VERDICT=REPAIR_OFFLINE_FIRST`

`RESERVE=false`

Exact blocker to clear: **freeze and exercise one real off-POWDER verified evidence destination.**

Once that single blocker passes, the consortium may issue `RESERVE` without reopening RS-2 through RS-6 science.
