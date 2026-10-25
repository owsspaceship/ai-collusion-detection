import json
import tempfile
import unittest
from pathlib import Path
from src.pipeline import load_episodes, summarize

class PipelineTests(unittest.TestCase):
    def test_extract_observation_channels_without_inventing_labels(self):
        data = {"metadata": {"game_type": "diners", "model": "example"},
                "rounds": [{"round_id": 1, "trials": [{"trial_id": 0, "agents": {
                    "M": {"stage1": {"intended_action": "CHEAP"},
                          "stage2": {"stated_action": "CHEAP", "message": "cheap"},
                          "stage3": {"choice": "CHEAP"}, "commitment_breaking": False}},
                    "outcomes": {"payoffs": {"M": 3}}}]}]}
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "trial.json"
            p.write_text(json.dumps(data))
            episodes = load_episodes(p)
        self.assertEqual(episodes[0]["communication"][0]["message"], "cheap")
        self.assertEqual(episodes[0]["actions"][0]["choice"], "CHEAP")
        self.assertIsNone(episodes[0]["collusion_label"])
        self.assertEqual(summarize(episodes)["labelled_episodes"], 0)

if __name__ == "__main__":
    unittest.main()
