#!/usr/bin/env python3
"""Actor-only H.A.R.D. paired pilot runner.

No evaluator key is accepted or read by this program. It validates exact actor
inputs before any model call. Semantic outcomes are retained but are not used
for pilot promotion; the pilot is pipeline-integrity only.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, pathlib, sys, time, urllib.request
from collections import Counter

EXPECTED_PLAN_SHA='90bda8d93763b2de76449c8efc13119db6f7bde11cc94e5228d2e6d73272ecaf'
EXPECTED_ACTOR_SHA='6d0ee9f701e4197556a61c3bd05a763cfc030508f200e07a51a0d27316752c02'
EXPECTED_MATRAIX='3633d8dab149a9482a71b024418a49ae828cc941'
EXPECTED_TRIALS=24

def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def write(path,obj):
    p=pathlib.Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(canon(obj))
def strict_load(path):
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d: raise ValueError('DUPLICATE_JSON_KEY')
            d[k]=v
        return d
    return json.loads(pathlib.Path(path).read_text(),object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('NONFINITE_JSON')))

def h2_sections(text):
    import re
    chunks=re.split(r'(?m)(?=^## )',text)
    return [c for c in chunks if c]

def material_equivalence(a,b):
    aa=[sha(x.encode()) for x in h2_sections(a)]
    bb=[sha(x.encode()) for x in h2_sections(b)]
    return Counter(aa)==Counter(bb) and len(aa)==len(bb)

def render_persona(native_root, persona_path):
    native_root=pathlib.Path(native_root).resolve(); persona_path=pathlib.Path(persona_path).resolve()
    sys.path[:0]=[str(native_root/p) for p in ('.','src','environment/runtime','environment/agents','packages/playground/src','application/playground')]
    from matraix.agents.persona.loader import load_persona
    from matraix.agents.persona.templating import PERSONA_SYSTEM_TEMPLATE, render_persona_template, resolve_persona_template
    loaded=load_persona(str(persona_path))
    template=resolve_persona_template(loaded,None,PERSONA_SYSTEM_TEMPLATE)
    out=render_persona_template(template,loaded).strip()
    if not out or '(a typical user)' in out: raise ValueError('PERSONA_FALLBACK')
    return out

def load_simulator(path):
    spec=importlib.util.spec_from_file_location('hard_simulator',path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def validate_inputs(plan_path,actor_path,persona_dir):
    plan_path=pathlib.Path(plan_path); actor_path=pathlib.Path(actor_path); persona_dir=pathlib.Path(persona_dir)
    if sha(plan_path.read_bytes())!=EXPECTED_PLAN_SHA: raise ValueError('PLAN_SHA_MISMATCH')
    if sha(actor_path.read_bytes())!=EXPECTED_ACTOR_SHA: raise ValueError('ACTOR_SHA_MISMATCH')
    plan=strict_load(plan_path); actor=strict_load(actor_path)
    if plan.get('sessions')!=EXPECTED_TRIALS or actor.get('pilot_session_count')!=EXPECTED_TRIALS: raise ValueError('TRIAL_COUNT')
    if actor.get('source_matraix_commit')!=EXPECTED_MATRAIX: raise ValueError('MATRAIX_IDENTITY')
    trials=actor.get('trials'); cases=actor.get('cases'); personas=actor.get('personas'); mats=actor.get('materials')
    if not isinstance(trials,list) or len(trials)!=EXPECTED_TRIALS: raise ValueError('TRIALS')
    if len({t['trial_id'] for t in trials})!=EXPECTED_TRIALS: raise ValueError('TRIAL_ID_DUP')
    if len(cases)!=12 or len({c['case_id'] for c in cases})!=12: raise ValueError('CASES')
    if set(mats)!= {'A','B'} or not material_equivalence(mats['A'],mats['B']): raise ValueError('MATERIAL_INFORMATION_DRIFT')
    pair=Counter((t['case_id'],t['arm_id']) for t in trials)
    if any(v!=1 for v in pair.values()) or len(pair)!=24: raise ValueError('PAIRING')
    per_persona=Counter(t['persona_id'] for t in trials)
    if sorted(per_persona.values())!=[4]*6: raise ValueError('PERSONA_BALANCE')
    known_cases={c['case_id'] for c in cases}; known_personas={p['persona_id']:p for p in personas}
    if set(t['case_id'] for t in trials)!=known_cases: raise ValueError('CASE_ASSIGNMENT')
    if set(t['persona_id'] for t in trials)!=set(known_personas): raise ValueError('PERSONA_ASSIGNMENT')
    for pid,p in known_personas.items():
        f=persona_dir/f'persona_{pid}.yaml'
        if not f.is_file() or sha(f.read_bytes())!=p['sha256']: raise ValueError(f'PERSONA_SHA:{pid}')
    return plan,actor

class LocalClient:
    def __init__(self,base,alias,timeout): self.base=base.rstrip('/'); self.alias=alias; self.timeout=timeout; self.calls=0
    def call(self,req):
        self.calls+=1
        r=urllib.request.Request(self.base+'/v1/chat/completions',data=canon(req),headers={'Content-Type':'application/json'},method='POST')
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*a,**kw): raise ValueError('REDIRECT')
        t=time.monotonic()
        with urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect()).open(r,timeout=self.timeout) as f: raw=f.read(2_000_001)
        if len(raw)>2_000_000: raise ValueError('OVERSIZE')
        env=json.loads(raw)
        if env.get('model')!=self.alias: raise ValueError('MODEL_ALIAS')
        choices=env.get('choices')
        if not isinstance(choices,list) or len(choices)!=1: raise ValueError('CHOICES')
        return raw,env,choices[0]['message']['content'],time.monotonic()-t

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--plan',required=True);ap.add_argument('--actor',required=True);ap.add_argument('--personas',required=True)
    ap.add_argument('--native',required=True);ap.add_argument('--simulator',required=True);ap.add_argument('--out',required=True)
    ap.add_argument('--shard',type=int,choices=(1,2,3,4),required=True);ap.add_argument('--endpoint',default='http://127.0.0.1:8765')
    ap.add_argument('--alias',required=True);ap.add_argument('--timeout',type=int,default=900)
    a=ap.parse_args(); out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=False)
    _,actor=validate_inputs(a.plan,a.actor,a.personas); sim=load_simulator(a.simulator)
    cases={c['case_id']:c for c in actor['cases']}; personas={p['persona_id']:p for p in actor['personas']}
    selected=[t for i,t in enumerate(actor['trials']) if i%4==a.shard-1]
    if len(selected)!=6: raise ValueError('SHARD_SIZE')
    client=LocalClient(a.endpoint,a.alias,a.timeout); rows=[]; persona_cache={}
    for t in selected:
        tid=t['trial_id']; td=out/tid; td.mkdir()
        pinfo=personas[t['persona_id']]; pfile=pathlib.Path(a.personas)/f"persona_{t['persona_id']}.yaml"
        persona=persona_cache.setdefault(t['persona_id'],render_persona(a.native,pfile))
        case=cases[t['case_id']]; material=actor['materials'][t['arm_id']]
        req=sim.request_for(case,material,persona,{'pipeline_pilot':True,'arm':t['arm_id'],'human_equivalence':'NOT_ESTABLISHED'},t['seed'])
        req['model']=a.alias; write(td/'request.json',req)
        status='transport_error'; response=None; error=None; elapsed=None
        try:
            raw,env,text,elapsed=client.call(req); (td/'provider.raw.json').write_bytes(raw); (td/'model.raw.txt').write_text(text)
            try: response=sim.strict_json(text.encode() if isinstance(text,str) else text)
            except Exception as e: error='RESPONSE_JSON:'+type(e).__name__+':'+str(e)[:160]; status='invalid_response'
            else:
                from jsonschema import Draft202012Validator
                try: Draft202012Validator(sim.schema()).validate(response)
                except Exception as e: error='RESPONSE_SCHEMA:'+type(e).__name__+':'+str(e)[:160]; status='invalid_response'
                else:
                    if response['case_id']!=t['case_id']: error='CASE_ID_MISMATCH'; status='invalid_response'
                    else: status='valid_response'
        except Exception as e: error=type(e).__name__+':'+str(e)[:180]
        row={'trial_id':tid,'case_id':t['case_id'],'arm_id':t['arm_id'],'persona_id':t['persona_id'],'persona_sha256':pinfo['sha256'],
             'material_sha256':sha(material.encode()),'status':status,'response':response,'error':error,'elapsed_seconds':elapsed,'attempts':1}
        write(td/'terminal.json',row);rows.append(row)
    summary={'schema_version':'hard-pipeline-pilot-result/1.0','shard':a.shard,'assigned':len(selected),'attempted':client.calls,
      'terminal_counts':dict(Counter(r['status'] for r in rows)),'all_accounted':len(rows)==len(selected),'automatic_retries':0,
      'semantic_outcomes_used_for_promotion':False,'human_equivalence':'NOT_ESTABLISHED','rows':rows}
    write(out/'summary.json',summary); print(json.dumps(summary,sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
