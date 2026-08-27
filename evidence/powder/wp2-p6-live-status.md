# WP2-P6 Live Status — FINAL

This file supersedes the intermediate Attempt-1 `FAIL_CLOSED` status that was written before same-reservation recovery and evidence salvage completed.

## Final P6 state

- WP2-P6 verdict: **PASS_RECOVERED_SINGLE_RUN**
- Experiment ID: `5579cf25-dbb1-4d04-87e3-ff558e3be2af`
- Experiment name: `wpg7498036`
- Scientific Golden run ID: `wp2-p6r-33099648133-20260827T174149Z`
- Original P6 source SHA: `bd1b5e12f3d2eca27ec81ccadbeec5afaa2f2159`
- Scored run: **NO**
- Scientific rerun: **NO**
- Second reservation: **NO**
- Raw evidence complete: **PASS**
- Evidence escrow gate: **PASS**
- Controller off-POWDER verification: **PASS**
- Teardown authorized: **YES**
- Teardown confirmed: **YES**
- Finalization workflow run: `33101564419`
- Persistent evidence path: `/proj/WellPulse/evidence-escrow/5579cf25-dbb1-4d04-87e3-ff558e3be2af/wp2-p6r-33099648133-20260827T174149Z`
- Deterministic TAR SHA-256: `ff72a50fd11db1d308f4049b49fffa317c8220c9290845434dbadc8dbef847cf`
- GitHub artifact ID: `9658678808`
- Artifact name: `wp2-p6-final-33101564419`
- Teardown confirmed UTC: `2026-08-27T18:04:31Z`

## Scientific reconstruction

- `t_rf_restore`: `2026-08-27T17:45:06.913285Z`
- `t_service_ready`: `2026-08-27T17:45:32.001525Z`
- `T_service`: `25.088240 s`
- `t_app_complete`: `2026-08-27T17:45:37.295360Z`
- `T_app`: `5.293835 s`
- `T_total`: `30.382075 s`
- Primary cohort: `181`
- Valid by 300 s horizon: `181/181`
- `completeness_300`: `1.0`
- Missing/checksum mismatch/duplicate/late primary-cohort records: `0/0/0/0`

The earlier reconstruction field `unexpected_attempts=325` is not used as a scientific defect: P7 established that it conflated intentionally generated post-cohort traffic with truly unknown record identities. The reusable reconstruction code now separates those classes without changing the primary cohort or endpoint.

Canonical detailed authority: `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`.
