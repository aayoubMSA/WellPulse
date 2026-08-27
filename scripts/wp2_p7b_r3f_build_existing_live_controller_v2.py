#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("r3f_builder_v1", HERE / "wp2_p7b_r3f_build_existing_live_controller.py")
if SPEC is None or SPEC.loader is None:
    raise SystemExit("R3F_V1_BUILDER_IMPORT_FAIL")
V1 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V1)


def replace_region(text: str, start: str, end: str, replacement: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(f"R3F_V2_PATCH_MARKER_MISMATCH:{text.count(start)}:{text.count(end)}")
    i = text.index(start)
    j = text.index(end, i) + len(end)
    return text[:i] + replacement + text[j:]


def build(source: Path, output: Path, expid: str, name: str, source_sha: str) -> None:
    V1.build(source, output, expid, name, source_sha)
    text = output.read_text(encoding="utf-8")
    start = "  bar 38 'EFCC target-runtime revalidation without package mutation'; echo\n"
    end = "  bar 45 'Establishing clean initial Q0 LTE user plane'; echo\n"
    runtime = r'''  bar 38 'EFCC target-runtime revalidation without package mutation'; echo
  check_common(){
    local user=$1 host=$2 port=$3 role=$4
    ssh "${SSH[@]}" -p "$port" "$user@$host" bash -s <<'EOS'
set -euo pipefail
PY="$HOME/.wp2-golden-venv/bin/python"
test -x "$PY"
ACTUAL_PY="$($PY -c 'import sys; print(".".join(map(str,sys.version_info[:3])))')"
test "$ACTUAL_PY" = 3.11.13
ACTUAL_PAHO="$($PY -c 'import importlib.metadata as m; print(m.version("paho-mqtt"))')"
test "$ACTUAL_PAHO" = 2.1.0
command -v bash >/dev/null
command -v mosquitto_pub >/dev/null
command -v openssl >/dev/null
command -v tar >/dev/null
command -v rsync >/dev/null
command -v sha256sum >/dev/null
test -d /proj/WellPulse && test -w /proj/WellPulse
! command -v jq >/dev/null 2>&1
"$PY" -m py_compile \
  "$HOME/WellPulse/scripts/wp2_p7b_c_node_r2.py" \
  "$HOME/WellPulse/scripts/wp2_p7b_c_node_r1.py" \
  "$HOME/WellPulse/scripts/wp2_p7b_c_node.py" \
  "$HOME/WellPulse/scripts/wp2_p7b_path_contract.py" \
  "$HOME/WellPulse/scripts/wp2_p7b_validate_readiness_v2.py" \
  "$HOME/WellPulse/scripts/reconstruct_wp2_p7b_v2.py"
EOS
    echo "$role TARGET_RUNTIME=PASS"
  }
  check_common "$CORE_USER" "$CORE_EXT" "$CORE_PORT" CORE || fail CORE_TARGET_RUNTIME 11
  check_common "$UE_USER" "$UE_EXT" "$UE_PORT" UE || fail UE_TARGET_RUNTIME 11
  ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" bash -s <<'EOS' || fail CORE_MOSQUITTO_ROLE_CONTRACT 11
set -eu
command -v mosquitto >/dev/null
OUT="$(mosquitto -h 2>&1 || true)"
printf '%s\n' "$OUT" | grep -q 'mosquitto version 1.4.15'
EOS
  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" bash -s <<'EOS' || fail UE_JAVA_ROLE_CONTRACT 11
set -eu
command -v java >/dev/null
command -v javac >/dev/null
java -version 2>&1 | grep -q '11.0.19'
EOS

  bar 45 'Establishing clean initial Q0 LTE user plane'; echo
'''
    text = replace_region(text, start, end, runtime)
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
    print("R3F_EXISTING_RESERVATION_CONTROLLER_V2_BUILD=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
