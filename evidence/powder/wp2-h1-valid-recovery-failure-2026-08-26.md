# WP2-H1 W1 recovery calibration — Trial #1 valid recovery failure

Date: 2026-08-26
Experiment: WP-HCAL-E
Run ID: `wp2h1-a1-20260826-001`
Scored: false
Classification: `VALID_W1_RECOVERY_FAILURE`
Scientific consequence: H is not frozen; do not run replacement calibration trials under the frozen H-calibration rule. Scored runs remain unauthorized.

## Frozen trial schedule observed

- Q0 programmed on attenuator IDs `1 33 2 34` before readiness.
- Q3 programmed to 55 dB.
- Q3 full-state duration: 120.000117905 s.
- Q0 restored after Q3.
- Trial stopped after the frozen post-restore bound because backlog did not drain and H would exceed 300 s.

Key sender summary:

- cohort cutoff UTC: `2026-08-26T18:16:00.428045+00:00`
- cohort records: 211
- generated records: 361
- queue pending zero: null
- final pending count: 270
- app inflight: 20
- MQTT connected at final snapshot: false
- initial session present: false
- Q0 pre-readiness: 5/5 ping success over `tun_srsue`
- Q0 post-recovery health check: 0/3 ping success
- sender status: `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`
- sender rc: 20

## Failure diagnosis captured live

The UE process remained alive; `tun_srsue` remained UP with `172.16.0.2/24`, and the route to `172.16.0.1` still resolved through `tun_srsue`, but packets did not traverse after Q0 restoration.

The radio side itself recovered sufficiently for successful uplink decoding: the eNB remained alive and later logged PUSCH traffic with CRC OK and approximately 33 dB SNR. This rules out an eNB process crash and indicates physical/radio recovery occurred.

The EPC/MME/SPGW logs instead showed repeated attach/session-context churn after the outage:

- repeated attach requests for IMSI `001010123456789`
- `UE Context already exists`
- `Create Session Request being called for an UE with an active GTP-C connection`
- `Could not find GTP-C Tunnel info to delete`
- successive SPGW address allocations (`172.16.0.3`, `.4`, `.5`, `.6`, `.7`) while the UE tunnel interface remained at `172.16.0.2`
- UE-side attach/release/radio-link-failure loops

Interpretation: the observed non-recovery is dominated by post-outage LTE core/session-context/IP continuity failure in this srsLTE stack, not by MQTT or WellPulse durable-queue logic. The trial nevertheless remains a technically valid W1 recovery failure under the frozen protocol because the required user-plane recovery did not occur within the bound.

## Raw evidence preservation

The live raw evidence was copied from `/tmp` into the user's persistent POWDER home storage on both nodes and archived separately.

- nuc1 archive: `/users/aayoub/wellpulse-powder-evidence/wp2-h1-valid-failure-20260826/nuc1-wp2-h1-evidence.tar.gz`
  - SHA-256: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2 archive: `/users/aayoub/wellpulse-powder-evidence/wp2-h1-valid-failure-20260826/nuc2-wp2-h1-evidence.tar.gz`
  - SHA-256: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

Each node directory also contains a per-file `SHA256SUMS.txt` manifest. No secrets or private keys are intentionally included by this evidence step; the persistent bundle should be reviewed before any later public release.

## Decision

1. Preserve Trial #1; do not replace it.
2. Stop H calibration; H remains unfrozen.
3. Do not authorize scored B1/W1/B2 runs.
4. Use remaining live reservation time only for bounded diagnosis/recovery characterization and evidence preservation, not another H trial.
5. Before any future H-calibration attempt, define and validate a deterministic LTE recovery/re-attachment procedure that restores the intended UE user-plane identity/path without contaminating the scientific outage semantics.

No credentials or private keys are recorded in this evidence file.
