# G5 +41 dB candidate trial — INVALID for Q2/Q3 classification

Date: 2026-08-26
Experiment: WP-G5-RF-CAL
Status: NON-SCORED calibration

Observed RF behavior during +41 dB candidate trial:
- UE remained radio-connected in captured metrics.
- RSRP was approximately -100 dBm.
- SNR was approximately 17 dB.
- Reported BLER was 0% in the captured steady samples.
- After attenuation reset to 0 dB, RF metrics returned toward the strong baseline (~-60 dBm, SNR >40 dB).

However, the dedicated ping log for this trial reported 0 replies and 90 misses across the file. Because the miss interval extended beyond the intended 20 s +41 dB exposure and therefore also covered time after RF restoration, this trial cannot be used to classify +41 dB as Q2 or Q3. The data-plane health was not independently re-established at Q0 before interpreting the +41 dB result.

Scientific decision:
- Do not freeze +41 dB as Q2 or Q3 from this trial.
- Treat this trial as technically invalid for radio-state semantic classification because the application data path was already non-responsive or remained non-responsive outside the intended impairment window.
- Preserve prior valid RF calibration evidence.
- Next action is a bounded Q0 data-plane health check before any further attenuation change.
