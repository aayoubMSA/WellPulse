# WellPulse R14/RF9H Figure + Caption Upgrade — Archive Promotion

Date: 2026-08-30
Status: **PROMOTED / DRIVE READ-BACK VERIFIED / NOT SUBMITTED**

## Purpose

This record promotes the surgically upgraded R14/RF9H manuscript and its final Figure 1–4 artifact set without changing manuscript science beyond the authorized four figure environments.

Starting canonical R14/RF9H TeX SHA-256:

`18b1c3579ce0e04eb4b0cc3f4c835c4ecb6c9ecdc094acd26fc2f62727b46d98`

Final figure/caption-upgraded TeX SHA-256:

`b80e9b15221d0f79e2a96089f3c27d8524acdc6d9edfec53a336399a7fa59606`

Final manuscript PDF SHA-256:

`7f48cfb6f02bff65afda2532ec90c737215b0f5f7330a959f9c16b70af55b67b`

Final package ZIP SHA-256:

`68c704363a6ebe8933a7fb985497b2d3b72b88507f3cda41ecfe57741fb2cc6a`

## Figure authority

- Figure 1 PDF SHA-256: `bd855f923247836a7378e5d0462ebebf182ea3fecdd0bcb121daaa29b8c8b2e5`
- Figure 2 PDF SHA-256: `8ce2e1a3054a10787378f5648e437a3daa36a4816dcdd43160f51259f1ada89c`
- Figure 3 PDF SHA-256: `8004926f0168a86fddef749b5ac0002c9f0ba19448d42a96fe381d86bf411640`
- Figure 4 PDF SHA-256: `a0bb9fb61b6de95b9284d88428253324e9762d69545931e191c794d6a095a34e`

Figure 3 semantics are intentionally mixed by experiment view:
- Panel A: **ICMP response (%)** for directional E1R4/E2 sweeps.
- Panel C: **ICMP loss (%)** for E3 repeated-cycle observations.
- Frozen E3 loss values: 49 dB = `0,0,0`; 50 dB = `5,0,5`; 51 dB = `10,5,50`; 52 dB = `80,65,70`.

## QA authority

- canonical-to-upgrade source diff SHA-256: `d9ed5642e0a0b2ebd3ab883c167f551fc2483be6fc767bb4e6a571b009620227`
- QA receipt SHA-256: `a0f6f831772043cd832637edc155c08af4fab652306c968f5867145e521b700f`
- final captions SHA-256: `dae9b81c52cf1f261d6b041f72ef707f5834f7b3b67ca1d7c61249f6cb1d723d`
- Figure 3C correction script SHA-256: `cec97d7b6e80178b3465a8b95534a6cbefbae39fd3664b525832597352141c93`

The QA gate established that all bytes outside the four authorized LaTeX `figure` environments remained identical to the canonical R14/RF9H source.

## Google Drive durable archive

Parent project folder: `P12_WellPulse` (`1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`)

Promotion folder:
- name: `R14_RF9H_FigureCaptionUpgrade_FINAL_2026-08-30`
- folder ID: `1lxUZ6ZhKOamOAY6bZJgmErVW-MiOvwpu`
- URL: https://drive.google.com/drive/folders/1lxUZ6ZhKOamOAY6bZJgmErVW-MiOvwpu

Promoted binary authorities:
- final package ZIP ID: `1IA2NhpQLUAdUilQceamrkp6iBPDOwqh-`
- final manuscript PDF ID: `1izsyLpRtondjk1_mlPk_JoqEoY0jLPaJ`
- Figure 1 PDF ID: `1me1-AouU8MspWEvVwrJ8ygYQpVpRR7kf`
- Figure 2 PDF ID: `1znQWaF7j0J4bDp5FKs6FiPi-ZkgXB2Vt`
- Figure 3 PDF ID: `1tHE2vrAhv7PPpiPiy1RQuJIbwKhcHB7N`
- Figure 4 PDF ID: `1YgaXAd7HVyk5cxuiZy4ox38HSUlvH8Cc`
- final TeX ID: `1clBSiLfEnd22vZ4A0lvk2nipejkxvK6-`
- QA receipt ID: `1yDwKtQiuQvLRho1fI2Y6gJYseEHjGb-K`
- SHA256SUMS ID: `1Wg6A-vqPToYcj1oEBElEibKX560e_hCm`
- final captions ID: `1GFMD-h1Rw1lMnV71WbnLme6GWV7eJWTL`

### Read-back verification

The uploaded final package ZIP and final manuscript PDF were fetched back from Google Drive as raw files and independently re-hashed:

- ZIP read-back SHA-256 = `68c704363a6ebe8933a7fb985497b2d3b72b88507f3cda41ecfe57741fb2cc6a` — **PASS**
- PDF read-back SHA-256 = `7f48cfb6f02bff65afda2532ec90c737215b0f5f7330a959f9c16b70af55b67b` — **PASS**

## Operational boundary

This promotion does **not** update the existing double-anonymous portal bundle. That older bundle predates this figure/caption upgrade and must be rebuilt from the new manuscript authority before portal preview.

`DRIVE_PROMOTION=PASS`
`DRIVE_READBACK_HASH=PASS`
`MANUSCRIPT_FIGURE_CAPTION_UPGRADE=PASS`
`PORTAL_BUNDLE_SYNCHRONIZED=NO`
`SUBMISSION_EXECUTED=NO`
