# POWDER G5 RF Calibration — 58–62 dB Threshold Sprint

Date: 2026-08-26 (Cairo)
Experiment: WP-G5-RF-CAL
Purpose: non-scored threshold/outage characterization.

## Context
Prior calibrated points established a monotonic conducted-RF response from Q0 through +55 dB additional attenuation. This sprint tested +58, +60, and +62 dB with a safe reset to +40 dB afterward.

## Application-data observation
A timestamped continuous ping over `tun_srsue` to EPC SGi `172.16.0.1` showed replies for sequence 1–15, then no replies until sequence 96. The observed reply gap was about 82.9 seconds, spanning approximately 80 missing ping sequence numbers, followed by recovery after the attenuation sprint/reset.

The UE source IP during the initial ping interval was `172.16.0.3`; after repeated radio-link failures and recovery it later reattached with IP `172.16.0.4`.

## Radio behavior in outage region
Captured srsUE output in the high-attenuation region showed:
- RSRP approximately -112 dBm;
- DL SNR approximately 5.9–6.1 dB;
- DL MCS approximately 1.3–1.6;
- DL bitrate approximately 256–264 bit/s in shown samples;
- UL BLER approximately 73–74% in shown samples;
- repeated `Warning: Detected Radio-Link Failure`;
- repeated transitions to `RRC IDLE` / disconnected;
- repeated random-access attempts and temporary reconnects.

This is direct evidence that the 58–62 dB tested band contains an effective application-data outage regime (Q3 semantics).

## Recovery
After the safe reset to +40 dB, the UE reattached and recovered to approximately:
- RSRP -99 to -100 dBm;
- DL SNR 18–19 dB;
- DL BLER 0%;
- continued application-data connectivity.

## Scientific interpretation
- Q3 semantics are confirmed to exist within the tested +58 to +62 dB band.
- The exact first attenuation value producing repeatable Q3 is **not yet numerically frozen**, because the captured ping/RF excerpt is not stage-tagged tightly enough to attribute the first radio-link failure and outage to exactly +58, +60, or +62 dB.
- Q2 also remains to be isolated as a repeatable near-threshold/intermittent state, likely immediately below the Q3 boundary.

## Gate
Threshold/outage discovery: PASS.
Exact Q2/Q3 numeric freeze: PENDING bounded stage-tagged isolation.

This evidence is non-scored calibration only and does not authorize scored runs.
