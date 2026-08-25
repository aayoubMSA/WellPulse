# POWDER G5 RF Calibration — Application-Data Boundary Check

Date: 2026-08-26 (Cairo)
Experiment: WP-G5-RF-CAL
Purpose: non-scored WP2 boundary check between degraded/near-threshold and effective application-data outage.

## Tested programmable attenuation windows
- +48 dB: replies=0, misses=19
- +50 dB: replies=0, misses=19
- +52 dB: replies=0, misses=20
- +54 dB: replies=0, misses=20

These counts were reconstructed from timestamped `ping -D -O -W 1 -I tun_srsue -i 1 172.16.0.1` output over the exact stage windows recorded by `/tmp/g5_q2_stages.log`.

## Interpretation
All tested levels from +48 through +54 dB produced effective full-window application-data outage during the 20 s impairment interval, despite the radio stack continuing to report increasingly degraded RSRP/SNR/MCS values. Therefore none of +48/+50/+52/+54 qualifies as Q2 under the frozen semantic definition (`near-threshold/intermittent operating point suitable for repeatable transient delivery degradation`).

This narrows the unresolved Q2 boundary to the interval above the known continuously connected +40 dB point and below +48 dB. A smaller bounded isolation sweep is required in that interval before Q2 can be numerically frozen.

## Current frozen/non-frozen state
- Q0 = 0 dB additional attenuation: strong/stable, PASS.
- Q1 = +40 dB additional attenuation: degraded but continuously connected characterization point, PASS candidate/freeze-ready.
- Q2: NOT YET FROZEN; boundary lies between +40 and +48 dB based on current evidence.
- Q3: effective application-data outage is already demonstrated at +55 dB; this boundary check additionally shows that +48 dB and above are already sufficient to cause full-window application-data outage in this run.

This is calibration evidence only; no scored-run authorization is implied.