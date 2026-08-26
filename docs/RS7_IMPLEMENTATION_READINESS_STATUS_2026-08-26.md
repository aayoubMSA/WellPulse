# WellPulse WP2 — RS-7 Implementation & Reservation Readiness Status

Date: 2026-08-26
Owner: Pre-Reservation Consortium
Stage: PRE-RESERVATION / PRE-SCORE

## Executive verdict

**REPAIR_OFFLINE_FIRST — ONE MATERIAL BLOCKER REMAINS.**

The Golden E2E implementation package now exists and has passed offline static/functional QA, including a simulated rclone-based off-testbed path with exact SHA-256 read-back verification. A new POWDER reservation is not yet authorized because the real external rclone destination still requires one-time authentication/configuration and a live connectivity check.

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

### WP7.3 — Evidence, reconstruction, and fail-closed teardown — TECHNICAL PASS / DEPLOYMENT BLOCKED — 30/100 withheld until real external authentication passes

Implemented:

- `experiments/WP-PWD01/evidence_inventory_golden_v1.txt` v1.2
- `scripts/reconstruct_wp2_golden.py`
- `scripts/wp2_golden_evidence_escrow.sh`
- `scripts/wp2_golden_teardown_guard.sh`
- `scripts/wp2_golden_rclone_verify.py`
- `scripts/wp2_golden_offpowder_rclone.sh`
- `scripts/wp2_golden_teardown_guard_rclone.sh`
- `scripts/wp2_golden_offline_qa.sh`
- `.github/workflows/wp2-golden-offline-qa.yml`

Offline QA first exposed and corrected a real shell defect in the progress-bar implementation under `set -u`. GitHub Actions run `33013616916`, job `98326004030`, then completed **SUCCESS** for the corrected filesystem path.

A second QA round added the rclone adapter. GitHub Actions run `33013896313`, job `98326993180`, completed **SUCCESS**.

The successful QA proves:

1. bash syntax for Golden orchestration/restore/readiness/escrow/guard/rclone scripts;
2. Python compilation for Golden sender, reconstruction, and remote verifier code;
3. synthetic raw-record reconstruction;
4. fixed 300 s cohort computation logic;
5. source SHA-256 manifest creation;
6. persistent-copy verification;
7. second-copy filesystem verification;
8. rclone remote copy using a local backend simulation;
9. exact SHA-256 read-back verification by streaming each remote artifact through `rclone cat`;
10. teardown authorization only after verified copies pass;
11. deliberate corruption of the second copy causes the teardown guard to fail and does not emit `TEARDOWN_AUTHORIZED=YES`.

This is a valid functional simulation of both filesystem and rclone evidence chains. It is not proof that the final Google Drive or other external remote has been authenticated from POWDER.

## Remaining material blocker

The preferred external design is now **rclone-backed durable storage**, with Google Drive as the leading operational choice because it avoids requiring an independently reachable SSH server and supports read-after-write verification.

Before reservation, one real remote must be configured outside the repository, for example:

`gdrive:WellPulse/POWDER-Evidence`

Credentials/tokens must remain outside Git and outside scientific artifacts.

The pre-reservation gate is:

1. `rclone lsf <remote>` succeeds from the execution environment;
2. a small non-sensitive probe file can be written;
3. the file can be read back;
4. SHA-256 matches locally and remotely;
5. the probe is removed or moved according to evidence policy;
6. no secret material is captured in logs.

Until this passes, `RESERVE=false`.

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
| G9 evidence escrow | filesystem + rclone adapters + guards | functional PASS incl. corruption/read-back tests | **real remote authentication BLOCKED** |
| G10 Golden verdict | orchestrator | syntax PASS | G0-G9 live PASS |

## Current decision

`RS7_CURRENT_VERDICT=REPAIR_OFFLINE_FIRST`

`RESERVE=false`

**Accepted RS-7 progress: 45/100.** WP7.1 and WP7.2 gates passed. WP7.3 receives no acceptance credit until the real external remote passes the pre-reservation probe, despite the implementation itself passing offline QA.

Exact blocker to clear: **authenticate and probe one real rclone remote without exposing credentials.**

Once that single blocker passes, the consortium can close WP7.3, perform the final WP7.4 readiness review, and issue `RESERVE` without reopening RS-2 through RS-6 science.
