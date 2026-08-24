# POWDER access plumbing

This directory supports the WellPulse POWDER validation campaign.

## Security boundary

- Never commit passwords, private SSH keys, key passphrases, API tokens, experiment RPC tokens, certificate material, or POWDER credentials.
- Public-key fingerprints and sanitized manifests/log extracts may be committed.
- GitHub Actions secrets used by existing plumbing workflows include:
  - `POWDER_SSH_PRIVATE_KEY`
  - `POWDER_USERNAME`
  - `POWDER_API_TOKEN`
- `powder/target.env` contains non-secret experiment routing only.
- The POWDER control/SSH network is for orchestration and evidence collection only; publication telemetry must traverse the experimental radio/data path defined by the frozen protocol.

## Manual-first rule

Resource-creating POWDER automation is **frozen** until the equivalent manual path has first passed and been documented.

The verified manual infrastructure baseline is:

`powder/MANUAL_GOLDEN_PATH.md`

Evidence for the first accepted run is:

`evidence/powder/manual-golden-path-2026-08-24.md`

## Canonical SSH baseline

The current canonical manual SSH key registered in POWDER is labeled:

`WellPulse-POWDER-Golden`

Fingerprint:

`SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`

The private key is local only and protected by a user-held passphrase.

Older keys/workflows remain historical plumbing until deliberately re-qualified; do not assume that an older automation key is the current acceptance key.

## Verified infrastructure gate

On 2026-08-24, the following manual path passed:

`WellPulse project -> srsLTE-SIM:9 -> d430 -> READY -> explicit Golden-key SSH -> metadata checks -> manual terminate -> Current Usage 0`

This gate is infrastructure readiness only. It is **not** publication evidence and does not advance the scientific WP percentage.

## Existing read-only plumbing workflow

The repository contains a read-only SSH plumbing workflow. It does not reserve resources, instantiate/terminate experiments, change radio settings, or start a scored run.

When it is deliberately re-qualified for use:

1. Instantiate an already approved experiment/profile manually.
2. Copy the exact SSH hostname shown by POWDER for the active node.
3. Set `POWDER_HOST` in `powder/target.env` and optionally record the experiment/profile names.
4. Commit the change to invoke the read-only plumbing check.
5. Confirm SSH and sanitized metadata evidence only.

Do not populate `powder/target.env` with a historical hostname after an experiment has been destroyed.

## Scientific gate boundary

Passing SSH plumbing proves only control-plane access. Before any scored POWDER run, the project must still establish:

- a current controlled physical-RF profile;
- experimental user-plane traffic rather than control-network bypass;
- calibrated Q0–Q3 states;
- frozen runtime/session configuration;
- complete evidence capture and deterministic analysis.
