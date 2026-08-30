# WellPulse R14/RF9H Figure + Caption Upgrade — Surgical QA Receipt

Date: 2026-08-30
Status: PASS

## Baseline authority
- Canonical R14/RF9H LaTeX SHA-256: `18b1c3579ce0e04eb4b0cc3f4c835c4ecb6c9ecdc094acd26fc2f62727b46d98`
- Baseline clean replay: 28/28 pages pixel-identical to packaged canonical PDF at 150 dpi.

## Authorized scope
- Replace Figures 1–4 with the approved v2 figure set.
- Correct Figure 3 Panel C only from ICMP response to frozen E3 ICMP loss semantics.
- Replace Captions 1–4 with the approved detailed captions; Caption 3 uses "ICMP response" for A–B and "ICMP loss" for C–D to match the actual panel semantics.
- No manuscript text outside the four figure environments may change.

## Hard gates
- Outside-figure-environment byte identity: PASS.
- Figure 3C frozen values: 49 dB = 0/0/0; 50 dB = 5/0/5; 51 dB = 10/5/50; 52 dB = 80/65/70: PASS.
- Figure 3A remains ICMP response: PASS.
- Figure 3C is ICMP loss: PASS.
- No interpolation, smoothing, fitted threshold, new statistics, or FIT+POWDER pooling: PASS.
- Final LaTeX log undefined references/citations: 0 on final pass.
- Final LaTeX log overfull boxes: 0.
- PDF openable / unencrypted / non-scanned: PASS.
- Final manuscript visual inspection: 29/29 pages PASS.
- Figures 1–4 inspected at final manuscript display size: PASS.
- Known clipping / overlap / broken glyphs: 0.

## Final identities
- Final TeX SHA-256: `b80e9b15221d0f79e2a96089f3c27d8524acdc6d9edfec53a336399a7fa59606`
- Final PDF SHA-256: `7f48cfb6f02bff65afda2532ec90c737215b0f5f7330a959f9c16b70af55b67b`

## Change-control note
An initial working-copy replacement expression was rejected by the source-diff gate because it spanned beyond one figure environment. It was discarded before acceptance. The canonical source was never modified. The accepted patch was rebuilt from the original canonical bytes using explicit per-label environment boundaries and passed the outside-environment byte-identity gate.
