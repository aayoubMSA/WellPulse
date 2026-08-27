#!/usr/bin/env bash
set -euo pipefail
# Compatibility wrapper: the implementation's progress helper historically
# reads global p while declaring local p under set -u. Seed p so execution is
# safe without altering the frozen controller body.
export p="${p:-0}"
exec bash "$(dirname "$0")/wp2_golden_owner_impl.sh" "$@"
