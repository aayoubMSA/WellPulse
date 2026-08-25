# POWDER G5 RF Calibration — Q2 Candidate Sweep

Date: 2026-08-26 (Cairo)
Experiment: WP-G5-RF-CAL
Purpose: non-scored isolation sweep to locate the near-threshold/intermittent Q2 state between frozen Q1 and Q3 candidates.

## Stage schedule
- 48 dB additional attenuation: 1787697134.699359262 -> 1787697154.861219971
- 50 dB additional attenuation: 1787697185.022371548 -> 1787697205.186505410
- 52 dB additional attenuation: 1787697235.352389237 -> 1787697255.512457535
- 54 dB additional attenuation: 1787697285.679279693 -> 1787697305.841793180
- Each stage was followed by a return to 0 dB additional attenuation and approximately 30 s recovery.

## Radio observations
Approximate steady-state observations from the UE metrics log, excluding the initial transition seconds:
- 48 dB: RSRP -106 dBm, DL SNR ~12 dB, DL MCS ~10.
- 50 dB: RSRP -107 dBm, DL SNR ~10-11 dB, DL MCS ~10.
- 52 dB: RSRP -108 dBm, DL SNR ~9.1-9.5 dB, DL MCS ~7.2-10; one transient sample rendered as 100% DL BLER in the captured text.
- 54 dB: RSRP -109 dBm, DL SNR ~8.3-8.6 dB, DL MCS ~6.8-8.9; two transient samples rendered as 100% DL BLER in the captured text.

Recovery after each tested point returned the UE to approximately -60 dBm RSRP and ~41-45 dB DL SNR at 0 dB additional attenuation.

## Interpretation boundary
The radio metrics show monotonic degradation and place 52-54 dB in the near-threshold region. However, semantic Q2 requires intermittent application-data degradation rather than a full-window outage. The corresponding timestamped ping log must be reconciled before Q2 is numerically frozen.

This is non-scored calibration evidence only. No scored-run authorization is implied.