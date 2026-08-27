from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class GoldenReconstructionContractTests(unittest.TestCase):
    def _make_run(self, generated_rows: str, received_rows: str) -> Path:
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name) / "run"
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
            "record_id,generated_ts_utc,payload_sha256,payload_json\n" + generated_rows,
            encoding="utf-8",
        )
        (root / "receiver" / "telemetry_received.csv").write_text(
            "record_id,received_ts_utc,payload_sha256,payload_json\n" + received_rows,
            encoding="utf-8",
        )
        return root

    def _run(self, root: Path) -> dict:
        script = Path(__file__).resolve().parents[1] / "scripts" / "reconstruct_wp2_golden.py"
        result = subprocess.run(
            [sys.executable, str(script), "--root", str(root)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads((root / "analysis" / "golden_reconstruction.json").read_text())

    def test_rf_restore_marker_not_trailing_cleanup_q0_is_authoritative(self) -> None:
        root = self._make_run(
            generated_rows=(
                "r1,2026-08-27T17:45:04+00:00,a,{}\n"
                "r2,2026-08-27T17:45:06+00:00,b,{}\n"
                "r3,2026-08-27T17:45:07+00:00,c,{}\n"
            ),
            received_rows=(
                "r1,2026-08-27T17:45:34+00:00,a,{}\n"
                "r2,2026-08-27T17:45:35+00:00,b,{}\n"
                "r3,2026-08-27T17:45:36+00:00,c,{}\n"
            ),
        )
        payload = self._run(root)
        self.assertEqual(payload["t_rf_restore"], "2026-08-27T17:45:06+00:00")
        self.assertEqual(payload["t_service_ready"], "2026-08-27T17:45:32+00:00")
        self.assertEqual(payload["T_service_s"], 26.0)
        self.assertEqual(payload["primary_cohort_count"], 2)
        self.assertEqual(payload["received_valid_by_horizon"], 2)
        self.assertEqual(payload["completeness_300"], 1.0)
        self.assertEqual(payload["post_cohort_valid_attempts"], 1)
        self.assertEqual(payload["unexpected_attempts"], 0)
        self.assertEqual(
            payload["t_rf_restore_authority"],
            "sender/rf_restore.ready_crosschecked_to_attenuation_timeline",
        )

    def test_planned_post_cohort_traffic_is_not_unexpected(self) -> None:
        root = self._make_run(
            generated_rows=(
                "r1,2026-08-27T17:45:04+00:00,a,{}\n"
                "r2,2026-08-27T17:45:06+00:00,b,{}\n"
                "r3,2026-08-27T17:45:07+00:00,c,{}\n"
                "r4,2026-08-27T17:45:08+00:00,d,{}\n"
            ),
            received_rows=(
                "r1,2026-08-27T17:45:34+00:00,a,{}\n"
                "r2,2026-08-27T17:45:35+00:00,b,{}\n"
                "r3,2026-08-27T17:45:36+00:00,c,{}\n"
                "r4,2026-08-27T17:45:37+00:00,WRONG,{}\n"
                "u1,2026-08-27T17:45:38+00:00,z,{}\n"
            ),
        )
        payload = self._run(root)
        self.assertEqual(payload["primary_cohort_count"], 2)
        self.assertEqual(payload["post_cohort_generated_count"], 2)
        self.assertEqual(payload["post_cohort_valid_attempts"], 1)
        self.assertEqual(payload["post_cohort_checksum_mismatch_attempts"], 1)
        self.assertEqual(payload["unexpected_attempts"], 1)
        self.assertEqual(payload["unexpected_record_ids"], ["u1"])
        self.assertEqual(payload["received_valid_by_horizon"], 2)
        self.assertEqual(payload["completeness_300"], 1.0)

    def test_p7_transport_alias_and_retirement_contracts(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        orch = (repo / "scripts" / "wp2_golden_orchestrator.sh").read_text(encoding="utf-8")
        aliases = (repo / "scripts" / "wp2_golden_prepare_management_aliases.sh").read_text(encoding="utf-8")

        self.assertNotIn('$CORE_EVDIR/receiver/." "$EVDIR/receiver/"', orch)
        self.assertIn("tar -C '$CORE_EVDIR/receiver' -cf - .", orch)
        self.assertIn('tar -C "$EVDIR/receiver" -xf -', orch)
        self.assertIn("WP_CORE_MANAGEMENT_HOST", orch)
        self.assertIn("WP_UE_MANAGEMENT_HOST", orch)
        self.assertIn("wp2_golden_prepare_management_aliases.sh", orch)
        self.assertIn("WP2_GOLDEN_MANAGEMENT_ALIAS_GATE=PASS", aliases)
        self.assertIn("getent ahostsv4", aliases)
        self.assertNotIn("nuc1.emulab.net", aliases)
        self.assertNotIn("nuc2.emulab.net", aliases)

        self.assertEqual(list((repo / ".github" / "workflows").glob("wp2-p6*.yml")), [])
        self.assertEqual(list(repo.glob(".wp2-p6*trigger")), [])


if __name__ == "__main__":
    unittest.main()
