from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from wellpulse.harness import run_local_scenario
from wellpulse.manifest import build_run_manifest

CONFIG = ROOT / "experiments" / "WP-RT01" / "experiment.json"
w1 = run_local_scenario(10_000, "W1_offline_first", "C2_outage_restart")
assert w1["generated"] == 10_000
assert w1["received_unique"] == 10_000
assert len(w1["missing"]) == 0
assert w1["duplicates"] == 0
b0 = run_local_scenario(10_000, "B0_publish_only", "C1_outage_no_restart")
assert b0["generated"] == 10_000
assert len(b0["missing"]) == 2_000
assert b0["duplicates"] == 0
manifest = build_run_manifest(
    root=ROOT,
    run_id="LOCAL-GATE-WP-RT01-v1.0",
    experiment_version="WP-RT01-v1.0",
    config_path=CONFIG,
    architecture="W1_plus_B0_sanity",
    condition="C2_W1_plus_C1_B0",
    raw_path="data/raw/<real_run_id>/",
    derived_path="results/runs/<real_run_id>/",
)
print(json.dumps({"manifest": manifest, "results": [w1, b0]}, indent=2))
