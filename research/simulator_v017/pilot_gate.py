#!/usr/bin/env python3
"""Fail-closed pipeline-only gate for the 24-session paired pilot.

This gate intentionally does NOT compare A/B semantic efficacy. It checks
identity, pairing, raw evidence retention, leakage, retries, neutral smoke,
and response transport/schema integrity only.
"""
from __future__ import annotations
import argparse, json, pathlib, hashlib
from collections import Counter

EXPECTED_TRIALS=24
EXPECTED_PAIRS=12
EXPECTED_SMOKES=2
EXPECTED_ACTOR_SHA='6d0ee9f701e4197556a61c3bd05a763cfc030508f200e07a51a0d27316752c02'
ARM_SHA={
 'A':'5d40c01356e82981de5a88d4e3c5119f5468be263064488e644e8da19a024260',
 'B':'32757344f7152fabe3a6e638e889a7e8c22ff8fad5630e262aae9f8e3c255829',
}
FORBIDDEN=[
 'acceptable_evidence_states','acceptable_routes','required_next_action_groups',
 'forbidden_actions','AUTHOR_PROPOSED_NOT_INDEPENDENTLY_ADJUDICATED','oracle_status'
]

def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(pathlib.Path(p).read_text())

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--actor',required=True)
 ap.add_argument('--results',nargs='+',required=True)
 ap.add_argument('--out')
 a=ap.parse_args()

 actor_path=pathlib.Path(a.actor)
 reasons=[]
 if sha(actor_path.read_bytes())!=EXPECTED_ACTOR_SHA: reasons.append('ACTOR_SHA_MISMATCH')
 actor=load(actor_path)
 expected={t['trial_id']:t for t in actor.get('trials',[])}
 if len(expected)!=EXPECTED_TRIALS: reasons.append(f'EXPECTED_ACTOR_TRIALS_{EXPECTED_TRIALS}_GOT_{len(expected)}')
 if actor.get('semantic_outcomes_blinded_until_full_plan_lock') is not True: reasons.append('ACTOR_BLINDING_FLAG')

 rows={}; duplicate=[]; smokes=[]; roots=[pathlib.Path(x) for x in a.results]
 for root in roots:
  for p in root.rglob('pilot-shard.json'):
   s=load(p)
   if s.get('semantic_scoring')!='NOT_PERFORMED': reasons.append(f'SEMANTIC_SCORING:{p}')
   if s.get('retries')!=0: reasons.append(f'RETRY_POLICY:{p}')
   if s.get('human_participants')!=0 or s.get('human_equivalence')!='NOT_ESTABLISHED':
    reasons.append(f'HUMAN_BOUNDARY:{p}')
   smokes.extend(s.get('smoke_rows') or [])
   for r in s.get('rows',[]):
    tid=r.get('trial_id')
    if tid in rows: duplicate.append(tid)
    rows[tid]=r

 missing=sorted(set(expected)-set(rows)); extra=sorted(set(rows)-set(expected))
 reasons.extend(f'MISSING:{x}' for x in missing)
 reasons.extend(f'EXTRA:{x}' for x in extra)
 reasons.extend(f'DUPLICATE:{x}' for x in duplicate)

 identity=[]; invalid=[]; attempts=[]; material_bad=[]; persona_bad=[]
 unseen=[]; human_claim=[]; origin_bad=[]; semantic_bad=[]
 for tid,t in expected.items():
  r=rows.get(tid)
  if not r: continue
  if any(r.get(k)!=t.get(k) for k in ('case_id','arm_id','persona_id','persona_slot','seed','within_pair_order')):
   identity.append(tid)
  if r.get('status')!='valid_response': invalid.append(tid)
  if r.get('model_origin')!='ACTUAL_QUANTIZED_MODEL_INFERENCE': origin_bad.append(tid)
  if r.get('claims_human_validation') is not False: human_claim.append(tid)
  if r.get('semantic_scored') is not False: semantic_bad.append(tid)
  if r.get('unseen_citations') not in ([],None): unseen.append(tid)
  if r.get('material_sha256')!=ARM_SHA.get(r.get('arm_id')): material_bad.append(tid)
  pmap={p['persona_id']:p['sha256'] for p in actor.get('personas',[])}
  if r.get('persona_sha256')!=pmap.get(r.get('persona_id')): persona_bad.append(tid)

 for name,vals in [
  ('IDENTITY',identity),('INVALID_RESPONSE',invalid),('ORIGIN',origin_bad),
  ('HUMAN_CLAIM',human_claim),('SEMANTIC_SCORE',semantic_bad),
  ('UNSEEN_CITATION',unseen),('MATERIAL',material_bad),('PERSONA',persona_bad)
 ]:
  reasons.extend(f'{name}:{x}' for x in vals)

 # Paired invariants
 by_pair={}
 for r in rows.values():
  key=(r.get('lineage_id'),r.get('case_id'),r.get('persona_id'),r.get('persona_slot'),r.get('seed'))
  by_pair.setdefault(key,[]).append(r)
 if len(by_pair)!=EXPECTED_PAIRS: reasons.append(f'EXPECTED_PAIRS_{EXPECTED_PAIRS}_GOT_{len(by_pair)}')
 lineages=set()
 for key,rr in by_pair.items():
  lineages.add(key[0])
  if len(rr)!=2: reasons.append(f'PAIR_COUNT:{key}:{len(rr)}'); continue
  if {x.get('arm_id') for x in rr}!={'A','B'}: reasons.append(f'PAIR_ARMS:{key}')
  if {x.get('within_pair_order') for x in rr}!={1,2}: reasons.append(f'PAIR_ORDER:{key}')
 if lineages!={f'L{i:02d}' for i in range(1,13)}: reasons.append('LINEAGE_COVERAGE')

 # Neutral smoke is required and remains outside the 24 sessions.
 if len(smokes)!=EXPECTED_SMOKES: reasons.append(f'EXPECTED_SMOKES_{EXPECTED_SMOKES}_GOT_{len(smokes)}')
 for s in smokes:
  if s.get('status')!='valid_response': reasons.append(f'SMOKE_INVALID:{s.get("id")}')
  if s.get('claims_human_validation') is not False: reasons.append(f'SMOKE_HUMAN_CLAIM:{s.get("id")}')
  if s.get('origin')!='ACTUAL_QUANTIZED_MODEL_INFERENCE': reasons.append(f'SMOKE_ORIGIN:{s.get("id")}')

 # Raw evidence completeness and evaluator-key leakage.
 request_count=0
 for root in roots:
  for p in root.rglob('request.json'):
   request_count+=1
   txt=p.read_text(errors='replace')
   for token in FORBIDDEN:
    if token in txt: reasons.append(f'ACTOR_KEY_LEAK:{token}:{p}')
 for tid in expected:
  found=[]
  for root in roots: found.extend(root.rglob(f'trials/{tid}'))
  if len(found)!=1:
   reasons.append(f'TRIAL_DIR:{tid}:{len(found)}'); continue
  d=found[0]
  required=[
   d/'observation.json',d/'behavior.json',d/'result.json',
   d/'inference/request.json',d/'inference/reserved.json',
   d/'inference/provider.raw.json',d/'inference/model.raw.txt',
   d/'inference/terminal.json'
  ]
  for p in required:
   if not p.is_file(): reasons.append(f'MISSING_RAW:{tid}:{p.name}')
 if request_count<26: reasons.append(f'REQUEST_FILES_EXPECT_AT_LEAST_26_GOT_{request_count}')

 reasons=sorted(set(reasons))
 gate=not reasons
 report={
  'schema_version':'hard-pipeline-pilot-gate/2.0',
  'expected_sessions':EXPECTED_TRIALS,
  'observed_sessions':len(rows),
  'pairs':len(by_pair),
  'lineages':len(lineages),
  'neutral_smokes':len(smokes),
  'gate_pass':gate,
  'formal_576_execution_eligible':gate,
  'reason_codes':reasons,
  'semantic_ab_effect_evaluated':False,
  'semantic_pilot_outcomes_used_for_promotion':False,
  'promotion_rule':'pipeline integrity only; no semantic A/B comparison',
  'human_participants':0,
  'human_equivalence':'NOT_ESTABLISHED',
  'next_if_pass':'Seal and execute the predeclared 576-session binding without changing cases, materials, persona binding, behavior mapping, or outcome rules.',
  'next_if_fail':'Do not launch 576 sessions. Preserve this failure and version any implementation correction.'
 }
 txt=json.dumps(report,sort_keys=True,indent=2)+'\n'
 if a.out:
  out=pathlib.Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(txt)
 print(txt,end='')
 return 0 if gate else 2
if __name__=='__main__': raise SystemExit(main())
