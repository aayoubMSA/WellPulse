# POWDER G4 — Continuation Reservation — 2026-08-26

**Evidence class:** NON-SCORED INFRASTRUCTURE QUALIFICATION / SCHEDULING STATE  
**Project:** `WellPulse`  
**Gate:** G4 controlled physical-RF lifecycle — IN PROGRESS  
**Scored scientific runs:** 0  
**`scored_runs_authorized`:** false

## Why a continuation window is required

The 2026-08-25 `WP-G4-CTRL-RF` session successfully reached the profile-authoritative EPC/eNodeB live-start checkpoint on `nuc1`, including EPC/eNB S1 setup exchange and B210 RF initialization. The session window then expired before `nuc2` UE startup/attach and LTE user-plane validation were completed.

This is **not a scientific FAIL**. It is an incomplete non-scored G4 lifecycle qualification caused by the reservation-window boundary.

## Approved continuation reservation

POWDER reservation request was submitted and immediately shown as approved on 2026-08-25 at 22:10 local portal time.

Reserved resources:

- `Emulab / nuc1 / 1`
- `Emulab / nuc2 / 1`
- OTA Lab: none
- frequency reservation: none
- class reservation: No

Approved continuation window:

- **Start:** 2026-08-26 19:00 Africa/Cairo
- **End:** 2026-08-26 22:00 Africa/Cairo

Reservation reason recorded in the portal:

> Continuation of an approved WellPulse controlled-RF qualification experiment using the srslte-controlled-rf profile. The previous session successfully validated EPC/eNodeB startup and B210 operation; this reservation is required to complete the non-scored UE attach and LTE user-plane qualification.

## Frozen continuation boundary

Do not repeat discovery, comparator science, or scored runs. The shortest valid continuation path is:

1. use the approved `nuc1`/`nuc2` window;
2. restore/instantiate the same `srslte-controlled-rf` G4 lifecycle without changing profile semantics;
3. verify both actual live SSH endpoints with the canonical explicit Golden key;
4. launch the profile-authoritative startup on `nuc1` and confirm EPC/eNB live state;
5. launch the profile-authoritative `srsue` path on `nuc2`;
6. verify UE attach/authentication/bearer establishment;
7. verify LTE user-plane connectivity through the experimental path, not the POWDER control network;
8. preserve credential-free raw evidence and concise provenance;
9. teardown manually and verify zero active usage;
10. only then classify G4 PASS/FAIL.

## Evidence boundary

This reservation changes **operational readiness only**. It adds no scientific percentage and authorizes no scored campaign. G4 remains **IN PROGRESS** until UE attach and user-plane qualification are evidenced.
