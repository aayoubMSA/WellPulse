# WP2-H1 GitHub Salvage Package — 2026-08-27

Evidence class: **DERIVED_GIT_GITHUB_SALVAGE**  
Experiment: `WP-HCAL-E`  
Experiment UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`  
Run: `wp2h1-a1-20260826-001`  
Frozen classification: `VALID_W1_RECOVERY_FAILURE`  
Scored: `false`

## Salvage verdict

`H1_GITHUB_SALVAGE=PASS`

`H1_FULL_RAW_FROM_GITHUB=NOT_RECOVERED`

`H1_DERIVED_LOG_EVIDENCE=AVAILABLE`

`H1_RECORD_LEVEL_RECONSTRUCTION_FROM_GITHUB=BLOCKED`

`RS1_RAW_RECONSTRUCTION=BLOCKED_ON_RAW_BUNDLES`

This package consolidates the H1 evidence that still exists in Git and GitHub. It does **not** recreate the missing raw record-level corpus. Narrative summaries, sanitized log excerpts, counts, timestamps, hashes, commit history, and recovery-characterization records are secondary evidence and must never be represented as raw data.

## 1. Authority and storage correction

Historical 2026-08-26 records described `/users/aayoub/wellpulse-powder-evidence/...` as persistent POWDER home storage. Later lifecycle review established that this location was not durable for the relevant experiment teardown lifecycle. The H1 node archives were not escrowed to `/proj/WellPulse` or copied off POWDER before the experiment was destroyed.

Therefore the current handover and this salvage package supersede the historical **storage characterization**, while preserving the old records unchanged as provenance. The SHA-256 values remain integrity anchors for the historical archive bytes, but the bytes are presently unavailable for independent re-hashing or record-level analysis.

## 2. Experiment identity that survives in Git

- Profile: `PowderProfiles/srslte-controlled-rf`
- Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- Logical/physical binding: `enb1 -> nuc1`, `rue1 -> nuc2`
- Image recorded pre-H: `PowderProfiles:U18LL-SRSLTE:1`
- Exact deployed WellPulse H source commit: `95ba9a57bef159450b00b8a439d393d22e1c0519`
- Pre-H isolated runtime: Python `3.11.16`, Paho MQTT `2.1.0`, Mosquitto `2.0.20`, isolated OpenSSL `3.6.4`
- MQTT application contract: MQTT v3.1.1, QoS1, TLS, fresh session (`session_present=false`)

## 3. H1 derived quantitative record

The surviving Git-native H1 record reports:

- Q0/Q3 schedule: Q0 -> Q3 at `55 dB` -> Q0 restoration
- Q3 full-state duration: `120.000117905 s`
- RF restoration / primary-cohort cutoff: `2026-08-26T18:16:00.428045+00:00`
- generated records: `361`
- primary cohort records: `211`
- final pending count: `270`
- application inflight: `20`
- publish calls: `111`
- PUBACK callbacks: `91`
- queue pending zero: not reached
- initial MQTT session present: `false`
- MQTT connected at final snapshot: `false`
- Q0 pre-readiness health: `5/5` ping PASS over `tun_srsue`
- post-restoration health: `0/3` ping
- sender status: `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`
- sender return code: `20`

These values are **derived/live-captured summaries** retained in Git. Without the original raw files they cannot be independently recomputed record-by-record from GitHub alone.

## 4. Failure chronology retained in Git

The surviving diagnostic record states:

1. The UE process remained alive and `tun_srsue` remained UP at `172.16.0.2/24` after RF restoration, but user-plane packets did not traverse.
2. The eNB later decoded uplink traffic with CRC OK at approximately `33 dB` SNR, supporting physical/radio recovery rather than an eNB process crash.
3. EPC/MME/SPGW evidence showed repeated attach/session-context churn, including:
   - repeated attach requests for the test IMSI;
   - `UE Context already exists`;
   - an active GTP-C connection during Create Session processing;
   - failed old-tunnel deletion lookup;
   - successive UE IP allocations `.3` through `.7` while the UE tunnel retained `.2`;
   - UE-side attach/release/radio-link-failure loops.
4. The preserved interpretation is that the dominant H1 non-recovery was below the WellPulse application layer, in LTE core/session-context/IP continuity behavior. This does not prove failure of the WellPulse durable queue.

The frozen scientific classification nevertheless remains `VALID_W1_RECOVERY_FAILURE` because the required user-plane recovery did not occur inside the prospectively bounded trial.

## 5. Recovery characterization retained in Git

| Recovery action | Result | Derived evidence retained |
|---|---|---|
| UE-only restart | `FAIL` | Cell rediscovery/RRC connection occurred, but usable attach did not recover; final elapsed about 96 s. |
| EPC/eNB reset with UE left running | Core/RAN reset `PASS`; user-plane recovery `FAIL` | Q0 user plane did not return within the bounded check (~61 s). |
| Clean ordered restart: stop UE -> EPC -> eNB -> fresh UE | `PASS` | `tun_srsue` returned at `172.16.0.2`; 10/10 Q0 packets, 0% loss; RTT `12.947/19.176/25.593/3.953 ms`. |

The clean-order restart is operational/testbed recovery knowledge only. It is not a retroactive repair of H1 and is not an authorized in-trial scientific treatment unless frozen prospectively in a future amendment.

## 6. Post-recovery application-path evidence

After clean-order LTE recovery, three independent fresh sessions passed the full application path:

`LTE user plane -> TLS -> MQTT v3.1.1 -> QoS1 SUBACK/PUBACK -> broker round-trip -> payload hash equality`

| Qualification | Payload SHA-256 | Preserved evidence-record SHA-256 | Result |
|---:|---|---|---|
| 1 | `a8b348847f2dff2032155d33bee8799628b79b8699304c90d96b6011615dfb6a` | `fa7e34b289b32f48fcc3805d28cdc6643d95503f976815179767d8c604371e3a` | PASS |
| 2 | `4874e3e5ac18c85cf3e3dc4fa47d9e322e1b1c9c7e456b0be0afbd770ab77a4d` | `4031016406085535b9582d2b19ffdb955b6eb5bcb7d6931c452c19a876391cc0` | PASS |
| 3 | `9645bf064a5e4d3a4935067d481dedc106f8c8cd2ca2bb2c82452f988fdfc023` | `4f1b25fb8f7ba62dc8ab02ae2429fcdc56f26b9580e0e5b76429aab4c6153e61` | PASS |

`WP2_POST_RECOVERY_APP_REPEATABILITY=3_OF_3_PASS`

This supports the recovered operational path only; it does not change H1 or freeze H.

## 7. Historical archive and integrity anchors

### Original H1 node archives

- nuc1: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

### Recovery-characterization archives

- nuc1: `71aaea25a50ad955fa797a358b14cce4efc0e76ec0861468b3b99dd224c7dd55`
- nuc2: `431855c8662fa46a82f7baca60b5f3deeda4fd849cf4d90bfc4889800be3e71d`

### Reproducibility fingerprints

- nuc1 runtime record: `1ef8b04a8d3a634c1cc3ded2b84c80a7140d877758a0d63010411971eab8607f`
- nuc1 reproducibility archive: `af601716237082be410be3680f1e33b36240beae77e7b644f0f5bef811c1b647`
- nuc2 runtime record: `fc1c131602c49b8376733ad8e190c4fc5d8d1976b62fe59c1e5becbe41cf8d5a`
- nuc2 reproducibility archive: `ada35310a2dd46dba6c28a26604d41f28884799e0fc27c0846a7bf66421935bc`

### Node-local chain-of-custody manifests

- nuc1: 22 files; manifest SHA-256 `9596f23f4e9359d3395f29f6e0081d5acdec05dc6a986c0e0b0f19ac5fa35811`
- nuc2: 34 files; manifest SHA-256 `343a9deb1e432c0f5d30cbf55def3d133726a214a595d9f7f0723a5e87d8ec2e`

**Current availability:** hash values AVAILABLE; archive/manifest bytes NOT AVAILABLE from current user-accessible persistent storage or GitHub.

## 8. Git/GitHub provenance anchors

- `9cd7789a8960fd396ba35806127c16251ea8574a` — initial H1 valid-recovery-failure record and LTE diagnosis, committed `2026-08-26T18:23:18Z`.
  - GitHub Actions runs associated with this head SHA: **0**.
- `375f767bae237729458f558b1c64c60633c00673` — recovery archive hash record, committed `2026-08-26T18:36:54Z`.
  - GitHub Actions runs associated with this head SHA: **0**.
- `37c0924d673da6f62228ff65e03dd591e0d48224` — UE-only recovery failure characterization.
- `4a49a904eb249bc64cd4a7d7d01eb04d3e1a6fba` — clean-order LTE recovery characterization.
- `5572476040e59089aa04e97ce5e9d38da62e4d81` — 3/3 recovered application-path repeatability.
- `fd3978dacfc541e985a8daae9aa362b3c727c5fa` — reproducibility fingerprints.
- `f6ff776a15a8b15fa01d9d643c0d735cf18da0d5` — operator-history snapshot description.
- `74722415dc6e6f0fff6af023d8e7efffd998be3b` — session-level evidence closeout.
- Pre-H live SSH workflow run `32993568290` has **0 uploaded Actions artifacts**.

GitHub therefore preserves the audit trail and derived evidence, but not the raw H1 experiment corpus.

## 9. Git repository raw-data check

At salvage time:

- `data/raw/` contains only `.gitkeep`.
- `results/runs/` contains only `.gitkeep`.
- no H1 CSV/JSONL/SQLite/tar raw bundle is present in these canonical Git paths.

## 10. Raw artifacts required for true RS-1 reconstruction but unavailable

The raw-based RS-1 procedure requires, at minimum, the H1 sender artifacts:

- `sender_summary.json`
- `calibration_manifest.json`
- `attenuation_timeline.csv`
- `telemetry_generated.csv`
- `queue_timeline.csv`
- `mqtt_events.jsonl`
- `w1_queue.sqlite`

It additionally requires receiver raw events/record identities and the full UE/eNB/EPC/SPGW logs for record-level and cross-layer reconciliation.

These bytes are not present in GitHub and are not currently recoverable from the terminated POWDER node-local storage.

## 11. Reconstruction limits

From GitHub alone it is **not** scientifically defensible to independently recompute or verify:

- every generated record identity and timestamp;
- primary-cohort membership record-by-record;
- duplicate/missing record counts from sender vs receiver raw streams;
- queue trajectory and exact durable-state transitions;
- exact attenuation event timeline from the original CSV;
- MQTT publish/PUBACK event ordering from the original JSONL;
- SQLite queue contents/state counts;
- receiver-side record-level reconciliation;
- the complete LTE/EPC/eNB/UE chronology from full raw logs;
- the historical archive hashes against the original bytes.

Consequently, the existing `docs/RS1_OFFLINE_RECONSTRUCTION.md` remains a valid raw-reconstruction method, but **RS-1A through RS-1E cannot be closed from GitHub alone while the raw bundles are unavailable**.

## 12. What remains scientifically usable

The Git-native evidence is sufficient to preserve:

- experiment/run identity and provenance;
- H1's frozen adverse classification;
- the bounded high-level quantitative summary;
- the distinction between RF restoration and failed user-plane/service recovery;
- the documented below-application-layer failure localization;
- recovery-characterization outcomes;
- post-recovery transport repeatability;
- historical integrity/hash anchors;
- explicit evidence-loss limitations and threats to reproducibility.

It is **not** sufficient to upgrade H1 into a record-level reconstructed dataset or to make new quantitative claims that require the missing raw corpus.

## 13. Forward evidence rule

All future POWDER Golden/calibration/scored sessions must preserve raw evidence before teardown through the fail-closed sequence:

`freeze writers -> inventory raw -> SHA-256 manifest -> /proj/WellPulse persistent escrow -> verify -> off-POWDER copy -> read-back/hash verify -> provenance record -> teardown authorization`

Required before teardown:

`RAW_EVIDENCE_COMPLETE=PASS`

`EVIDENCE_ESCROW_GATE=PASS`

`TEARDOWN_AUTHORIZED=YES`

## 14. Scientific state after salvage

H1 remains `VALID_W1_RECOVERY_FAILURE`.

`H=UNFROZEN`

`scored_runs_authorized=false`

`REBOOK_GOLDEN=false`

No scientific completion credit is added by this salvage patch.