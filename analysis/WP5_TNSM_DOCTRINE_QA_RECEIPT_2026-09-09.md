# WP5 — IEEE TNSM Doctrine QA Receipt

**Date:** 2026-09-09  
**Target:** IEEE Transactions on Network and Service Management (TNSM)  
**Status:** PRE-PORTAL QA PASS / CONTROLLED RELEASE PASS / NOT SUBMITTED

## Final controlled-release identity

- title: **Beyond Reconnection: Receiver-Verified Service Recovery in MQTT Telemetry Across Failure Domains**
- manuscript source SHA-256: `80abe30f23a2ba5018ea370f250d642ef94fb9289a4872689536901401a1c5f3`
- manuscript PDF SHA-256: `f9a9cbb8b93197045c2b03dc1a9cb829eeb02dcf4bcdfd38ef1cb3ec0d0ef918`
- cover-letter PDF SHA-256: `f868eec7625affcff9fe66f65e711b39ba37b4ce1f26586c81a4752994ec8f42`
- reviewer supplement SHA-256: `3b6ede7ba4b73dd19767eff531eab05058e9220c95c873fb540cfad28677d5d9`
- controlled submission package SHA-256: `7945ccbd58b85aa128bf8163436f0a289d53a80fc8b743e5cc7e0cdae3e32802`
- submitted-IoT source authority SHA-256: `11ab226d32133e78e1bce29be55345f42cb6bdedad877efcadda7d298917efa5`

## Doctrine gates

- `P4_SCIENTIFIC_QA=PASS`
- `P4_EDITORIAL_QA=PASS`
- `ABSTRACT_GATE=PASS_181_WORDS_189_CONSERVATIVE_TOKENS`
- `PAGE_GATE=PASS_9_OF_10`
- `REFERENCE_ARCHITECTURE=PASS_23_OF_23_CITED`
- `CLEAN_SOURCE_REPLAY=PASS_0_OF_9_CHANGED_PAGES`
- `COVER_LETTER_REPLAY=PASS_0_OF_1_CHANGED_PAGES`
- `FIGURE_DUAL_QA=PASS`
- `SUPPLEMENT_SELFCHECK=PASS`
- `SUPPLEMENT_MANIFEST=PASS_48_OF_48`
- `SUPPLEMENT_PRIVACY_SCAN=PASS_ZERO_HITS`
- `ACTIVE_STALE_IDENTITY_SCAN=PASS_ZERO_HITS`
- `NESTED_ARCHIVE_TEST=PASS`
- `RELEASE_HASH_READBACK=PASS`
- `P5_CONTROLLED_RELEASE=PASS`

## Scientific Red Hat

The strongest surviving empirical result is internal to W1: communication reconnects in about 1.3 s while complete receiver-confirmed backlog reconciliation requires about 68 s under the tested FIT workload. The B0 80% versus W1 100% result remains a bounded negative mechanism-isolation contrast; B0 is not a durable-MQTT competitor.

The most damaging reviewer objection remains the absence of a matched strong durable-MQTT comparator. Residual novelty/significance risk is **MEDIUM**, not a correctness or packaging blocker, because the retained contribution is receiver-verified recovery closure plus the post-reconnect incomplete-state interval and failure-domain/endpoint/timing semantics. Layered network/service/data recovery itself is explicitly conceded as prior art.

## Production corrections made during doctrine QA

1. Expanded manuscript-facing non-obvious acronyms at first substantive use, including MQTT, TCP, QoS, POWDER, RF, LTE, UE, ICMP, and RTT.
2. Added the required FIT IoT-LAB acknowledgment while retaining the testbed reference.
3. Completed Gaspar et al. 2026 bibliographic metadata to IEEE Internet of Things Magazine 9(5):166–172.
4. Shortened the abstract from a borderline tokenizer count to 181 whitespace words / 189 conservative tokens, preserving the same evidence and claims.
5. Removed unused Figure 01 from the controlled main-source release; it remains preserved in the reviewer supplement as provenance.
6. Rebuilt the controlled release as `UPLOAD/`, `SOURCE/`, and `ADMIN/`, excluding build clutter, old candidate source, stale Elsevier files, and unused main-source assets.

## Remaining author-controlled gates

- `FINAL_AUTHOR_APPROVAL_OF_EXACT_RELEASE_BYTES=WAITING`
- `PORTAL_ARTICLE_TYPE_EXACT_WORDING=WAITING_FOR_LIVE_PORTAL`
- `PORTAL_GENERATED_PDF_QA=WAITING_FOR_UPLOAD`
- `FINAL_SUBMIT_AUTHORIZED=NO`
- `EXTERNAL_SUBMISSION_EXECUTED=NO`

## Exact next action

After Dr. Ahmed authorizes portal entry, upload only the three controlled files in `UPLOAD/`, map metadata against the live TNSM Author Portal, stop if reviewer suggestions are mandatory, inspect the journal-generated combined PDF/render, and request explicit final authorization before pressing Submit.
