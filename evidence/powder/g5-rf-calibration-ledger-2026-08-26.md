# G5 RF Calibration Ledger — 2026-08-26

## Purpose
Canonical, sanitized record of the non-scored POWDER conducted-RF calibration used by WP-PWD01. This ledger exists to support paper traceability, later handover, and independent reproduction of the Q0-Q3 radio states.

## Scientific status
- Calibration only; NON-SCORED.
- Scored runs remain unauthorized until all remaining pre-score gates pass.
- Frozen RF state values from the valid evidence are Q0=0 dB, Q1=40 dB, Q2=52 dB, Q3=55 dB programmed additional attenuation.
- Invalid stale-bearer trials are retained as technical evidence but excluded from RF-state classification.

## Testbed / profile identity
- Project: WellPulse
- Experiment: WP-G5-RF-CAL
- Experiment UUID: 575d246e-8d01-4827-9a84-f4368d272cea
- Controlled-RF profile: srslte-controlled-rf
- Profile revision: a6da96560b6526dc6816761282722c996418fd8c
- eNB/EPC node: enb1 -> nuc1
- UE node: rue1 -> nuc2
- UE tunnel endpoint during clean baseline: 172.16.0.2
- SGi peer: 172.16.0.1

No credentials, keys, tokens, or private material are stored in this ledger.

## Attenuation control
The POWDER RF-matrix path exposed four attenuation IDs and all four were changed together:

```bash
for id in 1 33 2 34; do
  /usr/local/etc/emulab/tmcc attenuator "$id" VALUE
done
```

`VALUE` is the programmed additional attenuation in dB. The RF matrix contributes an approximate fixed minimum path loss of about 30 dB, so physical total path loss is approximately 30 dB + programmed value; this approximation is contextual only. The canonical Q-state values below are the programmed additional attenuation values.

## Clean baseline readiness gate
After a bounded EPC/eNB/UE reset, Q0 was restored at 0 dB and the UE data plane passed:

- `ping -I tun_srsue -c 5 172.16.0.1`
- 5 transmitted / 5 received / 0% loss
- RTT min/avg/max = 23.974/43.251/109.768 ms
- subsequent post-state Q0 checks also passed 3/3 with 0% loss.

This clean baseline was required before the final boundary tests.

## Valid calibration evidence

### Q0 — strong/stable reference
- Programmed attenuation: 0 dB
- Representative RSRP: about -60 dBm
- Representative DL SNR: about 40-45 dB
- BLER: 0 in the recorded baseline
- User-plane ping: 10/10, 0% loss in the formal baseline
- Interpretation: strong/stable reference

Primary evidence commit: `9e4e8b0ee14f9919a8ca8b5a5e5f615fdb33e62d`
Clean post-bearer-reset recovery evidence: `6f4cb5d01ceb2eb402f638534c24a7b04a3276da`

### Q1 — degraded but continuously connected
- Programmed attenuation: 40 dB
- Representative RSRP: about -100 dBm
- Representative DL SNR: about 18-19 dB
- Representative MCS: reduced relative to Q0
- BLER: 0 in the representative valid segment
- Continuous user-plane replies were observed through the valid +40 stage
- Interpretation: clearly degraded radio conditions while continuously connected

Primary evidence commit: `7a4dc3891977b0e643850bfa713e6a0ae9c0a16c`

### Q2 — near-threshold / intermittent
Final clean isolated test:
- Programmed attenuation: 52 dB
- Exact window start: `1787699431.463366881`
- Exact window end: `1787699451.623496520`
- Window duration: about 20.16 s
- Timestamped user-plane classification: 6 replies / 12 misses
- Q0 restored at `1787699451.789937970`
- Immediate post-reset health check: 3/3 replies, 0% loss
- Interpretation: near-threshold intermittent data delivery with preserved recovery to a healthy baseline

Canonical clean Q2 evidence commit: `3b9d1992cfeb18ceb5be468b1fe751b0d2a40a9e`

### Q3 — effective application-data outage
Valid isolated +55 stage performed before the later stale-bearer incident:
- Programmed attenuation: 55 dB
- Stage start: `1787696467.301811616`
- Reset to Q0: `1787696487.465765451`
- Last pre-impairment reply: sequence 38
- No replies for sequences 39-57 during the impairment window
- First reply after reset: sequence 58 at about `1787696487.845`
- Interpretation: effective application-data outage for essentially the entire 20 s impairment window with recovery after Q0 restoration

Primary evidence commit: `cf57bf8646f39c1be9443c4e08160a69697c7ba1`

## Clean boundary checks supporting Q2 selection
These checks were performed only after restoring a healthy Q0 bearer and using a fresh timestamped ping logger.

| Programmed attenuation | Exact result | Interpretation |
|---:|---|---|
| 41 dB | 20 replies / 0 misses | continuously connected |
| 42 dB | 20 replies / 0 misses | continuously connected |
| 49 dB | 21 replies / 0 misses | continuously connected |
| 52 dB | 6 replies / 12 misses | intermittent; selected Q2 |
| 55 dB | valid isolated full-window outage in earlier clean stage | selected Q3 |

Clean +41 evidence commit: `ae2baa30065c606f54d819ff2c6610b10fe30bdc`
Clean +42 evidence commit: `41011cee93f5ab100061edfc2076d966e44824d9`

## Invalid / excluded calibration episodes
Repeated RLF/re-attach activity eventually produced a stale/dead user-plane bearer. At 0 dB the UE still held an IP address but:
- UE -> SGi Q0 health check failed 0/5;
- EPC -> UE reverse check failed 0/3.

Therefore later classifications made while that bearer was stale are technically invalid for RF-state inference. This includes the contaminated 48/50/52/54 sweep, 42/44/46/47 boundary sweep, and the first +41 attempt. Those raw observations remain preserved but must not be used to define Q2/Q3.

Relevant technical-evidence commits:
- contaminated 48-54 sweep: `9fa053d9b38a69bd6655668a2fcbd148aef90b98`
- contaminated interpretation follow-up: `14845fd556fc7cb60aef9d70d68c7d2d393c7b4a`
- contaminated 42-47 boundary: `8df86670324756a276c81159c73e1cf7878a9fbb`
- invalid first +41 / stale-bearer diagnosis: `a67126b2fdbf30f69b1038e45d63e5d3547b8d67`

Scientific rule: a failed Q0 user-plane readiness check invalidates subsequent RF-state classification until the bearer is cleanly restored.

## Frozen RF-state table

| State | Programmed additional attenuation | Semantic definition | Calibration evidence |
|---|---:|---|---|
| Q0 | 0 dB | strong/stable reference | 0% loss; RSRP ~-60 dBm; SNR ~40-45 dB |
| Q1 | 40 dB | degraded but continuously connected | RSRP ~-100 dBm; SNR ~18-19 dB; continuous replies |
| Q2 | 52 dB | near-threshold/intermittent | 6 replies / 12 misses in exact clean 20 s window; Q0 recovery PASS |
| Q3 | 55 dB | effective application-data outage | essentially full 20 s user-plane outage; recovery after Q0 reset |

## Reproduction rules for future runs
1. Set all four path IDs together; never change only a subset.
2. Begin from Q0=0 dB and pass a user-plane readiness check before applying any scored RF schedule.
3. Use timestamped RF-transition logs and a timestamped data-plane probe so results can be reconstructed by exact time window.
4. After every impairment stage, restore Q0 and verify the bearer is healthy before accepting the stage as technically valid.
5. Preserve invalid runs and label them; never replace an unfavorable scientific result, only a technically invalid run under the frozen protocol rule.
6. Do not infer RF state from attach/IP presence alone; the user plane must also be verified.
7. The values in this ledger are for the frozen `srslte-controlled-rf` profile/revision and this conducted path; a materially different RF profile/path requires new non-scored calibration.

## Paper-use note
For the manuscript/methods section, report the semantic state definitions, frozen programmed attenuation values, representative radio context, exact calibration principle, and the Q0 technical-readiness rule. The complete exploratory history and invalid stale-bearer episodes belong in the reproducibility/evidence package rather than the main results narrative.
