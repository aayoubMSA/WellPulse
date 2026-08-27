#!/usr/bin/env python3
"""Fail if an active GitHub workflow appears to invoke the unsafe RF CLI.

Comments and assertions that merely search for the forbidden token are ignored;
the guard is looking for executable-looking invocations, not documentation.
"""
from pathlib import Path
import re
import sys

root = Path('.github/workflows')
needle = re.compile(r'(?i)(?:^|[;&|]\s*|\b(?:sudo|timeout)\s+)(?:/[^\s]+/)?tmcc\s+attenuator\b')
violations = []
for path in sorted(root.glob('*.y*ml')):
    for no, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith('#'):
            continue
        # Assertions/searches are not RF invocations.
        if 'grep ' in s or 'grep -' in s:
            continue
        if needle.search(s):
            violations.append(f'{path}:{no}:{s}')

if violations:
    print('K7_ACTIVE_WORKFLOW_RF_GUARD=FAIL')
    for v in violations:
        print(v)
    raise SystemExit(7)
print('K7_ACTIVE_WORKFLOW_RF_GUARD=PASS')
