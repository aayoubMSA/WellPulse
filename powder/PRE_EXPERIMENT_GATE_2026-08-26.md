# POWDER Pre-Experiment Gate — 2026-08-26

This file is a mandatory pre-read before the next POWDER experiment. It records operational readiness and the allocator lesson from the 2026-08-26 14:00–16:00 Africa/Cairo reservation without storing secret values.

## Credential / automation readiness

The GitHub Actions automation path is operationally provisioned with the required secret material. Secret values are never stored here.

Verified runtime capabilities:

- `POWDER_API_TOKEN` is available to GitHub Actions and the official Portal API client can authenticate.
- `POWDER_SSH_PRIVATE_KEY` is stored in GitHub Actions Secrets.
- `POWDER_SSH_KEY_PASSPHRASE` is stored in GitHub Actions Secrets.
- the private key structure is valid and the passphrase successfully unlocks it in GitHub Actions.
- the SSH identity loads into `ssh-agent` successfully.
- the corresponding public key has been registered with POWDER for future experiment instantiations.
- Portal API experiment list/get/manifests/create/terminate paths have been exercised successfully.
- exact profile bindings can be supplied through the Portal API.

Security rule: never write private keys, passphrases, API tokens, RPC tokens, certificate material, or raw credential-bearing exports into Git, chat, evidence bundles, or workflow logs.

## Operational lesson from the 14:00–16:00 reservation

Observed sequence:

1. `WP-HCAL-A` reached READY and had correct physical bindings, but its originally injected SSH key did not authorize the current automation identity.
2. After registering the current public key, `WP-HCAL-A` was terminated and `WP-HCAL-B` was created immediately on the same reserved `nuc1+nuc2` resources.
3. The immediate recreate remained stuck in allocator/control-plane recovery and did not reach READY.
4. `WP-HCAL-B` was terminated and a deliberate cooldown was allowed.
5. After cooldown, the resource-release gate reported no active H-cal experiments and `WP-HCAL-C` creation succeeded.
6. `WP-HCAL-C` nevertheless oscillated between `provisioning` and `pending` for about 23 minutes and never reached READY before the retry gate ended.
7. After the reservation expired, a read-only Portal API check showed zero visible/active H-cal experiments and a clean final release gate.

Scientific consequence: no H-calibration trial, LTE user-plane test, MQTT trial, or scored run occurred in this reservation. The window is operationally failed but scientifically clean.

## Frozen allocator/recreate rule

Treat experiment teardown and allocator/resource release as asynchronous control-plane operations.

Never use:

`terminate -> immediate recreate`

Use:

`terminate -> positively verify old experiment/resource release -> allow convergence interval -> recreate only if still necessary`

A successful terminate request alone is not proof that the same nodes are immediately reusable.

## Next reservation execution rule

For the next clean reservation:

1. read this file and `docs/DECISIONS.md` D-020 before creating anything;
2. instantiate exactly one fresh `PowderProfiles/srslte-controlled-rf` experiment early in the reservation;
3. use exact bindings `enb_node=nuc1`, `ue_node=nuc2`, `ue_type=srsue` only if the live reservation still grants those resources;
4. inject/use the current registered automation SSH public key through the approved secure path;
5. wait for `READY`; do not churn the allocator by terminate/recreate loops;
6. after READY, verify live manifest mapping and SSH on both nodes before any LTE/RF/scientific action;
7. if provisioning stalls, preserve state and diagnose; do not repeatedly recreate inside the same reservation;
8. no scored run is authorized until the existing WP2 gates close.

## Mandatory principle

The automation is now credential-ready. The remaining operational risk is testbed provisioning/control-plane convergence, not missing secret material. Future agents must not ask the user to re-enter or paste secret values unless independent evidence shows a credential has actually become invalid.
