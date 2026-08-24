# AGENT HANDOVER — WellPulse POWDER Validation Owner

**Handover timestamp:** 2026-08-24 23:56 Africa/Cairo  
**Canonical repository:** `aayoubMSA/WellPulse`  
**Current scientific completion:** **20%**  
**Current execution gate:** **G4 — Controlled physical-RF lifecycle discovery and qualification — NEXT**

## Mandate

Own continuation of the WellPulse POWDER validation lane from the accepted G0–G3 infrastructure baseline through the minimum defensible publication-grade controlled-RF/OTA evidence. Preserve reproducibility, security boundaries, scientific discipline, and exact milestone accounting.

Optimize for:

`scientific value × reproducibility × reviewer defensibility ÷ execution risk × unnecessary scope × resource cost`

Do not broaden the project merely because POWDER exposes additional capabilities.

## Read order — mandatory before execution

Read these files in this order before taking any action:

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

Treat GitHub and the Drive handover index as canonical state. Do not reconstruct project status from chat memory.

## Scientific WP state

- WP0 — Novelty & Venue Lock — **8/8 complete**.
- WP1 — Confirmatory Protocol & Statistics Freeze — **12/12 complete**.
- WP2 — RF Calibration & Measurement Validation — **0/15 — NEXT scientific WP**, blocked until G4 establishes a valid controlled physical-RF lifecycle/user-plane.
- WP3 — Conducted-RF Confirmatory Campaign — **0/30 — blocked by WP2**.
- WP4 — OTA External Replication — **0/15 — blocked by WP3**.
- WP5 — Analysis + Artifact + Paper Closure — **0/20 scientific closure**.

Weighted scientific completion: **20%**.

Planning estimate remaining: **~27–48 active hours**, realistically **~5–8 calendar days**, extending to **~1–2 weeks** if compatible controlled-RF or OTA resources require waiting.

## POWDER infrastructure state

- G0 Account + WellPulse project — **PASS**.
- G1 Manual compute provisioning — **PASS**.
- G2 Explicit-key SSH + node verification + clean teardown — **PASS**.
- G3 Simulated stack/data path — **PASS**.
- G4 Controlled physical-RF lifecycle — **NEXT**.
- G5 RF impairment plumbing — **PENDING**.

G0–G3 are enabling infrastructure only. They do not add scientific WP percentage.

## Accepted G3 baseline

Canonical evidence:

`evidence/powder/g3-simstack-2026-08-24.md`

Accepted experiment:

- experiment: `WP-G3-SIMSTACK`
- UUID: `3484b01d-7eca-48e7-9e34-866680057b0d`
- profile: `srsLTE-SIM:9`
- profile UUID: `80dda605-7e5f-11e9-8006-e4434b2381fc`
- hardware: one `d430`
- node: `pc757`
- image: `PowderProfiles:gnuradio-srslte`
- remote hostname: `node.wp-g3-simstack.wellpulse.emulab.net`
- explicit Golden-key SSH: PASS
- transmitter: completed with `Done`
- receiver: MIB/PDCCH/PDSCH decoded, multiple `TB decoded OK`, `RX_RC=0`
- waveform bytes: `2304000`
- waveform SHA-256: `103de59d52e75252e916d7ed62c5c9b76401e817ffec3178363879e0bed71678`
- temporary output cleanup: PASS
- portal teardown: PASS; `Current Usage: 0 Node Hours`, no active experiments

Evidence boundary: G3 is a **file-based simulated LTE path only**. No SDR, no physical RF, no attenuation, no OTA, no MQTT/WellPulse scored science.

## Exact next gate — G4

Goal: discover and manually qualify a **current controlled physical-RF lifecycle** on POWDER before any WP2 calibration.

Procedure:

1. Use the live authenticated POWDER UI to inspect current controlled physical-RF example/profile candidates.
2. Verify exact profile name, owner/project, revision, requested radio/hardware resources, WellPulse entitlement and live availability.
3. Do not infer compatibility from stale repository code, remembered profile names or earlier exploratory attempts.
4. Do not reuse `srsran-handover` as a baseline without fresh verification.
5. Do not resubmit `srs-rf-matrix` unchanged; its previous topology required an unavailable `n310` entitlement.
6. Select the smallest current profile that can prove the required controlled physical-RF lifecycle.
7. Provision **one manual, non-scored qualification experiment only**.
8. Verify READY and exact resource bindings from the live portal/manifest.
9. SSH using an explicit registered key and the current live endpoint.
10. Capture only sanitized reproducibility metadata.
11. Terminate cleanly and verify zero active usage.
12. Save a durable G4 PASS/FAIL artifact and update GitHub + Drive before proceeding.

No automation of G4 resource creation is authorized at this stage.

G4 PASS still does not authorize scored work.

## After G4

Only after a valid controlled physical-RF lifecycle is established:

- prove the experimental cellular user-plane rather than POWDER control-network bypass;
- reproduce the frozen Paho session settings;
- run non-scored RF calibration;
- freeze Q0–Q3 plus observed radio context;
- freeze recovery horizon H;
- validate analyzer timing/evidence completeness;
- only then consider explicit `scored_runs_authorized=true`.

## Automation troubleshooting — quarantine

The attach-only G3 workflow exists at `.github/workflows/powder-g3-attach.yml`, but its repository SSH credential is currently not trustworthy.

Sanitized diagnosis:

`evidence/powder/g3-key-format-diag.json`

Known issue:

- `POWDER_SSH_PRIVATE_KEY` contains a public key rather than an usable private key;
- earlier CI attempts failed before target validation;
- they did not execute the G3 workload;
- they did not terminate the target;
- accepted G3 evidence was completed manually with `WellPulse-POWDER-Golden`.

Do not rerun CI merely to duplicate an already accepted G3 result.

The full resource-creating workflow `.github/workflows/powder-g3-simstack.yml` remains **FROZEN / DO NOT RUN** under the owner mandate.

## Known failed/exploratory history — quarantine

- `wpplmb6787317` / `srs-rf-matrix` — failed because topology requested an `n310` while WellPulse entitlement was 0. **Do not resubmit unchanged.**
- `wphnd8201533` / `srsran-handover` — exploratory/invalid feasibility attempt. Not an accepted current RF baseline.
- earlier pre-Golden `WP-G1-SIM` runs — troubleshooting only.
- failed G3 CI attach attempts — credential troubleshooting only.

## Frozen scientific design — do not drift

Primary comparator:

`B1_MQTT_QOS1` — MQTT v3.1.1, QoS1, TLS scored path, automatic reconnect, volatile client state, no application-level disk durability/reconciliation.

WellPulse:

`W1_OFFLINE_FIRST` — same low-level Paho session plus SQLite durable queue, stable identity/checksum, replay, idempotent receiver and reconciliation.

Frozen low-level settings:

- `paho-mqtt==2.1.0`
- MQTT v3.1.1
- QoS1
- `clean_session=False`
- keepalive 60 s
- reconnect 1–8 s
- outgoing queue 4096
- inflight 20

Scenarios: S0 healthy, S1 intermittent, S2 hard outage, S3 outage + gateway-process restart.

Run is the statistical unit. Conducted campaign is 24–36 scored runs under the frozen precision rule. OTA replication is 12 scored runs for S1/S2 only.

`scored_runs_authorized = false` until every pre-score gate in `protocol.md` passes.

## Evidence boundary

POWDER may support claims about networking, radio-link resilience, edge/cloud recovery, telemetry integrity/completeness, reconnect behavior, process-restart recovery and resilience overhead.

It does **not** validate pump mechanics, hydraulics, groundwater, crop physiology, Siwa conditions, agricultural field performance or rural generalization.

## Security / reproducibility rules

Never commit or expose:

- private SSH keys;
- SSH passphrases;
- POWDER API tokens;
- experiment RPC tokens;
- certificate blocks;
- raw credential-like portal material.

Preserve sanitized reproducibility fields instead: experiment/profile IDs, resource bindings, image/software identity, actual endpoint/auth mode, state transitions, timestamps, commands, exit codes, hashes, verdicts, evidence boundaries and teardown state.

## Manual-first rule

Resource-creating POWDER automation remains **FROZEN by owner mandate**. Each new infrastructure/profile layer must be qualified manually before automation is considered.

## Required handover discipline

At the end of every material work block:

1. update `HANDOVER_CURRENT.md`;
2. update `docs/MILESTONE_STATUS.md`;
3. update `docs/STATUS.md` and `docs/DECISIONS.md` only if a decision changed;
4. save sanitized evidence under `evidence/powder/`;
5. update the Drive `WellPulse — Current Handover Index` including `MILESTONES`;
6. preserve publication-relevant raw evidence without secrets;
7. ensure exact next action is recoverable without chat history.

## Stop conditions

Stop rather than improvise if:

- live profile/resource identity differs from expectation;
- a hidden hardware entitlement appears;
- user-plane cannot be distinguished from control-network traffic;
- mandatory evidence cannot be reconstructed;
- protocol amendment is required;
- a scientific result is unfavorable — never rerun merely to improve it.

## Immediate acceptance target

Produce exactly one durable G4 lifecycle qualification artifact with a PASS/FAIL verdict and clean teardown before beginning G5/WP2 RF calibration.