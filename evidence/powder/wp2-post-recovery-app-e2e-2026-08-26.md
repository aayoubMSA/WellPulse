# WP2 post-recovery application E2E qualification

Date: 2026-08-26
Experiment: WP-HCAL-E
Context: non-scored recovery characterization after preserved H1 `VALID_W1_RECOVERY_FAILURE`.

## Purpose

Verify that the coordinated clean-order LTE recovery primitive (`EPC -> eNB -> UE`) restores not only ICMP Q0 connectivity but the actual WellPulse application transport prerequisites over `tun_srsue`.

## Preliminary probe

The first application probe was technically invalid because its Paho MQTT v2 callback attempted `int(reason_code)` on a `ReasonCode` object and raised `TypeError` before MQTT qualification completed. LTE/Q0 remained healthy during that run. This probe is classified only as `TECHNICALLY_INVALID_PROBE` and is not evidence of an MQTT or WellPulse failure.

## Corrected application-path probe

UTC start: `2026-08-26T18:40:00Z`

Preconditions observed:

- `tun_srsue` UP with `172.16.0.2/24`
- route to `172.16.0.1` through `tun_srsue`
- Q0 ICMP confirmation: 5/5 packets received, 0% loss
- Q0 RTT min/avg/max/mdev: `9.636/12.690/15.695/2.166 ms`
- Python environment used pinned `paho-mqtt==2.1.0`

MQTT/TLS evidence:

- client ID: `wp2-postrec-20260826T184005Z-3585`
- topic: `wellpulse/wp2/post-recovery/20260826T184005Z-3585`
- connect reason: `Success`
- initial `session_present=false`
- TLS MQTT connect: PASS
- QoS1 SUBACK: PASS
- QoS1 PUBACK: PASS
- MQTT round-trip receive: PASS
- payload SHA-256: `a8b348847f2dff2032155d33bee8799628b79b8699304c90d96b6011615dfb6a`
- received SHA-256: `a8b348847f2dff2032155d33bee8799628b79b8699304c90d96b6011615dfb6a`
- payload integrity: PASS
- `WP2_POST_RECOVERY_APP_E2E=PASS`
- `WP2_POST_RECOVERY_FULL_PATH=PASS`

Persistent terminal evidence file:

`/users/aayoub/wellpulse-powder-evidence/wp2-h1-recovery-characterization-20260826/nuc2/post-recovery-app-e2e-v2.txt`

SHA-256:

`fa7e34b289b32f48fcc3805d28cdc6643d95503f976815179767d8c604371e3a`

## Interpretation

The coordinated clean-order LTE recovery primitive restored the full WellPulse transport path through the UE tunnel: LTE user plane, TLS, MQTT v3.1.1 client operation, QoS1 acknowledgement semantics, broker round-trip delivery, and payload integrity.

This remains recovery-characterization evidence only. It does not retroactively convert H1 into a successful calibration trial, does not freeze H, and does not authorize scored B1/W1/B2 runs.
