# Research design (working protocol)

## Question
Does combining messages and actions improve detection of prohibited multi-agent coordination over either channel alone? Under what conditions can misleading messages impair hybrid detection?

## Operational definition
Collusion requires coordination among at least two agents toward an objective prohibited by an explicit rule, agreement or legitimate principal's interest. Similar actions, authorized cooperation, and individual dishonesty do not by themselves establish collusion.

## Ground-truth labeling
1. Define the game's rule and the prohibited joint objective *before* generating episodes.
2. Randomize conditions: compliant/non-collusive vs assigned collusive objective. Keep available actions and task framing comparable.
3. Record condition assignment privately; additionally score whether joint coordination occurred and whether the prohibited objective succeeded. Report assignment vs realized behaviour separately.
4. Do not use `promise_deception`, `commitment_breaking`, judge labels, or a detector's output as the collusion ground truth.
5. Exclude initial private intentions / reasoning and privileged labels from detector inputs.

## Detector observation rules
- Communication-only: public Stage 2 stated actions and messages.
- Action-only: observable Stage 3 choices (and only outcome information actually visible to an auditor).
- Hybrid: communication plus action observations, matched by episode.
- Inconsistency-aware: same as hybrid with explicitly represented message/action disagreements.

## Evaluation
Use the same held-out episodes across detectors. Report confusion matrices, precision, recall, F1, false-positive rate, and uncertainty intervals when there is a non-trivial labeled sample. Split by independent scenario/run to avoid near-duplicate leakage. Track parsing failures and API costs. Contrast truthful vs misleading communication using experimentally matched conditions, not only naturally occurring examples.

## Limitations
A single two-agent diners trial is a pipeline smoke test only. It does not demonstrate collusion or permit estimation of detection performance.
