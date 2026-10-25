# Experiments

Run the organisers' simulation separately in `~/collusion_hackathon/llm-trust-breaking`.
Do not copy secrets or the entire simulation repository here.

Then extract the generated JSON from this project's root:

```bash
python -m src.pipeline \
  --input ~/collusion_hackathon/llm-trust-breaking/outputs/experiments/diners/2agents/openai_gpt-4o-mini_endogenous.json \
  --output results/diners_smoke_episodes.json
```

**Methodological status:** These are trust-breaking-game observations, not verified collusion labels. A controlled benchmark with documented prohibited objectives and valid ground truth is required before reporting collusion-detection metrics.
