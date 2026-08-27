#!/usr/bin/env bash
set -euo pipefail

# R1 preservation-path helpers. These functions contain no POWDER authority and
# perform no SSH by themselves. Callers must supply already-resolved absolute
# remote paths; literal $HOME/~ tokens are rejected before any copy command.

p7b_require_absolute_remote_path() {
  local value=${1:?path required}
  python3 scripts/wp2_p7b_path_contract.py validate --path "$value" >/dev/null
}

p7b_resolve_home_from_ssh_output() {
  local raw=${1:?resolved home required}
  p7b_require_absolute_remote_path "$raw"
  printf '%s\n' "$raw"
}

p7b_join_remote_path() {
  local base=${1:?base required}
  shift
  p7b_require_absolute_remote_path "$base"
  python3 scripts/wp2_p7b_path_contract.py join --base "$base" "$@" | sed -n '1p'
}

p7b_assert_writer_watcher_contract() {
  local core_cell_dir=${1:?core cell dir required}
  p7b_require_absolute_remote_path "$core_cell_dir"
  local out
  out="$(python3 scripts/wp2_p7b_path_contract.py receiver --core-cell-dir "$core_cell_dir")"
  grep -q '"writer_watcher_path_equal": true' <<<"$out"
  ! grep -q '\$HOME\|~/' <<<"$out"
}

p7b_copy_tree_with_hash_manifest() {
  local src=${1:?source required}
  local dst=${2:?destination required}
  p7b_require_absolute_remote_path "$src"
  p7b_require_absolute_remote_path "$dst"
  test -d "$src"
  test -n "$(find "$src" -type f -print -quit)"
  rm -rf "$dst"
  mkdir -p "$dst/raw"
  (
    cd "$src"
    find . -type f -print0 | sort -z | xargs -0 sha256sum
  ) > "$dst/SOURCE_SHA256SUMS"
  (
    cd "$src"
    find . ! -type f ! -type d -printf '%y %p -> %l\n' | sort
  ) > "$dst/SOURCE_NONREGULAR_FILES.txt"
  rsync -a --no-specials --no-devices "$src/" "$dst/raw/"
  (
    cd "$dst/raw"
    sha256sum -c ../SOURCE_SHA256SUMS >/dev/null
  )
  printf 'P7B_PRESERVATION_COPY=PASS\n'
}
