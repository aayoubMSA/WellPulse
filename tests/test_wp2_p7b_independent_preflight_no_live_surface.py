from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IndependentPreflightNoLiveSurfaceTests(unittest.TestCase):
    def test_no_independent_preflight_workflow(self):
        wf = ROOT / '.github' / 'workflows'
        self.assertEqual(list(wf.glob('*independent*preflight*.yml')), [])

    def test_no_independent_preflight_trigger(self):
        self.assertEqual(list(ROOT.glob('.*independent*preflight*trigger*')), [])


if __name__ == '__main__':
    unittest.main()
