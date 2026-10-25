# When More Evidence Misleads: Evaluating Hybrid Collusion Detectors

**Apart Research AI Collusion Sprint 2026 — Track 2 (Detection and Audit)**

This project investigates whether public communication combined with observable agent actions improves detection of *prohibited coordination*, and when misleading communication undermines that improvement.

## Project layout

- `src/pipeline.py` — parses endogenous-game JSON into separated observable channels and diagnostics.
- `notebooks/01_exploration.ipynb` — inspect the data and document initial observations.
- `experiments/` — commands and future experimental configurations.
- `results/` — generated data/metrics (avoid secrets or private information).
- `docs/research_report.pdf` — typeset research-paper report; source: `docs/research_report.md`.
- `docs/research_design.md` — operational definition, labeling and evaluation protocol.
- `docs/results_notes.md` — honest, dated observations and limitations.
- `tests/` — minimal pipeline checks.

## Quick start

From the research repository root:

```bash
python -m src.pipeline \
  --input ~/collusion_hackathon/llm-trust-breaking/outputs/experiments/diners/2agents/openai_gpt-4o-mini_endogenous.json \
  --output results/diners_smoke_episodes.json
```

Inspect `results/diners_smoke_episodes.json` and `results/summary.json`, then run the notebook. The extractor only requires Python's standard library.

**Important:** The existing trust-breaking experiment does *not* supply verified collusion labels. Therefore the output intentionally sets `collusion_label` to `null`. Do not treat deception, commitments, or same-action choices as collusion ground truth.

## Research status

- [x] First two-agent diners simulation output inspected.
- [x] Data extraction and analysis scaffold.
- [ ] Define validated collusion/non-collusion experimental conditions.
- [ ] Generate matched labelled trajectories.
- [ ] Compare detectors on held-out episodes.
- [ ] Report limitations and final results.

## Research Paper

**When More Evidence Misleads: Evaluating Hybrid Collusion Detectors**

Research conducted for the Apart Research AI Collusion Research Sprint 2026, Track 2: Detection and Audit of Collusion.

The paper examines whether combining public communication and observable actions can produce false-positive collusion alarms.

- [Read the research paper (PDF)](docs/AI_Collusion_Sprint_Submission.pdf)
- [Download the editable Word document](docs/AI_Collusion_Sprint_Submission.docx)
