# AGENT HANDOVER — WellPulse POWDER Validation Owner

**Handover timestamp:** 2026-08-26 16:25 Africa/Cairo  
**Canonical repository:** `aayoubMSA/WellPulse`  
**Canonical branch:** `main`  
**Current scientific completion:** **20%**  
**Current scientific frontier:** **WP2 — physical W1 H calibration**  
**Scored authorization:** `scored_runs_authorized = false`

## 1. Mandate

Own continuation of the WellPulse POWDER validation lane from the current verified G0–G5 / frozen-RF state through the smallest defensible publication-grade validation package.

Optimize for:

`scientific value × reproducibility × reviewer defensibility ÷ execution risk × unnecessary scope × resource cost`

Do not reopen frozen science, do not broaden scope because POWDER exposes more capabilities, and do not treat infrastructure activity as scientific percentage.

## 2. Mandatory read order before any POWDER action

Do not reconstruct state from chat history. Read the repository in this order:

1. `HANDOVER_CURRENT.md`
2. `powder/PRE_EXPERIMENT_GATE_2026-08-26.md`
3. `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`
4. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
5. `experiments/WP-PWD01/PRE_SCORE_P1_AMENDMENT_2026-08-26.md`
6. `docs/MILESTONE_STATUS.md`
7. `docs/STATUS.md`
8. `docs/DECISIONS.md` — especially D-016 through D-020
9. `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`
10. `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`
11. `experiments/WP-PWD01/B2_SEMANTICS_GATE_v1.md`
12. `evidence/local/wp2-b2-semantics-latest.md`
13. `evidence/local/wp2-h-preflight-latest.md`
14. `experiments/WP-PWD01/protocol.md`
15. `experiments/WP-PWD01/analysis-plan.md`
16. `experiments/WP-PWD01/evidence-schema.md`
17. `experiments/WP-PWD01/randomization-plan.csv`
18. `experiments/WP-PWD01/b2-sensitivity-plan.csv`
19. `experiments/WP-PWD01/run-matrix.yaml`
20. `powder/MANUAL_GOLDEN_PATH.md`

Treat GitHub plus the Drive `WellPulse — Current Handover Index` as systems of record. If they disagree, stop and reconcile before execution.

## 3. Executive scientific state

- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- WP0: **8/8 PASS**.
- WP1: **12/12 design complete; P0/P1 frozen; B2 local semantics PASS**.
- WP2: **ACTIVE — physical H calibration is the scientific frontier**.
- WP3: **0/30 — BLOCKED**.
- WP4: **0/15 — BLOCKED**.
- WP5: **0/20 scientific closure**.
- Weighted scientific completion remains **20%** until WP2 closes.
- No scored B1/W1/B2 run is authorized.

Infrastructure success, booking activity, SSH qualification, H calibration attempts, and B2 local semantics do not independently increase scientific percentage.

## 4. POWDER infrastructure state

- G0 Account + `WellPulse` project — **PASS**.
- G1 Manual provisioning — **PASS**.
- G2 explicit-key SSH + teardown — **PASS**.
- G3 simulated LTE stack/data path — **PASS**.
- G4 controlled physical-RF lifecycle — **PASS**.
- G5 controlled attenuation / numeric RF calibration — **PASS / FROZEN**.

Historical G5 accepted profile:

- profile: `PowderProfiles/srslte-controlled-rf`
- profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- historical experiment UUID: `575d246e-8d01-4827-9a84-f4368d272cea`
- historical binding: `enb1 -> nuc1`, `rue1 -> nuc2`

These bindings are historical evidence only. Every future experiment must verify its own live manifest.

## 5. Frozen RF calibration — DO NOT REOPEN

- `Q0 = 0 dB` — strong/stable.
- `Q1 = 40 dB` — degraded but continuously connected.
- `Q2 = 52 dB` — near-threshold/intermittent; clean 20 s evidence = 6 replies / 12 misses.
- `Q3 = 55 dB` — effective application-data outage.
- attenuation IDs: `1 33 2 34`, changed together.

No further attenuation hunting is authorized.

Every scientific/non-scored/scored run requires explicit **Q0 end-to-end LTE user-plane PASS**. Attach state and UE IP are insufficient because a stale bearer was previously observed.

## 6. H calibration — exact active frontier

H is one common post-restoration observation horizon, frozen before scored work and used unchanged for all arms/scenarios.

Successful non-scored W1 trial:

`30 s readiness -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

Frozen W1 configuration includes:

- 1 record/s;
- Paho MQTT `2.1.0`;
- MQTT v3.1.1;
- QoS1;
- `clean_session=False`;
- keepalive 60;
- reconnect 1–8;
- queue 4096;
- inflight 20;
- SQLite WAL + `synchronous=FULL`;
- TLS required;
- run-isolated client IDs/topic;
- first fresh connection requires `session_present=false`.

Outcome classes:

- `TECHNICALLY_INVALID` — preserve; replacement allowed only for predefined infrastructure/protocol invalidity.
- `VALID_W1_RECOVERY_FAILURE` — preserve; not replaceable as invalid; blocks H freeze and requires investigation.
- `VALID_W1_RECOVERY_SUCCESS` — exactly three successful trials required; no extra successful calibration trials.

Drain semantics:

- cutoff = final Q3→Q0 transition;
- all pre-restoration cohort records must arrive with valid identity/checksum;
- pending durable cohort must reach zero;
- drain completion = max(sink cohort complete, queue pending zero).

With exactly three successes, nearest-rank p95 is the maximum observed successful drain time.

`H = max(120 s, ceil_to_30s(2 × p95))`

If `H > 300 s`, **STOP AND INVESTIGATE; never cap**. If backlog is not drained by 150 s after restoration, stop because later success would imply H > 300 s.

## 7. Comparator and claim freeze

Primary matched comparator:

`B1_MQTT_QOS1`

WellPulse arm:

`W1_OFFLINE_FIRST`

B2 sensitivity comparator:

`B2_MQTT_DURABLE_CLIENT`

B2 is already locally qualified with Eclipse Paho Java 1.2.5 + file persistence + persistent disconnected buffer: three trials each recovered `5/5 unique, 0 missing, 0 duplicates` after broker outage and abrupt client-process destruction.

If later scored authorization is explicitly granted, B2 scope is fixed to exactly:

- 3 B2 S2 runs;
- 3 B2 S3 runs;
- no B2 S0/S1;
- no adaptive B2 replication;
- B2-vs-W1 remains non-primary sensitivity analysis.

The confirmatory story is failure-domain bounded. Primary inferential endpoint remains unique primary-cohort completeness at common H. Do not claim a separately powered recovery-time advantage. Use `cross-testbed consistency` / `triangulation`, not broad transportability. Claim remains bounded to 1 Hz low-rate telemetry.

## 8. Credential and automation readiness — CURRENT

The next agent must **not** ask the user to paste or recreate secret values unless independent evidence shows a credential has actually failed.

GitHub Actions currently has the required secure runtime material:

- `POWDER_API_TOKEN` — official Portal API authentication proven;
- `POWDER_SSH_PRIVATE_KEY` — valid private-key structure;
- `POWDER_SSH_KEY_PASSPHRASE` — unlock proven;
- SSH identity loads into `ssh-agent` successfully;
- corresponding public key has been registered with POWDER for future experiment instantiations.

Current automation SSH identity fingerprint observed during validation:

`SHA256:/oW1viOGqRKnPVgLPqE1qKDohVeQ0QALXQX/XNyGkDQ`

Historical manual Golden-key fingerprint remains:

`SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`

Do not confuse the two identities.

Important boundary: the current automation key is **credential-ready but not yet accepted on both nodes of a fresh READY experiment**. The 14:00 experiment was instantiated before that public key was registered, so its SSH failure does not prove the newly registered path is invalid.

Portal API capabilities already exercised successfully include list/get/manifests/create/terminate and parameter bindings. No secret value belongs in Git, chat, evidence, or logs.

## 9. 2026-08-26 14:00–16:00 operational window — CLOSED / SCIENTIFICALLY CLEAN

Reservation resources: `nuc1+nuc2`.

Observed sequence:

1. `WP-HCAL-A` reached READY.
2. UUID: `cf31bf66-bebe-48f3-81e0-7812e9f0a6c9`.
3. Live profile/bindings were correct: `enb_node=nuc1`, `ue_node=nuc2`, `ue_type=srsue`.
4. Physical manifest verified `enb1 -> nuc1`, `rue1 -> nuc2`.
5. SSH using the current work-PC/GitHub key failed because that key had not been injected into this already-instantiated experiment.
6. The public key was registered in POWDER.
7. `WP-HCAL-A` was terminated and `WP-HCAL-B` was created immediately on the same reservation. It did not recover to READY.
8. `WP-HCAL-B` was terminated and a deliberate cooldown was allowed.
9. A positive resource-release gate then passed.
10. `WP-HCAL-C` was created successfully; UUID `8942bcec-bf88-42ed-b512-d466cb0f09cc`.
11. `WP-HCAL-C` oscillated between `provisioning` and `pending` for about 23 minutes and never reached READY.
12. After reservation expiry, final read-only API check found zero visible/active H-cal experiments: `FINAL_RELEASE_GATE=PASS`.

Scientific consequence: **zero H trials, zero scored runs, zero scientific RF actions in this window**. No evidence exclusion or statistical repair is required.

Key workflow provenance:

- recreate attempt: GitHub Actions run `32963561374`;
- guarded B release: `32964929263`;
- cooldown retry / C creation: `32967831937`;
- final read-only status: `32972461567`.

## 10. D-020 allocator rule — mandatory

The testbed teardown/allocation control plane is asynchronous.

Never use:

`terminate -> immediate recreate`

Use only:

`terminate -> positively verify release -> allow convergence interval -> recreate only if still necessary`

For a short reserved window, prefer **one early instantiation and patience** over allocator churn. A successful terminate request does not prove immediate node reuse.

If provisioning stalls, preserve state and diagnose. Do not repeatedly terminate/recreate within the same reservation.

## 11. Next clean reservation

Existing reservation is intentionally preserved:

**2026-08-26 19:00–22:00 Africa/Cairo — `nuc1+nuc2`**.

Recommended fresh experiment name for traceability: `WP-HCAL-D`.

At the reservation start:

1. Re-read `powder/PRE_EXPERIMENT_GATE_2026-08-26.md` and D-020.
2. Verify the reservation is still active and really owns `nuc1+nuc2`.
3. Instantiate **once**, early, using `PowderProfiles/srslte-controlled-rf` and live-valid bindings only.
4. Supply the registered current automation public key through the secure Portal/API path.
5. Wait for `READY`; no teardown/recreate loop.
6. Capture fresh experiment UUID, exact profile revision, manifest, node mapping and SSH endpoints.
7. Prove SSH on **both** nodes with the current automation identity before LTE/RF action.
8. Establish EPC/eNB + UE lifecycle.
9. Pass explicit Q0 end-to-end LTE user-plane readiness.
10. Prove route to `172.16.0.1` uses `tun_srsue`.
11. Verify remote runtime/Paho version and fresh MQTT run/session isolation.
12. Only then execute non-scored physical W1 H calibration.
13. Stop immediately for a valid adverse W1 recovery failure or any H > 300 implication.
14. Freeze H only after exactly three valid successful trials and deterministic finalization.
15. Use the same evidence bundle to close runtime/path/identity/clock/analysis gates where justified.

If meaningful time remains after H is scientifically closed, only non-scored S3/B2 implementation qualification may follow. **No WP3 scored run.**

## 12. Automation workflow safety map

Today's live troubleshooting created several one-off workflows. Do not assume every workflow under `.github/workflows/` is a reusable next-run owner.

- `.github/workflows/powder-hcal-release.yml` — one-off release logic for `WP-HCAL-B`; **do not reuse as a generic runner**.
- `.github/workflows/powder-hcal-cooldown-retry.yml` — one-off `WP-HCAL-C` cooldown retry with date/name assumptions; **do not rerun for the evening reservation**.
- `.github/workflows/powder-hcal-final-status.yml` — read-only final status artifact; safe historically, not the next execution path.
- `.github/workflows/powder-live-discovery.yml` was repurposed during the live recreate episode; **do not trigger it blindly despite the filename**.
- key validation/secret-presence workflows are diagnostic only.

Before the evening run, either construct a fresh reservation-specific owner workflow that obeys this handover, or use the verified Portal API + SSH gates explicitly. It must have **no automatic recreate loop**.

## 13. Stop conditions

Stop rather than improvise if:

- reservation/resources differ from expectation;
- profile revision/bindings differ materially;
- experiment fails to reach READY;
- SSH fails after a fresh experiment that definitely includes the current registered key;
- Q0 user-plane fails;
- MQTT route bypasses `tun_srsue`;
- first fresh MQTT connection reports `session_present=true`;
- runtime/Paho does not match the frozen design;
- evidence identity/checksum cannot be reconstructed;
- a `VALID_W1_RECOVERY_FAILURE` occurs;
- H would exceed 300 s;
- protocol amendment becomes necessary;
- any temptation arises to rerun because a scientific result is unfavorable.

## 14. Evidence and security boundary

POWDER supports networking/radio/telemetry/recovery/process-restart claims only. It does not validate pump mechanics, hydraulics, groundwater, agronomy, Siwa field performance, or broad rural generalization.

Never commit or expose:

- private SSH keys;
- key passphrases;
- POWDER API tokens;
- RPC tokens;
- certificate private material;
- raw credential-bearing portal exports.

Preserve sanitized reproducibility metadata: experiment/profile IDs, revisions, bindings, endpoint/auth mode, software/image identity, state transitions, UTC timestamps, commands, exit codes, checksums, verdicts and teardown state.

## 15. Required end-of-block discipline

After every material POWDER work block:

1. update `HANDOVER_CURRENT.md`;
2. update this file if the execution frontier changes;
3. update `docs/MILESTONE_STATUS.md`;
4. update `docs/STATUS.md` and `docs/DECISIONS.md` if state/decisions changed;
5. update `docs/NEXT_GATE.md`;
6. save sanitized evidence under `evidence/powder/`;
7. update Drive `WellPulse — Current Handover Index`, including `MILESTONES`;
8. leave the exact next action recoverable without chat history.

## Immediate acceptance target

A fresh reservation must first prove:

`single instantiate -> READY -> live manifest PASS -> SSH both nodes PASS -> Q0 user-plane PASS -> tun_srsue route PASS -> runtime/session isolation PASS`

Only then may physical W1 H trials begin.