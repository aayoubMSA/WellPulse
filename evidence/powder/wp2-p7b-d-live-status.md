# WP2-P7B-D Evidence Survival — authoritative retained status

- Checked UTC: 2026-08-27T20:42:17Z
- Experiment UUID: `26b6f315-459d-4a56-9167-69228e339f24`
- P7B-C run ID: `wp2-p7b-c-33113016138-20260827T203140Z`
- Evidence class: **NON-SCORED PRE-SCORE PHYSICAL QUALIFICATION**
- P7B-C retained verdict: **BLOCKED: RECEIVER_CONNECT_TIMEOUT**
- Completed P7B-C cells: **NONE**
- Scientific measurement started: **NO**
- Scored run: **NO**

## P7B-D preservation chain

- First P7B-D preservation attempt: GitHub run `33114265831` — **FAIL-CLOSED before persistent copy** because of a preservation-script path quoting defect; no artifact and no teardown occurred in that attempt.
- Same-reservation preservation retry: GitHub run `33114517583`, job `98665610066` — **workflow SUCCESS**.
- Persistent `/proj` escrow for the declared UE and core evidence roots: **PASS**.
- Controller pull plus internal SHA-256 verification: **PASS**.
- GitHub artifact upload: **PASS**.
- Artifact name: `wp2-p7b-d-33114517583`.
- Artifact ID: `9663926250`.
- Artifact ZIP digest reported by GitHub: `0bd31f534712d2f1fe3793008e7b00c1e6df85f58277686b3de5ffb5fd6455bb`.
- Deterministic inner TAR SHA-256: `f49263f77d673cf5961dd6efb3b0ce2a3d7dde5969d48f20e0c383f105693877`.
- Deterministic inner TAR bytes: `296960`.
- Independent artifact download: **PASS**.
- Independent inner TAR SHA-256 match: **PASS**.
- Independent internal `SOURCE_SHA256SUMS` verification for the captured UE/core roots: **PASS**.
- `CONTROLLER_OFFPOWDER_GATE=PASS`.
- `EVIDENCE_ESCROW_GATE=PASS` for the captured declared roots.
- Teardown authorized only after the independent read-back: **YES**.
- Teardown confirmed: **YES**; Portal transitioned through `terminating` and then the exact experiment UUID was no longer found.

## Known evidence gap discovered before closure

The expected core evidence root contained `cells/P7B-B1-S3/receiver/console.txt` but did **not** contain the expected `receiver_events.jsonl`. The preserved broker-side diagnostic output proves that receiver client `wp-hcrx-885b10cacb1c` nevertheless connected successfully, received CONNACK, subscribed to the exact B1 topic, and remained alive long enough to exchange repeated MQTT PINGREQ/PINGRESP traffic.

The live command construction in `scripts/wp2_p7b_c_node.py` passes the receiver `--output-dir` using a single-quoted path containing `$HOME`, while the console redirect and readiness wait use an expanded `$HOME` path. This is strong evidence of an orchestration path mismatch explaining why the receiver was alive at the broker while the readiness loop could not see its event ledger. The exact misplaced receiver event ledger was **not recovered into the escrow bundle before teardown**.

Therefore the workflow-level preservation mechanics succeeded, but strict complete-raw-evidence survival must not be overclaimed.

## Strict verdict

`WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`

- Captured declared-root preservation/read-back: **PASS**.
- Complete raw evidence claim: **BLOCKED**.
- Reservation teardown: **COMPLETE**.
- Replacement reservation authorized: **NO**.
- Automatic retry authorized: **NO**.
- P7B-E: **PASS_CANONICAL_BLOCKED_CLOSURE**.
- Scored authorization: **BLOCKED**.
- `scored_runs_authorized=false`.

## Retirement-trigger provenance

Repository cleanup deletion of `.wp2-p7b-d-trigger` caused GitHub run `33115100803`. It failed at **Freeze P7B-D authority boundary**; dependency install, evidence persistence, artifact upload/read-back and teardown were all skipped. It made **no POWDER contact and no state change**. Its temporary `skipped/NO_OR_UNCONFIRMED` status was non-authoritative and has been superseded by this restored retained record.
