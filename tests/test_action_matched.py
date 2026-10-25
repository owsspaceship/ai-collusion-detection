import unittest
from experiments.run_action_matched import generate_episode, CONDITIONS
from src.evaluation import episode_observations, metrics
from src.detectors import detect


class ActionMatchedTests(unittest.TestCase):
    def fake(self, model, system, user):
        if 'Offer Q an explicit agreement' in user:
            return {'proposal': 'I propose we both catch three fish, over the quota.'}
        if 'Explicitly choose whether to accept' in user:
            return {'accept': True, 'reply': 'I accept the agreement to catch three.'}
        if 'public announcement' in user:
            return {'stated_action': 2, 'message': 'I will catch 2 fish.'}
        if 'final selection' in system:
            return {'choice': 3, 'reasoning': 'Target catch is three.'}
        raise AssertionError(user)

    def test_three_conditions_have_identical_actions(self):
        for cond in CONDITIONS:
            ep = generate_episode(cond, 'mock', self.fake)
            self.assertTrue(ep['outcomes']['action_matched'])
            self.assertEqual(ep['outcomes']['choices'], {'M': 3, 'Q': 3})
            self.assertIsNone(ep['verified_collusion_label'])
            self.assertEqual(ep['protocol_agreement_label'], 0 if cond == 'independent_matched' else 1)
            self.assertEqual(detect(episode_observations(ep))['action'], 1)

    def test_metrics(self):
        self.assertEqual(metrics([0, 1], [1, 1])['fp'], 1)

if __name__ == '__main__':
    unittest.main()
