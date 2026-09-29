#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib

def load_jsons(root):
    out=[]
    for p in sorted(pathlib.Path(root).rglob('*.json')):
        try:
            j=json.load(open(p))
        except Exception:
            continue
        if isinstance(j,dict):
            out.append((p,j))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('roots',nargs='+')
    ap.add_argument('--expected',type=int,default=16)
    a=ap.parse_args()
    cases={}
    for root in a.roots:
        for p,j in load_jsons(root):
            if isinstance(j.get('case_results'),list):
                for row in j['case_results']:
                    if isinstance(row,dict) and row.get('case_id'):
                        cases[row['case_id']]=row
            if j.get('case_id') and any(k in j for k in ('operational_case_pass','passed','categorical_checks')):
                cases[j['case_id']]=j
    rows=[]
    for cid,row in sorted(cases.items()):
        passed=row.get('operational_case_pass')
        if passed is None: passed=row.get('passed')
        rows.append({'case_id':cid,'pass':passed is True})
    report={
      'schema_version':'qualification-gate/1.0',
      'expected_cases':a.expected,
      'observed_unique_cases':len(rows),
      'passed_cases':sum(x['pass'] for x in rows),
      'failed_case_ids':[x['case_id'] for x in rows if not x['pass']],
      'gate_pass':len(rows)==a.expected and all(x['pass'] for x in rows),
      'rule':'exactly expected unique cases AND every operational_case_pass=true; no partial credit',
      'human_equivalence':'NOT_ESTABLISHED',
    }
    print(json.dumps(report,sort_keys=True,indent=2))
    return 0 if report['gate_pass'] else 2
if __name__=='__main__': raise SystemExit(main())
