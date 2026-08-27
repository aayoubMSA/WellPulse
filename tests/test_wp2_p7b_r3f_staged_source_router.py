import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
R2 = ROOT / "scripts/wp2_p7b_c_node_r2.py"


class R3FStagedSourceRouterTests(unittest.TestCase):
    def test_authoritative_r2_requires_explicit_core_staged_root(self):
        text = R2.read_text(encoding="utf-8")
        compile(text, str(R2), "exec")
        self.assertIn('WP_CORE_REPO_ROOT', text)
        self.assertIn('CORE_REPO_ROOT_NOT_SUPPLIED', text)
        self.assertIn('CORE_REPO_ROOT_UNSAFE', text)
        self.assertIn('R3F_CORE_STAGED_SOURCE_ROUTER=PASS:', text)

    def test_legacy_core_repo_paths_are_rerouted_only_inside_ssh_commands(self):
        text = R2.read_text(encoding="utf-8")
        self.assertIn('str(cmd[0]) == "ssh"', text)
        self.assertIn('remote.replace(\'cd "$HOME/WellPulse"\'', text)
        self.assertIn('legacy_absolute = r1._q(f"/users/{base.REMOTE_USER}/WellPulse")', text)
        self.assertIn('remote.replace(f"cd {legacy_absolute}"', text)

    def test_frozen_scientific_values_remain_contract_injected(self):
        text = R2.read_text(encoding="utf-8")
        for token in (
            'base.ATTENUATORS = tuple(int(x) for x in p["attenuator_ids"])',
            'base.Q0_DB = int(p["q0_db"])',
            'base.Q3_DB = int(p["q3_db"])',
            'base.PRE_Q0_S = int(s["pre_impairment_q0_s"])',
            'base.Q3_S = int(s["q3_s"])',
            'base.RESTART_OFFSET_S = int(s["restart_offset_into_q3_s"])',
            'base.H_APP_S = int(s["h_app_s"])',
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
