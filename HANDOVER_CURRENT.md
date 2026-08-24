# WellPulse — Current Handover

Last updated: 2026-08-24 22:36 Africa/Cairo

## Standing handover rule

No material project state may exist only in chat. Decisions, results, artifacts, blockers, evidence boundaries, milestone percentages, time estimates, and the exact next action must be recoverable from GitHub and/or Drive.

## Executive state

WellPulse has one completed embedded-hardware validation layer on FIT IoT-LAB and has now completed the first POWDER manual infrastructure golden path.

Current scientific progress is deliberately conservative: **20%**.

- WP0 Novelty & Venue Lock: **8/8 complete**.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 complete**.
- WP2 RF Calibration & Measurement Validation: **0/15 — next scientific WP**.
- WP3 Conducted-RF Confirmatory Campaign: **0/30 — blocked by WP2**.
- WP4 OTA External Replication: **0/15 — blocked by WP3**.
- WP5 Analysis + Artifact + Paper Closure: **0/20 scientific closure**; substantial analysis/reproducibility scaffolding is already prepared but is not counted as completed scientific WP credit.

Canonical milestone dashboard: `docs/MILESTONE_STATUS.md`.

Current POWDER infrastructure state:

- G0 account/project baseline: **PASS**.
- G1 simple compute provisioning: **PASS**.
- G2 explicit-key manual SSH + node identity + clean teardown: **PASS**.
- G3 simulated radio/data-path validation: **NEXT / NOT STARTED**.
- Controlled physical-RF lifecycle: **NOT STARTED**.
- Scored POWDER campaign: **NOT AUTHORIZED**.

Resource-creating POWDER automation remains **FROZEN** until the equivalent manual layer has passed.

## Canonical repositories and workspaces

- GitHub: `aayoubMSA/WellPulse`.
- Drive project root `P12_WellPulse`: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`.
- Drive validation workspace `00_Validation_Workspace`: `1SydHCA2jlkatxdGgUtJ1P8atgyi8_ta3`.
- Drive raw evidence `02_RAW_EVIDENCE`: `11xaitxG0vkV6fCzK_JgLAacrdhjz7GBf`.
- Drive handover folder `WellPulse Handover`: `1Du4j_YkMLvQjWJCxV5zqxxK6OGG2Q0hA`.
- Drive current handover index: `1Gd4FzyJ_dW6-AK6wQc4FW7LAWVb2GNzG0t-xHaSEwn4`.

## Scientific work packages

### WP0 — Novelty & Venue Lock — 8%

Status: **PASS / 100%**.

Frozen position:

- Do not claim novelty for generic MQTT, store-and-forward, buffering, offline-first operation, or 5G/LTE.
- Contribution is durable record identity + idempotent reconciliation + strong matched MQTT baseline + causal real-RF manipulation + OTA replication + reproducible cross-testbed evidence ladder.
- Primary manuscript-fit target: `Internet of Things (Elsevier)`; `Computer Networks` and `Computer Communications` remain fit-dependent backups. Re-verify venue metadata at submission.

### WP1 — Confirmatory Protocol & Statistics Freeze — 12%

Status: **PASS / 100%**.

Canonical protocol: `experiments/WP-PWD01/protocol.md`, version v0.4.

Frozen essentials:

- Primary comparator `B1_MQTT_QOS1`: MQTT v3.1.1, QoS1, TLS scored path, automatic reconnect, volatile client state, no application-level disk durability/reconciliation.
- WellPulse `W1_OFFLINE_FIRST`: same low-level Paho session plus SQLite durable queue, stable record identity/checksum, replay, idempotent receiver and reconciliation.
- `paho-mqtt==2.1.0`, `clean_session=False`, keepalive 60 s, reconnect 1–8 s, outgoing queue 4096, inflight 20.
- Scenarios S0 healthy, S1 intermittent, S2 hard outage, S3 outage + gateway-process restart.
- Run is the statistical unit.
- Conducted campaign: 24–36 scored runs under precision-based replication.
- OTA replication: 12 scored runs for S1/S2 only.
- Primary cohort closes at final Q0 restoration; arrivals observed through frozen recovery horizon H.
- `scored_runs_authorized` remains false until all pre-score RF/runtime/evidence gates pass.

Supporting files:

- `experiments/WP-PWD01/analysis-plan.md`
- `experiments/WP-PWD01/evidence-schema.md`
- `experiments/WP-PWD01/randomization-plan.csv`
- `experiments/WP-PWD01/run-matrix.yaml`

### WP2 — RF Calibration & Measurement Validation — 15%

Status: **0% / NEXT SCIENTIFIC WP**.

Cannot start until manual infrastructure sequence reaches a valid controlled physical-RF profile and user-plane path.

Required outputs:

- exact current profile/revision and physical node/radio bindings;
- real experimental user-plane traffic, not POWDER control-network bypass;
- calibrated numeric Q0/Q1/Q2/Q3 states;
- synchronized RF/context metrics and application evidence;
- non-scored recovery trials sufficient to freeze H;
- complete evidence bundle and deterministic analyzer validation.

Planning estimate after G3/controlled-RF access is available: **~4–8 active hours**.

### WP3 — Conducted-RF Confirmatory Campaign — 30%

Status: **0% / BLOCKED BY WP2**.

Execute frozen B1/W1 randomized paired campaign only after WP2 PASS and explicit scored authorization.

Planning estimate: **~6–10 active hours**, excluding queue/resource wait time.

### WP4 — OTA External Replication — 15%

Status: **0% / BLOCKED BY WP3**.

Compact replication only: S1 and S2, B1/W1, 3 paired blocks each = 12 scored OTA runs.

Planning estimate: **~3–6 active hours**, highly dependent on OTA availability.

### WP5 — Analysis + Artifact + Paper Closure — 20%

Status: **0% scientific closure**.

Prepared already: deterministic analysis design, evidence schema, run matrix, randomization, protocol, local pre-score tests. Do not count these as final WP5 completion before real POWDER evidence exists.

Planning estimate after data acquisition: **~12–20 active hours**.

## Overall scientific progress and remaining time

Scientific completion: **20%**.

Planning estimate from current state to a paper-ready POWDER package:

- active hands-on work: **~28–50 hours**;
- best case with immediate resource availability: **~3–4 intensive working days**;
- realistic elapsed time: **~5–8 calendar days**;
- resource-constrained case: **~1–2 weeks** if conducted-RF or OTA resources are unavailable.

These are planning estimates, not commitments. The largest elapsed-time uncertainty is current compatible controlled-RF/OTA resource availability, not local software or SSH plumbing.

## FIT IoT-LAB — completed prior evidence layer

Status: **COMPLETE / FINAL EVIDENCE PASS**.

Canonical result: `experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md`.

Evidence class: `FINAL_WP_RT01_FIT_A8`.

- Grenoble A8 hardware.
- B0/W1 × C0/C1/C2 × 3 replicates = 18 final cells.
- 10,000 records/cell.
- 18/18 final reconciliation PASS.
- W1 retained 100% completeness with zero permanent loss and zero duplicates under controlled broker outage and gateway-process restart.
- B0 retained 80% in C1/C2.

Evidence boundary: communications, buffering, process-restart recovery and reconciliation on real embedded hardware under controlled connectivity impairment only. No pump/hydraulic/groundwater/agronomic/Siwa-field claim.

## POWDER canonical manual golden path — G0/G1/G2 PASS

Canonical evidence: `evidence/powder/manual-golden-path-2026-08-24.md`.

Canonical runbook: `powder/MANUAL_GOLDEN_PATH.md`.

Accepted reference run:

- experiment: `WP-G1-SIM`;
- experiment UUID: `0dc233d7-44a0-4e6c-9734-6d4c8ea0e2ad`;
- profile: `srsLTE-SIM:9`;
- profile UUID: `80dda605-7e5f-11e9-8006-e4434b2381fc`;
- hardware: one `d430`;
- allocated node: `pc734`;
- disk image: `PowderProfiles:gnuradio-srslte`;
- SSH endpoint: `pc734.emulab.net:22`;
- remote user: `aayoub`;
- canonical remote hostname: `node.wp-g1-sim.wellpulse.emulab.net`;
- observed OS: Ubuntu 18.04.1 LTS;
- observed kernel: Linux 4.15.0-33-generic x86_64;
- observed UTC check: Mon Aug 24 19:15:48 UTC 2026;
- history start: 2026-08-24 22:07 portal-local;
- destroyed: 2026-08-24 22:17 portal-local;
- portal history PHours: 0.16;
- teardown: `Current Usage: 0 Node Hours`.

Canonical manual SSH key:

- label: `WellPulse-POWDER-Golden`;
- fingerprint: `SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`;
- local private-key path: `%USERPROFILE%\.ssh\wellpulse_powder_golden`;
- private key and passphrase must never be committed, pasted into evidence, or requested by a future agent.

Successful acceptance command pattern:

```powershell
ssh -o IdentitiesOnly=yes `
  -i "$HOME\.ssh\wellpulse_powder_golden" `
  aayoub@ACTUAL_HOSTNAME_FROM_POWDER_LIST_VIEW
```

Never reuse historical hostnames. Always obtain the active endpoint from List View.

Profile evidence boundary: `srsLTE-SIM:9` is a one-node srsLTE file-based simulation profile with **no SDR and no RF**. G1/G2 therefore prove provisioning, key injection, SSH and teardown only.

## POWDER troubleshooting history — quarantined

Do not promote any of these into scientific evidence:

1. `wpplmb6787317` / `srs-rf-matrix`: failed before READY; hidden `n310` requirement with zero availability/entitlement; re-submitting unchanged is prohibited.
2. `wphnd8201533` / `srsran-handover`: exploratory/invalid feasibility attempt; not a current controlled-RF baseline.
3. `WP-G1-SIM` started 21:06: provisioning passed but intended local key was not the registered POWDER key; destroyed 21:42.
4. `WP-G1-SIM` started 21:45: troubleshooting rerun before Golden-key reset; destroyed 22:04.
5. `WP-G1-SIM` started 22:07: **canonical G1/G2 PASS**; destroyed 22:17.

Portal-history troubleshooting usage is provenance only, not scientific evidence.

## Security and log-minimization rule

Never commit or copy into handover artifacts:

- private SSH keys;
- SSH-key passphrases;
- `POWDER_API_TOKEN`;
- experiment RPC tokens;
- certificate blocks;
- raw portal credential-like material.

Raw POWDER logs may contain encrypted token/certificate material. Preserve sanitized extracts containing only the fields required for reproducibility: experiment/profile IDs, resource bindings, image/runtime identity, state transitions, SSH endpoint/auth mode, timestamps and acceptance outcomes.

Existing GitHub Actions secret names include `POWDER_SSH_PRIVATE_KEY`, `POWDER_USERNAME`, and `POWDER_API_TOKEN`. Do not echo their values.

## Exact next gate — G3 simulated stack/data-path validation

Status: **NEXT / NOT STARTED**.

Purpose: prove that a current simulated radio-stack/data-path experiment works manually before selecting/automating a physical-RF path.

Preferred immediate reuse candidate: `srsLTE-SIM:9`, because it is already verified to instantiate and its profile instructions expose file-based eNodeB/UE examples. G3 is still non-scored and still no RF.

Manual sequence:

1. Confirm `Current Usage: 0 Node Hours`.
2. Re-run `srsLTE-SIM:9` manually under project `WellPulse` with a distinct G3 name such as `WP-G3-SIMSTACK`.
3. Wait for READY.
4. Read the actual SSH endpoint from List View.
5. SSH using the explicit Golden key.
6. Execute only the profile-authoritative srsLTE simulated send/receive example and capture stdout/stderr plus file metadata/checksum.
7. Verify expected receive behavior; do not infer RF.
8. Remove only temporary test output if appropriate after evidence capture.
9. Exit and terminate manually.
10. Confirm zero active usage.
11. Record a sanitized G3 evidence file and update this handover.

After G3 PASS, manually discover a **current** controlled physical-RF profile through the live POWDER UI. Do not trust stale remembered profile names. `srs-rf-matrix` remains blocked as-is because of its `n310` dependency.

## Other remote-testbed lanes

### ARA rural OTA

Status: qualified access lane / not executed. Preserve for a distinct rural/outdoor OTA claim only; do not use it to duplicate the entire conducted matrix.

### COSMOS/ORBIT

Status in the prior handover was activation/access work. It remains a fallback lane if POWDER controlled-RF access stalls. Re-verify live account state before acting; do not assume the 2026-08-23 activation status is still the current operational state.

## Reproducibility read order for a new agent

A new agent should read, in this order:

1. `HANDOVER_CURRENT.md` — canonical operational state.
2. `docs/MILESTONE_STATUS.md` — WP progress, gates and time estimate.
3. `docs/STATUS.md` — current validation/science status.
4. `docs/DECISIONS.md` — frozen decisions and anti-drift rules.
5. `powder/MANUAL_GOLDEN_PATH.md` — verified POWDER access procedure.
6. `evidence/powder/manual-golden-path-2026-08-24.md` — accepted reference evidence.
7. `experiments/WP-PWD01/protocol.md` — scientific protocol v0.4.
8. `experiments/WP-PWD01/analysis-plan.md`.
9. `experiments/WP-PWD01/evidence-schema.md`.
10. `experiments/WP-PWD01/run-matrix.yaml` and `randomization-plan.csv`.

The new agent should not infer current testbed availability or current profile compatibility from historical files; verify the live POWDER UI before provisioning each new layer.

## Handover completion checklist

Before ending any material WellPulse work block:

1. Update this file.
2. Update `docs/MILESTONE_STATUS.md` when a WP/gate/progress/time estimate materially changes.
3. Update the relevant protocol/result/evidence file.
4. Update the Drive Current Handover Index and milestone tab.
5. Preserve durable raw evidence where appropriate without committing secrets.
6. Record exact PASS/FAIL, exclusions, evidence boundary, teardown state and next action.
7. Verify that a new agent can resume without reading chat history.
