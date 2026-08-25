# G5 clean +41 dB boundary retest — 2026-08-26

Status: VALID NON-SCORED CALIBRATION EVIDENCE

## Preconditions

- Conducted POWDER LTE experiment WP-G5-RF-CAL.
- RF attenuator IDs 1, 33, 2, 34 controlled together.
- LTE/EPC and UE were cleanly restarted after a stale user-plane bearer was detected.
- Clean Q0 health gate passed immediately before this retest: UE IP 172.16.0.2, 5/5 ICMP replies to 172.16.0.1, 0% loss.

## +41 dB isolated window

- Q41_START: 1787698937.848392294
- Q41_END: 1787698958.013882713
- Q0_RESTORED: 1787698958.167489227
- Programmed attenuation: +41 dB on all four controlled attenuator IDs.
- Window duration: approximately 20.17 s.

Timestamp-scoped ICMP reconstruction for the +41 dB window:

- replies: 20
- misses: 0
- packet loss in the isolated window: 0%

Post-reset Q0 health check:

- 3/3 ICMP replies
- 0% loss
- RTT min/avg/max/mdev = 12.087/13.187/13.840/0.782 ms

## Interpretation

+41 dB is not an effective application-data outage under the clean baseline. It remains continuously connected at the application-data level in this isolated retest.

Earlier +41 evidence collected while the LTE user-plane bearer had become stale remains invalid for RF-state classification and is not superseded silently; it is retained as invalid infrastructure evidence.

The next scientifically bounded action is one isolated clean +42 dB test from a verified Q0 baseline. No broader sweep is justified until that boundary point is resolved.

Scored runs remain unauthorized.
