# POWDER G5 RF Calibration — +10 dB Point

Date: 2026-08-26 (Cairo)
Experiment: WP-G5-RF-CAL
Purpose: non-scored WP2 RF calibration point following Q0 baseline.

## Bound resources
- enb1 -> nuc1 (network/eNB side)
- rue1 -> nuc2 (UE side)
- RFLink path: `1,33,2,34:nuc2/nuc1`

## Programmed attenuation
All four programmable attenuator IDs were set to `10` dB additional attenuation.
Relative to Q0, this is a +10 dB programmed step.

## Connectivity under continuous traffic
A continuous ping from UE (`nuc2`) to EPC SGi (`172.16.0.1`) remained active.
Captured samples (seq 142–161) all received replies, with observed RTTs approximately 10.6–28.9 ms over the shown tail.
No outage was observed in the captured interval.

## Live UE radio metrics
With srsUE metrics enabled:
- PCI: 1
- RSRP: -70 dBm (stable across captured samples)
- path loss field: 70 dB
- CFO: ~70–76
- DL SNR: ~39–42 dB
- DL BLER: 0%
- UL BLER: 0%

## Calibration observation
Q0 RSRP was -60 dBm at 0 dB additional attenuation. After a +10 dB programmed attenuation step, RSRP moved to -70 dBm: an observed -10 dB response matching the programmed change.

This validates that the selected POWDER RFLink attenuator path is controllable and produces the expected monotonic RF response.

## Gate
+10 dB calibration point: PASS.

This is a non-scored calibration point. It is not yet a final freeze of the semantic Q1 state; additional points are required to locate the degraded, near-threshold, and outage regimes.
