# WellPulse — Alternative Remote-Testbed Scan — 2026-08-23

Status: QUALIFICATION SCAN COMPLETE

## Purpose
Identify defensible remote real-hardware/wireless alternatives beyond ARA and POWDER without inflating the experiment count or creating unrelated wireless-stack work.

## Decision
### 1. COSMOS/ORBIT — GO FOR ACCESS QUALIFICATION
Best immediate third lane.

Why it matters:
- current COSMOS/ORBIT scheduler exposes `sb4.orbit-lab.org` RF Attenuator Matrix for repeatable topology/path-loss control;
- `outdoor.orbit-lab.org` exposes an approximately 22-node outdoor wireless domain;
- COSMOS supports remote reservations, SSH/VPN access, SDR and COTS wireless resources;
- COSMOS Sandbox 1 has a current 5G NR OTA tutorial with end-to-end IP traffic through a real 28 GHz gNB↔UE link;
- portal documentation states account activation + group PI approval typically takes a day or two.

Scientific role if qualified:
- primary: controlled RF attenuation/recovery on ORBIT SB4 as a fallback/substitute for POWDER controlled RF;
- optional: outdoor ORBIT/COSMOS or 5G OTA only if it adds a distinct claim after controlled-RF validation.

Do not run both POWDER and COSMOS final matrices if they prove the same claim; use whichever clears access/capability first unless the second adds a materially different physical layer or environment.

### 2. AERPAW — QUALIFY LATER / HIGHER-COMPLEXITY OUTDOOR OPTION
AERPAW is an active large-scale outdoor PAWR platform with real 4G/5G, SDR, LoRa, autonomous ground/aerial vehicles and current 2026 live outdoor experiments. It supports external users and remote experiment development; official materials include an experiment portal, self-paced tutorial portal, and current user stories transitioning from digital-twin development to real outdoor execution.

Potential WellPulse role:
- outdoor/mobile wireless resilience under real motion and interference;
- could strengthen the environmental/mobility evidence beyond controlled lab RF.

Why not first:
- greater operational/field coordination than COSMOS/ORBIT;
- UAV/autonomy capabilities are unnecessary for WellPulse and must not pull the project off-scope;
- physical outdoor execution may depend on operations-team scheduling and safety procedures.

### 3. NITOS — HOLD
NITOS still exposes real SDR/LTE/Wi-Fi hardware and a 50-node isolated indoor deployment, but current access/onboarding clarity and incremental claim value are weaker than COSMOS/ORBIT.

### 4. Colosseum — HOLD / NOT A PHYSICAL-ENVIRONMENT SUBSTITUTE
Colosseum provides large-scale SDR hardware and a massive RF channel emulator. It is scientifically valuable for repeatable wireless-network emulation but does not by itself provide the same physical-environment evidence as outdoor OTA. It could be used only if scale/repeatable channel diversity becomes a specific manuscript need.

## Ranking after this scan
1. ARA — strongest rural/agricultural OTA realism; access pending.
2. POWDER — strongest controlled real-RF + optional outdoor OTA path; access/project approval pending.
3. COSMOS/ORBIT — GO third lane; likely fastest practical substitute for controlled RF and offers optional outdoor/5G OTA.
4. AERPAW — strong outdoor/mobile option if a distinct mobility/environment claim is needed.
5. NITOS — hold.
6. Colosseum — hold unless RF-emulation scale becomes a specific research need.

## Execution rule
Parallelize ACCESS gates, not redundant FINAL experiments. Whichever of POWDER or COSMOS/ORBIT becomes usable first should take the controlled-RF capability smoke. Keep ARA pending for rural confirmation. Add AERPAW only if outdoor mobility materially strengthens the paper.

## Evidence boundary
None of these remote wireless testbeds establish Siwa pump mechanics, hydraulics, groundwater, inverter/Modbus physical compatibility, or agronomic outcomes. Claims must remain limited to the layer actually exercised.

## External-action guardrail
No external account creation, project creation, reservation, outreach, or paid action is authorized by this scan alone.