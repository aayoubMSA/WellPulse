# POWDER G5 — RF Calibration Scheduled State — 2026-08-26

**Evidence class:** NON-SCORED INFRASTRUCTURE / RF CALIBRATION SCHEDULING  
**Project:** `WellPulse`  
**Experiment:** `WP-G5-RF-CAL`  
**Profile:** `srslte-controlled-rf`  
**RefSpec:** `refs/heads/master (a6da9656)`  
**Scored scientific runs:** 0  
**`scored_runs_authorized`:** false

## Scheduled window

- Start: **2026-08-26 00:00 Africa/Cairo**
- End: **2026-08-26 03:00 Africa/Cairo**
- Reserved resources: `Emulab / nuc1 / 1`, `Emulab / nuc2 / 1`
- OTA Lab: none
- Separate frequency reservation: none
- Class reservation: No

## Purpose

G5 follows the successful G4 controlled-LTE lifecycle qualification. It is intended only to verify the actual RF-control/attenuation mechanism exposed by the current profile/runtime, observe available radio/link metrics, and non-scored-calibrate reproducible Q0-Q3 link states before any scored WellPulse campaign.

## Frozen execution boundary

1. Wait for `READY`; do not assume role-to-node bindings from G4.
2. Capture the live `enb1`/`rue1` bindings and SSH endpoints.
3. Reproduce the already-qualified LTE baseline only as needed: network side first, UE side second, attach, then bounded user-plane sanity.
4. Identify the actual RF-control mechanism from the current profile/runtime before issuing any attenuation command. Do not guess RF commands.
5. Record available radio/link observables and only then define candidate non-scored Q0-Q3 calibration points.
6. No B1/W1/B2 scored runs are authorized.
7. Preserve credential-free evidence and teardown manually with zero active usage.

## Evidence boundary

This scheduled state adds no scientific percentage. G5/WP2 remains non-scored calibration until repeatable RF states and their observable context are evidenced and frozen.
