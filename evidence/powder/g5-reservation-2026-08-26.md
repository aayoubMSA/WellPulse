# POWDER G5 — RF Calibration Reservation — 2026-08-26

**Evidence class:** NON-SCORED INFRASTRUCTURE / CALIBRATION SCHEDULING  
**Project:** `WellPulse`  
**Gate:** G5 / WP2 RF impairment + measurement calibration — READY TO SCHEDULE EXPERIMENT  
**Scored scientific runs:** 0  
**`scored_runs_authorized`:** false

## Approved reservation

Portal shows the request as approved on 2026-08-25 at 23:33 local portal time.

Reserved resources:

- `Emulab / nuc1 / 1`
- `Emulab / nuc2 / 1`
- OTA Lab: none
- frequency reservation: none
- class reservation: No

Approved window:

- **Start:** 2026-08-26 00:00 Africa/Cairo
- **End:** 2026-08-26 03:00 Africa/Cairo

Reason entered:

> WellPulse G5 non-scored RF calibration following successful G4 controlled-LTE qualification. The session will verify programmable RF attenuation/control, observable radio metrics, and calibrate reproducible Q0-Q3 link states before any scored experiment.

## Execution boundary

Use the same proven `srslte-controlled-rf` profile semantics from G4. Do not score any run. Do not assume numeric Q0-Q3 attenuation values before live calibration. First restore the proven LTE lifecycle, then discover/verify the profile's available RF-control mechanism and measurable radio/link metrics. Freeze numeric Q0-Q3 values only after repeatable non-scored observations.

Keep the separately approved 2026-08-26 19:00–22:00 reservation as fallback until G5 calibration is either completed or intentionally deferred.
