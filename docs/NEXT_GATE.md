# Next Gate — STOPPED Before Golden

**Current frontier:** WP2-P5 HCI/raw-evidence closure complete / closed / STOPPED  
**Scientific completion:** 20%  
**WP2 management/readiness:** 80/100  
**K1–K8 compatibility:** `PASS / CLOSED`  
**Pre-integration compatibility:** `PASS`  
**AUDIT-R1:** `PASS`  
**Live HCI/raw-evidence gate:** `PASS / CLOSED`  
**Golden rebook authorization:** `false`  
**Scored authorization:** `false`

Canonical P5 closure:

`docs/WP2_P5_HCI_RAW_EVIDENCE_CLOSURE_2026-08-27.md`

Frozen HCI/raw contract:

`docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`

## WP2-P5 closure

The passive HCI and exact raw-evidence/finalization contract are now frozen and accepted offline:

1. `HCI_CONTROL_ACTIONS_ENABLED=false`;
2. HCI consumes orchestrator-owned state only and cannot issue independent POWDER probes or controls;
3. HCI failure is non-authoritative and cannot stop or invalidate scientific execution;
4. `orchestration/hci_events.jsonl` is conditional observer evidence, not mandatory scientific evidence;
5. exact mandatory scientific filenames/signals are frozen in Golden evidence inventory v1.5;
6. no background/in-run `/proj` checkpoint is enabled during protected science;
7. G9 persistent escrow occurs only after G8 reconstruction;
8. only controller artifact read-back plus outer/internal SHA-256 verification can emit `TEARDOWN_AUTHORIZED=YES`.

No POWDER contact, reservation, SSH, Golden, H calibration or scored B1/W1/B2 work occurred during P5.

## Exact next bounded patch — only after separate explicit user continuation

`WP2-P6 — ONE CLEAN NON-SCORED GOLDEN REHEARSAL`

It is **not started and not authorized by this file**.

When separately authorized, the shortest path is:

1. immediately before booking, inspect protocol v0.6.1 advisory POWDER resource information at `https://www.powderwireless.net/resinfo.php`;
2. record `RESOURCE_AVAILABILITY_PREFLIGHT=PASS|DEFER|UNKNOWN` without changing the frozen hardware/profile to chase capacity;
3. use Portal lifecycle/READY/manifest as authoritative;
4. book exactly one clean non-scored G0-G10 Golden rehearsal;
5. use the frozen passive HCI only;
6. reconstruct the run from raw evidence;
7. freeze/hash/copy to `/proj/WellPulse` after protected observation/reconstruction;
8. controller-pull and independently verify the GitHub Actions artifact round-trip;
9. require `EVIDENCE_ESCROW_GATE=PASS` and `TEARDOWN_AUTHORIZED=YES` before teardown;
10. STOP and decide WP2-P7 formal scientific closure/scored authorization separately.

## Frozen controls

- H1 remains `VALID_W1_RECOVERY_FAILURE`; original H1 raw bundles were not recovered.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; IDs `1 33 2 34` remain coupled.
- K1–K8 remain PASS/CLOSED absent a material interface change.
- `H_app=300 s from t_service_ready` is frozen.
- outcome-derived/W1-derived H recalibration is prohibited.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.
- no WP3 B1/W1/B2 scored execution is authorized.

Shortest path:

`AUDIT-R1 PASS -> WP2-P5 PASS -> STOP -> separate explicit resume -> resinfo advisory preflight -> one clean non-scored Golden -> WP2-P7 closure/scored authorization -> WP3 -> WP4 -> WP5`
