# G5 +42 dB clean validation — 2026-08-26

Status: NON-SCORED calibration evidence.

Clean baseline was restored before this test (UE IP 172.16.0.2; Q0 user-plane ping 5/5 PASS).

Programmed attenuation path IDs: 1, 33, 2, 34.

Stage timestamps (node clock):
- Q42_START = 1787699103.686048662
- Q42_END = 1787699123.865730237
- Q0_RESTORED = 1787699124.023306958

Application-data result during the +42 dB window:
- replies = 20
- misses = 0

Post-reset Q0 verification:
- ping 3/3
- 0% packet loss
- RTT min/avg/max/mdev = 13.977/15.219/15.855/0.878 ms

Interpretation:
- +42 dB is NOT an effective application-data outage under a clean bearer state.
- Earlier +42 dB outage-like evidence was contaminated by a stale/broken LTE user-plane bearer and must not be used to freeze Q2/Q3.
- The valid static-state boundary is now constrained above +42 dB. Previously valid clean evidence still supports Q0 = 0 dB and continuous-connectivity behavior at +41/+42 dB.

No scored run is authorized by this evidence.