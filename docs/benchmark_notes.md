# Synthetic baseline benchmark — methodological status

The eight scenarios in `experiments/run_collusion_benchmark.py` are **constructed examples**, not observations of LLMs. The label indicates whether a prohibited agreement is built into the written scenario; it is *not independently verified agent intent*. Scenario P4 represents **attempted but unexecuted** collusion. Distinguish collusive agreement from successful prohibited actions in the final paper.

For the actual study, modify prompts or use a separate controlled experimental runner to create independently verified collusive and non-collusive agent trajectories. Keep treatment assignment/privileged instructions out of the detector inputs. Include matched-action negatives, innocent coordination positives for cooperation, and communication concealment. Report empirical LLM results separately from this debugging demonstration.

Rule-based action-score flags two fishers exceeding an *introduced quota of 2 fish each*; that quota is **not a rule of the original fishing game**. The demo does not call `llm-trust-breaking` or require API credits.
