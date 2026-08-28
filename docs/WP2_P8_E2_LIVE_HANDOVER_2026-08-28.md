# WP2-P8 E2 — Live Handover

Date: 2026-08-28
Repository: `aayoubMSA/WellPulse`
Branch: `main`
Platform: POWDER / srsLTE controlled RF
Campaign: `WP2-P8 — Modular Manual RF Experiment Campaign`
Current experiment: `P8-E2 — RF Hysteresis / Spontaneous Recovery`

## 1. Scientific boundary

This campaign is manual, exploratory, non-scored reference work. It does not alter the frozen historical scored P7B state.

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`
`P8_CAMPAIGN_CLASS=NON_SCORED_MANUAL_REFERENCE`

## 2. Live topology

- `nuc1 / CORE`: EPC, eNB, Mosquitto broker, MQTT receiver, reverse-path monitor.
- `nuc2 / UE`: srsUE, RF attenuation control, UE->CORE ping, MQTT publisher.
- Attenuators: `[1,33,2,34]`.
- Known healthy UE tunnel address during clean baseline: `172.16.0.2/24`.
- CORE LTE endpoint: `172.16.0.1`.

## 3. Three-screen operating layout

- `nuc1-A` top-left: visible MQTT receiver only.
- `nuc1-B` top-right: CORE->UE ping monitor and CORE-side evidence commands.
- `nuc2` bottom-right: RF treatment, UE->CORE ping, MQTT publisher, UE evidence.

All instructions must identify one of these roles explicitly. Do not collapse the experiment into a one-node B1-style script.

## 4. Completed campaign evidence

### P8-E0 — Stable baseline qualification

Clean two-node baseline was established before the valid threshold work:

- CORE->UE ping: 10/10, 0% loss.
- UE->CORE ping: 10/10, 0% loss.
- UE tunnel stable at `172.16.0.2/24`.
- `srsepc`, `srsenb`, `srsue` stable.
- 10/10 MQTT messages visibly delivered from nuc2 to nuc1-A.

`P8_E0_BASELINE_QUALIFIED=PASS`

### P8-E1 initial attempt

Initial E1 raw evidence was preserved but analysis showed the nominal baseline was already unhealthy before treatment. It is diagnostic only and is not valid for RF-threshold inference.

`P8_E1=NULL_ABORTED_INVALID_PRETREATMENT_BASELINE`
`EVIDENCE_INTEGRITY=PASS`
`DIAGNOSTIC_VALUE=HIGH`

### P8-E1R2 — 0 to 30 dB

Clean run with bidirectional connectivity and MQTT completeness through 30 dB.

- MQTT generated/received: 65/65.
- missing: 0.
- duplicates: 0.
- packet loss: 0% at every tested point through 30 dB.

Off-platform archive hashes:

- CORE: `A8DBA3B486FA9E86CCD80E8704DA2AE277BACC6998C5B4292B53C52BBBD62B4A`
- UE: `7A1C2F2F32DF22E6C0B2E0F3A4480C8A7D7B64C290129AE84FC5E47F181E348B`

`P8_E1R2_OFFPLATFORM_PRESERVATION=PASS`

### P8-E1R3 — 30 to 50 dB

Clean extension located the first degraded region.

- 48 dB: known-good.
- 50 dB: first confirmed packet-loss degradation.
- 50 dB confirmation: 20 transmitted / 19 received / 5% loss; RTT min/avg/max approximately 28.142/43.581/90.091 ms.

Off-platform archive hashes:

- CORE: `00699132F302018585972A81503E464272B2BACE3E85DDA9A94D224C844B13E5`
- UE: `0C32700B3A4751EFFA7B7109614E64A9425AB874068E372AC365B5CE3AB4E837`

`P8_E1R3_OFFPLATFORM_PRESERVATION=PASS`

### P8-E1R4 — 48 to 52 dB micro-sweep

Raw archives were preserved off-platform and analyzed. Derived profile:

| Attenuation | UE->CORE ping loss | CORE->UE ping loss | MQTT received | Mean app delay |
|---:|---:|---:|---:|---:|
| 48 dB | 0% | 0% | 20/20 | ~98 ms |
| 49 dB | 0% | 0% | 20/20 | ~92 ms |
| 50 dB | 0% | ~3.3% | 20/20 | ~170 ms |
| 51 dB | ~30% | ~30% | 20/20 | ~448 ms |
| 52 dB | ~60% | ~64% | 13/20 | ~8.0 s |

Independent 52 dB confirmation: 30 transmitted / 6 received / 80% loss.

Missing MQTT sequences at 52 dB: `82,84,90,91,92,96,97`.

After restoring RF to 0 dB without service restart:

- 20/20 ping, 0% loss.
- mean RTT approximately 22.6 ms.
- 10/10 recovery MQTT messages received.

Interpretation frozen for exploratory use:

- `<=49 dB`: healthy region.
- `50-51 dB`: degrading but application-resilient region.
- `>=52 dB`: severe intermittent region with application loss.

Off-platform archive hashes:

- CORE: `70F3CF784517ABB32D98F33118634FD48B736DB5EC5F46C54556E57A2237DD25`
- UE: `4CE3CEBEF0292E8276B46B1249A95E4766CE6E0E060843346E772D811AB8838F`

`P8_E1R4_OFFPLATFORM_PRESERVATION=PASS`
`P8_E1R4=FROZEN`

## 5. P8-E2 — RF hysteresis / spontaneous recovery — COMPLETE

Scientific question: does recovery occur at the same RF condition at which degradation appears, or is there hysteresis/state dependence; can the stack recover autonomously without service restart?

Run ID:

`p8-e2-20260828A`

Treatment sequence:

`0 -> 52 -> 51 -> 50 -> 49 -> 48 -> 46 -> 0 dB`

No `srsue`, `srsepc`, `srsenb`, or Mosquitto restart occurred during treatment/recovery.

### UE->CORE ping results on descending recovery path

| Attenuation | Received | Loss | Mean RTT |
|---:|---:|---:|---:|
| initial 0 dB | 20/20 | 0% | 22.803 ms |
| 52 dB | 7/20 | 65% | 59.909 ms |
| 51 dB | 18/20 | 10% | 41.312 ms |
| 50 dB | 20/20 | 0% | 40.341 ms |
| 49 dB | 20/20 | 0% | 31.318 ms |
| 48 dB | 20/20 | 0% | 34.717 ms |
| 46 dB | 20/20 | 0% | 36.158 ms |
| final 0 dB | 20/20 | 0% | 24.900 ms |

### MQTT reconciliation

160 messages were generated; 151 were received. All 9 missing messages occurred at 52 dB. Every message sent from 51 dB downward was received.

| Attenuation | Sent | Received | Missing | Mean app delay | Median | Max |
|---:|---:|---:|---:|---:|---:|---:|
| initial/final 0 dB combined | 40 | 40 | 0 | 68.3 ms | 68.7 ms | 70.1 ms |
| 52 dB | 20 | 11 | 9 | 2555 ms | 2140 ms | 8088 ms |
| 51 dB | 20 | 20 | 0 | 454 ms | 347 ms | 1361 ms |
| 50 dB | 20 | 20 | 0 | 158 ms | 115 ms | 409 ms |
| 49 dB | 20 | 20 | 0 | 96.8 ms | 93.2 ms | 138 ms |
| 48 dB | 20 | 20 | 0 | 86.6 ms | 82.4 ms | 129 ms |
| 46 dB | 20 | 20 | 0 | 69.2 ms | 68.8 ms | 77.6 ms |

UE-side command-level MQTT failures at 52 dB were recorded for sequences `22,23,24,29,33,36,38,39,40`; receiver reconciliation is authoritative for application completeness.

### Exploratory interpretation

E2 demonstrates autonomous cross-layer recovery while attenuation is reduced, without any service restart. Severe impairment is present at 52 dB. By 51 dB, MQTT completeness has recovered to 20/20 while ICMP still shows 10% loss and elevated RTT. By 50 dB, forward ICMP completeness is 20/20 and MQTT remains complete, though latency remains elevated versus baseline. By 49 dB and below, the path is effectively back in the healthy regime.

This supports a recovery transition centered approximately between 52 and 50 dB, with application completeness recovering earlier than full latency normalization. It is evidence of state-dependent recovery behavior, but one manual reference run is not sufficient for a publication-level probabilistic hysteresis claim. P8-E3 repeatability is therefore still required.

`P8_E2_EXECUTION=PASS`
`P8_E2_SPONTANEOUS_RECOVERY=OBSERVED`
`P8_E2_SERVICE_RESTART_REQUIRED=NO`
`P8_E2_MQTT_RECOVERY_BY_51DB=20_OF_20`
`P8_E2_FORWARD_PING_RECOVERY_BY_50DB=20_OF_20`

## 6. E2 evidence preservation — PASS

The one-end home-PC evidence controller v1.2 was used after experiment writers were quiesced. The first preservation prototype correctly exposed a live-writer race on `CORE/core_monitor.log`; v1.2 closes that race by quiescing experiment-only evidence writers before hashing.

Freeze controller timestamp:

`2026-08-28T19:44:48.0323478Z`

Verified archive SHA256:

- CORE: `DEF0BC6FB44687E5375699932C8EA6C5A5D87B5B43CC333B4C4E82540EA1E719`
- UE: `8A1AB7F0221A83EFD25827F65D7D6C2398B1CDC02EE7E879F57E3C93D4C6AA73`

The receipt records:

- `EXPERIMENT_WRITERS_QUIESCED=PASS`
- `PER_FILE_VERIFICATION=PASS`
- `OFFPLATFORM_PRESERVATION=PASS`

`P8_E2_OFFPLATFORM_PRESERVATION=PASS`
`P8_E2_RAW_EVIDENCE=FROZEN_VERIFIED`
`ONE_END_PULL_V1_2=PASS`

## 7. Evidence storage doctrine

Raw experiment archives should NOT be committed directly to normal Git history as the primary store.

Recommended split:

### Google Drive = durable raw evidence store

Store immutable per-run CORE/UE archives, hashes, manifests, and later publication-ready raw-evidence packages under the WellPulse validation/evidence workspace. Drive is preferred for binary raw archives because it avoids repository bloat and preserves the original bundles separately from code.

### GitHub = canonical scientific control plane

Commit only:

- experiment contracts/plans;
- run manifests and SHA256 values;
- analysis scripts;
- derived CSV/JSON tables small enough for review;
- reconciliation outputs;
- concise results/closure documents;
- Drive artifact pointer/ID and digest;
- handovers.

Do not duplicate large raw archives into Git unless there is a deliberate Git LFS release policy.

### Home PC = temporary independent third copy

Keep the verified local copy until Drive upload/read-back verification is complete. Do not treat PC-only storage as canonical.

Recommended preservation chain:

`POWDER node-local raw -> quiesce experiment writers -> remote per-file manifest -> direct SSH stream to home PC -> local archive hash -> local extraction/per-file verification -> Drive immutable upload -> Drive read-back/hash verification -> GitHub manifest/pointer/results`

Do not release a reservation while unique raw evidence exists only on POWDER.

## 8. Next experiment

Remain inside the existing P8 WP. Do not drift.

Next:

`P8-E3 — Near-threshold Repeatability`

Purpose: repeat the near-threshold transition enough to determine whether the E1/E2 50-52 dB behavior is reproducible rather than a one-run state artifact.

Remaining planned experiments after E3:

1. `P8-E4` RF-only recovery;
2. `P8-E5` UE-restart recovery;
3. `P8-E6` CORE-restart recovery;
4. `P8-E8` broker-only fault control;
5. `P8-E9` duration-matched no-fault control;
6. `P8-E7` combined recovery stress case, only if time/value remains.

E2 already supplies strong RF-only spontaneous recovery evidence. After E3 repeatability, decide whether E4 can be narrowed rather than duplicated.

## 9. Stop state

`WP2_P8_STATUS=ACTIVE`
`P8_E2_STATE=COMPLETE_FROZEN_VERIFIED`
`CURRENT_EXPERIMENT=P8-E3_NEXT`
`LAST_RUN_ID=p8-e2-20260828A`
`SCORED_P7B_STATUS=UNCHANGED`
`RAW_STORAGE_POLICY=DRIVE_PRIMARY_GITHUB_MANIFEST`
`LIVE_TEARDOWN=NOT_YET`
