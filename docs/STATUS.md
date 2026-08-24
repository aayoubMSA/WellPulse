# Project Validation Status

## Current state — 2026-08-24

- Canonical GitHub repository: established.
- Canonical Drive validation workspace: established.
- FIT IoT-LAB WP-RT01: **COMPLETE / FINAL EVIDENCE PASS** on Grenoble A8 hardware; 18/18 final cells reconciled.
- POWDER project/access: **APPROVED**.
- Dedicated POWDER SSH automation key: configured.
- GitHub POWDER secrets: SSH username/private key and Portal API token configured.
- POWDER Portal API authentication: **PASS** via read-only `experiment list`.
- Official Portal API lifecycle syntax: **VERIFIED** (`experiment create/get/manifests/terminate`).
- First automated `PowderTeam/srs-rf-matrix` non-scored lifecycle attempt: **FAILED BEFORE READY**. Portal resolved the correct profile and defaults, but the topology requested one `n310`; POWDER reported 0 available and project WellPulse allowed 0. Re-submitting the same profile unchanged is prohibited.
- Failed `srs-rf-matrix` experiment cleanup: **PASS — experiment absent** (`evidence/powder/cleanup-latest.md`). No RF manipulation or scientific workload occurred.
- Controlled-RF fallback candidate identity: **RESOLVED** as `PowderProfiles/srsran-handover`, creator `dmaas`, profile repository `https://gitlab.flux.utah.edu/dmaas/srsran-handover`. The profile provides programmable physical attenuation in the conducted RF matrix. Its current live feasibility run has provisioned/running status; final manifest/SSH/cleanup evidence is still pending.
- Candidate profile warning: POWDER issued a deprecation warning for its Ubuntu 18 image. This does not invalidate feasibility, but the final scored profile/runtime must use a maintained/pinned environment or an explicitly justified immutable legacy image; do not silently adopt the deprecated image for the Q1 corpus.
- WP0 novelty/venue design: **PASS / LOCKED FOR CAMPAIGN DESIGN**.
- Primary venue-fit target: **Internet of Things (Elsevier)**; Computer Networks and Computer Communications retained as fit-dependent backups. Current Q1/indexing/APC status must be re-verified at submission.
- WP-PWD01 protocol: **v0.4 DESIGN FROZEN PENDING LIFECYCLE AND RF CALIBRATION**; scored runs remain unauthorized.
- Primary POWDER comparator: **B1 standard MQTT v3.1.1 QoS1 + automatic reconnect + volatile client state**, matched to W1 at the low-level transport.
- Frozen B1/W1 low-level session: `paho-mqtt==2.1.0`, QoS1, TLS scored path, `clean_session=False`, keepalive 60 s, reconnect 1–8 s, bounded outgoing queue 4096, max inflight 20. Only W1 adds application-level disk durability/reconciliation.
- Pre-score local software/analysis gate: **PASS — 15/15 tests** on Python 3.12.14 with Paho MQTT 2.1.0 (`evidence/local/pre-score-gate-latest.md`). This includes B1/W1 outage/restart semantics, frozen Paho configuration, and deterministic primary-endpoint reconstruction.
- Primary cohort/censoring rule: **FROZEN**. The confirmatory denominator contains records generated at or before final Q0 restoration; arrivals are observed through `H`. Post-restoration generation continues as load but is excluded from the primary denominator to avoid unequal right-censoring.
- Randomization order: **PRE-GENERATED/FROZEN** in `experiments/WP-PWD01/randomization-plan.csv`, seed `26082401`; reserve pairs 4–5 execute only under the precision rule.
- Conducted POWDER scored design: **24–36 runs** under pre-frozen paired precision-based replication.
- Planned OTA replication: **12 runs** for intermittent and hard-outage scenarios only, kept separate from conducted inference.

## Current evidence state

### Existing scientific evidence

FIT WP-RT01 supports communications/durable-buffering/restart-recovery/reconciliation claims on real embedded hardware under controlled connectivity impairment. It does not support radio-propagation, field, pump, hydraulic, groundwater, agronomic, or rural-generalization claims.

### POWDER evidence

Current POWDER files under `evidence/powder/` are **infrastructure/plumbing/feasibility evidence only**. No POWDER run has yet been admitted to the scientific scored corpus.

Key infrastructure records:
- `api-smoke.md` — Portal API authentication PASS;
- `profile-probe.md` — API/profile-resolution evidence;
- `lifecycle-latest.md` — failed `srs-rf-matrix` dry run, no scientific action;
- `cleanup-latest.md` — cleanup PASS / experiment absent;
- `handover-feasibility-latest.md` — candidate controlled-RF feasibility evidence.

### Next gates before any scored POWDER run

1. Finish candidate controlled-RF lifecycle gate: READY -> manifest -> SSH -> fail-safe terminate, and freeze exact profile/runtime choice.
2. Replace or explicitly modernize the candidate's deprecated Ubuntu 18 runtime before scored data if feasible without changing the scientific instrument.
3. Reproduce the frozen Paho session settings in the remote runtime manifest.
4. Verify WellPulse telemetry traverses the experimental cellular data path, not the POWDER control network.
5. Run non-scored physical-RF calibration to freeze Q0–Q3 plus observed radio context.
6. Compute/freeze recovery horizon H and verify cohort/horizon timing.
7. Validate the deterministic analyzer against a non-scored real pilot bundle and verify clock alignment/evidence completeness.
8. Only then set `scored_runs_authorized: true`.
