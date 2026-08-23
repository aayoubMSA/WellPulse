# WP-RT03 — POWDER Controlled Real-RF Qualification

Status: ACCESS / PROJECT APPROVAL GATE
Date frozen: 2026-08-23

## Purpose
Add a scientifically distinct real-radio validation layer to WellPulse in parallel with the pending ARA rural-OTA lane.

WP-RT01 already validated application/transport-layer outage recovery on FIT IoT-LAB real A8 hardware. WP-RT03 must therefore introduce impairment at the RF layer, not repeat iptables/application-layer blocking.

## Platform path
Primary environment: POWDER `srs-rf-matrix` conducted RF environment.

Rationale:
- real 5G radios with programmable conducted RF attenuation;
- controlled and repeatable RF path loss;
- ability to introduce interference/noise and emulate handover scenarios;
- lower coordination burden than immediate outdoor OTA;
- suitable stepping stone to later indoor/outdoor OTA if needed.

## Frozen first-stage conditions
- P0 — reference RF condition with stable connectivity.
- P1 — degraded-but-connected RF condition created through controlled attenuation.
- P2 — RF-induced connectivity loss followed by restoration and recovery.

Exact attenuation values and transition timings are NOT frozen until capability smoke confirms the accessible profile/API and operating limits.

## Workload
Reuse the WellPulse 10,000-record workload and durable/non-durable comparison architecture where technically compatible.

The experiment must preserve:
- unique record identity;
- durable queue semantics for W1;
- independent receiver reconciliation;
- final unique count, permanent missing, duplicates, completeness;
- reconnect/recovery timing;
- RF-condition log synchronized to application events.

## Minimum capability gate
- [ ] POWDER account email verified.
- [ ] POWDER project approved.
- [ ] SSH login to allocated experiment node proven.
- [ ] `srs-rf-matrix` profile accessible.
- [ ] attenuation can be read and changed programmatically by the project.
- [ ] user-plane connectivity can be proven under P0.
- [ ] P1 degraded-but-connected state can be created repeatably without application-layer blocking.
- [ ] P2 RF-induced disconnect/recovery can be created repeatably without application-layer blocking.
- [ ] RF state/time series can be preserved with experiment evidence.
- [ ] frozen workload can run without major architectural redesign.

## Kill / pivot rules
Kill or pivot the POWDER lane if:
- access requires substantial paid use before a bounded evaluation;
- the controlled RF matrix is unavailable to the approved project;
- RF state cannot be synchronized with application evidence;
- reproducing P1/P2 requires substantial custom 5G-stack research unrelated to the WellPulse claim.

If controlled RF passes, evaluate whether outdoor OTA/mobility adds a material publication claim before spending further effort.

## Evidence boundary
POWDER evidence may support claims about controlled real-RF degradation, connectivity loss/recovery, application completeness, and recovery behavior on real wireless infrastructure.

It must NOT be described as:
- Siwa field validation;
- solar-pump mechanical/hydraulic validation;
- inverter/Modbus physical-hardware validation;
- groundwater or agronomic validation;
- rural/agricultural environmental validation unless an actual outdoor/rural environment is later used.

## Current access state
Mailbox evidence on 2026-08-23 shows POWDER account creation was initiated and a WellPulse SSH public key was accepted by Emulab infrastructure. No project/account approval message has yet been found. No experiment has been reserved or executed.
