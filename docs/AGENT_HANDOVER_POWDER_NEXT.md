# AGENT HANDOVER — WellPulse POWDER Validation Owner

**Handover timestamp:** 2026-08-24 22:44 Africa/Cairo  
**Canonical repository:** `aayoubMSA/WellPulse`  
**Current scientific completion:** **20%**  
**Current execution gate:** **G3 — Simulated stack/data-path validation — NEXT / NOT STARTED**

## Mandate

You now own the continuation of the WellPulse POWDER validation lane. Your job is to advance the project from the verified manual infrastructure baseline through the minimum defensible POWDER evidence needed for publication, while preserving reproducibility and refusing evidence inflation.

Optimize for:

`scientific value × reproducibility × reviewer defensibility ÷ execution risk × unnecessary scope × resource cost`

Do not broaden the project merely because POWDER exposes additional capabilities.

## Read order — mandatory before execution

Read these files in this order before taking any action:

1. `HANDOVER_CURRENT.md`
2. `docs/MILESTONE_STATUS.md`
3. `docs/STATUS.md`
4. `docs/DECISIONS.md`
5. `powder/MANUAL_GOLDEN_PATH.md`
6. `evidence/powder/manual-golden-path-2026-08-24.md`
7. `experiments/WP-PWD01/protocol.md`
8. `experiments/WP-PWD01/analysis-plan.md`
9. `experiments/WP-PWD01/evidence-schema.md`
10. `experiments/WP-PWD01/randomization-plan.csv`
11. `experiments/WP-PWD01/run-matrix.yaml`

Treat GitHub and the Drive handover index as canonical state. Do not reconstruct project status from chat memory.

## Scientific WP state

- WP0 — Novelty & Venue Lock — **8/8 complete**.
- WP1 — Confirmatory Protocol & Statistics Freeze — **12/12 complete**.
- WP2 — RF Calibration & Measurement Validation — **0/15 — NEXT scientific WP**.
- WP3 — Conducted-RF Confirmatory Campaign — **0/30 — blocked by WP2**.
- WP4 — OTA External Replication — **0/15 — blocked by WP3**.
- WP5 — Analysis + Artifact + Paper Closure — **0/20 scientific closure**; analysis/reproducibility scaffolding exists but is intentionally not counted yet.

Weighted scientific completion: **20%**.

Planning estimate remaining: **~28–50 active hours**, realistically **~5–8 calendar days**, extending to **~1–2 weeks** if compatible controlled-RF or OTA resources require waiting.

## POWDER infrastructure state

- G0 Account + WellPulse project — **PASS**.
- G1 Manual compute provisioning — **PASS**.
- G2 Explicit-key SSH + node verification + clean teardown — **PASS**.
- G3 Simulated stack/data path — **NEXT / NOT STARTED**.
- G4 Controlled physical-RF lifecycle — **PENDING**.
- G5 RF impairment plumbing — **PENDING**.

G0–G2 are enabling infrastructure only. They do not add scientific WP percentage.

## Accepted manual golden baseline

Canonical accepted experiment:

- experiment: `WP-G1-SIM`
- UUID: `0dc233d7-44a0-4e6c-9734-6d4c8ea0e2ad`
- profile: `srsLTE-SIM:9`
- profile UUID: `80dda605-7e5f-11e9-8006-e4434b2381fc`
- hardware: `d430`
- allocated node: `pc734`
- image: `PowderProfiles:gnuradio-srslte`
- SSH endpoint: `pc734.emulab.net:22`
- remote user: `aayoub`
- canonical remote hostname: `node.wp-g1-sim.wellpulse.emulab.net`
- OS: Ubuntu 18.04.1 LTS
- kernel: Linux 4.15.0-33-generic x86_64
- teardown: PASS; portal returned to `Current Usage: 0 Node Hours`

Canonical manual SSH key label:

`WellPulse-POWDER-Golden`

Public fingerprint:

`SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`

The private key and its passphrase are local-only secrets and must never be requested, echoed, committed, or copied into evidence.

## Exact next gate — G3

Goal: prove that the profile-authoritative file-based srsLTE simulated eNodeB/UE path executes correctly on POWDER. This remains **non-scored**, **no SDR**, **no RF**, and **not scientific evidence**.

Procedure:

1. Manually instantiate a fresh `srsLTE-SIM:9` experiment under project `WellPulse` with a distinct name such as `WP-G3-SIMSTACK`.
2. Use one `d430`; no reservation unless the portal requires it.
3. Wait for `State: ready`.
4. Open List View and record the **actual** active SSH endpoint. Never guess or reuse a historical hostname.
5. SSH from Windows using the explicit Golden key and `IdentitiesOnly=yes`.
6. Execute only the profile-authoritative file-based example:

```bash
/usr/local/srsLTE/build/lib/examples/pdsch_enodeb -o foo -n 5 -m 9 -v
/usr/local/srsLTE/build/lib/examples/pdsch_ue -i foo -n 5 -r 1234 -v -d
```

7. Capture stdout/stderr, exit codes, output-file metadata and SHA-256 checksum.
8. Verify expected simulated receive behavior without introducing WellPulse/MQTT yet.
9. Remove only temporary test output created by G3 if safe and unambiguous.
10. Exit, terminate manually, verify `Current Usage: 0 Node Hours`.
11. Write sanitized G3 evidence and update `HANDOVER_CURRENT.md`, `docs/MILESTONE_STATUS.md`, `docs/STATUS.md`, and the Drive handover index.

G3 PASS does not authorize scored work.

## After G3

Proceed to G4 only through the live POWDER UI:

- discover a **current** controlled physical-RF profile;
- verify owner/project/profile revision and hardware from current portal state;
- manually provision it before trusting automation;
- prove READY -> manifest -> SSH -> clean terminate;
- then prove the experimental user-plane rather than POWDER control-network bypass;
- only after that begin WP2 calibration and freeze Q0–Q3 plus H.

Do not infer a current usable profile from old workflow names or remembered examples.

## Known failed/exploratory history — quarantine

Do not silently reuse or promote these:

- `wpplmb6787317` / `srs-rf-matrix` — failed because topology requested an `n310` while WellPulse had entitlement 0. **Do not resubmit unchanged.**
- `wphnd8201533` / `srsran-handover` — exploratory/invalid feasibility attempt. Not an accepted current controlled-RF baseline.
- earlier `WP-G1-SIM` runs before the Golden-key reset — troubleshooting only.

Only the final 22:07–22:17 `WP-G1-SIM` run is the canonical G1/G2 PASS reference.

## Frozen scientific design — do not drift

Primary comparator:

`B1_MQTT_QOS1` — MQTT v3.1.1, QoS1, TLS scored path, automatic reconnect, volatile client state, no application-level disk durability/reconciliation.

WellPulse:

`W1_OFFLINE_FIRST` — same low-level Paho session plus SQLite durable queue, stable identity/checksum, replay, idempotent receiver and reconciliation.

Frozen low-level settings:

- `paho-mqtt==2.1.0`
- MQTT v3.1.1
- QoS1
- `clean_session=False`
- keepalive 60 s
- reconnect 1–8 s
- outgoing queue 4096
- inflight 20

Scenarios: S0 healthy, S1 intermittent, S2 hard outage, S3 outage + gateway-process restart.

Run is the statistical unit. Conducted campaign is 24–36 scored runs under the frozen precision rule. OTA replication is 12 scored runs for S1/S2 only.

`scored_runs_authorized = false` until every pre-score gate in `protocol.md` passes.

## Evidence boundary

POWDER may support claims about networking, radio-link resilience, edge/cloud recovery, telemetry integrity/completeness, reconnect behavior, process-restart recovery and resilience overhead.

It does **not** validate pump mechanics, hydraulics, groundwater, crop physiology, Siwa conditions, agricultural field performance or rural generalization.

Do not inflate remote-testbed evidence into field evidence.

## Security / reproducibility rules

Never commit or expose:

- private SSH keys;
- SSH passphrases;
- POWDER API tokens;
- experiment RPC tokens;
- certificate blocks;
- raw credential-like portal material.

Preserve sanitized reproducibility fields instead:

- experiment/profile UUIDs and revisions;
- project and node bindings;
- image/software identity;
- actual SSH endpoint/auth mode;
- state transitions and timestamps;
- commands and exit codes;
- output hashes;
- acceptance/rejection verdict;
- evidence boundary;
- clean teardown state.

Raw POWDER portal logs may contain credential-like encrypted material. Do not blindly commit them. Preserve only the minimum sanitized extract necessary for audit/reproduction.

## Manual-first rule

Resource-creating POWDER automation remains **FROZEN** until the equivalent manual path has passed and been documented. Automation may later clone a proven path; it may not discover the path by trial and error.

## Required handover discipline

At the end of every material work block:

1. update `HANDOVER_CURRENT.md`;
2. update `docs/MILESTONE_STATUS.md`;
3. update `docs/STATUS.md` and `docs/DECISIONS.md` if state/decision changed;
4. save sanitized evidence under `evidence/powder/`;
5. update the Drive `WellPulse — Current Handover Index` including the `MILESTONES` tab;
6. preserve any publication-relevant raw evidence in the Drive validation/raw-evidence workspace with hashes;
7. ensure exact next action is recoverable without chat history.

## Stop conditions

Stop rather than improvise if:

- live profile/resource identity does not match expectation;
- a hidden hardware entitlement appears;
- the experimental user-plane cannot be distinguished from control-network traffic;
- mandatory evidence cannot be reconstructed;
- the protocol would need a scientific amendment;
- a result is unfavorable — never rerun merely to improve the result.

Technical-invalid reruns are allowed only under the frozen invalidity rules and the invalid raw run must remain preserved.

## Immediate acceptance target

The next owner should first produce exactly one new durable artifact:

`evidence/powder/g3-simstack-<date>.md`

with a PASS/FAIL verdict for the file-based simulated srsLTE path and a clean teardown record. Only after that should G4 controlled physical-RF discovery begin.
