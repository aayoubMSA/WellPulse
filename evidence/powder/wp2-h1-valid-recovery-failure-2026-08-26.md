# WP2-H1 W1 recovery calibration — Trial #1 valid recovery failure

Date: 2026-08-26
Experiment: WP-HCAL-E
Run ID: `wp2h1-a1-20260826-001`
Scored: false
Classification: `VALID_W1_RECOVERY_FAILURE`
Scientific consequence: H is not frozen; do not run replacement calibration trials under the frozen H-calibration rule. Scored runs remain unauthorized.

## Frozen trial schedule observed

- Q0 programmed on attenuator IDs `1 33 2 34` before readiness.
- Q3 programmed to 55 dB.
- Q3 full-state duration: 120.000117905 s.
- Q0 restored after Q3.
- Trial stopped after the frozen post-restore bound because backlog did not drain and H would exceed 300 s.

Key sender summary:

- cohort cutoff UTC: `2026-08-26T18:16:00.428045+00:00`
- cohort records: 211
- generated records: 361
- queue pending zero: null
- final pending count: 270
- app inflight: 20
- MQTT connected at final snapshot: false
- initial session present: false
- Q0 pre-readiness: 5/5 ping success over `tun_srsue`
- Q0 post-recovery health check: 0/3 ping success
- sender status: `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`
- sender rc: 20

## Failure diagnosis captured live

The UE process remained alive; `tun_srsue` remained UP with `172.16.0.2/24`, and the route to `172.16.0.1` still resolved through `tun_srsue`, but packets did not traverse after Q0 restoration.

The radio side itself recovered sufficiently for successful uplink decoding: the eNB remained alive and later logged PUSCH traffic with CRC OK and approximately 33 dB SNR. This rules out an eNB process crash and indicates physical/radio recovery occurred.

The EPC/MME/SPGW logs instead showed repeated attach/session-context churn after the outage:

- repeated attach requests for IMSI `001010123456789`
- `UE Context already exists`
- `Create Session Request being called for an UE with an active GTP-C connection`
- `Could not find GTP-C Tunnel info to delete`
- successive SPGW address allocations (`172.16.0.3`, `.4`, `.5`, `.6`, `.7`) while the UE tunnel interface remained at `172.16.0.2`
- UE-side attach/release/radio-link-failure loops

Interpretation: the observed non-recovery is dominated by post-outage LTE core/session-context/IP continuity failure in this srsLTE stack, not by MQTT or WellPulse durable-queue logic. The trial nevertheless remains a technically valid W1 recovery failure under the frozen protocol because the required user-plane recovery did not occur within the bound.

## Raw evidence preservation

The live raw evidence was copied from `/tmp` into the user's persistent POWDER home storage on both nodes and archived separately.

- nuc1 archive: `/users/aayoub/wellpulse-powder-evidence/wp2-h1-valid-failure-20260826/nuc1-wp2-h1-evidence.tar.gz`
  - SHA-256: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2 archive: `/users/aayoub/wellpulse-powder-evidence/wp2-h1-valid-failure-20260826/nuc2-wp2-h1-evidence.tar.gz`
  - SHA-256: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

Each node directory also contains a per-file `SHA256SUMS.txt` manifest. No secrets or private keys are intentionally included by this evidence step; the persistent bundle should be reviewed before any later public release.

## Recovery characterization

### UE-only restart

A bounded UE-only recovery test was run after the valid H1 failure. The existing `srsue` process was stopped, `tun_srsue` disappeared, and a fresh `srsue` was launched while EPC/eNB remained untouched. The fresh UE rediscovered the LTE cell and reached `RRC Connected`, but attach repeatedly failed. Final result after 96 s:

- `WP2_UE_ONLY_RECOVERY=FAIL`
- repeated `Attach failed`
- cell discovery and Random Access succeeded
- UE could not complete a usable user-plane attach

Conclusion: restarting only the UE is not sufficient to recover the post-outage state.

### EPC/eNB reset while UE remains running

EPC/eNB were then reset on `nuc1` while the fresh UE remained active on `nuc2`; the MQTT broker was intentionally left untouched. The core/RAN reset itself completed successfully (`WP2_CORE_RAN_RESET=PASS`). A bounded 60 s automatic-reacquisition check then failed:

- `WP2_POST_CORE_Q0_RECOVERY=FAIL`
- recovery check elapsed: 61 s
- UE again reported radio-link failure / RRC idle
- no working Q0 user-plane path returned

Conclusion: resetting EPC/eNB while the UE is already running is also insufficient.

### Coordinated clean-order LTE restart

A final bounded recovery characterization was then executed with strict ordering:

1. stop the UE completely on `nuc2`;
2. reset and stabilize EPC on `nuc1`;
3. start and stabilize eNB on `nuc1`;
4. start a fresh UE on `nuc2` only after core/RAN were stable.

This recovery path succeeded:

- `WP2_CLEAN_ORDER_RECOVERY=PASS`
- `tun_srsue` returned with source IP `172.16.0.2`
- route to `172.16.0.1` traversed `tun_srsue`
- final confirmation: 10/10 packets received, 0% loss
- RTT min/avg/max/mdev: `12.947/19.176/25.593/3.953 ms`

Operational conclusion: in this srsLTE/POWDER setup, deterministic Q0 recovery after the observed long-outage failure requires a coordinated clean-order LTE stack restart (`EPC -> eNB -> UE`) with the UE stopped before the core/RAN reset. UE-only restart and EPC/eNB reset with a live UE were both insufficient.

Scientific consequence: this is a recovery procedure for the testbed/runtime, not evidence that the original H1 trial recovered within the frozen scientific bound. Trial #1 remains a valid recovery failure, H remains unfrozen, and scored runs remain unauthorized. Any future H-calibration protocol that incorporates an explicit LTE-stack recovery primitive would constitute a protocol change and must be frozen before use.

## Operator-history snapshot during UE-only recovery characterization

A live POWDER browser-shell screenshot was captured during the bounded UE-only recovery test on `nuc2` at approximately `2026-08-26T18:26:24Z`.

The screenshot records the following operational sequence without interpreting the final recovery outcome:

- pre-restart state showed `srsue` running and `tun_srsue` present at `172.16.0.2/24` with route to `172.16.0.1` through the tunnel;
- the existing `srsue` instance was stopped cleanly;
- `tun_srsue` was absent after the stop;
- a fresh `srsue` instance started with PID `2341`;
- the live shell progress bar showed `37%`, corresponding to `Waiting for Q0 user plane 19s/90s` at the moment of capture.

This image is retained as operator-history evidence showing that the bounded recovery procedure was actually executing interactively on the reserved hardware. The screenshot alone does not establish PASS or FAIL of the UE-only recovery test; that classification is taken from the terminal's final result and associated logs.

## Decision

1. Preserve Trial #1; do not replace it.
2. Stop H calibration; H remains unfrozen.
3. Do not authorize scored B1/W1/B2 runs.
4. Treat `EPC -> eNB -> UE` as the currently demonstrated deterministic LTE recovery primitive for this environment, not as a retroactive repair of Trial #1.
5. Before any future H-calibration attempt, explicitly decide whether recovery by LTE-stack restart is scientifically admissible; if admitted, freeze that procedure prospectively before any new calibration trial.

No credentials or private keys are recorded in this evidence file.
