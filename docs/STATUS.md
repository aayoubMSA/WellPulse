# Project Validation Status

## Current state — 2026-08-24

- Canonical GitHub repository: established.
- Canonical Drive validation workspace: established.
- FIT IoT-LAB WP-RT01: **COMPLETE / FINAL EVIDENCE PASS** on Grenoble A8 hardware; 18/18 final cells reconciled.
- POWDER project/access: **APPROVED**.
- POWDER Portal API authentication: **PASS** via earlier read-only `experiment list`.
- Resource-creating POWDER automation: **FROZEN** until the corresponding manual path is proven first.
- Manual POWDER golden path: **PASS** on 2026-08-24 using `srsLTE-SIM:9` on one `d430` node.
- Canonical successful manual experiment: `WP-G1-SIM`, UUID `0dc233d7-44a0-4e6c-9734-6d4c8ea0e2ad`, allocated node `pc734`.
- Manual SSH: **PASS** with explicit local key `WellPulse-POWDER-Golden`; remote identity `aayoub`, canonical hostname `node.wp-g1-sim.wellpulse.emulab.net`.
- Manual teardown: **PASS**; portal returned to `Current Usage: 0 Node Hours`.
- Golden-path evidence: `evidence/powder/manual-golden-path-2026-08-24.md`.
- Reproducibility runbook: `powder/MANUAL_GOLDEN_PATH.md`.
- The `srsLTE-SIM:9` gate is compute/provisioning/SSH infrastructure only. Its own profile description states that interaction is simulated without SDR hardware; it is **not RF or scientific evidence**.
- Earlier automated/exploratory POWDER attempts are quarantined as troubleshooting history and excluded from the scientific corpus:
  - `PowderTeam/srs-rf-matrix` attempt `wpplmb6787317`: failed because the topology requested an `n310` while project WellPulse had entitlement 0; do not re-submit unchanged.
  - `srsran-handover` exploratory attempt `wphnd8201533`: not accepted as a controlled-RF baseline; do not treat its prior lifecycle output as current feasibility evidence.
  - two earlier `WP-G1-SIM` runs were troubleshooting attempts before the final Golden-key baseline and are not canonical evidence.
- Current next manual gate: **G3 — simulated radio/data-path validation** using a current profile verified in the POWDER UI. Do not infer a current profile name from stale automation code or prior memory.
- G3 safe attach automation: **PREPARED / NOT YET EXECUTED** in `.github/workflows/powder-g3-attach.yml`. Manual creation of a fresh `WP-G3-SIMSTACK` experiment remains required; after READY, the workflow may validate the exact experiment/profile/hardware/image, discover SSH from the manifest, execute the profile-authoritative file-based simulated path, capture sanitized evidence, and fail-safe terminate the validated experiment. It does not create POWDER resources.
- Full resource-creating G3 workflow `.github/workflows/powder-g3-simstack.yml`: **UNAPPROVED / DO NOT RUN YET**. Its existence does not override the manual-first freeze.
- Controlled physical-RF profile: **NOT YET FROZEN**. Selection must occur only after current manual UI/profile verification and a successful non-scored lifecycle/data-path gate.
- WP0 novelty/venue design: **PASS / LOCKED FOR CAMPAIGN DESIGN**.
- Primary venue-fit target: **Internet of Things (Elsevier)**; Computer Networks and Computer Communications retained as fit-dependent backups. Current Q1/indexing/APC status must be re-verified at submission.
- WP-PWD01 protocol: **v0.4 DESIGN FROZEN PENDING LIFECYCLE AND RF CALIBRATION**; scored runs remain unauthorized.
- Primary POWDER comparator: **B1 standard MQTT v3.1.1 QoS1 + automatic reconnect + volatile client state**, matched to W1 at the low-level transport.
- Frozen B1/W1 low-level session: `paho-mqtt==2.1.0`, QoS1, TLS scored path, `clean_session=False`, keepalive 60 s, reconnect 1–8 s, bounded outgoing queue 4096, max inflight 20. Only W1 adds application-level disk durability/reconciliation.
- Pre-score local software/analysis gate: **PASS — 15/15 tests** on Python 3.12.14 with Paho MQTT 2.1.0 (`evidence/local/pre-score-gate-latest.md`).
- Primary cohort/censoring rule: **FROZEN**. The confirmatory denominator contains records generated at or before final Q0 restoration; arrivals are observed through `H`.
- Randomization order: **PRE-GENERATED/FROZEN** in `experiments/WP-PWD01/randomization-plan.csv`, seed `26082401`; reserve pairs 4–5 execute only under the precision rule.
- Conducted POWDER scored design: **24–36 runs** under pre-frozen paired precision-based replication.
- Planned OTA replication: **12 runs** for intermittent and hard-outage scenarios only, kept separate from conducted inference.

## Current evidence state

### Existing scientific evidence

FIT WP-RT01 supports communications/durable-buffering/restart-recovery/reconciliation claims on real embedded hardware under controlled connectivity impairment. It does not support radio-propagation, field, pump, hydraulic, groundwater, agronomic, or rural-generalization claims.

### POWDER evidence

Current POWDER evidence is **infrastructure/plumbing/feasibility evidence only**. No POWDER run has yet been admitted to the scientific scored corpus.

Canonical current records:

- `evidence/powder/manual-golden-path-2026-08-24.md` — manual provision/SSH/teardown PASS;
- `powder/MANUAL_GOLDEN_PATH.md` — reproducible manual baseline procedure;
- `api-smoke.md` — earlier read-only Portal API authentication PASS;
- `lifecycle-latest.md` — failed `srs-rf-matrix` dry run; historical troubleshooting only;
- `cleanup-latest.md` — cleanup evidence for the failed RF-matrix attempt.

Any older file that describes `srsran-handover` as a live/current feasible controlled-RF baseline is superseded by this status until a fresh manual verification establishes otherwise.

### Next gates before any scored POWDER run

1. **G3:** create one fresh `srsLTE-SIM:9` experiment manually and, after READY, use the attach-only G3 workflow to execute the non-scored simulated end-to-end path check, capture evidence, and terminate cleanly.
2. Identify a current controlled physical-RF profile through the live POWDER UI; freeze exact profile revision and hardware only after manual provisioning succeeds.
3. Establish controlled-RF lifecycle manually: READY -> manifest -> SSH -> fail-safe terminate.
4. Reproduce the frozen Paho session settings in the remote runtime manifest.
5. Verify WellPulse telemetry traverses the experimental cellular data path, not the POWDER control network.
6. Run non-scored physical-RF calibration to freeze Q0–Q3 plus observed radio context.
7. Compute/freeze recovery horizon H and verify cohort/horizon timing.
8. Validate the deterministic analyzer against a non-scored real pilot bundle and verify clock alignment/evidence completeness.
9. Only then set `scored_runs_authorized: true`.
