#!/usr/bin/env python3
"""Actor-only runner for frozen 24-case generalization holdout."""
from __future__ import annotations
import argparse,hashlib,json,pathlib,importlib.util,time,urllib.request
EXPECTED_ACTOR_SHA='4343a83640a0bc5543c26cb8aec585f6981137bd7b44f0943edaa0083e75cbcd'
EXPECTED_CASES=24
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def write(p,x):p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(canon(x))
def load_sim(path):
 spec=importlib.util.spec_from_file_location('sim',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class Client:
 def __init__(self,alias,timeout):self.alias=alias;self.timeout=timeout;self.calls=0
 def call(self,req):
  self.calls+=1;r=urllib.request.Request('http://127.0.0.1:8765/v1/chat/completions',data=canon(req),headers={'Content-Type':'application/json'},method='POST')
  class NR(urllib.request.HTTPRedirectHandler):
   def redirect_request(self,*a,**kw):raise ValueError('REDIRECT')
  t=time.monotonic()
  with urllib.request.build_opener(urllib.request.ProxyHandler({}),NR()).open(r,timeout=self.timeout) as f:raw=f.read(2000001)
  if len(raw)>2000000:raise ValueError('OVERSIZE')
  env=json.loads(raw)
  if env.get('model')!=self.alias:raise ValueError('MODEL_ALIAS')
  ch=env.get('choices')
  if not isinstance(ch,list) or len(ch)!=1:raise ValueError('CHOICES')
  return raw,env,ch[0]['message']['content'],time.monotonic()-t
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--actor',required=True);ap.add_argument('--protocol',required=True);ap.add_argument('--simulator',required=True);ap.add_argument('--persona',required=True);ap.add_argument('--out',required=True);ap.add_argument('--shard',type=int,choices=(1,2,3,4),required=True);ap.add_argument('--alias',required=True);ap.add_argument('--timeout',type=int,default=900);a=ap.parse_args()
 actor_path=pathlib.Path(a.actor)
 if sha(actor_path.read_bytes())!=EXPECTED_ACTOR_SHA:raise ValueError('ACTOR_SHA')
 actor=json.load(open(actor_path));cases=actor['cases']
 if len(cases)!=EXPECTED_CASES or len({c['case_id'] for c in cases})!=EXPECTED_CASES:raise ValueError('CASE_COUNT')
 protocol=pathlib.Path(a.protocol).read_text();sim=load_sim(a.simulator);persona=pathlib.Path(a.persona).read_text()
 selected=[c for i,c in enumerate(cases) if i%4==a.shard-1]
 if len(selected)!=6:raise ValueError('SHARD_SIZE')
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=False);cl=Client(a.alias,a.timeout);rows=[]
 for c in selected:
  td=out/c['case_id'];td.mkdir();req=sim.request_for(c,protocol,persona,{'generalization_holdout':True,'human_equivalence':'NOT_ESTABLISHED'},20260929);req['model']=a.alias;write(td/'request.json',req)
  status='transport_error';resp=None;err=None;elapsed=None
  try:
   raw,env,text,elapsed=cl.call(req);(td/'provider.raw.json').write_bytes(raw);(td/'model.raw.txt').write_text(text)
   try:resp=sim.strict_json(text.encode() if isinstance(text,str) else text)
   except Exception as e:status='invalid_response';err='JSON:'+type(e).__name__+':'+str(e)[:180]
   else:
    from jsonschema import Draft202012Validator
    try:Draft202012Validator(sim.schema()).validate(resp)
    except Exception as e:status='invalid_response';err='SCHEMA:'+type(e).__name__+':'+str(e)[:180]
    else:
     if resp['case_id']!=c['case_id']:status='invalid_response';err='CASE_ID_MISMATCH'
     else:status='valid_response'
  except Exception as e:err=type(e).__name__+':'+str(e)[:180]
  row={'case_id':c['case_id'],'status':status,'response':resp,'error':err,'elapsed_seconds':elapsed,'attempts':1};write(td/'terminal.json',row);rows.append(row)
 summary={'schema_version':'holdout-actor-result/1.0','shard':a.shard,'assigned':len(selected),'attempted':cl.calls,'automatic_retries':0,'rows':rows,'human_equivalence':'NOT_ESTABLISHED'};write(out/'summary.json',summary);print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
