#!/usr/bin/env bash
set -euo pipefail

SRC="${WP_EVIDENCE_SRC:?WP_EVIDENCE_SRC is required}"
RUN_ID="${WP_RUN_ID:?WP_RUN_ID is required}"
EXPERIMENT_ID="${WP_EXPERIMENT_ID:?WP_EXPERIMENT_ID is required}"
PERSIST_ROOT="${WP_PERSIST_ROOT:-/proj/WellPulse/evidence-escrow}"
OFF_ROOT="${WP_OFF_POWDER_ROOT:?WP_OFF_POWDER_ROOT is required and must be outside POWDER}"
INVENTORY="${WP_EVIDENCE_INVENTORY:-experiments/WP-PWD01/evidence_inventory_golden_v1.txt}"
DEST_PERSIST="$PERSIST_ROOT/$EXPERIMENT_ID/$RUN_ID"
DEST_OFF="$OFF_ROOT/$EXPERIMENT_ID/$RUN_ID"

utc(){ date -u +%Y-%m-%dT%H:%M:%S.%NZ; }
bar(){
  local p="$1" m="$2" n
  n=$((p/5))
  printf '\r['
  printf '%*s' "$n" ''|tr ' ' '#'
  printf '%*s' "$((20-n))" ''|tr ' ' '-'
  printf '] %3d%%  %-48s' "$p" "$m"
}
fail(){ echo; echo "EVIDENCE_ESCROW_GATE=FAIL:$1" >&2; exit 40; }

[[ -d "$SRC" ]] || fail "SOURCE_NOT_DIRECTORY"
[[ -f "$INVENTORY" ]] || fail "INVENTORY_MISSING"
case "$OFF_ROOT" in /proj/*|/users/*|/share/*) fail "OFF_POWDER_ROOT_IS_ON_POWDER";; esac

bar 5 'Validating mandatory raw inventory'; echo
while IFS='|' read -r class rel nonempty desc; do
  [[ -z "$class" || "$class" == \#* ]] && continue
  [[ "$class" == "REQUIRED" ]] || continue
  p="$SRC/$rel"
  [[ -e "$p" ]] || fail "MISSING_REQUIRED:$rel"
  if [[ "$nonempty" == "yes" ]]; then [[ -s "$p" ]] || fail "EMPTY_REQUIRED:$rel"; fi
done < "$INVENTORY"

bar 15 'Freezing source SHA-256 manifest'; echo
mkdir -p "$SRC/escrow"
(
  cd "$SRC"
  find . -type f \
    ! -path './escrow/SOURCE_SHA256SUMS.txt' \
    ! -path './escrow/PERSISTENT_SHA256SUMS.txt' \
    ! -path './escrow/OFF_POWDER_SHA256SUMS.txt' \
    ! -path './escrow/escrow_provenance.json' \
    ! -path './escrow/EVIDENCE_ESCROW_GATE.PASS' \
    -print0 | sort -z | xargs -0 sha256sum > escrow/SOURCE_SHA256SUMS.txt
)
[[ -s "$SRC/escrow/SOURCE_SHA256SUMS.txt" ]] || fail "SOURCE_MANIFEST_EMPTY"

bar 30 'Copying immutable bundle to /proj'; echo
mkdir -p "$DEST_PERSIST"
rsync -a --delete "$SRC/" "$DEST_PERSIST/"

bar 45 'Verifying /proj copy against source hashes'; echo
(
  cd "$DEST_PERSIST"
  sha256sum -c escrow/SOURCE_SHA256SUMS.txt >/dev/null
  cp escrow/SOURCE_SHA256SUMS.txt escrow/PERSISTENT_SHA256SUMS.txt
) || fail "PERSISTENT_VERIFY_FAILED"

bar 60 'Copying verified bundle off POWDER'; echo
mkdir -p "$DEST_OFF"
rsync -a --delete "$DEST_PERSIST/" "$DEST_OFF/"

bar 75 'Verifying off-POWDER copy against source hashes'; echo
(
  cd "$DEST_OFF"
  sha256sum -c escrow/SOURCE_SHA256SUMS.txt >/dev/null
  cp escrow/SOURCE_SHA256SUMS.txt escrow/OFF_POWDER_SHA256SUMS.txt
) || fail "OFF_POWDER_VERIFY_FAILED"

bar 88 'Writing provenance record'; echo
python3 - "$SRC" "$DEST_PERSIST" "$DEST_OFF" "$RUN_ID" "$EXPERIMENT_ID" <<'PY'
import json,sys,datetime,pathlib
src,persist,off,run_id,exp=sys.argv[1:]
payload={
 'run_id':run_id,'experiment_id':exp,'source':src,'persistent_copy':persist,'off_powder_copy':off,
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'gate':'DUAL_COPY_VERIFIED'
}
text=json.dumps(payload,indent=2,sort_keys=True)+'\n'
(pathlib.Path(persist)/'escrow'/'escrow_provenance.json').write_text(text)
(pathlib.Path(off)/'escrow'/'escrow_provenance.json').write_text(text)
PY

bar 95 'Creating PASS markers only after dual verification'; echo
printf 'run_id=%s\nexperiment_id=%s\nutc=%s\n' "$RUN_ID" "$EXPERIMENT_ID" "$(utc)" > "$DEST_PERSIST/escrow/EVIDENCE_ESCROW_GATE.PASS"
cp "$DEST_PERSIST/escrow/EVIDENCE_ESCROW_GATE.PASS" "$DEST_OFF/escrow/EVIDENCE_ESCROW_GATE.PASS"

bar 100 'Evidence escrow PASS'; echo
printf 'PERSISTENT_EVIDENCE=%s\n' "$DEST_PERSIST"
printf 'OFF_POWDER_EVIDENCE=%s\n' "$DEST_OFF"
printf 'EVIDENCE_ESCROW_GATE=PASS\n'
