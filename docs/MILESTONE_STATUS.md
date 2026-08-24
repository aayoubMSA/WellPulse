# WellPulse — Milestone Status

Last updated: 2026-08-24 23:56 Africa/Cairo

This file is the canonical compact dashboard for scientific WP completion, infrastructure gates, critical path, and planning time remaining.

## Scientific work packages

| WP | Scope | Weight | Progress | Status | Remaining active-work estimate |
|---|---|---:|---:|---|---:|
| WP0 | Novelty & Venue Lock | 8% | 100% | PASS | 0 h |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 100% | PASS | 0 h |
| WP2 | RF Calibration & Measurement Validation | 15% | 0% | NEXT | ~4–8 h |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0% | BLOCKED BY WP2 | ~6–10 h |
| WP4 | OTA External Replication | 15% | 0% | BLOCKED BY WP3 | ~3–6 h |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0% scientific closure | PREPARED, NOT EXECUTED | ~12–20 h |

Scientific weighted completion: **20%**.

```text
WP0  ████████████████████  8/8
WP1  ████████████████████ 12/12
WP2  ░░░░░░░░░░░░░░░░░░░  0/15
WP3  ░░░░░░░░░░░░░░░░░░░  0/30
WP4  ░░░░░░░░░░░░░░░░░░░  0/15
WP5  ░░░░░░░░░░░░░░░░░░░  0/20

OVERALL  ████░░░░░░░░░░░░░░░░  20%
```

WP5 already has substantial scaffolding prepared — analysis plan, evidence schema, deterministic endpoint logic, randomization and run matrix — but none of that is counted as completed WP5 scientific closure before real POWDER evidence exists.

## POWDER infrastructure gates

```text
G0 Account + WellPulse project      ████████████████████ PASS
G1 Manual compute provisioning      ████████████████████ PASS
G2 Explicit-key SSH + teardown      ████████████████████ PASS
G3 Simulated stack/data path        ████████████████████ PASS
G4 Controlled physical-RF lifecycle ░░░░░░░░░░░░░░░░░░░ NEXT
G5 RF impairment plumbing           ░░░░░░░░░░░░░░░░░░░ PENDING
```

G0–G3 are enabling infrastructure gates and do **not** add scientific WP percentage.

Canonical G1/G2 evidence:

- `evidence/powder/manual-golden-path-2026-08-24.md`
- `powder/MANUAL_GOLDEN_PATH.md`

Canonical G3 evidence:

- `evidence/powder/g3-simstack-2026-08-24.md`
- experiment `WP-G3-SIMSTACK`
- UUID `3484b01d-7eca-48e7-9e34-866680057b0d`
- profile `srsLTE-SIM:9`
- one `d430`, live node `pc757`
- manual explicit-key SSH PASS
- `pdsch_enodeb -> IQ file -> pdsch_ue` PASS
- `RX_RC=0`
- waveform bytes `2304000`
- waveform SHA-256 `103de59d52e75252e916d7ed62c5c9b76401e817ffec3178363879e0bed71678`
- temporary waveform cleanup PASS
- portal teardown PASS; `Current Usage: 0 Node Hours`

G3 evidence is non-scored, no-SDR, no-RF infrastructure evidence only.

## Time remaining

From the current milestone to a paper-ready POWDER package, planning estimate:

- **active hands-on work:** ~27–48 hours;
- **best case:** ~3–4 intensive working days if compatible resources are immediately available;
- **realistic elapsed:** ~5–8 calendar days;
- **resource-constrained:** ~1–2 weeks if controlled-RF/OTA resources require waiting.

These are planning estimates rather than commitments. The main elapsed-time uncertainty is live compatible controlled-RF and OTA availability.

## Critical path

```text
G4 current controlled-RF profile + manual lifecycle
        ↓ ~2–6 h, availability-dependent
G5 / WP2 calibration + freeze Q0–Q3 and H
        ↓ ~4–8 h
WP3 24–36 conducted scored runs
        ↓ ~6–10 h
WP4 12 OTA replication runs
        ↓ ~3–6 h
WP5 deterministic analysis + artifact + manuscript closure
          ~12–20 h
```

## Current exact next gate

**G4 — Controlled physical-RF lifecycle discovery and qualification.**

Non-scored; no scientific corpus entry; manual-first.

1. Use the live authenticated POWDER UI to discover current controlled physical-RF example/profile candidates.
2. Verify the exact current profile name, owner/project, revision, requested hardware/radio resources and WellPulse entitlement/availability before provisioning.
3. Do not reuse stale `srsran-handover` assumptions.
4. Do not resubmit the blocked `srs-rf-matrix` topology unchanged; its prior `n310` requirement was incompatible with WellPulse entitlement.
5. Select the smallest current profile that can prove a controlled physical-RF lifecycle relevant to the scientific design.
6. Manually qualify one lifecycle first: provision -> READY -> inspect manifest/resource bindings -> explicit-key SSH -> clean terminate -> verify zero active usage.
7. Only after a valid G4 lifecycle may the project establish the real experimental user-plane and proceed into G5/WP2 calibration.

Resource-creating automation remains **FROZEN by owner mandate**. G3 PASS does not by itself authorize automatic resource creation for G4 or scored runs.

## Automation troubleshooting note

The attach-only G3 GitHub Actions path remains untrusted for execution until its SSH credential is repaired. Sanitized diagnosis established that repository secret `POWDER_SSH_PRIVATE_KEY` contains a public key rather than an usable private key. Earlier CI attempts failed before target validation; they did not execute G3 or terminate the experiment. The accepted G3 evidence is the manual run recorded above.

## Scientific authorization state

`scored_runs_authorized = false`.

No POWDER run currently belongs to the scored scientific corpus.

## Evidence boundary

Current POWDER G0–G3 evidence proves project access, d430 provisioning, explicit-key SSH, remote metadata capture, the profile-authoritative file-based simulated LTE stack/data path, temporary-artifact cleanup and clean teardown. It does **not** prove LTE/5G over physical RF, SDR operation, attenuation control, OTA behavior, WellPulse/MQTT resilience, field performance, hydraulics, groundwater or agronomic outcomes.