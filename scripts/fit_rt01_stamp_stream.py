#!/usr/bin/env python3
from __future__ import print_function

import sys
import time

for line in sys.stdin:
    line = line.rstrip("\r\n")
    if not line:
        continue
    sys.stdout.write("%.6f\t%s\n" % (time.time(), line))
    sys.stdout.flush()
