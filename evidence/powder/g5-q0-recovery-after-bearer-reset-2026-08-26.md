# G5 Q0 Recovery After Clean LTE Stack Reset — 2026-08-26

Status: NON-SCORED calibration evidence.

Context:
- Prior repeated RLF/re-attach activity left the LTE user plane unhealthy even after attenuation returned to 0 dB.
- The stale run was treated as invalid for RF-state classification.
- A bounded clean reset of srsepc/srsenb/srsue was performed, keeping RF attenuation at programmed 0 dB.

Post-reset Q0 health result on UE node:
- UE address: 172.16.0.2 on tun_srsue
- Target EPC SGi address: 172.16.0.1
- Command: `ping -I tun_srsue -c 5 172.16.0.1`
- 5 packets transmitted, 5 received
- Packet loss: 0%
- RTT min/avg/max/mdev: 23.974/43.251/109.768/33.302 ms

Interpretation:
- Clean Q0 user-plane baseline is restored.
- This validates that the previous persistent packet-loss condition was not an RF-calibration result and must not be used to classify Q1/Q2/Q3.
- RF calibration may resume only from this restored clean baseline.

No credentials, secrets, or raw manifest tokens are recorded here.
