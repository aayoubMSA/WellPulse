# WP2 RS-7 — External Evidence Escrow Destination Freeze

Date: 2026-08-27
Owner: Pre-Reservation Consortium
Stage: PRE-RESERVATION / PRE-SCORE

## Decision

The real off-POWDER evidence destination is now frozen to the canonical WellPulse Google Drive validation workspace.

Drive hierarchy:

`P12_WellPulse / 00_Validation_Workspace / 02_RAW_EVIDENCE / POWDER_EVIDENCE_ESCROW`

Folder ID:

`18i-tHVI7YYCqeZMHDB-bXvUsXZ1D68km`

Folder URL:

`https://drive.google.com/drive/folders/18i-tHVI7YYCqeZMHDB-bXvUsXZ1D68km`

This folder was created successfully through the authenticated Google Drive connection and is the approved durable second-copy target for future POWDER Golden/scored evidence.

## rclone binding

Preferred remote name: `gdrive`

The rclone configuration should bind the remote/root to the folder above, either by using `root_folder_id = 18i-tHVI7YYCqeZMHDB-bXvUsXZ1D68km` or by a path mapping that resolves exactly to this folder. OAuth credentials/tokens must remain outside Git, console evidence, and scientific artifacts.

## Remaining pre-reservation gate

Destination existence and ownership are now **PASS**. Transport authentication from the actual POWDER execution environment remains **PENDING**.

Before `RESERVE=true`, run from the intended execution environment:

`WP_RCLONE_REMOTE_ROOT='gdrive:' bash scripts/wp2_golden_rclone_preflight.sh`

The preflight must prove:

1. authenticated listing;
2. write of a non-sensitive probe;
3. read-back of that probe;
4. exact SHA-256 equality;
5. deletion and deletion verification;
6. no credential/token material in output.

Required terminal result:

`RCLONE_PREFLIGHT=PASS`

Anything else keeps:

`RESERVE=false`

## Security rule

Never commit `rclone.conf`, OAuth tokens, refresh tokens, client secrets, or browser authorization codes. Only remote name, folder ID, non-sensitive probe hash, and PASS/FAIL evidence may enter the scientific repository.

## Current consortium status

`EXTERNAL_DESTINATION_FROZEN=PASS`

`POWDER_TO_DRIVE_AUTHENTICATED_TRANSPORT=PENDING`

`RS7_CURRENT_VERDICT=REPAIR_OFFLINE_FIRST`
