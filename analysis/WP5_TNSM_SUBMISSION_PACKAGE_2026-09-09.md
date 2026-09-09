# WP5 — IEEE TNSM Manuscript Conversion & Submission Package

**Date:** 2026-09-09  
**Target:** IEEE Transactions on Network and Service Management (TNSM)  
**Status:** PASS — SUBMISSION-READY / NOT SUBMITTED  

## Outcome

The Internet of Things submitted scientific source was converted to a TNSM-specific IEEEtran manuscript without changing FIT or POWDER experiments, measurements, figure data, comparator scope, timing semantics, or claim prohibitions.

### Frozen title

**Beyond Reconnection: Receiver-Verified Service Recovery in MQTT Telemetry Across Failure Domains**

### Frozen contribution

The TNSM paper is centered on **receiver-verified recovery closure** for stateful MQTT telemetry. The primary empirical result is the post-reconnect incomplete-state interval in the durable FIT runs: path reconnection at about 1.3 s versus complete receiver-reconciled backlog recovery at about 68 s under the tested workload. B0 remains a non-durable negative mechanism-isolation control, not a durable-MQTT competitor. POWDER supplies complementary failure-domain and recovery-observability evidence; FIT and POWDER are not statistically pooled.

## TNSM format / QA gate

- IEEEtran journal two-column format: PASS
- formatted manuscript length: **9 pages**
- TNSM 10-page free threshold: PASS
- abstract: **184 words** (75–200 requirement)
- cited references: **23**
- unused bibliography entries: 0
- undefined citations/references: 0
- overfull boxes: 0
- visual render QA: 9/9 pages PASS
- cover letter: 1 page PASS
- reproducibility supplement self-check: PASS

## Scientific integrity gate

The exact validated figure authorities are preserved byte-identically:

- Figure01: `bd855f923247836a7378e5d0462ebebf182ea3fecdd0bcb121daaa29b8c8b2e5`
- Figure02: `8ce2e1a3054a10787378f5648e437a3daa36a4816dcdd43160f51259f1ada89c`
- Figure03: `8004926f0168a86fddef749b5ac0002c9f0ba19448d42a96fe381d86bf411640`
- Figure04: `a0bb9fb61b6de95b9284d88428253324e9762d69545931e191c794d6a095a34e`

Figure01 is retained as supporting provenance in the reviewer supplement but is not used in the TNSM main manuscript. Figures 02–04 are the three main scientific figures.

No new experiment was introduced. No generic durable-MQTT superiority, universal 52 dB threshold, pooled FIT+POWDER inference, or promotion of censored/upper-bound observations to exact latency is permitted.

## Package authorities

- main manuscript PDF SHA-256: `8bdb805b569f6335291798e5e9fea6d804b2fef4c05ac18869de52711cd23536`
- main manuscript TeX SHA-256: `4783ef9a718ddfda2ccf6c555b055869ac156c0398540244697a490a4e2429eb`
- cover letter PDF SHA-256: `f868eec7625affcff9fe66f65e711b39ba37b4ce1f26586c81a4752994ec8f42`
- reviewer supplement ZIP SHA-256: `3b6ede7ba4b73dd19767eff531eab05058e9220c95c873fb540cfad28677d5d9`
- complete submission package ZIP SHA-256: `3c47713a237749b3c3f35505537a45d52e031701eae8e85f52d4db0c89a2d499`

## Submission files

Portal-facing upload set:
1. `WellPulse_TNSM_Manuscript.pdf`
2. `WellPulse_TNSM_Supplement_Reproducibility_20260909.zip`
3. `WellPulse_TNSM_Cover_Letter.pdf`

Administrative metadata and source files are preserved in the complete package.

## Stop state

`WP5_TNSM=PASS`
`TNSM_SUBMISSION_READY=YES`
`NEW_EXPERIMENT_REQUIRED=NO`
`EXTERNAL_SUBMISSION_AUTHORIZED=NO`
`EXTERNAL_SUBMISSION_EXECUTED=NO`
`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`
`PAYMENT_AUTHORIZED=NO`

Next action only after explicit author approval: open the live TNSM Author Portal, map metadata, inspect the portal-generated manuscript/preview, and stop before final Submit if any new mandatory field, reviewer nomination, license/copyright action, or payment decision appears.