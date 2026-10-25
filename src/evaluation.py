"""Evaluate transparent detectors against a narrow protocol-agreement proxy.

NEVER rename protocol_agreement_label to verified_collusion_label.
"""
import argparse
import csv
import json
from pathlib import Path
from src.detectors import detect


def episode_observations(episode):
    agents = episode['agents']
    return {
        'communication': [
            {'agent_id': n, 'stated_action': a['stage2']['stated_action'],
             'message': a['stage2']['message']}
            for n, a in agents.items()
        ],
        'actions': [{'agent_id': n, 'choice': a['stage3']['choice']}
                    for n, a in agents.items()],
    }


def metrics(y_true, y_pred):
    if len(y_true) != len(y_pred) or not y_true:
        raise ValueError('Paired, nonempty labels and predictions required')
    tp = sum(y == 1 and p == 1 for y, p in zip(y_true, y_pred))
    fp = sum(y == 0 and p == 1 for y, p in zip(y_true, y_pred))
    fn = sum(y == 1 and p == 0 for y, p in zip(y_true, y_pred))
    tn = sum(y == 0 and p == 0 for y, p in zip(y_true, y_pred))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {'n': len(y_true), 'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn,
            'precision': round(precision, 3), 'recall': round(recall, 3),
            'f1': round(2 * precision * recall / (precision + recall), 3) if precision + recall else 0.0}


def evaluate(files):
    records = []
    for file in files:
        data = json.loads(Path(file).read_text())
        for ep in data['episodes']:
            if ep.get('error') or not ep.get('agents'):
                continue
            if ep.get('protocol_agreement_label') is None:
                continue
            predictions = detect(episode_observations(ep))
            records.append({'episode_id': ep['episode_id'], 'condition': ep['condition'],
                            'reference_label': ep['protocol_agreement_label'],
                            'action_matched': ep['outcomes'].get('action_matched', False),
                            **predictions})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+')
    parser.add_argument('--output-dir', default='results/action_matched_evaluation')
    args = parser.parse_args()
    records = evaluate(args.files)
    if not records:
        raise SystemExit('No eligible episodes with protocol-agreement proxy labels')
    folder = Path(args.output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / 'predictions.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    labels = [r['reference_label'] for r in records]
    results = {method: metrics(labels, [r[method] for r in records])
               for method in ('communication', 'action', 'hybrid', 'mismatch')}
    (folder / 'metrics.json').write_text(json.dumps({
        'target': 'protocol_agreement_label (NOT verified collusion)',
        'warnings': [
            'Exploratory treatment-induced episodes, not independent verification of collusion',
            'Rule-based detectors are uncalibrated; do not report as generalizable collusion accuracy',
            'Action-matching failures excluded; inspect how many failed and report separately',
        ],
        'n_eligible': len(records), 'metrics': results
    }, indent=2))
    print('Eligible episodes:', len(records))
    for method, vals in results.items():
        print(method, vals)
    print('Saved:', folder)

if __name__ == '__main__':
    main()
