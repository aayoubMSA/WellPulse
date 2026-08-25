# WP-PWD01 — RF Calibration Freeze v1

**Date:** 2026-08-26  
**Scope:** Conducted POWDER `srslte-controlled-rf` campaign only  
**Status:** FROZEN FOR REMAINING PRE-SCORE VALIDATION; scored runs are still NOT authorized.

This file is the post-calibration freeze artifact for the `Radio states` section of `experiments/WP-PWD01/protocol.md` v0.4. It does not alter the research questions, comparator design, scenario timing, endpoints, replication rule, or technical-invalidity rule.

## Frozen profile/path identity
- Profile: `srslte-controlled-rf`
- Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- eNB/EPC: `enb1 -> nuc1`
- UE: `rue1 -> nuc2`
- RF path attenuation IDs changed together: `1 33 2 34`

## Frozen semantic radio states

| State | Programmed additional attenuation | Frozen meaning |
|---|---:|---|
| `Q0` | `0 dB` | strong/stable reference |
| `Q1` | `40 dB` | degraded but continuously connected |
| `Q2` | `52 dB` | near-threshold/intermittent operating point |
| `Q3` | `55 dB` | effective application-data outage |

Representative calibration observations:
- Q0: RSRP about -60 dBm, DL SNR about 40-45 dB, 0% user-plane loss in the formal baseline.
- Q1: RSRP about -100 dBm, DL SNR about 18-19 dB, continuous user-plane delivery in the valid +40 stage.
- Q2: clean isolated +52 dB window produced 6 replies / 12 misses over about 20 s, followed by a clean Q0 3/3 recovery check.
- Q3: valid isolated +55 dB stage produced essentially a full 20 s application-data outage, with delivery resuming after Q0 restoration.

## Mandatory technical readiness rule learned during calibration
Before accepting any RF stage or scored run as technically valid:

1. Restore `Q0 = 0 dB` on all four attenuation IDs.
2. Verify end-to-end user-plane health through the experimental LTE path.
3. If Q0 user-plane health fails, the subsequent RF classification/run is technically invalid until the bearer is cleanly restored.
4. Attach state or possession of a UE IP address alone is not sufficient evidence of user-plane readiness.

This rule operationalizes the existing protocol's technical-invalidity principle and prevents stale-bearer contamination from being misclassified as RF impairment.

## Evidence source
Canonical calibration ledger:
`evidence/powder/g5-rf-calibration-ledger-2026-08-26.md`

The ledger contains the exact timestamps, clean boundary tests, representative radio observations, valid evidence commits, and the list of stale-bearer-contaminated trials excluded from RF-state inference.

## Remaining gates
The RF numeric-calibration requirement is closed. `scored_runs_authorized` remains false until the other pre-score requirements in the canonical protocol are satisfied, including H freeze, B1/W1 matched implementation audit, evidence/clock validation, and non-scored analysis reconstruction.
