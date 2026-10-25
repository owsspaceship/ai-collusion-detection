import unittest
from experiments.run_collusion_benchmark import make_cases, score
from src.detectors import detect


class DetectorDemoTests(unittest.TestCase):
    def test_matched_actions_do_not_establish_collusion(self):
        cases = {e['episode_id']: e for e in make_cases()}
        self.assertEqual(cases['N2']['actions'], cases['P2']['actions'])
        self.assertNotEqual(cases['N2']['collusion_label'], cases['P2']['collusion_label'])

    def test_communication_misses_concealed_agreement(self):
        cases = {e['episode_id']: e for e in make_cases()}
        self.assertEqual(detect(cases['P2'])['communication'], 0)

    def test_metrics_have_all_counts(self):
        cases = make_cases()
        rows = [dict(collusion_label=e['collusion_label'], **detect(e)) for e in cases]
        result = score(rows, 'hybrid')
        self.assertEqual(sum(result[k] for k in ('tp', 'fp', 'tn', 'fn')), len(cases))


if __name__ == '__main__': unittest.main()
