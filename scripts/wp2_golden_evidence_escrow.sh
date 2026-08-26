#!/usr/bin/env bash
set -euo pipefail

SRC="${WP_EVIDENCE_SRC:?WP_EVIDENCE_SRC is required}"
RUN_ID="${WP_RUN_ID:?WP_RUN_ID is required}"
EXPERIMENT_ID="${WP_EXPERIMENT_ID:?WP_EXPERIMENT_ID is required}"
PERSIST_ROOT="${WP_PERSIST_ROOT:-/proj/WellPulse/evidence-escrow}"
INVENTORY="${WP_EVIDENCE_INVENTORY:-experiments/WP-PWD01/evidence_inventory_golden_v1.txt}"
DEST_PERSIST="$PERSIST_ROOT/$EXPERIMENT_ID/$RUN_ID"

bar(){ local p="$1" m="$2" n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-48s' "$p" "$m"; }
fail(){ echo; echo "PERSISTENT_ESCROW_GATE=FAIL:$1" >&2; exit 40; }
utc(){ date -u +%Y-%m-%dT%H:%M:%S.%NZ; }

[[ -d "$SRC" ]] || fail SOURCE_NOT_DIRECTORY
[[ -f "$INVENTORY" ]] || fail INVENTORY_MISSING

bar 10 'Validating mandatory raw inventory'; echo
while IFS='|' read -r class rel nonempty desc; do
  [[ -z "$class" || "$class" == \#* ]] && continue
  [[ "$class" == REQUIRED ]] || continue
  p="$SRC/$rel"
  [[ -e "$p" ]] || fail "MISSING_REQUIRED:$rel"
  [[ "$nonempty" != yes || -s "$p" ]] || fail "EMPTY_REQUIRED:$rel"
done < "$INVENTORY"

bar 25 'Freezing source SHA-256 manifest'; echo
mkdir -p "$SRC/escrow"
(
  cd "$SRC"
  find . -type f \
    ! -path './escrow/SOURCE_SHA256SUMS.txt' \
    ! -path './escrow/PERSISTENT_SHA256SUMS.txt' \
    ! -path './escrow/PERSISTENT_ESCROW_GATE.PASS' \
    ! -path './escrow/escrow_provenance.json' \
    -print0 | sort -z | xargs -0 sha256sum > escrow/SOURCE_SHA256SUMS.txt
)
[[ -s "$SRC/escrow/SOURCE_SHA256SUMS.txt" ]] || fail SOURCE_MANIFEST_EMPTY

bar 50 'Copying evidence to persistent /proj'; echo
mkdir -p "$DEST_PERSIST"
rsync -a --delete "$SRC/" "$DEST_PERSIST/"

bar 75 'Verifying persistent copy against source hashes'; echo
(
  cd "$DEST_PERSIST"
  sha256sum -c escrow/SOURCE_SHA256SUMS.txt >/dev/null
  cp escrow/SOURCE_SHA256SUMS.txt escrow/PERSISTENT_SHA256SUMS.txt
) || fail PERSISTENT_VERIFY_FAILED

bar 90 'Writing persistent provenance'; echo
python3 - "$SRC" "$DEST_PERSIST" "$RUN_ID" "$EXPERIMENT_ID" <<'PY'
import json,sys,datetime,pathlib
src,persist,run_id,exp=sys.argv[1:]
payload={'run_id':run_id,'experiment_id':exp,'source':src,'persistent_copy':persist,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'gate':'PERSISTENT_COPY_VERIFIED'}
(pathlib.Path(persist)/'escrow'/'escrow_provenance.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
PY

printf 'run_id=%s\nexperiment_id=%s\nutc=%s\n' "$RUN_ID" "$EXPERIMENT_ID" "$(utc)" > "$DEST_PERSIST/escrow/PERSISTENT_ESCROW_GATE.PASS"

bar 100 'Persistent escrow PASS'; echo
printf 'PERSISTENT_EVIDENCE=%s\n' "$DEST_PERSIST"
printf 'PERSISTENT_ESCROW_GATE=PASS\n'
