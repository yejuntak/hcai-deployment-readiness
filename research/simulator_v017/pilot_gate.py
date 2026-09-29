#!/usr/bin/env python3
"""Pipeline-only gate for the 24-session paired pilot.
Does not read evaluator/expected semantic answer keys and does not compare A/B efficacy.
"""
from __future__ import annotations
import argparse,json,pathlib,hashlib
from collections import Counter
EXPECTED_TRIALS=24
EXPECTED_ACTOR_SHA='6d0ee9f701e4197556a61c3bd05a763cfc030508f200e07a51a0d27316752c02'
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--actor',required=True);ap.add_argument('--results',nargs='+',required=True);a=ap.parse_args()
 actor_path=pathlib.Path(a.actor)
 if sha(actor_path.read_bytes())!=EXPECTED_ACTOR_SHA: raise SystemExit('ACTOR_SHA_MISMATCH')
 actor=json.load(open(actor_path)); expected={t['trial_id']:t for t in actor['trials']}
 rows={}; duplicate=[]; retry_bad=[]
 for root in a.results:
  for p in pathlib.Path(root).rglob('summary.json'):
   s=json.load(open(p))
   if s.get('semantic_outcomes_used_for_promotion') is not False: raise SystemExit('SEMANTIC_PROMOTION_FLAG')
   if s.get('automatic_retries')!=0: retry_bad.append(str(p))
   for r in s.get('rows',[]):
    tid=r.get('trial_id')
    if tid in rows: duplicate.append(tid)
    rows[tid]=r
 missing=sorted(set(expected)-set(rows)); extra=sorted(set(rows)-set(expected))
 identity=[]; invalid=[]; attempts=[]
 for tid,t in expected.items():
  r=rows.get(tid)
  if not r: continue
  if any(r.get(k)!=t.get(k) for k in ('case_id','arm_id','persona_id')): identity.append(tid)
  if r.get('status')!='valid_response': invalid.append(tid)
  if r.get('attempts')!=1: attempts.append(tid)
 expected_material={k:sha(v.encode()) for k,v in actor['materials'].items()}
 material_bad=[tid for tid,r in rows.items() if r.get('material_sha256')!=expected_material.get(r.get('arm_id'))]
 pmap={p['persona_id']:p['sha256'] for p in actor['personas']}
 persona_bad=[tid for tid,r in rows.items() if r.get('persona_sha256')!=pmap.get(r.get('persona_id'))]
 pairs=Counter((r.get('case_id'),r.get('arm_id')) for r in rows.values())
 pair_bad=len(pairs)!=24 or any(v!=1 for v in pairs.values())
 gate=not any([missing,extra,duplicate,retry_bad,identity,invalid,attempts,material_bad,persona_bad,pair_bad]) and len(rows)==EXPECTED_TRIALS
 report={'schema_version':'hard-pipeline-pilot-gate/1.0','expected':24,'observed':len(rows),'gate_pass':gate,
  'missing':missing,'extra':extra,'duplicate':duplicate,'retry_bad':retry_bad,'identity_bad':identity,'invalid_response':invalid,
  'attempt_count_bad':attempts,'material_bad':material_bad,'persona_bad':persona_bad,'pair_bad':pair_bad,
  'semantic_ab_effect_evaluated':False,'human_equivalence':'NOT_ESTABLISHED',
  'promotion_rule':'pipeline integrity only; no semantic A/B comparison'}
 print(json.dumps(report,sort_keys=True,indent=2));return 0 if gate else 2
if __name__=='__main__':raise SystemExit(main())
