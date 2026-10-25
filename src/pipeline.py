"""Extract observable channels from the Poseidon endogenous-trial JSON format.

Important: deception and broken promises are NOT collusion labels.
This module deliberately does not infer collusion ground truth from them.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def load_episodes(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    episodes: list[dict] = []
    metadata = data.get("metadata", {})
    for rnd in data.get("rounds", []):
        round_id = rnd.get("round_id")
        for trial in rnd.get("trials", []):
            trial_id = trial.get("trial_id")
            agents = trial.get("agents", {})
            if not isinstance(agents, dict):
                raise ValueError("Unexpected trial format: agents must be a dictionary")
            observed_messages = []
            observed_actions = []
            diagnostics = []
            for agent_id, a in sorted(agents.items()):
                s1, s2, s3 = (a.get(f"stage{i}", {}) for i in (1, 2, 3))
                observed_messages.append({
                    "agent_id": agent_id,
                    "stated_action": s2.get("stated_action"),
                    "message": s2.get("message"),
                    "position": s2.get("position"),
                })
                observed_actions.append({"agent_id": agent_id, "choice": s3.get("choice")})
                # Diagnostic fields are retained separately, NOT used as target labels.
                diagnostics.append({
                    "agent_id": agent_id,
                    "initial_intention": s1.get("intended_action"),
                    "promise_deception": a.get("promise_deception"),
                    "commitment_breaking": a.get("commitment_breaking"),
                    "typology": a.get("typology"),
                    "stages_parse_ok": all(
                        s.get("_parse_ok", True) for s in (s1, s2, s3)
                    ),
                })
            episode_id = f"{path.stem}:r{round_id}:t{trial_id}"
            episodes.append({
                "episode_id": episode_id,
                "game": metadata.get("game_type"),
                "model": metadata.get("model"),
                "round_id": round_id,
                "trial_id": trial_id,
                "communication": observed_messages,
                "actions": observed_actions,
                "outcome": trial.get("outcomes", {}),
                "diagnostics_not_ground_truth": diagnostics,
                "collusion_label": None,
                "label_source": None,
            })
    return episodes


def summarize(episodes: list[dict]) -> dict:
    n = len(episodes)
    return {
        "episodes": n,
        "games": sorted({str(e["game"]) for e in episodes}),
        "agents_per_episode": [len(e["actions"]) for e in episodes],
        "labelled_episodes": sum(e["collusion_label"] is not None for e in episodes),
        "message_action_mismatches": sum(
            m.get("stated_action") != a.get("choice")
            for e in episodes
            for m, a in zip(e["communication"], e["actions"])
            if m.get("stated_action") is not None and a.get("choice") is not None
        ),
        "parse_failed_agent_records": sum(
            not d["stages_parse_ok"] for e in episodes
            for d in e["diagnostics_not_ground_truth"]
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract and summarize endogenous game trials")
    parser.add_argument("--input", type=Path, required=True, help="Path to source JSON")
    parser.add_argument("--output", type=Path, default=Path("results/episodes.json"))
    args = parser.parse_args()
    episodes = load_episodes(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(episodes, indent=2), encoding="utf-8")
    summary = summarize(episodes)
    summary_path = args.output.with_name("summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Extracted {len(episodes)} episodes to {args.output}")
    print(f"Summary saved to {summary_path}")
    print(json.dumps(summary, indent=2))
    if summary["labelled_episodes"] == 0:
        print("NOTE: No validated collusion ground-truth labels. Detection accuracy cannot yet be evaluated.")


if __name__ == "__main__":
    main()
