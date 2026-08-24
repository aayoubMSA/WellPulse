# WellPulse — Milestone Status

Last updated: 2026-08-24 22:58 Africa/Cairo

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
G3 Simulated stack/data path        ░░░░░░░░░░░░░░░░░░░ NEXT
G4 Controlled physical-RF lifecycle ░░░░░░░░░░░░░░░░░░░ PENDING
G5 RF impairment plumbing           ░░░░░░░░░░░░░░░░░░░ PENDING
```

G0–G2 are enabling infrastructure and do **not** add scientific WP percentage. G3 is also an enabling infrastructure gate and receives no scientific percentage when it passes.

Canonical G1/G2 evidence:

- `evidence/powder/manual-golden-path-2026-08-24.md`
- `powder/MANUAL_GOLDEN_PATH.md`

Accepted reference allocation:

- experiment UUID `0dc233d7-44a0-4e6c-9734-6d4c8ea0e2ad`;
- profile `srsLTE-SIM:9`;
- d430 node `pc734`;
- explicit Golden-key SSH PASS;
- manual teardown PASS;
- portal returned to zero active node usage.

## Time remaining

From the current milestone to a paper-ready POWDER package, planning estimate:

- **active hands-on work:** ~28–50 hours;
- **best case:** ~3–4 intensive working days if compatible resources are immediately available;
- **realistic elapsed:** ~5–8 calendar days;
- **resource-constrained:** ~1–2 weeks if controlled-RF/OTA resources require waiting.

These are planning estimates rather than commitments. The main elapsed-time uncertainty is live compatible controlled-RF and OTA availability.

## Critical path

```text
G3 simulated stack/data path
        ↓ ~1–2 h
current controlled-RF profile + manual lifecycle
        ↓ ~2–6 h, availability-dependent
WP2 calibration + freeze Q0–Q3 and H
        ↓ ~4–8 h
WP3 24–36 conducted scored runs
        ↓ ~6–10 h
WP4 12 OTA replication runs
        ↓ ~3–6 h
WP5 deterministic analysis + artifact + manuscript closure
          ~12–20 h
```

## Current exact next gate

**G3 — Simulated stack/data-path validation.**

Non-scored; no SDR; no RF; no scientific claim.

Approved execution mode: **manual resource creation + automated attach/test/evidence/teardown**.

1. Confirm the live POWDER portal shows `Current Usage: 0 Node Hours`.
2. Instantiate a fresh `srsLTE-SIM:9` experiment manually under project `WellPulse`, using one `d430` and a distinct name beginning `WP-G3-SIMSTACK`.
3. Wait for `State: ready` and copy the experiment UUID. No historical hostname is needed.
4. Run GitHub Action **POWDER G3 Attach to Manual Experiment** from `.github/workflows/powder-g3-attach.yml`, supplying that UUID and typing `G3ATTACH`.
5. Before test execution or automated teardown, the workflow must verify:
   - profile UUID `80dda605-7e5f-11e9-8006-e4434b2381fc`;
   - hardware `d430`;
   - image `PowderProfiles:gnuradio-srslte`;
   - project/name when exposed by the Portal API.
6. The workflow obtains the active SSH endpoint from the current manifest, uses the registered automation SSH identity, and executes only the profile-authoritative file-based `pdsch_enodeb -> waveform file -> pdsch_ue` example.
7. It retains credential-free stdout/stderr, exit codes, remote metadata, waveform byte count and SHA-256; the temporary waveform is removed.
8. It fail-safe terminates only after target identity validation and polls until the experiment is absent or terminal.
9. G3 PASS requires `PROCESS_GATE=PASS` and `cleanup=PASS` and produces sanitized evidence under `evidence/powder/g3/` plus `evidence/powder/g3-simstack-latest.md`.

The existing full resource-creating workflow `.github/workflows/powder-g3-simstack.yml` remains **FROZEN / UNAPPROVED / DO NOT RUN** until the equivalent G3 manual layer has passed and the canonical handover explicitly changes that authorization state.

After G3 PASS, discover and verify a **current** controlled physical-RF profile through the live POWDER UI. Do not retry `srs-rf-matrix` unchanged because the prior attempt exposed an unusable `n310` requirement, and do not promote remembered `srsran-handover` assumptions into current state.

## Scientific authorization state

`scored_runs_authorized = false`.

No POWDER run currently belongs to the scored scientific corpus.

## Evidence boundary

Current POWDER G0–G2 evidence proves project access, d430 provisioning, SSH-key injection/authentication, remote metadata capture and clean teardown. A future G3 PASS will add only evidence that the profile-authoritative file-based simulated stack/data path executes correctly on POWDER compute. It still will not prove LTE/5G over physical RF, SDR operation, attenuation control, OTA behavior, WellPulse/MQTT resilience, field performance, hydraulics, groundwater or agronomic outcomes.
