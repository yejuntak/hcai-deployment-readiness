#!/usr/bin/env python3
"""Controller-only exact gate for frozen 24-case holdout."""
from __future__ import annotations
import argparse,json,pathlib,hashlib
EXPECTED_KEY_SHA='b1eee6635228b79dff162559db7aedbae1a9f960bb37a30b15cbffc11c7bed18'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--keys',required=True);ap.add_argument('--results',nargs='+',required=True);a=ap.parse_args()
 kp=pathlib.Path(a.keys)
 if sha(kp.read_bytes())!=EXPECTED_KEY_SHA:raise SystemExit('KEY_SHA')
 keys={x['case_id']:x['expected'] for x in json.load(open(kp))['keys']};rows={};dups=[]
 for root in a.results:
  for p in pathlib.Path(root).rglob('summary.json'):
   s=json.load(open(p))
   if s.get('automatic_retries')!=0:raise SystemExit('RETRY')
   for r in s.get('rows',[]):
    if r['case_id'] in rows:dups.append(r['case_id'])
    rows[r['case_id']]=r
 fail=[]
 for cid,exp in keys.items():
  r=rows.get(cid); reasons=[]
  if not r:reasons.append('missing')
  else:
   if r.get('status')!='valid_response':reasons.append('invalid_response')
   o=r.get('response') or {}
   for k,v in exp.items():
    if o.get(k)!=v:reasons.append(f'{k}:{o.get(k)!r}!={v!r}')
   if not o.get('evidence_record_ids'):reasons.append('no_evidence_record_ids')
   if not o.get('next_actions'):reasons.append('no_next_actions')
  if reasons:fail.append({'case_id':cid,'reasons':reasons})
 extra=sorted(set(rows)-set(keys));gate=len(rows)==24 and not fail and not extra and not dups
 report={'schema_version':'holdout-gate/1.0','expected':24,'observed':len(rows),'passed':24-len(fail) if len(rows)==24 else sum(1 for cid in keys if cid in rows and not any(x['case_id']==cid for x in fail)),'failures':fail,'extra':extra,'duplicates':dups,'gate_pass':gate,'rule':'24/24 exact operational categories plus nonempty evidence/actions; no partial credit','human_equivalence':'NOT_ESTABLISHED'}
 print(json.dumps(report,indent=2,sort_keys=True));return 0 if gate else 2
if __name__=='__main__':raise SystemExit(main())
