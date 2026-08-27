# K1-P — Portal API Immutable Revision Resolution — 2026-08-27

## Scope

Resolve and freeze the exact immutable upstream Git revision for the supported current Emulab/POWDER Portal API client, without contacting a POWDER experiment or performing any live scientific work.

## Authoritative repository identity

POWDER's current Advanced Topics documentation identifies the supported Portal API client repository as:

`https://gitlab.flux.utah.edu/emulab/portal-api`

The same documentation states that the Portal API is under active development. Therefore a moving branch such as `master`/HEAD is not acceptable for the reproducibility-critical Golden path.

The legacy XML-RPC Portal API is explicitly deprecated and is not accepted as a substitute for this closure.

## Resolution attempts

1. Attempted to resolve `emulab/portal-api` as a GitHub repository. Result: not authoritative / not present there; the official source is GitLab Flux.
2. Queried current POWDER/Emulab documentation and confirmed the exact official GitLab repository path.
3. Attempted direct read of the official GitLab project through the available web runtime. Result: HTTP 403 from the GitLab project surface.
4. Attempted a direct `git ls-remote https://gitlab.flux.utah.edu/emulab/portal-api.git refs/heads/master` from the local execution container. Result: the container could not resolve `gitlab.flux.utah.edu`; no commit SHA was returned.
5. Searched indexed web sources for an authoritative immutable commit URL/hash for the current repository. No authoritative commit SHA was recoverable.

## Evidence rule

No SHA was guessed, copied from an unofficial fork, inferred from a mirror, or substituted from the deprecated legacy API. A branch name, tag name, cached page, or third-party fork is insufficient for this gate.

## Verdict

`K1P=BLOCKED_AUTHORITATIVE_PORTAL_API_REVISION_UNAVAILABLE`

`PORTAL_API_REPOSITORY=https://gitlab.flux.utah.edu/emulab/portal-api`

`PORTAL_API_REVISION=UNRESOLVED`

`K1=BLOCKED_PORTAL_API_REVISION`

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

`REBOOK_GOLDEN=false`

## Scientific consequence

None. This patch is infrastructure/reproducibility governance only. No scientific run was performed, no POWDER reservation was contacted, and no completion credit is added.

## Exact next action

Do not advance to K2 under the current patch discipline. K1 can pass only when an authoritative immutable revision becomes available from the official GitLab repository or when the Portal client dependency is deliberately redesigned out of the future Golden path under a separately declared patch.
