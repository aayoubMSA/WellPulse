# WellPulse — Current Handover

Last updated: 2026-08-26, after WP2-H recovery-horizon implementation preflight, Africa/Cairo

## Standing handover rule

No material project state may exist only in chat. Decisions, results, artifacts, blockers, evidence boundaries, milestone percentages and the exact next action must be recoverable from GitHub and/or Drive.

## Executive state

- FIT IoT-LAB scientific evidence layer: **FINAL PASS**.
- POWDER G0–G4: **PASS**.
- POWDER G5 RF impairment/control + numeric RF-state calibration: **PASS**.
- Old G5 experiment UUID `575d246e-8d01-4827-9a84-f4368d272cea`: **ABSENT / CLEANUP PASS** as of 2026-08-26T00:14:52Z; no scientific action occurred during cleanup.
- WP0 Novelty & Venue Lock: **8/8 PASS**.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 design complete**; comparator sufficiency still open pre-score.
- WP2 RF Calibration & Measurement Validation: **IN PROGRESS**.
  - numeric RF-state calibration: **PASS / FROZEN**;
  - common recovery-horizon `H` design: **FROZEN**;
  - W1 H-calibration implementation: **IMPLEMENTED + LOCALLY VERIFIED**;
  - physical W1 H-calibration observations: **NOT YET EXECUTED**;
  - remaining measurement/evidence/comparator pre-score gates: **OPEN**.
- WP3: **0/30 — BLOCKED** by WP2 + comparator freeze + explicit scored authorization.
- WP4: **0/15 — BLOCKED** by WP3.
- WP5: **0/20 scientific closure**.
- Gate-based scientific weighted completion remains **20%** until WP2 closes.
- `scored_runs_authorized = false`.

No G5 calibration observation and no WP2-H implementation test is a scored B1/W1 scientific result.

## Canonical repositories and workspaces

- GitHub: `aayoubMSA/WellPulse`.
- Drive project root `P12_WellPulse`: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`.
- Drive validation workspace `00_Validation_Workspace`: `1SydHCA2jlkatxdGgUtJ1P8atgyi8_ta3`.
- Drive raw evidence `02_RAW_EVIDENCE`: `11xaitxG0vkV6fCzK_JgLAacrdhjz7GBf`.
- Drive handover folder `WellPulse Handover`: `1Du4j_YkMLvQjWJCxV5zqxxK6OGG2Q0hA`.
- Clean G5 snapshot: `docs/handovers/2026-08-26_G5_RF_CALIBRATION_HANDOVER.md`.
- WP2-H calibration plan: `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`.
- WP2-H implementation preflight: `evidence/local/wp2-h-preflight-latest.md`.

## Frozen scientific design

Canonical protocol remains `experiments/WP-PWD01/protocol.md` v0.4.

Primary comparison remains:

- `B1_MQTT_QOS1`: Paho Python MQTT v3.1.1, QoS1, TLS on scored path, automatic reconnect, `clean_session=False`, volatile client state, no application-level disk durability/reconciliation.
- `W1_OFFLINE_FIRST`: same low-level Paho session plus SQLite durable application queue, stable record identity/checksum, replay, idempotent receiver and reconciliation.

Frozen low-level parameters: `paho-mqtt==2.1.0`, keepalive 60 s, reconnect 1–8 s, outgoing queue 4096, inflight 20.

Comparator caveat remains open: B1 is the clean matched same-implementation comparator but not the strongest durable MQTT client generally. Candidate `B2_MQTT_DURABLE_CLIENT` must be qualified/frozen before scoring if retained. Prefer a compact S2/S3 sensitivity amendment if B2 qualifies rather than expanding the entire primary matrix.

## G5 accepted experiment state and teardown

Historical non-scored G5 experiment:

- `WP-G5-RF-CAL`;
- UUID `575d246e-8d01-4827-9a84-f4368d272cea`;
- profile `srslte-controlled-rf`;
- profile revision `a6da96560b6526dc6816761282722c996418fd8c`;
- historical live binding `enb1 -> nuc1` (EPC/eNB), `rue1 -> nuc2` (UE);
- UE `172.16.0.2`, EPC SGi `172.16.0.1` after clean bearer restoration;
- attenuation path IDs `1 33 2 34`, always changed together.

The historical bindings above **must never be assumed for a new experiment**. Capture and verify new live logical-to-physical bindings every time.

At G5 handover the final commanded RF state was restored to 0 dB and the last explicit Q0 health check was 3/3 replies, 0% loss. The old experiment has since been verified absent by `evidence/powder/cleanup-latest.md`; no further G5 log-preservation or teardown action is required.

Fallback reservation remains available for `nuc1+nuc2` on **2026-08-26 19:00–22:00 Africa/Cairo**. Use it for unfinished WP2 validation, not RF hunting.

## RF calibration — FROZEN

Numeric authority: `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`.  
Calibration ledger: `evidence/powder/g5-rf-calibration-ledger-2026-08-26.md`.

| State | Programmed attenuation | Meaning | Accepted observation |
|---|---:|---|---|
| Q0 | **0 dB** | strong/stable | ~-60 dBm RSRP, SNR ~40–45 dB, BLER 0; clean user-plane PASS |
| Q1 | **40 dB** | degraded but continuously connected | ~-100 dBm RSRP, SNR ~18–19 dB; continuous ping |
| Q2 | **52 dB** | near-threshold/intermittent | clean isolated 20 s window: **6 replies / 12 misses**; clean Q0 recovery |
| Q3 | **55 dB** | effective application-data outage | first isolated valid 20 s outage with immediate recovery after Q0 reset |

Clean boundary checks after bearer restoration:

- +41 dB: 20 replies / 0 misses;
- +42 dB: 20 replies / 0 misses;
- +49 dB: 21 replies / 0 misses;
- +52 dB: 6 replies / 12 misses.

**No more attenuation sweep is authorized or scientifically useful.**

## Critical invalidity and safeguard

Repeated severe RLF/re-attach testing eventually produced a stale user-plane bearer while the UE still appeared attached and had an IP. The contaminated 48/50/52/54 sweep, 42/44/46/47 sweep, and first +41 attempt remain preserved for provenance but are excluded from canonical RF classification.

The bearer was restored by a bounded clean LTE reset and Q0 user-plane re-verification.

**Frozen safeguard:** before every future scientific/non-scored calibration or scored run, Q0 must pass an explicit end-to-end user-plane readiness check through the experimental radio path. Attached state or assigned IP alone is insufficient. If Q0 user-plane health fails, the run is technically invalid and must not enter the scientific corpus.

## WP2-H recovery-horizon design — FROZEN

Authority: `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`; Decision D-017.

Use exactly **three valid non-scored W1 hard-outage calibration trials**:

`30 s readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

Frozen rules:

- architecture: `W1_OFFLINE_FIRST` only;
- workload: 1 record/s;
- TLS enabled on the MQTT calibration path;
- Q0 = 0 dB, Q3 = 55 dB; attenuation IDs `1 33 2 34` move together;
- no Q1/Q2 sweep and no B1/S3/scored comparison in this calibration gate;
- `cohort_cutoff_utc` = exact final Q3 -> Q0 restoration timestamp;
- backlog drain completes only when both the pre-restoration cohort is complete at the sink with matching identity/checksum and the W1 durable queue has zero pending cohort records;
- empirical nearest-rank p95; for n=3, p95 is the maximum valid observed drain time;
- `H = max(120 s, ceil_to_30s(2 × p95))`;
- if calculated `H > 300 s`, **STOP AND INVESTIGATE**; never cap it;
- a technically invalid calibration trial is preserved as invalid evidence and excluded from the p95 calculation; replacement is allowed only for documented technical invalidity.

## WP2-H implementation — IMPLEMENTED + LOCALLY VERIFIED

Implemented components:

- `src/wellpulse/horizon.py` — deterministic percentile/H calculation;
- `src/wellpulse/powder_w1.py` — non-blocking durable W1 replay above the frozen Paho session;
- `scripts/wp_pwd01_h_sender.py` — route/Q0 readiness, 1 Hz generation, independent RF controller, queue evidence and fail-safe Q0 reset;
- `scripts/wp_pwd01_h_receiver.py` — TLS MQTT receiver attempt ledger with record identity and SHA-256;
- `scripts/finalize_wp_pwd01_h_calibration.py` — deterministic sink/queue drain reconstruction and H finalization;
- `powder/wp2_h_epc_broker.sh` — ephemeral TLS broker bootstrap with private keys excluded from evidence;
- `experiments/WP-PWD01/run-matrix.yaml` — reconciled to the frozen `srslte-controlled-rf` / Q0-Q3 state while keeping H and remaining pre-score gates open.

Dedicated local preflight `evidence/local/wp2-h-preflight-latest.md` passed on tested SHA `d8ab08df5f4cac7394e16c78097b8dc2ca192649`:

- 28/28 tests PASS;
- Python pilot scripts compile PASS;
- broker shell syntax PASS;
- frozen-state guards PASS;
- POWDER interaction NONE;
- scored-run interaction NONE.

This establishes **implementation readiness only**. The physical value of `H` is still unknown until the three valid POWDER trials execute.

## Current execution blockers

1. **No live fresh POWDER experiment exists now.** A new `srslte-controlled-rf` experiment must be instantiated during an available reservation and its live bindings verified.
2. **Automated SSH private-key path is known bad.** `evidence/powder/g3-key-format-diag.json` shows the current `POWDER_SSH_PRIVATE_KEY` Actions value is a public-key-form value rather than a private key. Do not trust that automation path until repaired or explicitly bypassed with the canonical local acceptance key. Never place a private key, passphrase, RPC token or credential-bearing manifest in Git/evidence/chat.

These are execution-access blockers, not scientific evidence against the H design or implementation.

## Remaining pre-score work

Do not authorize scored runs yet. Material open gates:

1. physically execute the frozen three-trial W1 H calibration and freeze `H`;
2. reproduce frozen Paho/runtime configuration on the remote path;
3. verify MQTT payload traverses the experimental cellular data path rather than the POWDER control network;
4. verify B1/W1 implementation matching and end-to-end identity/checksum preservation;
5. verify evidence capture and clock alignment for mandatory endpoints;
6. run deterministic analysis on a non-scored pilot bundle without manual spreadsheet edits;
7. close the B2 durable-client comparator decision/amendment;
8. repair or explicitly bypass the known-bad automated POWDER SSH path before scored automation is trusted.

Some of gates 2–6 should be closed using the same valid H-pilot bundle if the evidence is sufficient; do not create extra experiments merely to increase experiment count.

## Exact next action

At the next fresh `srslte-controlled-rf` experiment, and **only within WP2**:

1. capture experiment/profile identity and verify live logical-to-physical bindings;
2. start the profile-authoritative EPC/eNB and UE lifecycle;
3. pass explicit Q0 LTE user-plane readiness and verify the MQTT route uses `tun_srsue` toward `172.16.0.1`;
4. execute exactly three valid non-scored W1 H-calibration trials under the frozen plan;
5. preserve generated/received/queue/RF/clock/runtime evidence and bundle checksums;
6. run `finalize_wp_pwd01_h_calibration.py` to reconstruct the three drain times and calculate `H`;
7. if `H <= 300 s`, freeze it canonically; if `H > 300 s`, stop and investigate without capping.

Do **not** start WP3. Do **not** execute B1/W1/B2 scored cells. Do **not** reopen RF attenuation calibration. Do **not** change `scored_runs_authorized` until all remaining pre-score gates pass.

## Reproducibility read order

1. `HANDOVER_CURRENT.md`
2. `docs/handovers/2026-08-26_G5_RF_CALIBRATION_HANDOVER.md`
3. `docs/MILESTONE_STATUS.md`
4. `docs/STATUS.md`
5. `docs/DECISIONS.md`
6. `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`
7. `evidence/powder/g5-rf-calibration-ledger-2026-08-26.md`
8. `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`
9. `evidence/local/wp2-h-preflight-latest.md`
10. `experiments/WP-PWD01/protocol.md`
11. `docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`
12. `experiments/WP-PWD01/analysis-plan.md`
13. `experiments/WP-PWD01/evidence-schema.md`
14. `experiments/WP-PWD01/randomization-plan.csv`
15. `experiments/WP-PWD01/run-matrix.yaml`
16. `powder/MANUAL_GOLDEN_PATH.md`

Never infer future node roles from prior runs. Never persist secrets, private keys, passphrases, RPC tokens, credential blocks, or raw credential-bearing manifests.