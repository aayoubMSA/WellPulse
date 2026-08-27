# H1-PSH — Home-PC PowerShell History Salvage

**Status:** PLANNED / HIGH-ROI RECOVERY SUBPATCH  
**Parent lane:** H1 evidence salvage  
**Mode:** LOCAL / READ-ONLY / NO POWDER CONTACT  
**Scientific state:** unchanged (`H=UNFROZEN`, `scored_runs_authorized=false`, `REBOOK_GOLDEN=false`)

## Why this subpatch exists

The H1 experiment was operated from the user's home PC through PowerShell. Local shell history may therefore retain commands, paths, timestamps or adjacent terminal evidence that were not preserved in GitHub or POWDER persistent storage.

This is a potentially high-value recovery path because it may identify:

- exact H1 commands actually issued;
- local paths used for copied/downloaded evidence;
- archive names and transfer commands;
- SCP/SFTP/rclone/Git commands used during closeout;
- stdout/stderr fragments copied into commands or variables;
- temporary local files referenced by the shell;
- command chronology around H1, recovery characterization, hashing, and teardown;
- evidence that raw bundles may have been copied to the home PC or another local/off-platform path.

PowerShell history itself is not automatically scientific raw evidence. It is a provenance/recovery source that may lead to stronger local artifacts.

## Evidence safety rules

1. Read-only first. Do not clear, rewrite, truncate, deduplicate, normalize, or otherwise mutate shell history before preservation.
2. Preserve the original history file(s) byte-for-byte before analysis and record SHA-256.
3. Do not paste or commit credentials, tokens, private keys, passphrases, certificates, RPC secrets, bearer tokens, or other secret material.
4. Redaction occurs only on a derived analysis copy; the original local evidence should remain private and immutable.
5. Do not infer that a command succeeded merely because it appears in history.
6. Separate:
   - command history;
   - command-output/transcript evidence;
   - recovered local files;
   - Git/GitHub-derived evidence;
   - missing/unverified claims.
7. Do not change H1 classification from `VALID_W1_RECOVERY_FAILURE` based on history alone.

## Target locations to inspect

Potential PowerShell/terminal sources include, depending on the user's environment:

- PSReadLine history from `(Get-PSReadLineOption).HistorySavePath`;
- Windows PowerShell and PowerShell 7 profile-specific history locations;
- Windows Terminal state/session remnants where available;
- explicit PowerShell transcripts if `Start-Transcript` was used;
- command history exposed by the current shell session;
- terminal text files or pasted command scripts created during H1;
- Downloads/Desktop/Documents/temp directories referenced by H1 commands;
- local Git clone/repository working tree and reflog if H1 commands wrote local artifacts before commit;
- SSH/SCP/rclone client command references that may reveal destination paths.

Do not assume any one default path; determine the actual history path from PowerShell first.

## Search anchors

Search the preserved history copy and nearby local filesystem metadata for at least:

- `WP-HCAL-E`
- `wp2h1-a1-20260826-001`
- `9153e16a-1eb1-45f5-88bf-303636a9d1ec`
- `nuc1`
- `nuc2`
- `wellpulse-powder-evidence`
- `wp2-h1-valid-failure-20260826`
- `sender_summary.json`
- `calibration_manifest.json`
- `attenuation_timeline.csv`
- `telemetry_generated.csv`
- `queue_timeline.csv`
- `mqtt_events.jsonl`
- `w1_queue.sqlite`
- `SHA256SUMS`
- `tar.gz`
- `scp`
- `sftp`
- `rclone`
- `/users/aayoub`
- `/proj/WellPulse`
- H1 archive hashes:
  - `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
  - `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

## Execution sequence for the future H1-PSH run

### PSH-0 — Freeze local source

- Determine exact PowerShell history path(s).
- Copy the original history file(s) to a private evidence workspace without modifying the originals.
- Compute SHA-256 for every preserved source.
- Record file size, last-write time, path, PowerShell edition/version where available.

Gate:

`PSH_HISTORY_SOURCE_FROZEN=PASS`

### PSH-1 — Bounded H1 extraction

- Search only the preserved copy for H1 anchors and a bounded surrounding command window.
- Produce a chronological, redacted command index.
- Mark every line as COMMAND_ONLY unless independent output/transcript evidence exists.

Gate:

`PSH_H1_COMMAND_WINDOW=PASS|NO_HIT`

### PSH-2 — Local artifact path recovery

For every candidate path/destination found in history:

- inspect existence read-only;
- inventory file names/sizes/timestamps;
- hash candidate files;
- compare hashes to known H1 archive/hash anchors;
- do not alter or open potentially secret-bearing files unnecessarily.

Possible high-value outcomes:

- full original H1 tar bundle recovered;
- extracted raw H1 directory recovered;
- partial raw file(s) recovered;
- PowerShell transcript/output recovered;
- transfer destination identified but data absent;
- no local artifact recovered.

Gate:

`PSH_LOCAL_ARTIFACT_RECOVERY=FULL|PARTIAL|PROVENANCE_ONLY|NONE`

### PSH-3 — Evidence classification

Classify each recovered object as one of:

- `RAW_ORIGINAL_BYTES`
- `RAW_EXTRACTED_FROM_VERIFIED_ARCHIVE`
- `TERMINAL_TRANSCRIPT`
- `COMMAND_HISTORY_ONLY`
- `DERIVED_LOCAL_OUTPUT`
- `PROVENANCE_POINTER`
- `SECRET_BEARING_QUARANTINE`

No object may be promoted to raw evidence without byte-level provenance and hash verification.

### PSH-4 — Reconcile against canonical H1 salvage

If raw bytes are recovered:

1. compare archive/file hashes against historical anchors;
2. preserve a new off-platform immutable copy;
3. update H1 salvage status accurately;
4. re-enable only the RS-1 components supported by the recovered corpus;
5. do not alter H1's frozen adverse classification.

If only history/provenance is recovered, extend the salvage package but keep record-level reconstruction blocked.

## Exit conditions

### PASS — Full recovery

`H1_POWERSHELL_SALVAGE=PASS_FULL_RAW_RECOVERED`

Only if the local machine yields the original H1 raw bundle(s) or an independently verifiable equivalent record-level corpus whose hashes/provenance can be reconciled.

### PASS — Partial/provenance recovery

`H1_POWERSHELL_SALVAGE=PASS_PARTIAL`

Useful commands, paths, transcript, or some raw files are recovered, but the complete record-level corpus is still unavailable.

### CLOSED — No recovery

`H1_POWERSHELL_SALVAGE=CLOSED_NO_RECOVERY`

History is preserved and searched correctly but yields no material H1 evidence.

## Relationship to K1

This subpatch **preempts K1** because recovery of H1 raw data has much higher scientific ROI than supply-chain pin cleanup and can be performed entirely offline on the home PC.

The next explicit execution patch should therefore be H1-PSH before K1.

After H1-PSH execution: update `HANDOVER_CURRENT.md` and STOP before any subsequent patch.
