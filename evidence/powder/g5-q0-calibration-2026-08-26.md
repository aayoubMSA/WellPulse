# POWDER G5 RF Calibration — Q0 Baseline

Date: 2026-08-26 (Cairo)
Experiment: WP-G5-RF-CAL
Purpose: non-scored WP2 RF calibration baseline before attenuation sweep.

## Bound resources
- enb1 -> nuc1 (network/eNB side)
- rue1 -> nuc2 (UE side)
- RFLink path reported by `tmcc attenuatorlist`: `1,33,2,34:nuc2/nuc1`

## Q0 attenuation
All four programmable attenuator IDs were set to `0` dB additional attenuation.
POWDER reference tooling documents roughly 30 dB minimum physical matrix attenuation, so Q0 corresponds to approximately 30 dB total path loss plus any residual path effects.

## Connectivity result
`ping -I tun_srsue -c 10 172.16.0.1`
- transmitted: 10
- received: 10
- packet loss: 0%
- RTT min/avg/max/mdev: 18.337/78.373/518.014/146.636 ms
- first packet incurred RRC wake-up latency (~518 ms); subsequent packets were ~18–37 ms.

## Live UE radio metrics
With srsUE metrics enabled (`t`):
- PCI: 1
- RSRP: -60 dBm (stable across captured samples)
- path loss field: 60 dB
- CFO: ~65–68
- DL SNR: ~40–45 dB
- DL BLER: 0%
- UL BLER: 0%

## Gate
Q0 baseline: PASS.

This run is non-scored calibration evidence only. No scored-run authorization is implied.
