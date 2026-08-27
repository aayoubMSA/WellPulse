# WP2 P7B — 10-Minute POWDER Preflight Contract v1

Status: PROSPECTIVE / NON-SCORED / READ-ONLY

Purpose: convert accumulated WellPulse lessons into one short target-environment gate before any future P7B scientific or RF action.

## Doctrine
A live reservation MUST NOT enter B1/W1/B2 until one read-only preflight capsule proves the exact target environment and external interface shapes used by the controller.

This preflight implements lessons LL-006, LL-020, LL-021, LL-022, LL-023, LL-024, LL-025 and LL-026.

## Maximum scope
The capsule MAY read Portal identity/manifest, resolve node logins, SSH to already-created nodes, read OS/tool/runtime versions, read `tmcc attenuator` output without changing attenuation, syntax-check intended sources with the exact executing interpreter, verify absolute path rules, verify preservation tooling, and emit a bounded report.

The capsule MUST NOT create/extend/terminate a reservation, change attenuation, start B1/W1/B2, start/restart broker/gateway/generator/receiver, publish scientific telemetry, change scored authorization, or delete evidence.

## Mandatory gates
1. `IDENTITY_GATE`: UUID/name/project/profile revision/bindings match the frozen reservation contract.
2. `TARGET_RUNTIME_GATE`: capture OS/image, system Python identities, pinned WellPulse Python, Bash, Java/Javac, Mosquitto clients and OpenSSL; map every executable to one exact interpreter/tool.
3. `SOURCE_COMPATIBILITY_GATE`: syntax-check each Python source with the exact interpreter that will execute it; preservation must remain shell-only unless a pinned interpreter is explicitly proven.
4. `EXTERNAL_INTERFACE_GATE`: capture raw `tmcc attenuator` output; parser fixture must match observed output; distinguish command failure, parser failure and semantic mismatch; Portal transport errors are observations, not experiment-state verdicts.
5. `SSH_STATE_GATE`: authentication and dependent SSH/SCP actions occur in one execution context or use explicit persisted state; no hidden cross-step `ssh-agent` dependency.
6. `PATH_GATE`: reject unresolved `$HOME`, `${...}` and `~`; writer path == watcher path == preservation path.
7. `PRESERVATION_GATE`: `find`, `tar`, `sha256sum`, `ssh`, `scp` available; `/proj/WellPulse` reachable; evidence survival does not depend on application Python; explicit per-node source ownership is defined.

## Verdict
Only:
`WP2_P7B_10MIN_PREFLIGHT=PASS`
or
`WP2_P7B_10MIN_PREFLIGHT=BLOCKED:<first_actionable_failure>`

PASS authorizes only progression to the separately authorized live protocol. It is not scientific evidence and cannot change `scored_runs_authorized=false`.

## Time budget
Target wall time <= 4 minutes on an already-ready reservation. Hard stop 8 minutes. If unresolved by 8 minutes, return BLOCKED rather than exploratory troubleshooting.
