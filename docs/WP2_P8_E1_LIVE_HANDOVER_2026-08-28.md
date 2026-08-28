# WellPulse — WP2-P8-E1 Live Handover

Date: 2026-08-28  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Platform: POWDER / `srslte-controlled-rf`  
Reservation: `WP-07-C`  
Status: **LIVE / NON-SCORED / P8-E1 IN PROGRESS**

## 1. Canonical boundary

This handover covers only the manual exploratory campaign `WP2-P8`, specifically:

`P8-E1 — Fine RF Threshold Sweep`

The campaign definition is:

`experiments/WP-PWD01/WP2_P8_MANUAL_RF_EXPERIMENT_CAMPAIGN_2026-08-28.md`

This does **not** alter scored P7B state. Historical scored authority remains unchanged and this manual campaign must not be promoted into scored P7B evidence.

## 2. Current reservation and topology

Experiment: `WP-07-C`  
State: `ready` when P8-E1 began.  
Profile: `srslte-controlled-rf`

Roles:

- `nuc1 / CORE`: EPC + eNB + Mosquitto broker + experiment receiver.
- `nuc2 / UE`: srsUE + experiment publisher + RF attenuation control.

Known-good LTE endpoints immediately before P8-E1:

- CORE: `172.16.0.1`
- UE: `172.16.0.2`

Known attenuator IDs:

`[1, 33, 2, 34]`

Permanent rule: every experiment must expose and preserve both node roles separately.

## 3. P8-E1 shared run identity

Shared run ID:

`p8-e1-20260828T1707Z`

Node-local evidence roots:

### nuc1 / CORE

`~/wellpulse-exploratory/p8-e1-20260828T1707Z/CORE/`

### nuc2 / UE

`~/wellpulse-exploratory/p8-e1-20260828T1707Z/UE/`

Do not change this RUN_ID for the in-progress run.

## 4. Pre-treatment preparation already completed

### nuc1 / CORE

Baseline capture was executed and reported complete. The block created:

- `events.log`
- `processes_baseline.txt`
- `ip_addr_baseline.txt`
- `ip_route_baseline.txt`
- `mqtt_socket_baseline.txt`
- `ping_ue_baseline.txt`

The user reported the CORE baseline block completed.

### nuc2 / UE

Before measurement, all attenuators were explicitly set to `0 dB` and baseline capture was executed, creating:

- `events.log`
- `processes_baseline.txt`
- `tun_baseline.txt`
- `ip_route_baseline.txt`
- `ping_core_baseline.txt`

The user reported the UE baseline block completed.

Immediately before P8-E1, the LTE path had been independently restored and verified with `3/3` UE-to-CORE ping, `0%` packet loss, with RTT approximately `25–27 ms` in the last visible baseline probe.

## 5. CORE receiver currently started

On `nuc1 / CORE`, an independent MQTT receiver was started for topic:

`wellpulse/p8/e1`

It timestamps each received message into:

`~/wellpulse-exploratory/p8-e1-20260828T1707Z/CORE/received.log`

The receiver PID was written to:

`receiver.pid`

The user-visible gate was:

`CORE_RECEIVER=READY`

The screenshot showed the `mosquitto_sub` receiver process active.

Do not stop the receiver until the sweep completes and final raw freeze is performed.

## 6. UE fine sweep currently running

On `nuc2 / UE`, the following treatment sequence was launched:

`0, 20, 30, 35, 40, 45, 48, 50, 52, 54, 55, 56, 58, 60 dB`

For each attenuation level, the script:

1. writes a timestamped `ATTENUATION_DB=<value>` event;
2. sets all four attenuators to that level;
3. records a 5-packet `ping` test to `172.16.0.1`;
4. sends five sequenced MQTT observations on topic `wellpulse/p8/e1`;
5. records publisher failures into `events.log`;
6. creates per-level `ping_<DB>dB.log` and `mqtt_<DB>dB.log` files;
7. appends every attempted message to `sent.log`.

Important: the treatment block intentionally did **not** restore attenuation to `0 dB` at its end. Do not alter RF until the current sweep has completed and evidence has been frozen or an explicit recovery step is started.

## 7. Visible live observations so far — DO NOT OVER-INTERPRET

From the user screenshot during the ongoing sweep:

- At `20 dB`, at least one `MQTT_FAIL` was visible.
- At `30 dB`, the displayed ping sample showed `5 transmitted, 0 received, 100% packet loss`.
- MQTT failures were visible at `30 dB` for at least some sequence numbers.

These are **console observations only** and are not yet final scientific findings.

Do **not** conclude that the true RF threshold is 20 or 30 dB until both-node raw evidence is frozen, exported, and reconciled.

Potential contamination mechanism already identified: after an early RF/LTE bearer loss, later attenuation points may represent a stale/disconnected bearer rather than independent steady-state behavior at each requested dB level.

Therefore the present E1 run is valuable as evidence, but its interpretation must wait for raw-data analysis.

## 8. Immediate action when the running sweep finishes

Do **not** immediately start another experiment.

Perform these steps in order:

1. Record the final visible sweep state without changing RF.
2. Freeze raw evidence on `nuc1 / CORE`.
3. Freeze raw evidence on `nuc2 / UE`.
4. Hash each node independently.
5. Bundle CORE and UE separately.
6. Pull both archives off POWDER to the user's home PC.
7. Verify SHA256 locally.
8. Reconcile sender/receiver sequence IDs and timestamps.
9. Only after analysis classify P8-E1 as accepted exploratory evidence, blocked/pre-science, or NULL/aborted.
10. Use the analysis to redesign E1 if required before E2.

## 9. Required evidence to preserve at sweep completion

### nuc1 / CORE

At minimum preserve:

- `received.log`
- `events.log`
- baseline process/network/socket snapshots
- current/final process snapshot
- current/final socket snapshot
- `ip addr`
- `ip route`
- EPC/eNB logs relevant to this run if available
- broker log/state if available
- receiver PID/process state
- node-local SHA256 manifest

### nuc2 / UE

At minimum preserve:

- `sent.log`
- `events.log`
- all `ping_*dB.log`
- all `mqtt_*dB.log`
- baseline process/tunnel/route snapshots
- current/final process snapshot
- current/final `ip addr`
- current/final `ip route`
- UE log relevant to this run if available
- node-local SHA256 manifest

## 10. Analysis required before revising E1

The first offline analysis must distinguish:

1. actual RF degradation/failure threshold;
2. post-failure stale bearer behavior;
3. MQTT command timeout behavior;
4. UE attachment/reattachment state;
5. sender attempt sequence versus receiver-delivered sequence;
6. whether any later level was independently reached in a healthy LTE state;
7. whether loss persisted after a previous point rather than being newly induced at the current point.

Do not infer these from the terminal alone.

## 11. Likely E1 revision if raw evidence confirms early bearer collapse

Only after analysis, the likely redesign is:

- add a pre-point readiness gate;
- stop the upward sweep at first confirmed bearer loss, or restore a known-good baseline before testing the next independent level;
- run a coarse low-range calibration first;
- then run a separate micro-sweep around the observed transition;
- keep CORE receiver + UE publisher evidence independent;
- preserve both node roles for every point.

A possible candidate micro-range discussed in chat was approximately:

`0, 5, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30 dB`

This is **not yet frozen** and must not be executed until current raw evidence is analyzed.

## 12. Campaign state after E1

Planned P8 experiments remain:

- `P8-E1` Fine RF Threshold Sweep — **IN PROGRESS**
- `P8-E2` RF Hysteresis Sweep — planned
- `P8-E3` Near-Threshold Repeatability — planned
- `P8-E4` RF-Only Recovery — planned
- `P8-E5` UE-Restart Recovery — planned
- `P8-E6` CORE-Restart Recovery — planned
- `P8-E7` Combined Recovery Stress Case — planned
- `P8-E8` Broker-Only Fault Control — planned
- `P8-E9` No-Fault Duration-Matched Control — planned

No later experiment should begin until P8-E1 raw evidence is frozen and its execution validity is understood.

## 13. Standing execution doctrine

For every live two-node experiment:

`nuc1 / CORE commands + nuc2 / UE commands + shared RUN_ID + independent raw evidence + independent hashes + off-platform preservation + reconciliation`

Manual two-node execution remains the reference implementation. Do not revert to a one-node monolithic B1-style runner.

## 14. Exact next state

`WP2_P8_E1_STATE=LIVE_SWEEP_IN_PROGRESS`

`NEXT_ACTION=WAIT_FOR_SWEEP_COMPLETION_THEN_FREEZE_BOTH_NODES`

`DO_NOT_START_E2=YES`

`DO_NOT_INTERPRET_THRESHOLD_FROM_CONSOLE_ONLY=YES`

`DO_NOT_RESTORE_RF_UNTIL_SWEEP_COMPLETES=YES`

`SCORED_P7B_STATUS=UNCHANGED`

STOP at this state until the running sweep finishes.
