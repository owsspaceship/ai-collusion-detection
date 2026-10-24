cat > README.md <<'EOF'
# When More Evidence Misleads: Evaluating Hybrid Collusion Detectors

## Overview

This project investigates whether combining AI agents' communications
and observable actions improves the detection of collusion compared
with monitoring either source independently.

The research is conducted as part of the Apart Research AI Collusion
Research Sprint (October 2026), Track 2: Detection and Audit of Collusion.

## Definition of Collusion

Collusion is coordination between two or more AI agents to pursue a
shared objective that violates an established rule, agreement, or
legitimate principal's interests.

Independent similar behaviour, legitimate cooperation, and individual
dishonesty do not automatically constitute collusion.

## Research Questions

1. Does hybrid monitoring outperform communication-only and action-only monitoring?
2. Can misleading communications reduce the reliability of hybrid detectors?
3. Can inconsistencies between messages and actions improve detection?

## Experimental Approach

The project will compare:

- Communication-only detection
- Action-only detection
- Hybrid communication-and-action detection
- Structured communication-action inconsistency detection

Evaluation will use labelled multi-agent interaction trajectories.
Collusion ground truth must be established independently of the
detectors' observations.

## Status

Research environment setup and experimental development in progress.
EOF