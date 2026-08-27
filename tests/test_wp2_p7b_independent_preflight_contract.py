from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / 'docs' / 'WP2_P7B_INDEPENDENT_PREFLIGHT_CONTRACT_2026-08-28.md'
PROBE = ROOT / 'scripts' / 'wp2_p7b_independent_preflight.sh'


class IndependentPreflightContractTests(unittest.TestCase):
    def test_contract_is_explicitly_offline_only(self):
        text = CONTRACT.read_text(encoding='utf-8')
        self.assertIn('OFFLINE DESIGN / NOT LIVE-AUTHORIZED', text)
        self.assertIn('A later live probe requires separate explicit authorization', text)

    def test_contract_prohibits_current_control_stack(self):
        text = CONTRACT.read_text(encoding='utf-8')
        for token in (
            'powder/wp2_p7b_r3_execute.sh',
            'scripts/wp2_p7b_target_node_preflight.sh',
            'scripts/wp2_portal_client_bootstrap.sh',
        ):
            self.assertIn(token, text)

    def test_probe_exists_without_live_workflow(self):
        self.assertTrue(PROBE.is_file())
        names = [p.name for p in (ROOT / '.github' / 'workflows').glob('*independent*preflight*.yml')]
        self.assertEqual(names, [])


if __name__ == '__main__':
    unittest.main()
