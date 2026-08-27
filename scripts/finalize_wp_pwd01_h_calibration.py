#!/usr/bin/env python3
"""Historical WP-PWD01 H-calibration entry point — superseded and fail-closed.

The pre-amendment implementation previously derived a common observation horizon
from W1 backlog-drain outcomes. That procedure is preserved in Git history and in
its historical evidence/documents, but it is no longer operational authority.

Current authority:
  experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md

Current prospective rule:
  H_app = 300 s, anchored at t_service_ready.

No W1 result, Golden result, or scored outcome may re-estimate this horizon.
"""

from __future__ import annotations

import sys


H_APP_S = 300
SUPERSESSION_AUTHORITY = "experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md"


def main() -> int:
    print("H_CALIBRATION_FINALIZER=BLOCKED_SUPERSEDED", file=sys.stderr)
    print(f"H_APP_S={H_APP_S}", file=sys.stderr)
    print("H_APP_ANCHOR=t_service_ready", file=sys.stderr)
    print(f"AUTHORITY={SUPERSESSION_AUTHORITY}", file=sys.stderr)
    print("OUTCOME_DERIVED_H_REESTIMATION=PROHIBITED", file=sys.stderr)
    return 64


if __name__ == "__main__":
    raise SystemExit(main())
