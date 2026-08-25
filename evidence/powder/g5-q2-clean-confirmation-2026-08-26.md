# G5 Q2 clean confirmation — 2026-08-26

Non-scored POWDER RF calibration evidence.

Clean LTE baseline was restored before this test. Programmed attenuation +52 dB was applied on all four controlled attenuator IDs for approximately 20 seconds, then reset to 0 dB.

Observed application-data result during the +52 dB window:
- successful ping replies: 6
- missed ping observations: 12
- classification: intermittent / near-threshold behavior, not continuous connectivity and not a full-window outage

Post-reset Q0 health check:
- 3/3 ping replies to 172.16.0.1
- 0% packet loss

Decision: freeze Q2 = +52 dB for WP-PWD01 conducted calibration. Existing evidence supports Q0 = 0 dB, Q1 = +40 dB, and Q3 = +55 dB. Trials affected by stale bearer state remain invalid and are excluded from calibration decisions.
