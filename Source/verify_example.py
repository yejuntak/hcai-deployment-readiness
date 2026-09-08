"""Recompute the synthetic worked example with Python 3 standard library."""
import csv
from pathlib import Path

base = Path(__file__).resolve().parents[1] / 'Worked-Example'
def read(name):
    with (base / name).open(newline='') as source:
        return list(csv.DictReader(source))

key = read('reference-key.csv')
findings = read('findings.csv')
requirements = read('requirements.csv')
recovery = read('recovery.csv')
batch = read('batch.csv')
ids = {row['defect_id'] for row in key}
assert len(ids) == len(key), 'Duplicate reference ID'
matched = {row['reference_id'] for row in findings if row['adjudication'] == 'Matched'}
assert matched <= ids, 'Unknown reference match'
omissions = {row['defect_id'] for row in key if row['reference_omission'] == '1'}
eligible = [row for row in batch if row['criterion_status'] == 'Nonready' and row['evaluator_judgment'] in {'Ready','Not ready','Unable to assess'}]
recall = len(matched)/len(ids)
results = {
    'reference_recall': recall,
    'expected_recall_gap_pp': (0.8-recall)*100,
    'omission_recognition': len(matched & omissions)/len(omissions),
    'recovery_coverage': sum(r['handoff_status']=='Verified' for r in recovery)/len(recovery),
    'requirements_coverage': sum(r['handoff_status']=='Verified' for r in requirements)/len(requirements),
    'false_ready_batch_rate': sum(r['evaluator_judgment']=='Ready' for r in eligible)/len(eligible),
}
expected = [0.625,17.5,1/3,0.5,0.7,0.75]
for (metric,result), target in zip(results.items(), expected):
    assert abs(result-target)<1e-9, metric
    print(f'{metric}: {result:.6f}')
print('Synthetic arithmetic verified. This does not validate the method empirically.')
