# WP2-H1 recovery characterization after valid W1 failure

Date: 2026-08-26
Experiment: WP-HCAL-E
Parent run: `wp2h1-a1-20260826-001`
Scored: false

## UE-only recovery attempt

Purpose: determine whether restarting only the UE process is sufficient to clear the post-Q3 recovery failure while leaving EPC/eNB and MQTT infrastructure untouched.

Observed sequence:

- stale pre-restart `srsue` was stopped;
- `tun_srsue` disappeared after stop;
- fresh `srsue` started;
- recovery was observed for 90 s;
- UE found the configured FDD cell (PCI 1, PRB 25) and repeatedly reached `RRC Connected`;
- attach nevertheless failed repeatedly and RRC connection releases followed;
- final terminal result: `WP2_UE_ONLY_RECOVERY=FAIL`;
- elapsed time: 96 s.

Interpretation: UE-process restart alone is insufficient to recover the user plane after the valid W1 failure. This strengthens the earlier diagnosis that stale EPC/MME/SPGW session/context state is materially involved. The result does not alter the parent trial classification: `VALID_W1_RECOVERY_FAILURE`. H remains unfrozen and scored runs remain unauthorized.

## Next bounded escalation

Characterize whether a controlled reset of the LTE control/data-plane stack can restore Q0 while leaving the MQTT broker and preserved H1 evidence untouched. This is diagnostic recovery work only and must not be treated as a replacement H-calibration trial.
