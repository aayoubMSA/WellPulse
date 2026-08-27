#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def replace_region(text: str, start: str, end: str, replacement: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(f"PATCH_MARKER_MISMATCH:{start[:40]}:{text.count(start)}:{text.count(end)}")
    i = text.index(start)
    j = text.index(end, i) + len(end)
    return text[:i] + replacement + text[j:]


def build(source: Path, output: Path, expid: str, name: str, source_sha: str) -> None:
    text = source.read_text(encoding="utf-8")
    old = 'SOURCE_SHA="${GITHUB_SHA:-$(git rev-parse HEAD)}"'
    if text.count(old) != 1:
        raise SystemExit("SOURCE_SHA_MARKER_MISMATCH")
    text = text.replace(old, f"SOURCE_SHA='{source_sha}'", 1)

    premut_start = "  # Premutation code/contract locks are checked before the first POWDER API call.\n"
    premut_end = "  portal_bootstrap; init_ssh\n"
    premut = f'''  # R3F: exact R3E-passed science source + executable/runtime contracts are frozen before POWDER contact.
  git cat-file -e "$SOURCE_SHA^{{commit}}" || fail AUTHORIZED_SOURCE_SHA_MISSING 5
  git cat-file -e "$SOURCE_SHA:scripts/wp2_p7b_c_node_r2.py" || fail R2_ENTRYPOINT_MISSING_AT_AUTHORIZED_SHA 5
  git cat-file -e "$SOURCE_SHA:experiments/WP-PWD01/p7b-executable-contract-v2.json" || fail EXECUTABLE_CONTRACT_V2_MISSING 5
  git cat-file -e "$SOURCE_SHA:experiments/WP-PWD01/p7b-target-runtime-contract-v2.json" || fail TARGET_RUNTIME_CONTRACT_V2_MISSING 5
  echo 'R3E_SOURCE_SHA={source_sha}'
  echo 'R3F_ENTRYPOINT=scripts/wp2_p7b_c_node_r2.py'
  echo 'AUTOMATIC_RETRY=NO'
  echo 'NEW_RESERVATION=NO'
  echo 'SCORED=NO'
  portal_bootstrap; init_ssh
'''
    text = replace_region(text, premut_start, premut_end, premut)

    live_start = "  bar 5 'Authority guards + no-active-P7B check'; echo\n"
    live_end = '  portal-cli experiment manifests get --experiment-id "$EXPID" > "$TMP/manifests.json" || fail MANIFEST_FETCH 8\n'
    live = f'''  bar 5 'Exact existing reservation corroboration; no create path'; echo
  EXPID='{expid}'
  EXP_NAME='{name}'
  set_output experiment_id "$EXPID"
  set_output experiment_name "$EXP_NAME"
  GET_OK=0
  for n in 1 2 3 4 5 6; do
    set +e
    portal-cli experiment get --experiment-id "$EXPID" > "$TMP/status.json" 2>"$TMP/status.err"
    grc=$?
    set -e
    if [[ "$grc" -ne 0 ]]; then echo "R3F_GET_${{n}}=ERROR:rc=$grc"; sleep 2; continue; fi
    STATUS="$(jq -r '.status // "unknown"' "$TMP/status.json")"
    GOT_ID="$(jq -r '.id // empty' "$TMP/status.json")"
    GOT_NAME="$(jq -r '.name // empty' "$TMP/status.json")"
    GOT_PROJECT="$(jq -r '.project // empty' "$TMP/status.json")"
    echo "R3F_GET_${{n}}=PASS:$STATUS"
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
  python3 scripts/wp2_prelaunch_time_guard.py --now-utc "$(utc)" --expires-utc "$EXPIRES" --min-remaining-s 7200 | tee "$TMP/time-gate.txt"
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
    if [[ "$mrc" -eq 0 ]]; then MOK=1; echo "R3F_MANIFEST_${{n}}=PASS"; break; fi
    echo "R3F_MANIFEST_${{n}}=ERROR:rc=$mrc"; sleep 2
  done
  [[ "$MOK" -eq 1 ]] || fail MANIFEST_FETCH_DEGRADED_CONTROL_PLANE 8
'''
    text = replace_region(text, live_start, live_end, live)

    runtime_start = "  bar 38 'Bootstrapping pinned Python/MQTT/Java runtimes'; echo\n"
    runtime_end = "  bar 45 'Establishing clean initial Q0 LTE user plane'; echo\n"
    runtime = '''  bar 38 'EFCC target-runtime revalidation without package mutation'; echo
  check_common(){ local user=$1 host=$2 port=$3 role=$4; ssh "${SSH[@]}" -p "$port" "$user@$host" 'set -euo pipefail; PY="$HOME/.wp2-golden-venv/bin/python"; test -x "$PY"; test "$($PY -c '\''import sys; print(".".join(map(str,sys.version_info[:3])))'\'')" = 3.11.13; test "$($PY -c '\''import importlib.metadata as m; print(m.version("paho-mqtt"))'\'')" = 2.1.0; command -v bash >/dev/null; command -v mosquitto_pub >/dev/null; command -v openssl >/dev/null; command -v tar >/dev/null; command -v rsync >/dev/null; command -v sha256sum >/dev/null; test -d /proj/WellPulse && test -w /proj/WellPulse; ! command -v jq >/dev/null 2>&1; "$PY" -m py_compile "$HOME/WellPulse/scripts/wp2_p7b_c_node_r2.py" "$HOME/WellPulse/scripts/wp2_p7b_c_node_r1.py" "$HOME/WellPulse/scripts/wp2_p7b_c_node.py" "$HOME/WellPulse/scripts/wp2_p7b_path_contract.py" "$HOME/WellPulse/scripts/wp2_p7b_validate_readiness_v2.py" "$HOME/WellPulse/scripts/reconstruct_wp2_p7b_v2.py"'; echo "$role TARGET_RUNTIME=PASS"; }
  check_common "$CORE_USER" "$CORE_EXT" "$CORE_PORT" CORE || fail CORE_TARGET_RUNTIME 11
  check_common "$UE_USER" "$UE_EXT" "$UE_PORT" UE || fail UE_TARGET_RUNTIME 11
  ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'set -eu; command -v mosquitto >/dev/null; OUT="$(mosquitto -h 2>&1 || true)"; printf "%s\n" "$OUT" | grep -q "mosquitto version 1.4.15"' || fail CORE_MOSQUITTO_ROLE_CONTRACT 11
  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'set -eu; command -v java >/dev/null; command -v javac >/dev/null; java -version 2>&1 | grep -q "11.0.19"' || fail UE_JAVA_ROLE_CONTRACT 11

  bar 45 'Establishing clean initial Q0 LTE user plane'; echo
'''
    text = replace_region(text, runtime_start, runtime_end, runtime)

    if "$R1_ENTRYPOINT" not in text:
        raise SystemExit("R1_ENTRYPOINT_EXECUTION_MARKER_MISSING")
    text = text.replace("$R1_ENTRYPOINT", "scripts/wp2_p7b_c_node_r2.py")

    preserve_start = "  bar 82 'Persistent /proj escrow using resolved absolute paths'; echo\n"
    preserve_end = "}\n\nfinalize(){\n"
    preserve = '''  bar 82 'Shell-only origin-node /proj escrow + controller pull'; echo
  PDIR="/proj/WellPulse/evidence-escrow/$EXPID/$RUN_ID"
  preserve_origin(){
    local role=$1 user=$2 host=$3 port=$4 src=$5 dest="$PDIR/$1" remote_tar="/tmp/${RUN_ID}-$1.tar"
    ssh "${SSH[@]}" -p "$port" "$user@$host" bash -s -- "$src" "$dest" "$remote_tar" <<'EOS'
set -euo pipefail
SRC=$1; DEST=$2; TAR=$3
case "$SRC" in /*) ;; *) echo BAD_SOURCE_PATH >&2; exit 71;; esac
case "$DEST" in /proj/WellPulse/*) ;; *) echo BAD_ESCROW_PATH >&2; exit 72;; esac
test -d "$SRC"
rm -rf "$DEST"; mkdir -p "$DEST/raw"
rsync -a "$SRC/" "$DEST/raw/"
(cd "$SRC"; find . -type f -print0 | sort -z | xargs -0 -r sha256sum) > "$DEST/SOURCE_SHA256SUMS"
(cd "$DEST/raw"; sha256sum -c ../SOURCE_SHA256SUMS >/dev/null)
printf 'EVIDENCE_ESCROW_GATE=PASS\n' > "$DEST/EVIDENCE_ESCROW_GATE.PASS"
tar -C "$DEST" -cf "$TAR" .
(cd "$(dirname "$TAR")"; sha256sum "$(basename "$TAR")" > "$(basename "$TAR").sha256")
EOS
    scp "${SSH[@]}" -P "$port" "$user@$host:$remote_tar" "$TMP/${RUN_ID}-$role.tar" >/dev/null
    scp "${SSH[@]}" -P "$port" "$user@$host:$remote_tar.sha256" "$TMP/${RUN_ID}-$role.tar.sha256" >/dev/null
    (cd "$TMP"; sha256sum -c "${RUN_ID}-$role.tar.sha256" >/dev/null)
  }
  preserve_origin ue "$UE_USER" "$UE_EXT" "$UE_PORT" "$UE_SRC" || fail UE_SHELL_PRESERVATION 72
  preserve_origin core "$CORE_USER" "$CORE_EXT" "$CORE_PORT" "$CORE_SRC" || fail CORE_SHELL_PRESERVATION 72
  rm -rf "$TMP/controller"; mkdir -p "$TMP/controller/ue" "$TMP/controller/core"
  tar -C "$TMP/controller/ue" -xf "$TMP/${RUN_ID}-ue.tar"
  tar -C "$TMP/controller/core" -xf "$TMP/${RUN_ID}-core.tar"
  (cd "$TMP/controller/ue/raw" && sha256sum -c ../SOURCE_SHA256SUMS >/dev/null)
  (cd "$TMP/controller/core/raw" && sha256sum -c ../SOURCE_SHA256SUMS >/dev/null)
  printf 'EVIDENCE_ESCROW_GATE=PASS\nCONTROLLER_PULL_EACH_ORIGIN_NODE=PASS\n' > "$TMP/controller/PERSISTENT_ESCROW_GATE.PASS"
  if [[ "$NODE_RC" -eq 0 ]]; then
    strict_bundle_check "$TMP/controller" || fail STRICT_RAW_EVIDENCE_COMPLETENESS 73
    echo 'STRICT_RAW_EVIDENCE_COMPLETENESS=PASS'
  else
    echo "STRICT_RAW_EVIDENCE_COMPLETENESS=DEFERRED_NODE_RC_$NODE_RC"
  fi
  echo 'EVIDENCE_ESCROW_GATE=PASS'
  echo 'CONTROLLER_PULL_GATE=PASS'
  BUNDLE="$TMP/wp2-p7b-r3f-$RUN_ID.tar"
  tar --sort=name --mtime='UTC 1970-01-01' --owner=0 --group=0 --numeric-owner -C "$TMP/controller" -cf "$BUNDLE" .
  BUNDLE_SHA="$(sha256sum "$BUNDLE" | awk '{print $1}')"; BUNDLE_BYTES="$(stat -c%s "$BUNDLE")"
  printf 'EXPID=%q\nEXP_NAME=%q\nRUN_ID=%q\nNODE_RC=%q\nBUNDLE_SHA=%q\nBUNDLE_BYTES=%q\nPREPARE_GATE=PASS\n' "$EXPID" "$EXP_NAME" "$RUN_ID" "$NODE_RC" "$BUNDLE_SHA" "$BUNDLE_BYTES" > "$STATE"
  set_output bundle_path "$BUNDLE"; set_output bundle_sha256 "$BUNDLE_SHA"; set_output bundle_bytes "$BUNDLE_BYTES"
  echo "CONTROLLER_BUNDLE_SHA256=$BUNDLE_SHA"
  bar 90 'Evidence bundle ready for independent GitHub round-trip'; echo
}

finalize(){
'''
    text = replace_region(text, preserve_start, preserve_end, preserve)

    old_term = '''    if [[ "$rc" -ne 0 ]]; then TERMINATED=1; echo "P7B_R3_TERMINATION_POLL_${i}=NOT_FOUND"; break; fi
    st="$(jq -r '.status // "unknown"' "$TMP/postterm.json")"; echo "P7B_R3_TERMINATION_POLL_${i}=$st"'''
    new_term = '''    if [[ "$rc" -ne 0 ]]; then
      if grep -Eiq '(404|not[ -]?found)' "$TMP/postterm.err" 2>/dev/null; then TERMINATED=1; echo "P7B_R3_TERMINATION_POLL_${i}=TYPED_NOT_FOUND"; break; fi
      echo "P7B_R3_TERMINATION_POLL_${i}=GET_ERROR_UNCONFIRMED"; sleep 5; continue
    fi
    st="$(jq -r '.status // "unknown"' "$TMP/postterm.json")"; echo "P7B_R3_TERMINATION_POLL_${i}=$st"'''
    if text.count(old_term) != 1:
        raise SystemExit("TERMINATION_MARKER_MISMATCH")
    text = text.replace(old_term, new_term, 1)
    text = text.replace('portal-cli experiment get --experiment-id "$EXPID" > "$TMP/postterm.json" 2>/dev/null', 'portal-cli experiment get --experiment-id "$EXPID" > "$TMP/postterm.json" 2>"$TMP/postterm.err"', 1)

    if "portal-cli experiment create" in text:
        raise SystemExit("NEW_RESERVATION_PATH_SURVIVED")
    if text.count("portal-cli experiment terminate") != 1:
        raise SystemExit("TERMINATE_COUNT_NOT_ONE")
    if "scripts/wp2_p7b_c_node_r2.py" not in text:
        raise SystemExit("R2_ENTRYPOINT_NOT_BOUND")
    output.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="powder/wp2_p7b_r3_execute.sh")
    ap.add_argument("--output", required=True)
    ap.add_argument("--experiment-id", required=True)
    ap.add_argument("--experiment-name", required=True)
    ap.add_argument("--source-sha", required=True)
    args = ap.parse_args()
    build(Path(args.source), Path(args.output), args.experiment_id, args.experiment_name, args.source_sha)
    print("R3F_EXISTING_RESERVATION_CONTROLLER_BUILD=PASS")
    print("NEW_RESERVATION=NO")
    print("AUTOMATIC_RETRY=NO")
    print("SCORED=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
