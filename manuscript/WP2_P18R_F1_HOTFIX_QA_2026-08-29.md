# WP2-P18R-F1-HOTFIX — Deterministic Figure-1 Correction and QA

Date: 2026-08-29  
Status: **PASS / ACCEPTED / CURRENT FIGURE-1 AUTHORITY / PROVENANCE REPAIRED**

## 1. Trigger

The original P18R Figure 1 was scientifically useful but contained unacceptable visual-layout defects. An AI-generated redesign was visually cleaner but was rejected as a publication asset because it lacked deterministic source-to-pixel provenance and introduced venue-policy risk.

The AI-generated image is therefore retained, if at all, as a visual-design reference only and is not canonical evidence or artwork.

## 2. Scientific correction

The hotfix corrects an important lifecycle ambiguity.

Canonical code shows that W1 marks a durable local record `SENT` only after Paho reports the QoS1 publish as acknowledged. Receiver evidence is independent: the receiver stores unique `record_id` values idempotently, and final completeness is computed by generated-versus-received identity reconciliation.

Therefore the publication-facing figure now separates:

### Sender-local state path

`Generate → stable identity/checksum → durable PENDING → MQTT QoS1 publish → Local SENT after PUBACK`

with:
- unavailable/retry returning to durable `PENDING`;
- conflicting identity reuse routed to the integrity-error guard.

### Independent receiver-evidence path

`Publish/delivery → idempotent receiver unique IDs → reconciliation → reported final completeness`

The figure no longer implies `Receiver → SENT`.

## 3. Consortium-mandated publication patches applied

1. `Local SENT` separated from receiver reconciliation.
2. Internal `IC-xx` project-control identifiers removed from the publication-facing figure.
3. FIT design explicitly states `3 runs/cell` and `10,000 records/run`.
4. POWDER is represented as the full `E0–E11` controlled characterization campaign.
5. `record-state survival ≠ path recovery` was replaced by the reader-facing wording **Two distinct resilience properties**.
6. Complementary evidence / no quantitative pooling remains explicit.
7. No POWDER W1-versus-baseline architecture effect is implied.

## 4. Deterministic implementation

Canonical generator:

`analysis/wp2_p18r_generate_f1_hotfix.py`

Current Git blob SHA-1:

`bf344808414b78d9b0c688140e9de9a755d9a1e7`

Current exact generator source SHA-256:

`3de810672749001e9fb2d50c43b531e87fec7c359878a5aa7c58deb8ad0e7be5`

The earlier QA receipt value `201897de563448037798678a73c998bd8b7a01f74bb4096995587f13d6667d48` is superseded for current generator identity by the value above. The current generator reproduces the already-frozen final PDF bit-for-bit; therefore this was provenance drift, not a scientific or visual-content change.

The generator validates source semantics in:
- `src/wellpulse/powder_w1.py`;
- `src/wellpulse/receiver.py`;
- `src/wellpulse/reconcile.py`;
- `src/wellpulse/records.py`;
- `src/wellpulse/store.py`.

It consumes no AI-generated image asset.

## 5. Final figure integrity

Final Figure 1 PDF SHA-256:

`4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

A fresh archival rebuild from the current GitHub generator reproduced exactly the same PDF SHA-256.

Production:
- PDF vector master;
- SVG vector master;
- PNG 600 dpi fallback;
- width exactly `7.16 in`;
- embedded PDF fonts: PASS;
- fixed PDF metadata includes author identity and institutional subject metadata.

## 6. Visual QA

Three deterministic iterations were reviewed during the hotfix lifecycle.

The first two were rejected before release because they still contained layout/topology defects.

Final released design:
- known text overlap: `0`;
- known clipping: `0`;
- known arrow/text crossing: `0`;
- known unintended color-cycle artifact: `0`;
- sender-local versus receiver-evidence ambiguity: `0`;
- FIT/POWDER role separation: PASS;
- synthesis convergence without text collision: PASS.

## 7. Durable archive verification

Final archival bundle:

`WellPulse_P18R_F1_Hotfix_Final_2026-08-29.zip`

Drive file ID:

`12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M`

ZIP SHA-256:

`e9d5a54b24506b879a748b5a06b39699e6f6ec1ed31093491c27b2be7d7e6e1d`

The object was fetched back from Drive and re-hashed; read-back SHA matched the local archival package exactly.

Canonical storage/provenance closure:

`docs/WP2_P18R_F1_DRIVE_ARCHIVAL_CLOSURE_2026-08-29.md`

## 8. Caption

**System, record-state, and evidence architecture of WellPulse.** The upper panel separates the sender-local durable lifecycle from independent receiver-side evidence. Each generated telemetry record receives a stable `run:boot:sequence` identity and SHA-256 checksum before entering a SQLite write-ahead-logged `PENDING` state. Publish attempts use MQTT QoS 1; unavailable delivery returns to the durable queue, while a QoS 1 PUBACK permits the sender-local record to transition to `SENT`. Independently, the receiver stores unique record identities idempotently, and final delivery is reported from generated-versus-received identity reconciliation. The lower panels assign non-overlapping experimental roles: FIT IoT-LAB evaluates architecture-level record-state survival under B0/W1 × C0/C1/C2 (three runs per cell, 10,000 records per run), whereas POWDER provides E0–E11 controlled communication-path degradation/recovery evidence across RF, UE, CORE, broker, and no-fault domains. These evidence layers support two distinct resilience properties—record-state survival and communication-path recovery—and are integrated as complementary evidence without pooled cross-platform reliability statistics or a POWDER W1-versus-baseline effect.

## 9. Current project-line verdict

`P18R_F1_HOTFIX=PASS_DETERMINISTIC_F1_ACCEPTED`

`P18R_F1_BITWISE_PDF_REBUILD=PASS`

`P18R_F1_KNOWN_OVERLAPS=0`

`P18R_F1_SCIENTIFIC_SEMANTICS=PASS`

`P18R_F1_DRIVE_ARCHIVE=PASS`

`PROVENANCE_DRIFT=REPAIRED`

`AI_F1=REFERENCE_ONLY_NOT_CANONICAL`

`SCIENTIFIC_CONTENT_CHANGED=NO`

P18RB is already complete. The exact next main gate is **WP2-P18RC — MAIN-FIGURE PRODUCTION NORMALIZATION** before P19 packaging.
