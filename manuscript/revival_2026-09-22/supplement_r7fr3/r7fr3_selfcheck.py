#!/usr/bin/env python3
from pathlib import Path
import csv
import re
import sys
import subprocess

root=Path(__file__).resolve().parents[3]
cfg=Path(__file__).with_name("R7fR3_EXECUTION_CONFIG.csv")
man=Path(__file__).with_name("R7fR3_CODE_MANIFEST.csv")

rows=list(csv.DictReader(cfg.open(encoding="utf-8")))
assert len(rows)==2
assert rows[0]["campaign"]=="historical_FIT_final"
assert rows[1]["campaign"]=="prospective_FIT_R5"
assert "paho-mqtt 1.6.1" in rows[0]["mqtt_library"]
assert rows[1]["fit_experiment"]=="449953"

mrows=list(csv.DictReader(man.open(encoding="utf-8")))
assert len(mrows)>=10
for row in mrows:
    p=root/row["path"]
    assert p.exists(), p
    observed=subprocess.check_output(
        ["git","-C",str(root),"rev-parse","HEAD:"+row["path"]],
        text=True
    ).strip()
    assert observed==row["git_blob_sha"], (row["path"],observed,row["git_blob_sha"])

runner=(root/"experiments/WP-RT01/fit_runner_py35.py").read_text(encoding="utf-8")
assert 'BROKER="mqtt4.iot-lab.info"; PORT=8883' in runner
assert 'OUTAGE_START=3001; OUTAGE_END=5000; RESTART_AT=4000' in runner
assert 'PRAGMA journal_mode=WAL' in runner
assert 'PRAGMA synchronous=FULL' in runner
assert '["iptables","-I","OUTPUT","1"]' in runner
assert '["iptables","-D","OUTPUT"]' in runner

q0=(root/"experiments/WP-RT01/fit_runner_q0_instrumented_py35.py").read_text(encoding="utf-8")
assert "class InstrumentedPublisher" in q0
assert "PUBACK" in q0 and "CONNACK_OK" in q0 and "SOURCE_GENERATED" in q0

loop=(root/"scripts/run_fit_r5_stage_a_loop.sh").read_text(encoding="utf-8")
for token in ["run_t1 R1","run_t1 R2","run_t1 R3","clock_sample","No Stage-B run was executed"]:
    assert token in loop

supp=Path(__file__).with_name("R7fR3_REPRODUCIBILITY_SUPPLEMENT.md").read_text(encoding="utf-8")
assert "journal_mode=DELETE" in supp and "journal_mode=WAL" in supp
assert "not recorded" in supp
assert "private Drive identifiers" in supp

for secret_pattern in [r"FIT_PASSWORD\s*=", r"BEGIN OPENSSH PRIVATE KEY", r"1jDv2kw0", r"1HxR_B7", r"1qS-_vv"]:
    assert not re.search(secret_pattern, supp)

print("R7FR3_SUPPLEMENT_SELFCHECK=PASS")
