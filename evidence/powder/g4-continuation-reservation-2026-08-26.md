# POWDER G4 — Continuation Reservation — 2026-08-26

**Evidence class:** NON-SCORED INFRASTRUCTURE QUALIFICATION / SCHEDULING STATE  
**Project:** `WellPulse`  
**Gate:** G4 controlled physical-RF lifecycle — IN PROGRESS  
**Scored scientific runs:** 0  
**`scored_runs_authorized`:** false

## Why a continuation window is required

The 2026-08-25 `WP-G4-CTRL-RF` session successfully reached the profile-authoritative EPC/eNodeB live-start checkpoint on `nuc1`, including EPC/eNB S1 setup exchange and B210 RF initialization. The session window then expired before `nuc2` UE startup/attach and LTE user-plane validation were completed.

This is **not a scientific FAIL**. It is an incomplete non-scored G4 lifecycle qualification caused by the reservation-window boundary.

## Approved continuation reservations

### Immediate late window — primary next attempt

A second WellPulse reservation was approved on 2026-08-25 at approximately 22:22 Africa/Cairo for:

- `Emulab / nuc1 / 1`
- `Emulab / nuc2 / 1`
- OTA Lab: none
- frequency reservation: none
- class reservation: No
- **Start:** 2026-08-25 23:00 Africa/Cairo
- **End:** 2026-08-26 00:00 Africa/Cairo

A rerun of the same experiment was then scheduled successfully:

- experiment name: `WP-G4-CTRL-RF`
- profile: `srslte-controlled-rf`
- profile repo/ref: `a6da9656`, `refs/heads/master`
- state after scheduling: `scheduled`
- scheduled start: **2026-08-25 23:00 Africa/Cairo**
- expiry: **2026-08-26 00:00 Africa/Cairo**

This one-hour window is the primary immediate attempt. Do not spend it repeating discovery or comparator work.

### Fallback reservation — preserved

The earlier approved fallback reservation remains available:

- `Emulab / nuc1 / 1`
- `Emulab / nuc2 / 1`
- OTA Lab: none
- frequency reservation: none
- class reservation: No
- **Start:** 2026-08-26 19:00 Africa/Cairo
- **End:** 2026-08-26 22:00 Africa/Cairo

Reservation reason recorded in the portal:

> Continuation of an approved WellPulse controlled-RF qualification experiment using the srslte-controlled-rf profile. The previous session successfully validated EPC/eNodeB startup and B210 operation; this reservation is required to complete the non-scored UE attach and LTE user-plane qualification.

## Frozen continuation boundary

Do not repeat discovery, comparator science, or scored runs. The shortest valid continuation path is:

1. wait for the scheduled experiment to reach `READY`;
2. verify both actual live SSH endpoints with the canonical explicit Golden key;
3. launch the profile-authoritative startup on `nuc1` and confirm EPC/eNB live state;
4. launch the profile-authoritative `srsue` path on `nuc2`;
5. verify UE attach/authentication/bearer establishment;
6. verify LTE user-plane connectivity through the experimental path, not the POWDER control network;
7. preserve credential-free raw evidence and concise provenance;
8. teardown manually and verify zero active usage;
9. only then classify G4 PASS/FAIL.

If the 23:00–00:00 window is insufficient, stop cleanly and resume in the approved 19:00–22:00 fallback window. Do not convert time pressure into weaker evidence or scored execution.

## Evidence boundary

These reservations change **operational readiness only**. They add no scientific percentage and authorize no scored campaign. G4 remains **IN PROGRESS** until UE attach and user-plane qualification are evidenced.
