# POWDER access plumbing

This directory supports the WellPulse POWDER validation campaign.

## Security boundary

- Never commit passwords, private SSH keys, API tokens, or POWDER credentials.
- GitHub Actions secrets used by the plumbing workflow:
  - `POWDER_SSH_PRIVATE_KEY`
  - `POWDER_USERNAME`
- `powder/target.env` contains non-secret experiment routing only.
- The POWDER control/SSH network is for orchestration and evidence collection only; publication telemetry must traverse the experimental radio/data path defined by the frozen protocol.

## Bootstrap state

The dedicated public key registered in POWDER is labeled `WellPulse-POWDER-Automation`.

The workflow is intentionally read-only with respect to POWDER. It does not reserve resources, instantiate/terminate experiments, change radio settings, or start a scored run.

## How a plumbing check is launched

1. Instantiate the approved POWDER experiment/profile manually.
2. Copy the exact SSH hostname shown by POWDER for one SSH-capable experiment node.
3. Set `POWDER_HOST` in `powder/target.env` and optionally record the experiment/profile names.
4. Commit the change. That push triggers `.github/workflows/powder-plumbing.yml`.
5. The workflow checks SSH and writes a sanitized result to `evidence/powder/latest.md`.

To repeat a check without changing the target, update `.powder-plumbing-trigger`.

## Gate

`POWDER_PLUMBING_PASS` requires:

- GitHub Actions can load the dedicated private key from secrets;
- SSH authentication succeeds non-interactively;
- the remote username and hostname can be read;
- basic OS/time metadata can be collected;
- no scientific experiment or radio reservation is modified.

Passing this gate is infrastructure readiness only. It is not publication evidence and does not advance the scientific WP percentage.
