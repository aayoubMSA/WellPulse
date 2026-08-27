# WP2-P7 — Scored Authorization Decision — 2026-08-27

## Verdict

`WP2_P7_HARDENING_QA=PASS`

`SCORED_AUTHORIZATION=BLOCKED`

`scored_runs_authorized=false`

`WP3=BLOCKED`

`POWDER_CONTACT_DURING_P7=NO`

`SCIENTIFIC_RUN_DURING_P7=NO`

P7 successfully hardened the reusable Golden/pre-score execution contracts and passed bounded offline QA. It does **not** authorize scored B1/W1/B2 execution because mandatory pre-score physical qualification gates remain open.

## Accepted P7 hardening

P7 incorporated the two live lessons exposed by the recovered P6 Golden while preserving the frozen scientific protocol:

1. **Management aliases are now explicit preconditions.** `scripts/wp2_golden_prepare_management_aliases.sh` requires the controller-provided management endpoints parsed from the authoritative Portal manifest, binds the logical aliases, and proves SSH reachability before G0. No physical node substitution or hard-coded `nuc1/nuc2` endpoint is introduced.
2. **Receiver evidence transfer is now the live-qualified tar-stream path.** The reusable orchestrator no longer uses the failed `scp .../receiver/.` form. It streams a tar archive from the exact receiver directory and validates mandatory receiver files before reconstruction.
3. **Post-cohort traffic is no longer mislabeled as unexpected.** `scripts/reconstruct_wp2_golden.py` now separates records generated after `t_rf_restore` from truly unknown record identities. Primary-cohort membership, `H_app=300 s`, `completeness_300`, and all frozen clock semantics are unchanged.
4. **Regression tests are executable under the repository's actual `unittest discover` gate.** The clock-authority, post-cohort classification, alias, receiver-transfer, and retired-P6-surface tests are now discovered and executed rather than merely present as non-discovered pytest-style functions.

## Runtime acceptance evidence

Bounded offline closure workflow:

- GitHub Actions run: `33103997677`
- Job: `98628861177`
- Result: **SUCCESS**
- Environment: GitHub-hosted Ubuntu 24.04
- POWDER contact: **NO**
- POWDER mutation: **NO**
- scientific run: **NO**
- scored run: **NO**

The run proved:

- `P7_STATIC_SYNTAX=PASS`
- `P7_UNIT_REGRESSIONS=PASS`
- **36/36 executable unit tests PASS**
- `P7_GOLDEN_HARDENING_STATIC_QA=PASS`
- `WP2_GOLDEN_OFFLINE_QA=PASS`
- persistent escrow simulation PASS
- independent controller TAR round-trip PASS
- outer-SHA corruption fails closed
- internal raw-SHA corruption fails closed
- `WP2_P7_OFFLINE_CLOSURE_QA=PASS`.

The temporary P7 closure workflow and trigger were deleted after PASS. Current active workflow surface returned to the six standing offline/static workflows; no P6/P7 live trigger remains.

## Pre-score evidence reconciled as closed

The following older `run-matrix.yaml` OPEN labels are superseded by later physical/non-scored evidence and P6/P7 validation. They are **not current blockers**:

- run/session isolation: physically demonstrated in `evidence/powder/wp2-pre-h-runtime-path-qualification-2026-08-26.md` (`session_present=false`, run-unique client/topic namespace);
- frozen remote Paho runtime: physically demonstrated with Python 3.11.x and `paho-mqtt==2.1.0`, and reproduced again in P6;
- experimental LTE/MQTT data path: physically demonstrated through `tun_srsue` to `172.16.0.1:8883`, not through the POWDER control network;
- physical record identity/checksum preservation for the W1 Golden path: P6 reconstructed 181/181 primary-cohort records with zero checksum mismatch and zero missing records;
- evidence/clock alignment: P6 reconstructed from `sender/rf_restore.ready`, `t_service_ready`, and the fixed 300 s horizon, with P7 regression coverage against the trailing cleanup-Q0 failure mode;
- deterministic non-scored analysis reconstruction: P6 + P7 PASS;
- automated SSH/controller path: the GitHub Actions controller successfully reached the exact manifested nodes during P6, and the reusable path is now hardened by manifest-derived alias checks;
- external evidence survival/teardown chain: P6 final escrow, independent artifact read-back, outer/internal SHA verification, and teardown confirmation PASS.

These closures do not upgrade any arm-specific or restart-domain evidence that was never executed.

## Mandatory blockers that remain open

### B1 — B1 accepted/unacknowledged instrumentation on the real remote path

Local regression proves the corrected accepted-but-unacknowledged accounting semantics, but the frozen pre-score matrix still requires arm-level physical evidence before scored execution. P6 exercised the W1 Golden path, not a matched B1 physical comparator run.

Status: `OPEN_NON_SCORED_PHYSICAL_QUALIFICATION_REQUIRED`.

### B2 — B1/W1 implementation matching on POWDER

The code contract says B1 and W1 share the same low-level Paho session and differ only in W1 application-level disk durability/reconciliation. This still needs a bounded remote pre-score manifest/probe showing exact runtime/config parity on the same POWDER data path before a scored comparison is authorized.

Status: `OPEN_NON_SCORED_REMOTE_MATCHING_REQUIRED`.

### B3 — S3 restart-domain separation

`PRE_SCORE_P0_AMENDMENT_2026-08-26.md` requires prospective, non-scored proof that:

- the telemetry generator remains outside the gateway/client restart domain;
- generation continues at 1 Hz through the restart;
- only the gateway/client process is restarted, not the node;
- W1 durable SQLite state survives the process restart;
- B1 volatile client state is destroyed/recreated with the same intra-run identity;
- source sequence continuity and restart timestamps/downtime are preserved.

No canonical artifact in the current repository proves this physical restart-domain contract.

Status: `OPEN_NON_SCORED_VERIFICATION_REQUIRED`.

### B4 — B2 remote runtime/path/restart qualification

B2 local semantics is PASS 3/3, but `PRE_SCORE_P1_AMENDMENT_2026-08-26.md` explicitly requires the exact Eclipse Paho Java 1.2.5 durable-client implementation to pass a non-scored remote runtime/path/restart-domain gate on the same POWDER LTE/TLS/payload/evidence path before any B2 scored run.

No canonical remote B2 physical qualification artifact exists.

Status: `OPEN_NON_SCORED_VERIFICATION_REQUIRED`.

### B5 — inter-run washout/readiness physical enforcement

The readiness rule is frozen and Q0 readiness has been demonstrated, but the scored campaign still requires an implementation that enforces the full per-run washout contract for B1/W1/B2: Q0 user plane, LTE route, fresh namespace/state, no broker/session residue, calibrated radio envelope, runtime/config lock, and healthy clock/evidence capture.

Status: `OPEN_PRE_SCORE_ENFORCEMENT_REQUIRED`.

### B6 — immutable pre-score snapshot

This is intentionally last. It cannot be created as an authorization snapshot while B1-B5 remain open. Once those gates PASS, freeze the exact implementation commit, protocol/amendments, run-matrix hash, randomization hashes, B2 plan hash, runtime locks, evidence schema, 300 s clock contract, comparator decision, and explicit authorization decision before any scored record is generated.

Status: `OPEN_BLOCKED_ON_B1_B5`.

## Lowest-burden closure route

Do **not** create separate reservations for each blocker. The shortest defensible next patch is one bounded non-scored pre-score qualification reservation that is designed prospectively to close B1-B5 together:

`WP2-P7B — SINGLE NON-SCORED PRE-SCORE PHYSICAL QUALIFICATION`

It should use the already-frozen conducted-RF profile/bindings and execute only the minimum diagnostic cells needed to prove:

1. B1 instrumentation + B1/W1 matched runtime/config;
2. S3 process-restart-domain mechanics without using the result as scientific evidence;
3. B2 Java durable-client runtime/path/restart mechanics;
4. the full inter-run washout/readiness gate.

If and only if all four qualification groups PASS, create the immutable pre-score snapshot as the final offline step and issue `SCORED_AUTHORIZATION=PASS`. Any scientific outcome observed during P7B is non-scored qualification evidence and must not be used to select, tune, rerun, or change the frozen protocol.

## Stop boundary

P7 ends here. It does not authorize a POWDER reservation, B1/W1/B2 scored work, OTA replication, or WP3 execution.

`SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`
