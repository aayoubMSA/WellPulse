# WP2-P7B-H2.5 — Contract/Runtime Regression Gate Closure — 2026-08-28

## Terminal verdict

`H2_5_REGRESSION=PASS`

`POWDER_CONTACT=NO`

`NETWORK_CONTACT=NO`

`LIVE_SERVICE_MUTATION=NO`

`RF_MUTATION=NO`

`RETRY=NO`

`W1_B2=NO`

`SCORED=NO`

`TEARDOWN=NO`

`WP3=NO`

H2.5 performed only offline integrated regression across the frozen executable contract, target-runtime/EFCC contract, H2 A1–A7 repair surfaces, H2.4 adversarial evidence, and the modular GitHub execution contract.

## Regression gap found and repaired

H2.5 identified one real prospective runtime-preflight gap before issuing PASS:

`TARGET_PREFLIGHT_DID_NOT_YET_COVER_H2_PROSPECTIVE_SOURCES`

The target preflight already checked the frozen r2 stack, but it did not yet syntax-compile the H2 wrapper/ownership layer or `bash -n` the H2-safe restore. This would have allowed a future H2 promotion to bypass exact target-image syntax verification.

Offline repair commit:

`a465a4849df768f57310e9b261e6875a014ac2ce`

The repair adds to `scripts/wp2_p7b_target_node_preflight.sh`:

- pinned-Python syntax compilation of `scripts/wp2_p7b_c_node_h2.py`;
- pinned-Python syntax compilation of `src/wellpulse/p7b_session_ownership.py`;
- `bash -n` validation of `scripts/wp2_p7b_service_restore_h2.sh`;
- explicit H2 guards against executable system-`python3` and remote-`jq` dependencies.

No live preflight was executed in H2.5.

## Integrated regression gate

Reusable offline gate:

`scripts/wp2_p7b_h2_regression_gate.py`

Commit:

`4057dd53ecc0dd95ffc4c629eba56deada5b0d45`

Regression test binding:

`tests/test_wp2_p7b_h2_regression_gate.py`

Commit:

`2bc8dc775d46438b93de7709ec75ec53c484b3ad`

Machine-readable result:

`evidence/powder/wp2-p7b-h2-5-regression.json`

The gate proves:

1. exact frozen blob integrity for executable contract v2, target-runtime contract v2, modular pipeline v1, and the historical Golden restore;
2. exact scientific equivalence across base contract, H2 delta, and modular contract;
3. exact profile revision, image, hardware, node bindings, Python/Paho/B2-JAR runtime binding;
4. H2 prospective sources are covered by target preflight and H2-safe restore is shell-syntax gated;
5. the H2 wrapper layers over frozen r2 and installs A1–A6 before inherited execution;
6. all H2 authority flags remain false;
7. the modular DAG preserves M2 controller-disjointness, M3 H2-safe ownership, B1→W1→B2 ordering, per-job SSH-state doctrine, evidence-first failure semantics, no automatic retry/reservation/teardown;
8. H2.4 remains 7/7 adversarial PASS;
9. no live P7B workflow exists and the Actions surface remains the six offline/QA workflows.

## Frozen artifact integrity

Exact Git blob identities remained unchanged:

- `p7b-executable-contract-v2.json` — `233aabeaf3081470bc3ebc1ee04168f8932fc415`
- `p7b-target-runtime-contract-v2.json` — `9531893989effb142e694294b95c0c7146353742`
- `p7b-modular-pipeline-contract-v1.json` — `2c85af21f502c092c2da0ecb1bf615c8f705069b`
- historical `wp2_golden_service_restore.sh` — `cdf865eaaaf1c08bc8f7a8896d7f705739e60b9c`

Therefore H2.5 did not rewrite frozen scientific/runtime authority to make the regression pass.

## Final QA

GitHub Actions:

- workflow: `Local Unit Tests`
- run: `33141861113`
- job: `98754235047`
- head: `2bc8dc775d46438b93de7709ec75ec53c484b3ad`
- Python validation host: `3.12.14`
- Paho MQTT: `2.1.0`
- **168/168 tests PASS**
- H2.5-specific tests: **5/5 PASS**

The same suite also reran the existing H2.4 adversarial regression stack.

## Authority interpretation

H2.5 is a compatibility PASS, not a live promotion.

The frozen executable/runtime contracts still identify r2 as their frozen authoritative entrypoint. The H2 wrapper remains a prospective layer over r2 and has not been promoted to live authority by H2.5.

This is intentional: H2.6 owns the finite decision whether the completed H2 repair is sufficient to authorize a **future non-scored requalification request**, and what exact prospective authority artifact must govern it. Even H2.6 PASS cannot itself contact POWDER; a separate explicit user live authorization remains mandatory.

## Next patch

`WP2-P7B-H2.6 — REQUALIFICATION AUTHORITY DECISION + CANONICAL CLOSURE`

H2 progress after this patch: **90%**.

H2.6 must remain offline and may only decide/promote the future non-scored authority state. It must not contact POWDER, create/select a reservation, SSH to a live target, mutate RF, restart services, retry B1, execute W1/B2, teardown, score, or start WP3.

**STOP — H2.5 CLOSED. H2.6 NOT STARTED.**
