# POWDER G5 RF Calibration — timestamped isolation at +55/+56/+57/+58 dB

Date: 2026-08-26 (Cairo)
Experiment: WP-G5-RF-CAL
Purpose: non-scored WP2 RF calibration; isolate application-data behavior near the RF failure threshold using timestamped 20 s attenuation stages separated by Q0 resets.

## Stage schedule (epoch seconds)
- Q0 0 dB start: 1787696443.901891455
- +55 dB: 1787696467.301811616 -> 1787696487.465765451
- Q0 0 dB: 1787696487.465765451 -> 1787696507.630607380
- +56 dB: 1787696507.630607380 -> 1787696527.788611009
- Q0 0 dB: 1787696527.788611009 -> 1787696547.951232393
- +57 dB: 1787696547.951232393 -> 1787696568.112323778
- Q0 0 dB: 1787696568.112323778 -> 1787696588.278900947
- +58 dB: 1787696588.278900947 -> 1787696608.451807423
- final Q0 0 dB: from 1787696608.451807423

## Timestamped application-data observations
The timestamped ping used `-D -O -W 1 -i 1` over `tun_srsue` to EPC SGi `172.16.0.1`.

### +55 dB
- Last successful reply before/at transition: epoch 1787696467.320213, icmp_seq=38.
- Starting 1787696469.347839, `no answer yet` is reported for seq 39 onward.
- No successful reply occurs during the +55 dB interval.
- First successful reply after restoration to Q0: epoch 1787696487.845094, icmp_seq=58.
- Therefore +55 dB produced an effective application-data outage for essentially the full 20 s impairment window, with immediate recovery after Q0 restoration.

### +56 dB
- Last successful Q0 reply before impairment: epoch 1787696506.820278, seq=77.
- Starting 1787696508.835837, `no answer yet` is reported throughout the +56 dB interval.
- No successful reply occurs during +56 dB.
- Replies resume after Q0 restoration, first shown at epoch 1787696529.340393, seq=99.
- Therefore +56 dB also produces a repeatable effective application-data outage.

### +57 dB
- Last successful Q0 reply before impairment: epoch 1787696547.360231, seq=117.
- From 1787696549.347837 onward, all shown probes report `no answer yet` through the +57 dB interval.
- The link does not recover during the following 20 s Q0 reset window before the +58 dB stage begins.
- Thus +57 dB is a hard-outage setting and can incur recovery longer than the 20 s reset interval.

### +58 dB
Because the link had not recovered from +57 dB before +58 dB began, the +58 dB interval is not independently interpretable as an isolation trial. It is retained as raw calibration context only and is not needed to establish the Q3 threshold.

## Recovery verification
After the final reset to 0 dB, live srsUE metrics returned to the original Q0 region:
- RSRP: about -60 dBm
- DL SNR: about 41-45 dB
- DL/UL BLER: 0%
This confirms the attenuation control remained reversible and the strong-link baseline was restored.

## Calibration conclusion
- +55 dB is sufficient to satisfy the protocol meaning of Q3: **effective application-data outage**.
- +56 and +57 dB also produce outage and therefore provide no advantage as the nominal Q3 setting; +55 dB is the lowest directly isolated tested value with full-window application outage in this sequence.
- Q3 may therefore be frozen at +55 dB additional attenuation, subject to final protocol-state reconciliation.
- Q2 is NOT frozen by this file. Earlier +50 dB RF metrics show a near-threshold radio regime, but a timestamped application-level isolated trial below +55 dB is still required if Q2 must be defined by repeatable transient delivery degradation rather than radio metrics alone.

This evidence is non-scored calibration only. No scored-run authorization is implied.