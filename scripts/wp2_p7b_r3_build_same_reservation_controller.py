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

    replacement = f'''  bar 5 'Same-reservation UUID corroboration with bounded Portal retries'; echo
  EXPID='{expid}'
  EXP_NAME='{name}'
  set_output experiment_id "$EXPID"
  set_output experiment_name "$EXP_NAME"
  printf 'EXPID=%q\\nEXP_NAME=%q\\nPREPARE_GATE=SAME_RESERVATION_RESCUE\\n' "$EXPID" "$EXP_NAME" > "$STATE"

  GET_OK=0
  for n in 1 2 3 4 5 6; do
    set +e
    portal-cli experiment get --experiment-id "$EXPID" > "$TMP/status.json" 2>"$TMP/status.err"
    grc=$?
    set -e
    if [[ "$grc" -ne 0 ]]; then
      echo "RESCUE_GET_${{n}}=ERROR:rc=$grc"
      tail -c 400 "$TMP/status.err" 2>/dev/null || true; echo
      sleep 2
      continue
    fi
    STATUS="$(jq -r '.status // "unknown"' "$TMP/status.json")"
    GOT_ID="$(jq -r '.id // empty' "$TMP/status.json")"
    GOT_NAME="$(jq -r '.name // empty' "$TMP/status.json")"
    GOT_PROJECT="$(jq -r '.project // empty' "$TMP/status.json")"
    echo "RESCUE_GET_${{n}}=PASS:$STATUS"
    [[ "$GOT_ID" == "$EXPID" ]] || fail RESERVATION_UUID_MISMATCH 6
    [[ "$GOT_NAME" == "$EXP_NAME" ]] || fail RESERVATION_NAME_MISMATCH 6
    [[ "$GOT_PROJECT" == WellPulse ]] || fail RESERVATION_PROJECT_MISMATCH 6
    [[ ! "$STATUS" =~ ^(terminated|destroyed|failed|error)$ ]] || fail "RESERVATION_TERMINAL_$STATUS" 6
    if [[ "$STATUS" == ready ]]; then GET_OK=1; break; fi
    sleep 2
  done
  [[ "$GET_OK" -eq 1 ]] || fail SAME_RESERVATION_READY_NOT_CORROBORATED 7

  python3 scripts/wp2_portal_record_guard.py --json "$TMP/status.json" --expected-experiment-id "$EXPID" | tee "$TMP/portal-record-gate.txt"
  grep -q '^PORTAL_RECORD_GATE=PASS$' "$TMP/portal-record-gate.txt" || fail PORTAL_RECORD_GATE 7
  EXPIRES="$(awk -F= '$1=="EXPIRES_UTC" {{print $2}}' "$TMP/portal-record-gate.txt" | tail -1)"
  if [[ -z "$EXPIRES" ]]; then EXPIRES='{fallback_expiry}'; echo "EXPIRY_SOURCE=CONSERVATIVE_UI_DERIVED:$EXPIRES"; else echo "EXPIRY_SOURCE=PORTAL_RECORD:$EXPIRES"; fi
  python3 scripts/wp2_prelaunch_time_guard.py --now-utc "$(utc)" --expires-utc "$EXPIRES" --min-remaining-s 3000 | tee "$TMP/time-gate.txt"
  grep -q '^PRELAUNCH_TIME_GATE=PASS$' "$TMP/time-gate.txt" || fail PRELAUNCH_TIME 7
  [[ "$(jq -r '.bindings.enb_node // empty' "$TMP/status.json")" == nuc1 ]] || fail BINDING_ENB 7
  [[ "$(jq -r '.bindings.ue_node // empty' "$TMP/status.json")" == nuc2 ]] || fail BINDING_UE 7
  [[ "$(jq -r '.bindings.ue_type // empty' "$TMP/status.json")" == srsue ]] || fail BINDING_UE_TYPE 7

  MOK=0
  for n in 1 2 3 4 5 6; do
    set +e
    portal-cli experiment manifests get --experiment-id "$EXPID" > "$TMP/manifests.json" 2>"$TMP/manifests.err"
    mrc=$?
    set -e
    if [[ "$mrc" -eq 0 ]]; then MOK=1; echo "RESCUE_MANIFEST_${{n}}=PASS"; break; fi
    echo "RESCUE_MANIFEST_${{n}}=ERROR:rc=$mrc"
    tail -c 400 "$TMP/manifests.err" 2>/dev/null || true; echo
    sleep 2
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
