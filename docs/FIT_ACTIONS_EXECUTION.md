# FIT IoT-LAB execution through GitHub Actions

## Purpose

Run the WellPulse FIT A8 capability smoke without exposing FIT credentials to the repository, ChatGPT, workflow artifacts, or remote command logs.

## One-time repository secrets

In the private `aayoubMSA/WellPulse` repository, open:

`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

Create exactly these two repository secrets:

- `FIT_USERNAME` — the IoT-LAB login.
- `FIT_PASSWORD` — the IoT-LAB password.

Do not commit either value to a file, issue, discussion, workflow input, or GitHub variable.

## Workflow

`.github/workflows/fit-a8-smoke.yml`

The workflow:

1. Creates an ephemeral `.iotlabrc` only inside the GitHub-hosted runner.
2. Validates FIT credentials through the official IoT-LAB CLI.
3. Inventories live A8 nodes.
4. Generates a one-run RSA SSH key and registers only its public key with FIT.
5. Attempts a bounded 15-minute reservation of one A8 node.
6. Waits for Linux boot and runs `scripts/fit_probe.sh`.
7. Retrieves the raw probe log and checksums it.
8. Attempts an authenticated MQTT publish/receive smoke without placing the password on a command line or in an artifact.
9. Stops the experiment even on failure.
10. Removes the ephemeral SSH public key from the FIT account.
11. Deletes local runner credentials and private key material.
12. Uploads only non-secret smoke evidence as a GitHub Actions artifact.

## Evidence boundary

This workflow produces `CAPABILITY_SMOKE_NOT_FINAL_EXPERIMENT` evidence only. Passing it authorizes WP-RT01 final scheduling; it does not count as a final experiment and cannot support Siwa pump/hydraulic/field claims.

## Trigger control

The workflow supports manual dispatch and a same-repository pull request that changes `.fit-smoke-trigger`. The latter is used so the run can be inspected through the connected GitHub tooling without exposing secrets.

## After the smoke

If FIT access will not be used again soon, remove `FIT_PASSWORD` from GitHub Actions secrets or rotate the FIT password. Never place the password in a chat message.
