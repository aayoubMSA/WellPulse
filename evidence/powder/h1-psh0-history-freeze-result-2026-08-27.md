# H1-PSH PSH-0 — Home-PC PowerShell History Freeze Result

Date: 2026-08-27
Evidence class: `LOCAL_SHELL_PROVENANCE_SNAPSHOT`

## Verdict

`H1_PSH0=PASS`

`H1_PSH0_HIGH_SPECIFICITY_H1_HITS=0`

`H1_PSH0_RAW_RECOVERY=NO`

This patch successfully preserved and hashed the discovered PowerShell history source without modifying it, then searched only the verified snapshot. It did **not** recover H1-specific commands or raw H1 artifacts.

## Runtime / source contract

Reported by the local PSH-0 run:

- PowerShell edition: `Core`
- PowerShell version: `7.6.5`
- current-host history path: `C:\Users\admino\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`
- history sources found: `1`
- network used: `NO`
- source mutation: `NO`
- source searched directly: `NO`
- snapshot/hash verification: `PASS`

## Search result

- total broad keyword hits: `1335`
- high-specificity H1 hits: `0`
- candidate command lines: `1266`

The broad counts are **not H1 evidence**. The first search vocabulary intentionally included generic operational terms such as `tar`, `Copy-Item`, `nuc1`, `WP2`, and related strings; this generated substantial non-H1 noise in a long pre-existing administrative/technical history. Only the high-specificity H1 anchors are scientifically relevant for PSH-0, and they returned zero matches.

No occurrence was found for the high-specificity anchors used by PSH-0, including the H1 experiment UUID/run ID and known H1 archive names/paths.

## Interpretation

PSH-0 proves only that the single discovered PSReadLine history source does not contain the targeted H1 anchors. It does **not** prove that no local H1 provenance exists elsewhere on the home PC.

Remaining plausible local evidence surfaces include, subject to a separate bounded read-only patch:

- additional PowerShell/Windows Terminal host histories not surfaced by the current PSReadLine path;
- PowerShell transcript files created by `Start-Transcript` or profile/automation scripts;
- terminal/session logs;
- local files/directories created or copied during H1;
- download/cache/temp paths and user-selected evidence directories;
- SSH/SCP/SFTP client logs or command records;
- shell history belonging to another Windows account/host context, if the H1 session was run under it.

Any next search must preserve the same contract: no network, no POWDER/GitHub coupling, no mutation, hash-before/hash-after for candidate provenance files, and no claim of raw recovery unless original bytes are independently verified.

## Scientific state

H1 remains `VALID_W1_RECOVERY_FAILURE`.

`H=UNFROZEN`

`scored_runs_authorized=false`

`REBOOK_GOLDEN=false`

Scientific weighted completion remains `20%`.
