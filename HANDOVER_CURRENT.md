# WellPulse — Current Handover

Last updated: 2026-08-23 16:23 Africa/Cairo

## Standing handover rule
No material project state may exist only in chat. Decisions, results, artifacts, blockers, evidence boundaries, and the exact next action must be recoverable from Drive and/or GitHub.

## Executive state
WellPulse has completed its first publication-grade remote-testbed validation layer on FIT IoT-LAB. Three next-layer access lanes are active/qualified: POWDER for controlled real-RF, COSMOS/ORBIT as the controlled-RF fallback, and ARA for rural outdoor OTA. Parallelize access gates, not redundant final experiments.

## WP-RT01 — FIT IoT-LAB
Status: **COMPLETE / FINAL EVIDENCE PASS**

Canonical result:
- `experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md`
- Evidence class: `FINAL_WP_RT01_FIT_A8`
- GitHub Actions run: `32628193889`
- Executed checkout SHA: `e257d22e1e6589b3e28ca2f2c14d3fab2ba2e483`
- Frozen workflow base commit: `fd5f07b947d44d2b03364a586cc1ac80aed5e070`
- Platform/site/node: FIT IoT-LAB / Grenoble / A8-100
- Matrix: B0/W1 × C0/C1/C2 × 3 replicates = 18 final cells
- Records per cell: 10,000
- Reconciliation: 18/18 PASS

Final result pattern in all three replicates:
- B0/C0: 100% completeness
- B0/C1: 80% completeness, exactly 2,000 permanent missing, 0 duplicates
- B0/C2: 80% completeness, exactly 2,000 permanent missing, 0 duplicates, restart_count=1
- W1/C0: 100% completeness, 0 missing, 0 duplicates
- W1/C1: 100% completeness, 0 missing, 0 duplicates
- W1/C2: 100% completeness, 0 missing, 0 duplicates, restart_count=1

Aggregates:
- W1/C1 total: 30,000/30,000 recovered, zero missing, zero duplicates
- W1/C2 total: 30,000/30,000 recovered, zero missing, zero duplicates
- W1/C1 reconnect mean 1.317088 s; SD 0.012321 s
- W1/C2 reconnect mean 1.344870 s; SD 0.027923 s
- W1/C1 backlog-drain mean 67.731246 s; SD 0.275086 s
- W1/C2 backlog-drain mean 67.870252 s; SD 0.851885 s
- Latency p50/p95/p99 were not instrumented and must not be claimed.

C2 semantics:
- WellPulse gateway-process exec restart after record 4000
- NOT a whole-node/hardware reboot

Evidence-supported claim:
> Under a controlled 10,000-record broker outage and gateway-process restart on FIT IoT-LAB A8 hardware, the WellPulse durable architecture achieved 100% final record completeness with zero permanent loss and zero duplicates in 3/3 replicates, while the non-durable baseline retained 80%.

Evidence boundary:
Validates communications, durable buffering, restart recovery, and edge-to-cloud reconciliation on real embedded hardware under controlled connectivity impairment. It does not validate Siwa field performance, pump mechanics, hydraulics, groundwater, inverter/Modbus physical hardware, motor/bearing faults, or agronomic outcomes.

Final durable artifacts:
- Rep 1: FIT 448265; GitHub artifact 9490962516; SHA-256 `1c18a5e93597607765fbd05ebb7d81554d31735b8644eccf613e2d5162423d55`; Drive `14SMrvpmFgX7J2eHIkBuUkEcCwI19c5Nl`
- Rep 2: FIT 448266; GitHub artifact 9491634827; SHA-256 `cf25bdcd4684b6be2d6e5b328776a5704f85a520068c5fe6ace4121c909a0fe7`; Drive `1Bi8zr7lO6UKn5BSoMrjQhoTcXIL5UtIX`
- Rep 3: FIT 448269; GitHub artifact 9492286379; SHA-256 `ef92f4c3cce6e3824669b7771a35ae8c2374275ef4e1b4937c69c79ef47ac3c8`; Drive `1Y1bBgs0iclyXeKsDr4tTI-ZcQEqr3EaO`

Structured run ledger:
- `WP-RT01_Run_Register_v1.0`
- Drive Sheet ID `1stmgZaWLGfavftgmzLyGW3S9Sefiiiy6QTtOB9AkBe0`
- Contains all 18 final rows marked COMPLETE

Closed audit trail:
- FIT readiness Issue #1 closed
- Trigger PRs #16, #17, #20, #21 closed unmerged

## WP-RT02 — ARA rural OTA
Status: **QUALIFIED / ACCESS GATE**

Canonical protocol:
- `experiments/WP-RT02/ARA_QUALIFICATION_2026-08-23.md`
- GitHub Issue #22

Purpose:
Add real rural outdoor OTA validation with COTS 5G first, timestamped radio state plus application evidence.

Gate before final design:
- approved MSA/Egypt access
- real field-deployed COTS UE path
- timestamped RSRP/SINR/RSRQ
- repeatable degraded-connected R1
- repeatable OTA detach/recovery R2
- WellPulse workload without major redesign

Current state:
- ARA remains preferred rural confirmation layer
- access/account approval still pending
- no reservation or experiment executed

## WP-RT03 — POWDER controlled real-RF
Status: **ACCESS / PROJECT APPROVAL GATE**

Canonical protocol:
- `experiments/WP-RT03/POWDER_QUALIFICATION_2026-08-23.md`
- GitHub Issue #23

Preferred path:
- `srs-rf-matrix`
- P0 stable RF
- P1 degraded-but-connected via programmable RF attenuation
- P2 RF-induced loss then restoration/recovery
- reuse 10,000-record WellPulse workload if capability smoke confirms compatibility

Current access evidence:
- POWDER account creation was initiated
- WellPulse SSH public key accepted by Emulab infrastructure
- no account/project approval email yet found
- do not create duplicate POWDER/Emulab account
- no reservation or experiment executed

## WP-RT04 — COSMOS/ORBIT controlled-RF fallback
Status: **ACTIVATION EMAIL RECEIVED / OWNER CLICK PENDING**

Canonical scan:
- `experiments/ALT_SCAN/ALTERNATIVE_TESTBEDS_2026-08-23.md`
- scan commit `01f7ab02eb61e6ad5fe1d63ef297d034d84f4481`
- GitHub Issue #24

Why this lane exists:
- COSMOS/ORBIT is the strongest third access lane if POWDER stalls
- ORBIT `sb4` exposes programmable RF attenuation
- ORBIT outdoor provides physical outdoor wireless resources
- COSMOS provides 5G OTA resources, remote reservations, and SSH/VPN access
- controlled RF is the preferred first use; outdoor/OTA only if it adds a distinct claim

Access precheck completed 2026-08-23:
- Gmail search found no prior COSMOS/ORBIT/WINLAB account, verification, or approval messages
- public search found no evidence that MSA / October University for Modern Sciences and Arts was already registered as a COSMOS/ORBIT organization
- current ORBIT policy explicitly allows university research users from non-US institutions
- current COSMOS/ORBIT workflow requires organization/group registration by the PI if the institution is absent; after group approval, the PI can approve user accounts
- user explicitly approved proceeding with this access gate

Activation milestone:
- COSMOS Support email received 2026-08-23 16:22 Cairo (13:22 UTC)
- subject: `ORBIT Group Account - Activation Required`
- sender: `support@cosmos-lab.org`
- confirmed group: `msa-university`
- confirmed PI username: `aayoub`
- activation link is in the email and must be clicked by the owner
- receipt of the activation email is **not** yet proof that the account/group is approved or usable

Exact next external action:
1. Owner clicks the activation link in the COSMOS Support email.
2. Verify the resulting organization/group approval and user-login state.
3. Upload the WellPulse public SSH key if needed and prove SSH/login access.
4. STOP before any reservation.
5. After access is proven, capability-smoke ORBIT SB4 RF attenuation before freezing attenuation values or launching final evidence.

No external reservation or experiment has been executed.

## AERPAW — secondary outdoor/mobile candidate
Status: **QUALIFIED CANDIDATE / HOLD**

Potential role:
Outdoor/mobile wireless resilience if mobility materially strengthens the manuscript. Hold because it carries greater operational complexity and could pull the project into unnecessary UAV/autonomy/6G work.

## Other alternatives
- NITOS: HOLD — weaker onboarding clarity/incremental claim value than COSMOS/ORBIT
- Colosseum: HOLD — powerful RF emulation, but not a physical-environment substitute for outdoor OTA

## Current validation ladder
1. FIT WP-RT01 — COMPLETE: real embedded hardware + controlled transport/connectivity outage
2. POWDER WP-RT03 — pending access: preferred controlled real-RF impairment/recovery
3. COSMOS/ORBIT WP-RT04 — activation email received; controlled-RF fallback pending activation/approval/login
4. ARA WP-RT02 — pending access: strongest rural outdoor OTA confirmation
5. AERPAW — hold for a distinct outdoor/mobile claim only
6. Actual Siwa/pump deployment — separate future physical field-validation layer

Decision rule:
Whichever of POWDER or COSMOS/ORBIT clears access/capability first takes the controlled-RF capability smoke. Do not run duplicate final matrices simply because both become available. ARA remains valuable only for a distinct rural-OTA claim.

## Canonical Drive locations
- Project root `P12_WellPulse`: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`
- Validation workspace `00_Validation_Workspace`: `1SydHCA2jlkatxdGgUtJ1P8atgyi8_ta3`
- Raw evidence `02_RAW_EVIDENCE`: `11xaitxG0vkV6fCzK_JgLAacrdhjz7GBf`
- Handover folder `WellPulse Handover`: `1Du4j_YkMLvQjWJCxV5zqxxK6OGG2Q0hA`
- Cross-project `Research & Grants — Lessons Learned Ledger`: `1BqUL_0DI0fAlG1eKNMCGLvE0wz2sSimR7bZ5tcStdeM`

## Handover completion checklist
Before ending any material WellPulse work block:
1. Update this file.
2. Update relevant GitHub issue/protocol/result file.
3. Update Drive run/evidence/handover index where applicable.
4. Copy ephemeral publication-relevant evidence into durable Drive storage and record checksums.
5. Add reusable lessons to the cross-project Lessons Learned Ledger.
6. Verify that a new agent can recover current state, exact artifacts, evidence boundaries, blockers, and next action without reading chat history.
