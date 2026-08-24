# POWDER G3 Simulated-Stack Automation

## Purpose

This is the first automated POWDER gate permitted after the manual G0-G2 golden path was proven. It remains **non-scored infrastructure evidence**.

The workflow automates the official `srsLTE-SIM` profile example:

`provision -> READY -> manifest -> SSH -> pdsch_enodeb -> file -> pdsch_ue -> evidence -> mandatory teardown`

It does not use SDR or RF and does not run WellPulse/MQTT scientific telemetry.

## Workflow

`.github/workflows/powder-g3-simstack.yml`

The workflow is `workflow_dispatch` only. It cannot start from an ordinary push.

To authorize exactly one run, open GitHub Actions, select **POWDER G3 Simulated Stack**, choose **Run workflow**, and enter:

```text
G3SIM
```

Any other value exits before resource creation.

## Existing secrets used

The workflow uses the existing repository secrets:

- `POWDER_API_TOKEN`
- `POWDER_USERNAME`
- `POWDER_SSH_PRIVATE_KEY`

The manual passphrase-protected key `WellPulse-POWDER-Golden` is deliberately not copied into CI. Automation uses the separate registered key `WellPulse-POWDER-Automation`.

Before creating an experiment, the workflow derives the automation public key non-interactively and requires this fingerprint:

```text
SHA256:jQGQvU86rtuEchT50N1HuB4Cmizpvbmp0zSBR4rowxY
```

If the secret is encrypted, malformed, or does not match that fingerprint, the workflow fails **before allocating POWDER resources**.

## Frozen automation target

```text
Project:         WellPulse
Profile project: PowderProfiles
Profile name:    srsLTE-SIM
Expected node:   d430
Expected image:  PowderProfiles:gnuradio-srslte
Duration:        1 hour maximum; normally terminated in minutes
```

The workflow parses the returned manifest and aborts if the hardware or image does not match the expected instrument.

## Remote test

The committed remote runner is:

`powder/g3_simstack_remote.sh`

It executes the profile's official file-based example:

```bash
/usr/local/srsLTE/build/lib/examples/pdsch_enodeb -o <temp-file> -n 5 -m 9 -v
/usr/local/srsLTE/build/lib/examples/pdsch_ue -i <temp-file> -n 5 -r 1234 -v -d
```

The process gate requires:

- transmitter executable present;
- transmitter exit code `0`;
- generated waveform file is non-empty;
- receiver executable present;
- receiver exit code `0`.

The waveform binary is deleted on the remote node after the run. Only its byte count and SHA-256 are retained.

## Evidence retained

Latest summary:

`evidence/powder/g3-simstack-latest.md`

Per-run text evidence:

`evidence/powder/g3/<github-run-id>/`

The per-run bundle contains only credential-free material such as:

- `remote-meta.txt`
- `result.env`
- `tx.log`
- `rx.log`
- `manifest-summary.json`
- `ssh-preflight.txt`

Raw Portal manifests and API responses that may contain encrypted RPC-token/certificate material are not committed.

## Fail-safe cleanup

Termination runs under `if: always()` after the experiment ID exists. The workflow then polls until the experiment is absent or reports a terminal destroyed/terminated state.

A run is final PASS only if both are true:

```text
PROCESS_GATE=PASS
cleanup=PASS
```

If execution fails but cleanup passes, the run is retained as failed troubleshooting evidence.

If cleanup cannot be proven, the workflow fails hard and the POWDER portal must be inspected immediately for a possible live allocation.

## Evidence boundary

A G3 PASS establishes only that the currently provisioned `srsLTE-SIM` software stack can complete its official simulated eNodeB-to-file-to-UE example on allocated POWDER compute under automated orchestration.

It does **not** establish physical RF operation, conducted attenuation, OTA behavior, real cellular user-plane performance, WellPulse telemetry resilience, or any scored WP-PWD01 endpoint.
