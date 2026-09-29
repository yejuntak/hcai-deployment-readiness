"""Versioned native task identity repair. No original study bytes are edited.

Only folder names and instrument IDs change; instruction, context, response
schema, evidence and answers are not rewritten. Same UID is NOT isolation.
"""
from pathlib import Path
import hashlib,json,shutil

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def repair_export(source:Path,destination:Path):
 source=source.resolve();destination=destination.resolve()
 if destination.exists():raise FileExistsError(destination)
 paths=sorted(p for p in source.iterdir() if p.is_dir())
 if not paths:raise ValueError('NO_TASKS')
 plan=[]
 for p in paths:
  if not p.name.startswith('task-') or p.is_symlink():raise ValueError('UNEXPECTED_TASK_DIRECTORY')
  if any(f.is_symlink() for f in p.rglob('*')):raise ValueError('SYMLINK')
  for required in ['instruction.md','task.toml','input/context.md','input/questionnaire.yaml']:
   if not (p/required).is_file():raise ValueError('INCOMPLETE_TASK')
  questionnaire=json.loads((p/'input/questionnaire.yaml').read_text())
  new_id='hard_multiaxis_'+p.name.removeprefix('task-')+'_v1'
  inv={str(f.relative_to(p)):digest(f) for f in p.rglob('*') if f.is_file()}
  plan.append((p,'survey_'+p.name,new_id,questionnaire,inv))
 if len(set(x[2] for x in plan))!=len(plan):raise ValueError('ID_COLLISION')
 destination.mkdir(parents=True,exist_ok=False);records=[]
 for p,name,new_id,questionnaire,inv in plan:
  target=destination/name;shutil.copytree(p,target)
  old_id=questionnaire['id'];questionnaire['id']=new_id
  (target/'input/questionnaire.yaml').write_text(json.dumps(questionnaire,indent=2,ensure_ascii=False)+'\n')
  actual={str(f.relative_to(target)):digest(f) for f in target.rglob('*') if f.is_file()}
  changes=[k for k in inv if actual[k]!=inv[k]]
  if changes!=['input/questionnaire.yaml']:raise ValueError('UNEXPECTED_COPY_DRIFT')
  old=json.loads((p/'input/questionnaire.yaml').read_text());new=json.loads((target/'input/questionnaire.yaml').read_text())
  del old['id'];del new['id']
  if old!=new:raise ValueError('QUESTION_CONTENT_CHANGED')
  records.append({'original_directory':p.name,'native_directory':name,'original_instrument_id':old_id,'new_instrument_id':new_id,'semantic_change':'instrument identity only; substantive input unchanged','before':inv,'after':actual})
 result={'adapter_version':'native-task-identity/1.1','status':'EXPORTED_NOT_NATIVE_EXECUTED','task_count':len(records),'tasks':records,'original_study_changed':False,'note':'Controller-only index. Final native prompt assertions remain mandatory. These paths/IDs must be registered in an amended plan before research; do not silently substitute under an old plan.'}
 (destination/'CONTROLLER_ONLY_REPAIR_INDEX.json').write_text(json.dumps(result,indent=2))
 return result
