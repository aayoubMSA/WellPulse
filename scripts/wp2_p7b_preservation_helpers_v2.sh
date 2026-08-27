#!/usr/bin/env bash
set -euo pipefail

# Prospective P7B preservation helpers for the observed POWDER target runtime.
# Deliberately has zero Python dependency: system python3 is 3.6.9 on both nodes.

p7b_require_absolute_remote_path() {
  local value=${1:?path required}
  [[ "$value" == /* ]] || return 64
  [[ "$value" != *'$'* ]] || return 65
  [[ "$value" != *'~'* ]] || return 66
  [[ "$value" != *$'\n'* && "$value" != *$'\r'* ]] || return 67
}

p7b_join_remote_path() {
  local base=${1:?base required}
  shift
  p7b_require_absolute_remote_path "$base"
  local out=${base%/} part
  for part in "$@"; do
    [[ -n "$part" ]] || return 68
    [[ "$part" != /* ]] || return 69
    [[ "$part" != *'$'* && "$part" != *'~'* ]] || return 70
    [[ "$part" != '..' && "$part" != ../* && "$part" != */../* && "$part" != */.. ]] || return 71
    out="$out/${part#/}"
  done
  p7b_require_absolute_remote_path "$out"
  printf '%s\n' "$out"
}

p7b_receiver_path_contract_shell() {
  local core_cell_dir=${1:?core cell dir required}
  p7b_require_absolute_remote_path "$core_cell_dir"
  local receiver_dir="${core_cell_dir%/}/receiver"
  printf 'receiver_output_dir=%s\n' "$receiver_dir"
  printf 'receiver_event_writer_path=%s/receiver_events.jsonl\n' "$receiver_dir"
  printf 'receiver_event_watcher_path=%s/receiver_events.jsonl\n' "$receiver_dir"
  printf 'receiver_console_path=%s/console.txt\n' "$receiver_dir"
  printf 'writer_watcher_path_equal=true\n'
}

p7b_copy_tree_with_hash_manifest_v2() {
  local src=${1:?source required}
  local dst=${2:?destination required}
  p7b_require_absolute_remote_path "$src"
  p7b_require_absolute_remote_path "$dst"
  for cmd in find sort xargs sha256sum rsync; do command -v "$cmd" >/dev/null; done
  test -d "$src"
  test -n "$(find "$src" -type f -print -quit)"
  rm -rf "$dst"
  mkdir -p "$dst/raw"
  (
    cd "$src"
    find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
  ) > "$dst/SOURCE_SHA256SUMS"
  (
    cd "$src"
    find . ! -type f ! -type d -printf '%y %p -> %l\n' | LC_ALL=C sort
  ) > "$dst/SOURCE_NONREGULAR_FILES.txt"
  rsync -a --no-specials --no-devices "$src/" "$dst/raw/"
  (
    cd "$dst/raw"
    sha256sum -c ../SOURCE_SHA256SUMS >/dev/null
  )
  printf 'P7B_PRESERVATION_COPY_V2=PASS\n'
}
