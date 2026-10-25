import unittest
from experiments.run_llm_collusion import CONDITIONS, make_prompts, run_episode


class RunnerTests(unittest.TestCase):
    def test_private_treatments_are_not_public_labels(self):
        for condition in CONDITIONS:
            s, u = make_prompts(condition, 'M', 1)
            self.assertTrue(s and u)

    def test_mock_episode_has_separated_assignment_and_verification(self):
        calls = iter([{'intended_action': 3}, {'intended_action': 3},
                      {'stated_action': 2, 'message': 'I will catch two'},
                      {'stated_action': 2, 'message': 'I will catch two'},
                      {'choice': 3}, {'choice': 3}])
        ep = run_episode('collusive_concealed', 'mock', call=lambda *_: next(calls))
        self.assertEqual(ep['assignment_label'], 1)
        self.assertIsNone(ep['verified_collusion_label'])
        self.assertEqual(ep['outcomes']['total_caught'], 6)
        self.assertEqual(ep['outcomes']['payoffs'], {'M': 3.0, 'Q': 3.0})


if __name__ == '__main__':
    unittest.main()
