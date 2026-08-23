# WellPulse — Current Handover

Last updated: 2026-08-23 16:10 Africa/Cairo

## Standing handover rule
No material project state may exist only in chat. Before leaving this workstream, ensure decisions, results, artifacts, blockers, evidence boundaries, and the exact next action are recoverable from Drive and/or GitHub.

## Project status
WellPulse has completed its first publication-grade remote-testbed validation layer on FIT IoT-LAB and now has three parallel access/qualification lanes for the next scientific layer. Parallelize access gates, not redundant final experiments.

### WP-RT01 — FIT IoT-LAB
Status: COMPLETE / FINAL EVIDENCE PASS

Canonical result file:
- `experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md`

Key facts:
- Evidence class: `FINAL_WP_RT01_FIT_A8`
- GitHub Actions run: `32628193889`
- Platform/site/node: FIT IoT-LAB / Grenoble / A8-100
- Matrix: B0/W1 × C0/C1/C2 × 3 replicates = 18 final cells
- Records per cell: exactly 10,000
- Reconciliation: 18/18 PASS
- W1/C1: 100% completeness, zero missing, zero duplicates in 3/3 replicates
- W1/C2: 100% completeness, zero missing, zero duplicates in 3/3 replicates
- B0/C1 and B0/C2: exactly 80% completeness and 2,000 permanent missing records in 3/3 replicates
- W1/C1 reconnect mean: 1.317088 s; backlog-drain mean: 67.731246 s
- W1/C2 reconnect mean: 1.344870 s; backlog-drain mean: 67.870252 s
- C2 was a gateway-process exec restart after record 4000, not a hardware reboot
- Latency p50/p95/p99 were not instrumented and must not be claimed

Evidence-supported claim:
> Under a controlled 10,000-record broker outage and gateway-process restart on FIT IoT-LAB A8 hardware, the WellPulse durable architecture achieved 100% final record completeness with zero permanent loss and zero duplicates in 3/3 replicates, while the non-durable baseline retained 80%.

Evidence boundary:
This validates communications, durable buffering, restart recovery, and edge-to-cloud reconciliation on real embedded hardware under controlled connectivity impairment. It does not validate Siwa field performance, pump mechanics, hydraulics, groundwater, inverter/Modbus physical hardware, bearing/motor faults, or agronomic outcomes.

Final evidence artifacts:
- Replicate 1: FIT exp 448265; GitHub artifact 9490962516; SHA-256 `1c18a5e93597607765fbd05ebb7d81554d31735b8644eccf613e2d5162423d55`; Drive archive ID `14SMrvpmFgX7J2eHIkBuUkEcCwI19c5Nl`
- Replicate 2: FIT exp 448266; GitHub artifact 9491634827; SHA-256 `cf25bdcd4684b6be2d6e5b328776a5704f85a520068c5fe6ace4121c909a0fe7`; Drive archive ID `1Bi8zr7lO6UKn5BSoMrjQhoTcXIL5UtIX`
- Replicate 3: FIT exp 448269; GitHub artifact 9492286379; SHA-256 `ef92f4c3cce6e3824669b7771a35ae8c2374275ef4e1b4937c69c79ef47ac3c8`; Drive archive ID `1Y1bBgs0iclyXeKsDr4tTI-ZcQEqr3EaO`

Drive structured run ledger:
- `WP-RT01_Run_Register_v1.0`
- Spreadsheet ID: `1stmgZaWLGfavftgmzLyGW3S9Sefiiiy6QTtOB9AkBe0`
- Contains all 18 final rows marked COMPLETE

Closed audit trail:
- FIT readiness Issue #1: closed/completed
- Trigger PRs #16, #17, #20, #21: closed unmerged

### WP-RT02 — ARA rural OTA
Status: QUALIFIED / ACCESS GATE

Canonical protocol:
- `experiments/WP-RT02/ARA_QUALIFICATION_2026-08-23.md`

Tracking:
- GitHub Issue #22 — open

Purpose:
Add a real rural outdoor OTA layer with COTS 5G first. Required evidence is timestamped radio state plus application evidence. Do not substitute application-layer blocking for RF/OTA impairment.

Current state:
- ARA remains the preferred rural confirmation layer
- No ARA account/project approval has yet been recorded in this repository
- No ARA experiment has been reserved or executed

### WP-RT03 — POWDER controlled real-RF
Status: ACCESS / PROJECT APPROVAL GATE

Canonical protocol:
- `experiments/WP-RT03/POWDER_QUALIFICATION_2026-08-23.md`

Tracking:
- GitHub Issue #23 — open

Preferred first path:
- POWDER `srs-rf-matrix`
- P0 stable reference RF
- P1 degraded-but-connected RF via controlled attenuation
- P2 RF-induced connectivity loss then restoration/recovery
- Reuse the 10,000-record WellPulse workload where technically compatible
- RF state must be synchronized with application evidence
- No iptables/application-layer outage may substitute for RF impairment

Current access evidence:
- Mailbox evidence shows POWDER account creation was initiated
- A WellPulse SSH public key was accepted by Emulab infrastructure
- No project/account approval message has yet been found
- Do not create a duplicate POWDER/Emulab account
- No POWDER experiment has been reserved or executed

### WP-RT04 — COSMOS/ORBIT controlled-RF fallback
Status: GO FOR ACCESS QUALIFICATION / NO EXTERNAL ACTION YET

Canonical alternative scan:
- `experiments/ALT_SCAN/ALTERNATIVE_TESTBEDS_2026-08-23.md`
- Commit introducing scan: `01f7ab02eb61e6ad5fe1d63ef297d034d84f4481`

Tracking:
- GitHub Issue #24 — open

Why this lane exists:
- current COSMOS/ORBIT scheduler exposes `sb4.orbit-lab.org` RF Attenuator Matrix for repeatable RF/topology control;
- `outdoor.orbit-lab.org` provides an approximately 22-node outdoor wireless domain;
- COSMOS supports remote reservations and SSH/VPN experiment access;
- COSMOS Sandbox 1 has a current 5G NR OTA path with end-to-end IP traffic through a real gNB↔UE air link;
- portal documentation states account activation plus group-PI approval typically takes a day or two.

Preferred role:
- first use ORBIT SB4 as a substitute/fallback for POWDER controlled RF;
- only use ORBIT outdoor or COSMOS 5G OTA if it adds a distinct material claim;
- do not run a redundant final matrix merely because both POWDER and COSMOS become available.

Current state:
- no COSMOS/ORBIT account/project/reservation action has been taken in this workstream;
- external registration/reservation requires owner approval.

### AERPAW — secondary outdoor/mobile candidate
Status: QUALIFIED CANDIDATE / HOLD UNTIL NEEDED

The 2026 scan confirms AERPAW is active and supports real outdoor 4G/5G, SDR, LoRa and autonomous ground/aerial vehicles, with external-user portal/tutorial infrastructure and current real-world outdoor experiments.

Potential role:
- outdoor/mobile wireless resilience under motion/interference if a mobility/environment claim materially strengthens the paper.

Reason to hold:
- greater operational/field coordination;
- UAV/autonomy is unnecessary for WellPulse;
- do not let the platform pull the research into unrelated autonomy/6G work.

### Other scanned alternatives
- NITOS: HOLD — real SDR/LTE/Wi-Fi and isolated indoor hardware exist, but onboarding clarity/incremental claim value are weaker than COSMOS/ORBIT.
- Colosseum: HOLD — valuable massive RF channel emulator with SDR hardware, but not a physical-environment substitute for outdoor OTA; use only if repeatable channel scale becomes a specific manuscript requirement.

## Current validation ladder
1. FIT WP-RT01 — COMPLETE: real embedded hardware + controlled transport/connectivity outage.
2. POWDER WP-RT03 — pending access: preferred controlled real-RF impairment/recovery.
3. COSMOS/ORBIT WP-RT04 — third access lane and controlled-RF fallback; optional outdoor/5G OTA if distinct.
4. ARA WP-RT02 — pending access: strongest rural outdoor OTA confirmation.
5. AERPAW — hold for a distinct outdoor/mobile claim only.
6. Actual Siwa/pump deployment remains a separate future physical field-validation layer.

Do not add testbeds merely to increase experiment count. Each platform must contribute a distinct material claim. Whichever of POWDER or COSMOS/ORBIT clears access/capability first should take the controlled-RF capability smoke; the other should not automatically receive a duplicate final matrix.

## Canonical Drive locations
Project root:
- `P12_WellPulse`
- Folder ID: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`

Validation workspace:
- `00_Validation_Workspace`
- Folder ID: `1SydHCA2jlkatxdGgUtJ1P8atgyi8_ta3`

Raw evidence:
- `02_RAW_EVIDENCE`
- Folder ID: `11xaitxG0vkV6fCzK_JgLAacrdhjz7GBf`

Handover folder:
- `WellPulse Handover`
- Folder ID: `1Du4j_YkMLvQjWJCxV5zqxxK6OGG2Q0hA`

Cross-project lessons ledger:
- `Research & Grants — Lessons Learned Ledger`
- Spreadsheet ID: `1BqUL_0DI0fAlG1eKNMCGLvE0wz2sSimR7bZ5tcStdeM`
- Location: `02 - Research & Grants / 00 - Research Operating Records`

## Cross-project lessons already captured
The general lessons ledger has been seeded with reusable rules covering handover-readiness, evidence classes, claim boundaries, freeze-before-final-run discipline, deterministic synthetic workloads, capability-first impairment selection, preservation of failed attempts, trigger-only PR hygiene, durable archival, TLS verification, account identifier resolution, parallel access lanes, duplicate-account avoidance, layered validation, independent receiver reconciliation, and precise fault semantics.

## Exact next action
Continue monitoring/resolving ARA and POWDER access gates. COSMOS/ORBIT is now the approved-in-principle third candidate for access qualification but no external signup is authorized by the scan itself.

If the owner approves COSMOS/ORBIT registration, first check for any existing account, then complete only the minimal account/group access path and stop before any reservation. After approval, capability-smoke SB4 RF attenuation before freezing final treatment values.

For POWDER, first prove account/project access and `srs-rf-matrix` availability before freezing attenuation values or running final evidence.

For ARA, first prove approved access to a real field-deployed COTS UE path and synchronized RSRP/SINR/RSRQ before freezing final OTA conditions.

No external account creation, reservation, outreach, or paid action should be taken without the project owner's explicit approval.

## Handover completion checklist for future agents
Before ending any material WellPulse work block:
1. Update this `HANDOVER_CURRENT.md`.
2. Update the relevant GitHub issue/protocol/result file.
3. Update Drive run/evidence registers where applicable.
4. Copy ephemeral publication-relevant artifacts into durable Drive storage and record checksums.
5. Add any reusable lesson to the cross-project Lessons Learned Ledger.
6. Verify that the next agent can identify current state, exact artifacts, evidence boundary, blockers, and next action without reading chat history.
