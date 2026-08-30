# WellPulse — Current Handover

**Last updated:** 2026-08-30 after the R14/RF9H Figure + Caption Upgrade surgical closure and durable archive promotion.  
**Repository:** `aayoubMSA/WellPulse`  
**Branch:** `main`

This is the canonical operational handover. Do not create a competing current-state document.

## Current state

- **R14/RF9H Figure + Caption Upgrade: CURRENT MANUSCRIPT AUTHORITY**
- Parent R14/RF9H scientific baseline: **PRESERVED / SUPERSEDED FOR DISPLAY BY THE FIGURE+CAPTION UPGRADE**
- Figure/caption surgical QA: **PASS**
- Google Drive archive promotion: **PASS**
- Google Drive raw-file read-back hash: **PASS**
- Original P5 journal-facing package: **HISTORICAL / VALID FOR ITS PRE-UPGRADE BYTES**
- Existing WP3/WP4 anonymous portal bundle: **HISTORICAL / STALE RELATIVE TO CURRENT MANUSCRIPT**
- Portal bundle synchronized to current manuscript: **NO**
- Portal-generated PDF inspection: **NOT YET PERFORMED**
- External submission: **LOCKED / NOT EXECUTED**
- Scientific blockers for the bounded claim: **0**
- New experiment required: **NO**

## Current manuscript authority

Title: **Beyond Reconnection: Failure-Domain-Aware Evaluation of Data Durability and Recovery in MQTT-Based IoT Telemetry**

Author/corresponding author: **Ahmed Ayoub**  
Affiliation: Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City 12451, Egypt  
Email: `aelsayedo@msa.edu.eg`  
ORCID: `0009-0004-7895-3191`

Target route:
- journal: **Internet of Things (Elsevier)**;
- live portal article-type wording: **Full Length Article**;
- default publication model: **Subscription / non-OA**;
- backup: **IEEE Internet of Things Journal** only if rerouting becomes necessary.

Current credited manuscript:
- PDF: `WellPulse_R14_RF9H_FIGURE_CAPTION_UPGRADE.pdf`
- pages: **29**
- PDF SHA-256: `7f48cfb6f02bff65afda2532ec90c737215b0f5f7330a959f9c16b70af55b67b`
- TeX: `wellpulse_role_model_r14_rf9h_FIGURE_CAPTION_UPGRADE.tex`
- TeX SHA-256: `b80e9b15221d0f79e2a96089f3c27d8524acdc6d9edfec53a336399a7fa59606`
- bibliography: **38/38 cited**
- abstract: **227 words / unchanged from R14/RF9H**
- keywords: **7 / unchanged**

Parent canonical R14/RF9H baseline retained for provenance:
- PDF: `WellPulse_Role_Model_R14_RF9H_Two_Minor_Closure.pdf`
- pages: **28**
- PDF SHA-256: `d5f8006ecc3b0a284c7b5836ba4fee505878efe4003380d8cdbf1454a42b2f3a`
- TeX SHA-256: `18b1c3579ce0e04eb4b0cc3f4c835c4ecb6c9ecdc094acd26fc2f62727b46d98`

The accepted upgrade was constructed from those exact canonical TeX bytes. The source-diff gate verified that every byte outside the four authorized LaTeX `figure` environments remained unchanged.

## Figure + caption upgrade authority

The current manuscript uses the approved v2 full-width figure set and four detailed captions.

### Figure 1
- asset: `Figure01_system_evidence_architecture_v2.pdf`
- SHA-256: `bd855f923247836a7378e5d0462ebebf182ea3fecdd0bcb121daaa29b8c8b2e5`
- role: W1 sender-local durable lifecycle, independent receiver reconciliation, FIT/POWDER complementary evidence.

### Figure 2
- asset: `Figure02_FIT_record_survival_reconnect_catchup_v2.pdf`
- SHA-256: `8ce2e1a3054a10787378f5648e437a3daa36a4816dcdd43160f51259f1ada89c`
- role: receiver-reconciled record-state survival, reconnect, and durable catch-up.

### Figure 3
- asset: `Figure03_POWDER_direction_and_cycle_variation_v2_LOSS_CORRECTED.pdf`
- SHA-256: `8004926f0168a86fddef749b5ac0002c9f0ba19448d42a96fe381d86bf411640`
- Panel A: **ICMP response (%)** for directional E1R4/E2 sweeps.
- Panel C: **ICMP loss (%)** for E3 repeated cycles.
- frozen E3 loss values:
  - 49 dB: `0,0,0`
  - 50 dB: `5,0,5`
  - 51 dB: `10,5,50`
  - 52 dB: `80,65,70`
- no interpolation, fitted threshold, or universal attenuation claim.

### Figure 4
- asset: `Figure04_failure_domain_and_recovery_semantics_v2.pdf`
- SHA-256: `a0bb9fb61b6de95b9284d88428253324e9762d69545931e191c794d6a095a34e`
- role: failure-domain coverage plus censored / exact / upper-bound recovery semantics.

Final captions SHA-256: `dae9b81c52cf1f261d6b041f72ef707f5834f7b3b67ca1d7c61249f6cb1d723d`.

QA:
- baseline clean replay: **28/28 pages pixel-identical** to canonical R14/RF9H;
- accepted upgraded manuscript visual QA: **29/29 pages PASS**;
- figures inspected at actual manuscript display size: **PASS**;
- undefined references/citations: **0**;
- overfull boxes: **0**;
- clipping / overlap / broken glyphs: **0**;
- clean-package replay of final manuscript: **29/29 pages pixel-identical** to frozen final PDF.

Detailed repository record:
`publication/r14_rf9h_figure_caption_upgrade_2026-08-30/README.md`

## Durable Google Drive archive

Parent folder: `P12_WellPulse` / `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`

Current promotion folder:
- name: `R14_RF9H_FigureCaptionUpgrade_FINAL_2026-08-30`
- folder ID: `1lxUZ6ZhKOamOAY6bZJgmErVW-MiOvwpu`

Promoted authorities:
- final package ZIP ID: `1IA2NhpQLUAdUilQceamrkp6iBPDOwqh-`
- final package ZIP SHA-256: `68c704363a6ebe8933a7fb985497b2d3b72b88507f3cda41ecfe57741fb2cc6a`
- final manuscript PDF ID: `1izsyLpRtondjk1_mlPk_JoqEoY0jLPaJ`
- final manuscript PDF SHA-256: `7f48cfb6f02bff65afda2532ec90c737215b0f5f7330a959f9c16b70af55b67b`
- final TeX ID: `1clBSiLfEnd22vZ4A0lvk2nipejkxvK6-`
- Figure 1 ID: `1me1-AouU8MspWEvVwrJ8ygYQpVpRR7kf`
- Figure 2 ID: `1znQWaF7j0J4bDp5FKs6FiPi-ZkgXB2Vt`
- Figure 3 ID: `1tHE2vrAhv7PPpiPiy1RQuJIbwKhcHB7N`
- Figure 4 ID: `1YgaXAd7HVyk5cxuiZy4ox38HSUlvH8Cc`
- QA receipt ID: `1yDwKtQiuQvLRho1fI2Y6gJYseEHjGb-K`
- SHA256SUMS ID: `1Wg6A-vqPToYcj1oEBElEibKX560e_hCm`
- final captions ID: `1GFMD-h1Rw1lMnV71WbnLme6GWV7eJWTL`

Raw-file read-back verification:
- final ZIP re-fetched from Drive and re-hashed: **PASS / exact SHA match**;
- final PDF re-fetched from Drive and re-hashed: **PASS / exact SHA match**.

## Historical pre-upgrade package state

Original credited P5 package:
- `WellPulse_Submission_Package_R14_RF9H_2026-08-30.zip`
- SHA-256: `62c79223c0bd825250f7dbf92fc9cb51c2e40678285b40d5b5432a4452bd8b33`
- signed cover-letter SHA-256: `d37d3f383bdc30ab498818987b435ae4227396b208ec59e071450ea8d97f0894`

Existing double-anonymous WP4 bundle:
- `WellPulse_IOT_DoubleAnonymous_Portal_Bundle_R14_WP4_2026-08-30.zip`
- SHA-256: `e4c1452771add93b5682c6764285e7f50cd9e2259f46b39676d5ebea0857618d`
- Drive ID: `1DUWkRXOtoeX_6YnMvNelH9yVFHsP0zln`
- original WP4 archive/read-back: **PASS for those historical bytes**.

These files remain valid provenance but **must not be used for the next portal preview** because they predate the current figure/caption manuscript authority.

The P5 signed cover letter, graphical abstract, title page, highlights, and unchanged portal metadata may be reused only after confirming they remain semantically compatible with the current manuscript; do not reconstruct them unnecessarily.

## Frozen scientific boundaries

### FIT IoT-LAB
- B0/W1 × C0/C1/C2 × 3 run-level replicates = 18 cells.
- 10,000 generated records/run; the **run** is the scientific unit.
- healthy C0: B0/W1 complete at the declared endpoint.
- C1/C2: B0 = 8,000/10,000 and W1 = 10,000/10,000 in every replicate.
- +20 percentage points is a **bounded mechanism-isolation contrast**, not generic MQTT superiority.
- C2 = broker outage + **gateway-process exec restart**.
- reconnect ~1.3 s; durable queue drain ~67.7–67.9 s.
- receiver count termination bounds the claim to the declared capture endpoint.

### POWDER
- physical RF/LTE/MQTT characterization; not architecture treatment-effect estimation.
- programmed attenuation behavior is experiment/profile-specific, not universal.
- E10-A remains censored with no scalar latency.
- E10-B exact preserved endpoints remain exact.
- E10-C-B exact preserved endpoints remain exact.
- E10-D remains upper-bound only.
- E10 publish-to-receipt 0.0602 s is descriptive because no independent inter-node clock-synchronization error bound was established.
- FIT and POWDER are **not statistically pooled**.

## Immutable claim prohibitions

Do not claim:
- strongest-durable-MQTT superiority;
- generic `WellPulse beats MQTT`;
- population reliability from three FIT runs or from message counts;
- universal 52 dB behavior;
- deterministic RF-only recovery;
- exact broker-restart recovery when only an upper bound is preserved;
- pooled FIT+POWDER inference;
- historical firstness for persistence/store-and-forward/layered recovery;
- field, agronomic, pump, hydraulic, groundwater, rural, crop, or industrial-process validation.

Historical scored state remains:
`B1=NULL_ABORTED_AFTER_Q3`
`HISTORICAL_B1=CONSUMED`
`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

## Exact next action

**Do not resume at the Elsevier portal yet.** The existing anonymous bundle is stale relative to the current manuscript authority.

Next finite gate:
1. derive a new double-anonymous manuscript from `wellpulse_role_model_r14_rf9h_FIGURE_CAPTION_UPGRADE.tex` without changing scientific content;
2. preserve the exact current Figures 1–4 and captions;
3. rebuild/synchronize anonymous S2 only where necessary to reflect the exact current figure authority;
4. rebuild the portal bundle and SHA-256 manifests;
5. clean-unpack QA, anonymity scan, render/visual QA, and figure-semantic checks;
6. promote the synchronized bundle to Drive and read-back verify it;
7. only then resume at the live Elsevier portal preview;
8. build and inspect the portal-generated combined PDF;
9. stop before final Submit, copyright/license acceptance, or payment unless explicit author authority is given.

If suggested reviewers are mandatory, **STOP** and prepare a conflict-screened shortlist; do not invent names.

## Stop state

`R14_RF9H_FIGURE_CAPTION_UPGRADE_CURRENT_AUTHORITY=YES`
`FIGURE_CAPTION_SURGICAL_QA=PASS`
`DRIVE_PROMOTION=PASS`
`DRIVE_READBACK_HASH=PASS`
`OLD_WP4_PORTAL_BUNDLE=HISTORICAL_STALE`
`PORTAL_BUNDLE_SYNCHRONIZED=NO`
`PORTAL_RENDER=NOT_DONE`
`SUBMISSION_AUTHORIZED=NO`
`SUBMISSION_EXECUTED=NO`
`PAYMENT_AUTHORIZED=NO`
`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`
`CURRENT_PHASE=REBUILD_DOUBLE_ANONYMOUS_BUNDLE_FROM_FIGURE_CAPTION_UPGRADE`
