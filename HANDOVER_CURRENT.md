# WellPulse — Current Handover

Last updated: 2026-08-24 23:56 Africa/Cairo

## Standing handover rule

No material project state may exist only in chat. Decisions, results, artifacts, blockers, evidence boundaries, milestone percentages, time estimates, and the exact next action must be recoverable from GitHub and/or Drive.

## Executive state

WellPulse has completed:

- FIT IoT-LAB embedded-hardware evidence layer;
- POWDER G0 account/project gate;
- POWDER G1 compute provisioning gate;
- POWDER G2 explicit-key SSH + teardown gate;
- POWDER G3 file-based simulated LTE stack/data-path gate.

Current scientific progress remains deliberately conservative: **20%**.

- WP0 Novelty & Venue Lock: **8/8 complete**.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 complete**.
- WP2 RF Calibration & Measurement Validation: **0/15 — next scientific WP**, blocked until a controlled physical-RF lifecycle/user-plane exists.
- WP3 Conducted-RF Confirmatory Campaign: **0/30 — blocked by WP2**.
- WP4 OTA External Replication: **0/15 — blocked by WP3**.
- WP5 Analysis + Artifact + Paper Closure: **0/20 scientific closure**.

Canonical milestone dashboard: `docs/MILESTONE_STATUS.md`.

Current POWDER infrastructure state:

- G0 account/project baseline: **PASS**.
- G1 simple compute provisioning: **PASS**.
- G2 explicit-key manual SSH + node identity + clean teardown: **PASS**.
- G3 simulated stack/data-path validation: **PASS**.
- G4 controlled physical-RF lifecycle discovery/qualification: **NEXT**.
- G5 RF impairment plumbing: **PENDING**.
- Scored POWDER campaign: **NOT AUTHORIZED**.

`scored_runs_authorized = false`.

Resource-creating POWDER automation remains **FROZEN by owner mandate**. G3 PASS does not automatically unfreeze G4 provisioning or scored runs.

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
- Primary manuscript-fit target: `Internet of Things (Elsevier)`; `Computer Networks` and `Computer Communications` are fit-dependent backups. Re-verify venue metadata at submission.

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
- Primary cohort closes at final Q0 restoration; arrivals are observed through frozen recovery horizon H.
- No scored run before all pre-score RF/runtime/evidence gates pass.

Supporting files:

- `experiments/WP-PWD01/analysis-plan.md`
- `experiments/WP-PWD01/evidence-schema.md`
- `experiments/WP-PWD01/randomization-plan.csv`
- `experiments/WP-PWD01/run-matrix.yaml`

### WP2 — RF Calibration & Measurement Validation — 15%

Status: **0% / NEXT SCIENTIFIC WP**.

Cannot begin until G4 establishes a current controlled physical-RF lifecycle and a valid experimental user-plane.

Required outputs:

- exact current profile/revision and physical node/radio bindings;
- real experimental user-plane traffic, not POWDER control-network bypass;
- calibrated numeric Q0/Q1/Q2/Q3 states;
- synchronized RF/context metrics and application evidence;
- non-scored recovery trials sufficient to freeze H;
- complete evidence bundle and deterministic analyzer validation.

Planning estimate after G4 access is established: **~4–8 active hours**.

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

Planning estimate from the current state to a paper-ready POWDER package:

- active hands-on work: **~27–48 hours**;
- best case with immediate resource availability: **~3–4 intensive working days**;
- realistic elapsed time: **~5–8 calendar days**;
- resource-constrained case: **~1–2 weeks** if controlled-RF or OTA resources are unavailable.

These are planning estimates, not commitments. The largest elapsed-time uncertainty is current compatible controlled-RF/OTA resource availability.

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

## POWDER G0/G1/G2 canonical manual golden path

Canonical evidence: `evidence/powder/manual-golden-path-2026-08-24.md`.

Canonical runbook: `powder/MANUAL_GOLDEN_PATH.md`.

Accepted G1/G2 reference run:

- experiment `WP-G1-SIM`;
- UUID `0dc233d7-44a0-4e6c-9734-6d4c8ea0e2ad`;
- profile `srsLTE-SIM:9`;
- profile UUID `80dda605-7e5f-11e9-8006-e4434b2381fc`;
- one `d430`;
- node `pc734`;
- image `PowderProfiles:gnuradio-srslte`;
- explicit Golden-key SSH PASS;
- clean teardown PASS;
- portal returned to `Current Usage: 0 Node Hours`.

Canonical manual SSH key:

- label `WellPulse-POWDER-Golden`;
- fingerprint `SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`;
- local private-key path `%USERPROFILE%\.ssh\wellpulse_powder_golden`.

Never request, echo, commit or copy the private key or its passphrase.

Never reuse historical node hostnames. Always take the endpoint from the current live POWDER experiment.

## POWDER G3 — PASS

Canonical evidence: `evidence/powder/g3-simstack-2026-08-24.md`.

Accepted G3 run:

- experiment `WP-G3-SIMSTACK`;
- UUID `3484b01d-7eca-48e7-9e34-866680057b0d`;
- profile `srsLTE-SIM:9`;
- profile UUID `80dda605-7e5f-11e9-8006-e4434b2381fc`;
- one `d430`;
- allocated node `pc757`;
- image `PowderProfiles/gnuradio-srslte`;
- SSH endpoint used `pc757.emulab.net:22`;
- remote hostname `node.wp-g3-simstack.wellpulse.emulab.net`;
- Ubuntu 18.04.1 / kernel 4.15.0-33;
- manual SSH with the Golden key: PASS.

Profile-authoritative commands:

```bash
/usr/local/srsLTE/build/lib/examples/pdsch_enodeb -o /tmp/wellpulse_g3.iq -n 5 -m 9 -v
/usr/local/srsLTE/build/lib/examples/pdsch_ue -i /tmp/wellpulse_g3.iq -n 5 -r 1234 -v -d
```

Observed acceptance evidence:

- transmitter completed with `Done`;
- MIB decoded;
- CFI/PDCCH/PDSCH decoded;
- code-block CRCs reported `CRC=OK`;
- multiple `TB decoded OK`;
- receiver exited `RX_RC=0`;
- waveform size `2304000` bytes;
- waveform SHA-256 `103de59d52e75252e916d7ed62c5c9b76401e817ffec3178363879e0bed71678`;
- temporary waveform deletion verified `IQ_CLEANUP=PASS`;
- SSH exited cleanly;
- manual experiment termination verified in the live dashboard;
- final dashboard: `Current Usage: 0 Node Hours` and no active experiments.

One first-block diagnostic line `Error in TB parity: par_tx=0x0, par_rx=0x0` is preserved in evidence. Subsequent transport blocks decoded successfully and receiver exit status was zero; it is not treated as a fatal G3 failure.

G3 evidence boundary: the path is **file-based simulation only**:

`pdsch_enodeb -> IQ file -> pdsch_ue`

It proves no SDR, no RF propagation, no attenuation, no OTA behavior, no MQTT/WellPulse scientific performance, and no field/agronomic outcome.

G3 contributes **0% scientific completion**.

## G3 automation troubleshooting — quarantined

A safe attach-only helper exists at `.github/workflows/powder-g3-attach.yml`, but earlier attach attempts failed before target validation.

Sanitized diagnosis: `evidence/powder/g3-key-format-diag.json`.

Current known issue:

- GitHub repository secret `POWDER_SSH_PRIVATE_KEY` contains a public key rather than an usable private key;
- failed attach attempts did not execute the G3 workload;
- failed attach attempts did not terminate the experiment;
- accepted G3 evidence is the manual Golden-key run above.

Do not rerun CI just to obtain a more automated copy of an already accepted G3 result.

The full resource-creating workflow `.github/workflows/powder-g3-simstack.yml` remains **FROZEN / DO NOT RUN** under the owner mandate.

## POWDER troubleshooting history — quarantined

Do not promote any of these into scientific evidence:

1. `wpplmb6787317` / `srs-rf-matrix`: failed before READY because topology requested `n310` while WellPulse entitlement was 0; do not resubmit unchanged.
2. `wphnd8201533` / `srsran-handover`: exploratory/invalid feasibility attempt; not a current controlled-RF baseline.
3. Earlier pre-Golden `WP-G1-SIM` attempts: troubleshooting only.
4. Failed G3 GitHub attach attempts: credential troubleshooting only; no target validation/test/teardown.

## Security and log-minimization rule

Never commit or copy into handover artifacts:

- private SSH keys;
- SSH-key passphrases;
- `POWDER_API_TOKEN`;
- experiment RPC tokens;
- certificate blocks;
- raw portal credential-like material.

Preserve sanitized experiment/profile IDs, resource bindings, image/runtime identity, state transitions, endpoint/auth mode, timestamps, commands, exit codes, hashes and acceptance outcomes.

## Exact next gate — G4 controlled physical-RF lifecycle

Status: **NEXT / NOT STARTED**.

Purpose: identify and manually qualify a **current** POWDER controlled physical-RF path before any WP2 calibration or scored run.

Manual-first procedure:

1. Use the live authenticated POWDER UI to inspect current example/project profiles relevant to controlled physical RF.
2. Verify exact profile name, owner/project, revision, requested radio/hardware resources, WellPulse entitlement and current availability.
3. Do not infer the current baseline from stale names or code.
4. Do not reuse `srsran-handover` without fresh live verification.
5. Do not resubmit `srs-rf-matrix` unchanged because its previous topology required unavailable `n310` resources.
6. Select the smallest current profile that can prove the required controlled physical-RF lifecycle.
7. Provision **one manual non-scored qualification experiment only**.
8. Verify READY and exact resource bindings in the live manifest/list view.
9. SSH using an explicit registered key and the current endpoint.
10. Capture only credential-free metadata needed for reproducibility.
11. Terminate cleanly and verify zero active usage.
12. Record a G4 PASS/FAIL artifact before any move into experimental user-plane or RF calibration.

No automation of G4 resource creation is authorized at this stage.

After G4 lifecycle PASS:

- establish the real experimental cellular user-plane rather than POWDER control-network bypass;
- reproduce the frozen Paho runtime/session;
- execute non-scored G5/WP2 RF calibration;
- freeze Q0/Q1/Q2/Q3 and recovery horizon H;
- validate evidence timing/analyzer;
- only then consider explicit scored-run authorization.

## Reproducibility read order for a new agent

Read in this order before acting:

1. `HANDOVER_CURRENT.md`
2. `docs/MILESTONE_STATUS.md`
3. `docs/STATUS.md`
4. `docs/DECISIONS.md`
5. `evidence/powder/g3-simstack-2026-08-24.md`
6. `powder/MANUAL_GOLDEN_PATH.md`
7. `evidence/powder/manual-golden-path-2026-08-24.md`
8. `experiments/WP-PWD01/protocol.md`
9. `experiments/WP-PWD01/analysis-plan.md`
10. `experiments/WP-PWD01/evidence-schema.md`
11. `experiments/WP-PWD01/randomization-plan.csv`
12. `experiments/WP-PWD01/run-matrix.yaml`

Do not infer current testbed availability or profile compatibility from historical files; verify the live POWDER UI before provisioning each new infrastructure layer.

## Handover completion checklist

Before ending any material WellPulse work block:

1. Update this file.
2. Update `docs/MILESTONE_STATUS.md` when a WP/gate/progress/time estimate changes.
3. Update `docs/STATUS.md`.
4. Update `docs/DECISIONS.md` only if a decision changed.
5. Update relevant sanitized evidence.
6. Update the Drive Current Handover Index and `MILESTONES` tab.
7. Preserve exact PASS/FAIL, exclusions, evidence boundary, teardown state and next action.
8. Ensure a new agent can resume without reading chat history.