from __future__ import annotations

from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
H2_ENTRY = ROOT / "scripts/wp2_p7b_c_node_h2.py"
SAFE_RESTORE = ROOT / "scripts/wp2_p7b_service_restore_h2.sh"
BASE = ROOT / "scripts/wp2_p7b_c_node.py"


class P7BH2FrontierEvidenceTests(unittest.TestCase):
    def test_restart_transition_contains_exact_a4_fields(self):
        text = H2_ENTRY.read_text(encoding="utf-8")
        required = (
            "generator_pid_before", "generator_pid_after", "old_gateway_pid",
            "old_gateway_exit_observed", "new_gateway_pid", "new_gateway_start_observed",
            "client_identity", "topic_identity", "restart_request_utc",
            "restart_request_monotonic", "old_exit_utc", "old_exit_monotonic",
            "new_start_utc", "new_start_monotonic", "new_ready_utc",
            "new_ready_monotonic", "source_generation_continuity_status",
        )
        for field in required:
            self.assertIn(f'"{field}"', text)
        self.assertIn('cell_dir / "restart_transition.json"', text)

    def test_restart_transition_is_written_at_replacement_ready_hook(self):
        text = H2_ENTRY.read_text(encoding="utf-8")
        hook = text.index("def wait_gateway_started")
        write = text.index('_durable_json(cell_dir / "restart_transition.json"', hook)
        self.assertGreater(write, hook)
        self.assertIn("original_wait_gateway_started(arch, cell_dir, p, prior_start_count)", text[hook:write])
        self.assertIn("transition_written", text[hook:write + 500])

    def test_restart_request_is_captured_before_old_gateway_destruction(self):
        text = H2_ENTRY.read_text(encoding="utf-8")
        fn = text[text.index("def close_process"):text.index("def wait_gateway_started")]
        self.assertLess(fn.index('match["restart_request_utc"]'), fn.index("original_close_process"))
        self.assertGreater(fn.index('match["old_exit_utc"]'), fn.index("original_close_process"))

    def test_transition_does_not_replace_final_restart_proof(self):
        h2 = H2_ENTRY.read_text(encoding="utf-8")
        base = BASE.read_text(encoding="utf-8")
        self.assertIn('restart_transition.json', h2)
        self.assertIn('write_json(cell_dir / "restart_proof.json", restart_proof)', base)
        self.assertNotIn('restart_proof.json', h2)

    def test_restore_frontier_has_exact_ordered_a5_markers(self):
        shell = SAFE_RESTORE.read_text(encoding="utf-8")
        wrapper = H2_ENTRY.read_text(encoding="utf-8")
        ordered_shell = [
            "RESTORE_REQUESTED", "UE_CLEANUP_BEGIN", "UE_CLEANUP_END",
            "CORE_CLEANUP_BEGIN", "CORE_CLEANUP_END", "CORE_START_BEGIN",
            "CORE_START_END", "CORE_STABLE_READY", "UE_START_BEGIN",
            "UE_START_END", "UE_PROCESS_READY",
        ]
        positions = [shell.index(f"frontier {x} ") for x in ordered_shell]
        self.assertEqual(positions, sorted(positions))
        self.assertLess(wrapper.index('"SERVICE_READY_PROBE_BEGIN"'), wrapper.index('"SERVICE_READY_PROBE_END"'))

    def test_frontier_rows_have_phase_utc_monotonic_status_and_durable_flush(self):
        shell = SAFE_RESTORE.read_text(encoding="utf-8")
        fn = shell[shell.index("frontier(){"):shell.index("case \"$CONTROLLER_PID\"")]
        for token in ('"phase"', '"utc"', '"monotonic"', '"status"'):
            self.assertIn(token, fn)
        self.assertIn('sync "$FRONTIER"', fn)
        self.assertNotIn("sleep", fn)
        entry = H2_ENTRY.read_text(encoding="utf-8")
        self.assertIn("os.fsync", entry)

    def test_failed_service_probe_still_writes_end_frontier(self):
        text = H2_ENTRY.read_text(encoding="utf-8")
        begin = text.index('"SERVICE_READY_PROBE_BEGIN"')
        call = text.index('wp2_golden_service_ready_probe.sh', begin)
        end = text.index('"SERVICE_READY_PROBE_END"', call)
        failure = text.index("SERVICE_READY_PROBE_FAIL", end)
        self.assertLess(begin, call)
        self.assertLess(call, end)
        self.assertLess(end, failure)
        self.assertIn('"PASS" if p2.returncode == 0 else "FAIL"', text[call:failure])

    def test_a6_hooks_are_supplementary_only_and_cover_exit_term_hup(self):
        text = H2_ENTRY.read_text(encoding="utf-8")
        self.assertIn("atexit.register", text)
        self.assertIn("signal.SIGTERM", text)
        self.assertIn("signal.SIGHUP", text)
        self.assertIn('"supplementary_only": True', text)
        self.assertIn("P7B_H2_PARENT_EXIT_HOOKS=SUPPLEMENTARY_ONLY", text)
        self.assertNotIn("SIGKILL", text)

    def test_frontier_instrumentation_is_bound_before_inherited_main(self):
        text = H2_ENTRY.read_text(encoding="utf-8")
        run = text.index("return r2.main()")
        for binding in (
            "install_h2_frontier_instrumentation()",
            "install_h2_safe_restore(identity)",
            "install_supplementary_exit_hooks()",
        ):
            self.assertLess(text.index(binding, text.index("def main()")), run)

    def test_safe_restore_is_shell_syntax_valid_after_frontier_instrumentation(self):
        p = subprocess.run(["bash", "-n", str(SAFE_RESTORE)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_h2_3_adds_no_live_authority_or_retry_surface(self):
        combined = H2_ENTRY.read_text(encoding="utf-8") + SAFE_RESTORE.read_text(encoding="utf-8")
        self.assertIn("LIVE_AUTHORIZATION=SEPARATE_REQUIRED", combined)
        self.assertIn("SCORED_AUTHORIZATION=BLOCKED", combined)
        for forbidden in (
            "portal-cli experiment create", "portal-cli experiment terminate",
            "scored_runs_authorized=true", "AUTOMATIC_RETRY=YES",
        ):
            self.assertNotIn(forbidden, combined)

    def test_h2_3_does_not_duplicate_frozen_scientific_controls(self):
        combined = H2_ENTRY.read_text(encoding="utf-8") + SAFE_RESTORE.read_text(encoding="utf-8")
        for token in ("Q0_DB", "Q1_DB", "Q2_DB", "Q3_DB", "ATTENUATORS", "P7B-B1-S3", "P7B-W1-S3", "P7B-B2-S3"):
            self.assertNotIn(token, combined)


if __name__ == "__main__":
    unittest.main()
