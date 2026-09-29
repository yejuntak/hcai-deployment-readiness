"""Transport compact actor recipes; regenerate and verify exact planned bytes.

This is not a prompt summarizer. Native persona text and public protocol text are
reconstructed from pinned sources and must match the pre-execution file digests.
"""
from pathlib import Path
import argparse,json,base64,zlib,sys
import simulator as s
FILES={'config.json','reservation.json','response.schema.json','input-files.sha256.json'}

def encode_recipe(data):
 b=s.canonical(data);return {'encoding':'zlib-base64-json','sha256':s.sha(b),'uncompressed_bytes':len(b),'data':base64.b64encode(zlib.compress(b,9)).decode()}
def decode_recipe(envelope):
 if envelope['encoding']!='zlib-base64-json' or envelope['uncompressed_bytes']>2000000:raise ValueError('RECIPE_BOUND')
 d=zlib.decompressobj();b=d.decompress(base64.b64decode(envelope['data'],validate=True),2000001)
 if len(b)>2000000 or d.unconsumed_tail or not d.eof or d.unused_data:raise ValueError('DECOMPRESSION_BOUND')
 if len(b)!=envelope['uncompressed_bytes'] or s.sha(b)!=envelope['sha256']:raise ValueError('RECIPE_HASH')
 return s.strict_json(b)

def pack(checkpoint,out):
 checkpoint=Path(checkpoint);study=checkpoint/'study-rc2';ext=study/'external/v013';out=Path(out);out.mkdir(parents=True,exist_ok=False)
 a=(study/'plan/materials/current-full.md').read_text();b=(study/'plan/materials/reordered-full.md').read_text()
 chunks=s.sections(a);order=[chunks.index(c) for c in s.sections(b)]
 pp={x['slot']:x for x in s.strict_json((ext/'personas.json').read_bytes())['rows']}
 for shard in range(1,7):
  src=checkpoint/f'remote-actor-inputs/shard-{shard}'
  actor=s.strict_json((src/'actor-inputs.json').read_bytes());behavior=s.strict_json((src/'behavior-plan.json').read_bytes())
  trials=actor['trials'];slots={t['persona_slot'] for t in trials}
  data={'schema_version':'actor-recipe/1.0','actor_version':actor['version'],'native_pin':s.NATIVE_PIN,
   'protocol_sha256':s.sha(a.encode()),'reordered_sha256':s.sha(b.encode()),'reorder_indices':order,'trials':trials,
   'cases':{r['case']['case_id']:r['case'] for r in actor['requests'].values()},
   'personas':{slot:{'path':pp[slot]['path'],'prompt_sha256':pp[slot]['prompt_sha256']} for slot in slots},
   'policy':{tid:{'profile':row['behavior_profile'],'chaos':row['chaos']} for tid,row in behavior.items()},
   'files':{name:(src/name).read_text() for name in FILES}}
  s.write_json(out/f'shard-{shard}.json',encode_recipe(data))
 return out

def inflate(recipe,native,protocol,out,renderer=None):
 data=decode_recipe(s.strict_json(Path(recipe).read_bytes()));root=Path(native).resolve();out=Path(out).resolve()
 if data['schema_version']!='actor-recipe/1.0' or data['native_pin']!=s.NATIVE_PIN:raise ValueError('RECIPE_VERSION')
 if set(data['files'])!=FILES:raise ValueError('FILE_ALLOWLIST')
 a=Path(protocol).read_text();chunks=s.sections(a);order=data['reorder_indices']
 if sorted(order)!=list(range(len(chunks))):raise ValueError('SECTION_PERMUTATION')
 arms={'A':a,'B':''.join(chunks[i] for i in order)}
 if s.sha(a.encode())!=data['protocol_sha256'] or s.sha(arms['B'].encode())!=data['reordered_sha256']:raise ValueError('MATERIAL_DRIFT')
 if renderer is None:
  import subprocess
  if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=s.NATIVE_PIN:raise ValueError('NATIVE_COMMIT_DRIFT')
  sys.path[:0]=[str(root/p) for p in ('.','src','environment/runtime','environment/agents','packages/playground/src','application/playground')]
  from matraix.agents.persona.loader import load_persona
  from matraix.agents.persona.templating import PERSONA_SYSTEM_TEMPLATE,resolve_persona_template,render_persona_template
  def renderer(name):
   path=root/'persona/datasets/matraix-persona-dev-sample'/name
   person=load_persona(str(path));template=resolve_persona_template(person,None,PERSONA_SYSTEM_TEMPLATE)
   return render_persona_template(template,person).strip()
 pp={}
 for slot,row in data['personas'].items():
  if Path(row['path']).name!=row['path'] or not row['path'].endswith('.yaml'):raise ValueError('PERSONA_PATH')
  pp[slot]=renderer(row['path'])
  if s.sha(pp[slot].encode())!=row['prompt_sha256']:raise ValueError('PERSONA_RENDER_DRIFT')
 requests={};behaviors={}
 for t in data['trials']:
  case=data['cases'][t['case_id']];policy=data['policy'][t['trial_id']]
  obs,text,meta,trace=s.observe(case,arms[t['arm_id']],policy['profile'],t['seed'],policy['chaos'])
  requests[t['trial_id']]={'case':case,'request':s.request_for(obs,text,pp[t['persona_slot']],meta,t['seed'])}
  behaviors[t['trial_id']]={'observed_case':obs,'observed_material':text,'limits':meta,'synthetic_events':trace,'behavior_profile':policy['profile'],'chaos':policy['chaos']}
 actor={'version':data['actor_version'],'trials':data['trials'],'requests':requests}
 out.mkdir(parents=True,exist_ok=False)
 s.write_json(out/'actor-inputs.json',actor);s.write_json(out/'behavior-plan.json',behaviors)
 for name,text in data['files'].items():(out/name).write_text(text)
 expected=s.strict_json((out/'input-files.sha256.json').read_bytes())
 if set(expected)!={'actor-inputs.json','behavior-plan.json','config.json','reservation.json','response.schema.json'}:raise ValueError('EXPECTED_FILE_SET')
 for name,h in expected.items():
  if s.sha((out/name).read_bytes())!=h:raise ValueError('PLANNED_BYTES_DIFFER:'+name)
 return {'files_verified':len(expected),'trials':len(data['trials']),'model_calls':0,'no_prompt_summarization':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['pack','inflate']);p.add_argument('--checkpoint');p.add_argument('--recipe');p.add_argument('--native');p.add_argument('--protocol');p.add_argument('--out',required=True);a=p.parse_args()
 print(pack(a.checkpoint,a.out) if a.mode=='pack' else json.dumps(inflate(a.recipe,a.native,a.protocol,a.out)))
