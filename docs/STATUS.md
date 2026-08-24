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
- First automated `PowderTeam/srs-rf-matrix` non-scored lifecycle attempt: **FAILED BEFORE READY**. Portal resolved the correct profile and its defaults, but the topology requested one `n310`; POWDER reported 0 `n310` available and project WellPulse allowed 0. Re-submitting the same profile unchanged is prohibited because the portal explicitly states it will always fail.
- Failed experiment cleanup: **PASS — experiment absent** (`evidence/powder/cleanup-latest.md`). No RF manipulation or scientific workload occurred.
- Controlled-RF fallback feasibility: **IN PROGRESS**. `srsran-handover` is being evaluated only as a non-scored candidate because it provides programmable physical attenuation in the conducted RF matrix. No protocol RAT switch is yet final.
- WP0 novelty/venue design: **PASS / LOCKED FOR CAMPAIGN DESIGN**.
- Primary venue-fit target: **Internet of Things (Elsevier)**; Computer Networks and Computer Communications retained as fit-dependent backups. Current Q1/indexing/APC status must be re-verified at submission.
- WP-PWD01 protocol: **v0.3 DESIGN FROZEN PENDING LIFECYCLE AND RF CALIBRATION**; scored runs remain unauthorized.
- Primary POWDER comparator: **B1 standard MQTT v3.1.1 QoS1 + automatic reconnect + volatile client state**, matched to W1 at the low-level transport.
- Frozen B1/W1 low-level session: `paho-mqtt==2.1.0`, QoS1, TLS scored path, `clean_session=False`, keepalive 60 s, reconnect 1–8 s, bounded outgoing queue 4096, max inflight 20. Only W1 adds application-level disk durability/reconciliation.
- Legacy local B0/B1/W1 semantics gate: **PASS — 9/9**. Extended pinned-Paho transport gate is being re-run and must supersede this line when 12/12 evidence is available.
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

1. Select and pass one executable controlled physical-RF profile with automated create -> READY -> manifest -> SSH -> fail-safe terminate.
2. Close the pinned-Paho local/remote transport gate and reproduce exact session settings in the runtime manifest.
3. Verify WellPulse telemetry traverses the experimental cellular data path, not the POWDER control network.
4. Run non-scored physical-RF calibration to freeze Q0–Q3 plus observed radio context.
5. Compute and freeze recovery horizon H.
6. Verify end-to-end evidence capture, clock alignment, and one-command primary-endpoint reconstruction.
7. Only then set `scored_runs_authorized: true`.
