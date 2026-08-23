# WP-RT01 Final FIT IoT-LAB Results — 2026-08-23

## Status

**FINAL FIT GATE: PASS**

- Evidence class: `FINAL_WP_RT01_FIT_A8`
- GitHub Actions run: `32628193889`
- Executed checkout SHA: `e257d22e1e6589b3e28ca2f2c14d3fab2ba2e483`
- Frozen workflow base commit: `fd5f07b947d44d2b03364a586cc1ac80aed5e070`
- Operational trigger head: `a099e31b2bc3673761b25a8f266bdc2c35a1b081`
- Platform: FIT IoT-LAB
- Site: Grenoble
- Hardware: A8-100
- Matrix: B0/W1 × C0/C1/C2 × 3 replicates = **18 cells**
- Records per cell: exactly **10,000**
- Reconciliation: **18/18 PASS**

## Frozen semantics

- `B0`: publish-only / non-durable baseline.
- `W1`: WellPulse durable offline-first queue + reconciliation.
- `C0`: normal connectivity, no restart.
- `C1`: deterministic broker outage, no restart.
- `C2`: deterministic broker outage + WellPulse gateway-process exec restart after record 4000.
- Outage for C1/C2: `iptables REJECT` broker TCP/8883 during records 3001–5000.
- C2 is **not** a whole-node or hardware reboot.

## Final 18-cell reconciliation

| Rep | Arch | Cond | Generated | Cloud unique | Missing | Duplicates | Completeness | Reconnect s | Backlog drain s | Restart count |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | B0 | C0 | 10000 | 10000 | 0 | 0 | 100% | — | — | 0 |
| 1 | B0 | C1 | 10000 | 8000 | 2000 | 0 | 80% | 1.307214 | — | 0 |
| 1 | B0 | C2 | 10000 | 8000 | 2000 | 0 | 80% | 1.329756 | — | 1 |
| 1 | W1 | C0 | 10000 | 10000 | 0 | 0 | 100% | — | — | 0 |
| 1 | W1 | C1 | 10000 | 10000 | 0 | 0 | 100% | 1.309382 | 67.596918 | 0 |
| 1 | W1 | C2 | 10000 | 10000 | 0 | 0 | 100% | 1.377100 | 67.320791 | 1 |
| 2 | B0 | C0 | 10000 | 10000 | 0 | 0 | 100% | — | — | 0 |
| 2 | B0 | C1 | 10000 | 8000 | 2000 | 0 | 80% | 1.306527 | — | 0 |
| 2 | B0 | C2 | 10000 | 8000 | 2000 | 0 | 80% | 1.380250 | — | 1 |
| 2 | W1 | C0 | 10000 | 10000 | 0 | 0 | 100% | — | — | 0 |
| 2 | W1 | C1 | 10000 | 10000 | 0 | 0 | 100% | 1.331298 | 68.047688 | 0 |
| 2 | W1 | C2 | 10000 | 10000 | 0 | 0 | 100% | 1.329536 | 68.851579 | 1 |
| 3 | B0 | C0 | 10000 | 10000 | 0 | 0 | 100% | — | — | 0 |
| 3 | B0 | C1 | 10000 | 8000 | 2000 | 0 | 80% | 1.362495 | — | 0 |
| 3 | B0 | C2 | 10000 | 8000 | 2000 | 0 | 80% | 1.376358 | — | 1 |
| 3 | W1 | C0 | 10000 | 10000 | 0 | 0 | 100% | — | — | 0 |
| 3 | W1 | C1 | 10000 | 10000 | 0 | 0 | 100% | 1.310584 | 67.549132 | 0 |
| 3 | W1 | C2 | 10000 | 10000 | 0 | 0 | 100% | 1.327973 | 67.438386 | 1 |

## Aggregate observations

Across all three replicates:

- B0/C0: 100% completeness in 3/3 replicates.
- B0/C1: exactly 80% completeness and exactly 2,000 permanent missing records in 3/3 replicates.
- B0/C2: exactly 80% completeness and exactly 2,000 permanent missing records in 3/3 replicates.
- W1/C0: 100% completeness, zero missing, zero duplicates in 3/3 replicates.
- W1/C1: 100% completeness, zero missing, zero duplicates in 3/3 replicates.
- W1/C2: 100% completeness, zero missing, zero duplicates in 3/3 replicates with one gateway-process exec restart per replicate.
- W1/C1 reconnect mean: **1.317088 s**; backlog-drain mean: **67.731246 s**.
- W1/C2 reconnect mean: **1.344870 s**; backlog-drain mean: **67.870252 s**.
- Latency p50/p95/p99 were **not instrumented** in this final workflow and must not be claimed from WP-RT01.

## H1 evaluation

H1 required at least 98% record preservation in the controlled 10,000-record outage/restart test, with zero permanent loss and zero duplicate final records.

**Result: H1 is supported for the controlled FIT IoT-LAB experiment.**

In W1/C2, all three final replicates produced 10,000 generated records and 10,000 unique final cloud records, with zero permanent missing records and zero final duplicates. The observed final completeness was 100% in 3/3 replicates.

A precise evidence-supported claim is:

> Under a controlled 10,000-record broker outage and gateway-process restart on FIT IoT-LAB A8 hardware, the WellPulse durable architecture achieved 100% final record completeness with zero permanent loss and zero duplicates in 3/3 replicates, while the non-durable baseline retained 80%.

## Evidence boundary

These results validate the **communications / durable buffering / restart recovery / edge-to-cloud reconciliation layer on real embedded hardware under controlled connectivity impairment**.

They do **not** establish:

- Siwa field performance;
- pump mechanical condition or faults;
- hydraulic performance;
- groundwater behavior;
- motor/bearing diagnostics;
- agronomic or crop outcomes;
- general rural-radio performance outside the controlled FIT setup.

Any manuscript or presentation must preserve this boundary.

## Final artifacts

| Replicate | FIT experiment | GitHub artifact | Artifact ZIP SHA-256 | Durable Drive archive ID |
|---:|---:|---:|---|---|
| 1 | 448265 | 9490962516 | `1c18a5e93597607765fbd05ebb7d81554d31735b8644eccf613e2d5162423d55` | `14SMrvpmFgX7J2eHIkBuUkEcCwI19c5Nl` |
| 2 | 448266 | 9491634827 | `cf25bdcd4684b6be2d6e5b328776a5704f85a520068c5fe6ace4121c909a0fe7` | `1Bi8zr7lO6UKn5BSoMrjQhoTcXIL5UtIX` |
| 3 | 448269 | 9492286379 | `ef92f4c3cce6e3824669b7771a35ae8c2374275ef4e1b4937c69c79ef47ac3c8` | `1Y1bBgs0iclyXeKsDr4tTI-ZcQEqr3EaO` |

The Drive `WP-RT01_Run_Register_v1.0` contains all 18 final rows and is the canonical structured run ledger.

## Pre-final separation

The successful Grenoble pre-final dry run remains separate evidence class `PREFINAL_REAL_A8_DRY_RUN_NOT_FINAL_EXPERIMENT` and is **not pooled into the final matrix**.

## Next scientific layer

The highest-value next remote-testbed layer is outdoor/rural-network validation (ARA Wireless Living Lab or a defensible alternative) to test the broader claim of resilient remote monitoring under intermittent rural connectivity. This next layer still cannot substitute for eventual pump/hydraulic/Siwa field validation.
