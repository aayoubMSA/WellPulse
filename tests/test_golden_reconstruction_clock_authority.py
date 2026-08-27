from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


def test_golden_reconstruction_uses_rf_restore_marker_not_trailing_cleanup_q0(tmp_path: Path) -> None:
    root = tmp_path / "run"
    for rel in ("sender", "receiver", "substrate", "analysis"):
        (root / rel).mkdir(parents=True, exist_ok=True)

    (root / "sender" / "attenuation_timeline.csv").write_text(
        "command_start_utc,command_end_utc,programmed_attenuation_db,attenuator_ids\n"
        "2026-08-27T17:42:00+00:00,2026-08-27T17:42:01+00:00,0,1 33 2 34\n"
        "2026-08-27T17:43:00+00:00,2026-08-27T17:43:01+00:00,55,1 33 2 34\n"
        "2026-08-27T17:45:05+00:00,2026-08-27T17:45:06+00:00,0,1 33 2 34\n"
        # Fail-safe cleanup after the 300 s horizon. This MUST NOT become t_rf_restore.
        "2026-08-27T17:50:40+00:00,2026-08-27T17:50:41+00:00,0,1 33 2 34\n",
        encoding="utf-8",
    )
    (root / "sender" / "rf_restore.ready").write_text(
        "2026-08-27T17:45:06+00:00\n", encoding="utf-8"
    )
    (root / "substrate" / "service_ready_probe.txt").write_text(
        "T_SERVICE_READY=2026-08-27T17:45:32+00:00\nWP2_GOLDEN_SERVICE_READY=PASS\n",
        encoding="utf-8",
    )
    (root / "sender" / "telemetry_generated.csv").write_text(
        "record_id,generated_ts_utc,payload_sha256,payload_json\n"
        "r1,2026-08-27T17:45:04+00:00,a,{}\n"
        "r2,2026-08-27T17:45:06+00:00,b,{}\n"
        "r3,2026-08-27T17:45:07+00:00,c,{}\n",
        encoding="utf-8",
    )
    (root / "receiver" / "telemetry_received.csv").write_text(
        "record_id,received_ts_utc,payload_sha256,payload_json\n"
        "r1,2026-08-27T17:45:34+00:00,a,{}\n"
        "r2,2026-08-27T17:45:35+00:00,b,{}\n"
        "r3,2026-08-27T17:45:36+00:00,c,{}\n",
        encoding="utf-8",
    )

    script = Path(__file__).resolve().parents[1] / "scripts" / "reconstruct_wp2_golden.py"
    result = subprocess.run(
        [sys.executable, str(script), "--root", str(root)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads((root / "analysis" / "golden_reconstruction.json").read_text())
    assert payload["t_rf_restore"] == "2026-08-27T17:45:06+00:00"
    assert payload["t_service_ready"] == "2026-08-27T17:45:32+00:00"
    assert payload["T_service_s"] == 26.0
    assert payload["primary_cohort_count"] == 2
    assert payload["received_valid_by_horizon"] == 2
    assert payload["completeness_300"] == 1.0
    assert payload["t_rf_restore_authority"] == (
        "sender/rf_restore.ready_crosschecked_to_attenuation_timeline"
    )
