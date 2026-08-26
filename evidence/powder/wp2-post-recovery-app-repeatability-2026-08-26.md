# WP2 post-recovery application-path repeatability

Date: 2026-08-26
Experiment: WP-HCAL-E
Scope: non-scored recovery characterization after preserved H1 valid recovery failure
Scientific state: H remains unfrozen; scored runs remain unauthorized.

## Result

`WP2_POST_RECOVERY_APP_REPEATABILITY=3_OF_3_PASS`

After the coordinated clean-order LTE recovery (`EPC -> eNB -> UE`), three independent fresh application-path qualifications succeeded through `tun_srsue` to the TLS MQTT broker at `172.16.0.1:8883`.

Each successful qualification required:

- live `tun_srsue` path from UE source address `172.16.0.2` to `172.16.0.1`;
- Paho MQTT `2.1.0`;
- MQTT v3.1.1;
- TLS broker connection;
- fresh run-unique client/topic identity;
- QoS1 SUBACK and PUBACK;
- broker round-trip receive;
- exact SHA-256 payload equality.

### Qualification #1

- `WP2_POST_RECOVERY_APP_E2E=PASS`
- `WP2_POST_RECOVERY_FULL_PATH=PASS`
- connection reason: `Success`
- initial `session_present=false`
- payload SHA-256: `a8b348847f2dff2032155d33bee8799628b79b8699304c90d96b6011615dfb6a`
- received SHA-256 matched exactly
- persistent evidence file SHA-256: `fa7e34b289b32f48fcc3805d28cdc6643d95503f976815179767d8c604371e3a`

### Qualification #2

- client ID: `wp2-postrec-20260826T184230Z-3639`
- topic: `wellpulse/wp2/post-recovery/20260826T184230Z-3639`
- connection reason: `Success`
- initial `session_present=false`
- TLS: PASS
- QoS1 SUBACK/PUBACK: PASS
- round-trip receive: PASS
- payload SHA-256: `4874e3e5ac18c85cf3e3dc4fa47d9e322e1b1c9c7e456b0be0afbd770ab77a4d`
- received SHA-256 matched exactly
- preserved app evidence SHA-256: `4031016406085535b9582d2b19ffdb955b6eb5bcb7d6931c452c19a876391cc0`

### Qualification #3

- client ID: `wp2-postrec-20260826T184236Z-3691`
- topic: `wellpulse/wp2/post-recovery/20260826T184236Z-3691`
- connection reason: `Success`
- initial `session_present=false`
- TLS: PASS
- QoS1 SUBACK/PUBACK: PASS
- round-trip receive: PASS
- payload SHA-256: `9645bf064a5e4d3a4935067d481dedc106f8c8cd2ca2bb2c82452f988fdfc023`
- received SHA-256 matched exactly
- preserved app evidence SHA-256: `4f1b25fb8f7ba62dc8ab02ae2429fcdc56f26b9580e0e5b76429aab4c6153e61`

## Interpretation

The demonstrated clean-order LTE recovery restored more than ICMP reachability: it restored the exact application transport prerequisites required by WellPulse, and that recovered application path was repeatable across three fresh run-isolated MQTT sessions.

This does not retroactively repair H1. Trial `wp2h1-a1-20260826-001` remains `VALID_W1_RECOVERY_FAILURE`, H remains unfrozen, and no scored B1/W1/B2 runs are authorized. These results characterize the recovery primitive and post-recovery transport stability only.

No credentials or private keys are recorded here.
