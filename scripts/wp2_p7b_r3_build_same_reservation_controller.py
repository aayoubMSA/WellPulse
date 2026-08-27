#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def build(source: Path, output: Path, expid: str, name: str, source_sha: str, fallback_expiry: str) -> None:
    text = source.read_text(encoding="utf-8")
    old = 'SOURCE_SHA="${GITHUB_SHA:-$(git rev-parse HEAD)}"'
    if text.count(old) != 1:
        raise SystemExit("SOURCE_SHA_MARKER_MISMATCH")
    text = text.replace(old, f"SOURCE_SHA='{source_sha}'", 1)

    start = "  bar 5 'Authority guards + no-active-P7B check'; echo\n"
    end = '  portal-cli experiment manifests get --experiment-id "$EXPID" > "$TMP/manifests.json" || fail MANIFEST_FETCH 8\n'
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit("RESCUE_PATCH_MARKER_MISMATCH")
    i = text.index(start)
    j = text.index(end, i) + len(end)

    replacement = f'''  bar 5 'Same-reservation identity + degraded-control-plane corroboration'; echo
  EXPID='{expid}'
  EXP_NAME='{name}'
  set_output experiment_id "$EXPID"
  set_output experiment_name "$EXP_NAME"
  printf 'EXPID=%q\\nEXP_NAME=%q\\nPREPARE_GATE=SAME_RESERVATION_RESCUE\\n' "$EXPID" "$EXP_NAME" > "$STATE"

  LIST_OK=0
  for n in 1 2 3; do
    set +e
    portal-cli experiment list > "$TMP/list-existing.json" 2>"$TMP/list-existing.err"
    lrc=$?
    set -e
    if [[ "$lrc" -eq 0 ]]; then LIST_OK=1; break; fi
    echo "RESCUE_LIST_${{n}}=ERROR:rc=$lrc"
    sleep 2
  done
  EXPIRES=''
  if [[ "$LIST_OK" -eq 1 ]]; then
    MATCH_COUNT="$(jq --arg id "$EXPID" --arg name "$EXP_NAME" '[.[]? | select(.project=="WellPulse" and ((.id|tostring)==$id) and ((.name|tostring)==$name))] | length' "$TMP/list-existing.json" 2>/dev/null || echo 0)"
    if [[ "$MATCH_COUNT" == 0 ]]; then
      MATCH_COUNT="$(jq --arg id "$EXPID" --arg name "$EXP_NAME" '[.experiments[]? | select(.project=="WellPulse" and ((.id|tostring)==$id) and ((.name|tostring)==$name))] | length' "$TMP/list-existing.json" 2>/dev/null || echo 0)"
    fi
    [[ "$MATCH_COUNT" == 1 ]] || fail "EXACT_RESERVATION_MATCH_COUNT_$MATCH_COUNT" 6
    ROW="$(jq -c --arg id "$EXPID" --arg name "$EXP_NAME" '.[]? | select(.project=="WellPulse" and ((.id|tostring)==$id) and ((.name|tostring)==$name)' "$TMP/list-existing.json" 2>/dev/null | head -1)"
    if [[ -z "$ROW" ]]; then ROW="$(jq -c --arg id "$EXPID" --arg name "$EXP_NAME" '.experiments[]? | select(.project=="WellPulse" and ((.id|tostring)==$id) and ((.name|tostring)==$name)' "$TMP/list-existing.json" 2>/dev/null | head -1)"; fi
    LIST_STATUS="$(jq -r '.status // "unknown"' <<<"$ROW")"
    [[ ! "$LIST_STATUS" =~ ^(terminated|destroyed|failed|error)$ ]] || fail "RESERVATION_TERMINAL_$LIST_STATUS" 6
    EXPIRES="$(jq -r '.expires_at // .expires // .expiration // empty' <<<"$ROW")"
    echo "SAME_RESERVATION_LIST_GATE=PASS:$LIST_STATUS"
  else
    echo 'SAME_RESERVATION_LIST_GATE=DEGRADED_UNAVAILABLE'
  fi
  if [[ -z "$EXPIRES" ]]; then
    EXPIRES='{fallback_expiry}'
    echo "EXPIRY_SOURCE=CONSERVATIVE_UI_DERIVED:$EXPIRES"
  else
    echo "EXPIRY_SOURCE=PORTAL_LIST:$EXPIRES"
  fi
  python3 scripts/wp2_prelaunch_time_guard.py --now-utc "$(utc)" --expires-utc "$EXPIRES" --min-remaining-s 3000 | tee "$TMP/time-gate.txt"
  grep -q '^PRELAUNCH_TIME_GATE=PASS$' "$TMP/time-gate.txt" || fail PRELAUNCH_TIME 7

  MOK=0
  for n in 1 2 3 4; do
    set +e
    portal-cli experiment manifests get --experiment-id "$EXPID" > "$TMP/manifests.json" 2>"$TMP/manifests.err"
    mrc=$?
    set -e
    if [[ "$mrc" -eq 0 ]]; then MOK=1; echo "RESCUE_MANIFEST_${{n}}=PASS"; break; fi
    echo "RESCUE_MANIFEST_${{n}}=ERROR:rc=$mrc"
    tail -c 400 "$TMP/manifests.err" 2>/dev/null || true; echo
    sleep 3
  done
  [[ "$MOK" -eq 1 ]] || fail MANIFEST_FETCH_DEGRADED_CONTROL_PLANE 8
'''

    out = text[:i] + replacement + text[j:]
    if "portal-cli experiment create" in out:
        raise SystemExit("NEW_RESERVATION_PATH_SURVIVED")
    output.write_text(out, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="powder/wp2_p7b_r3_execute.sh")
    ap.add_argument("--output", required=True)
    ap.add_argument("--experiment-id", required=True)
    ap.add_argument("--experiment-name", required=True)
    ap.add_argument("--source-sha", required=True)
    ap.add_argument("--fallback-expiry", required=True)
    args = ap.parse_args()
    build(Path(args.source), Path(args.output), args.experiment_id, args.experiment_name, args.source_sha, args.fallback_expiry)
    print("SAME_RESERVATION_CONTROLLER_BUILD=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
