"""One-time freeze and mechanical version advance; published candidates are immutable."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
old = root / 'protocol/0.1-rc.4-candidate.2'
new = root / 'protocol/0.1-rc.4-candidate.3'
manifest = root / 'historical/candidate-2-manifest.json'
if manifest.exists() or new.exists():
    raise SystemExit('Already advanced; refusing to overwrite historical artifacts')
paths = [*old.glob('*.md'), * (root/'output/pdf').glob('*v0.1-rc.4-candidate.2.pdf'),
         root/'Pilot-Kit/rc4-candidate-2-external-packet.md',
         root/'release/HCAI-v0.1-rc.4-candidate.2.zip',
         root/'release/hcai_readiness_mcp-0.2.0rc2-py3-none-any.whl',
         root/'release/ai-ready-0.2.0-rc.2.zip']
payload = {'protocol':'0.1-rc.4-candidate.2', 'mcp':'0.2.0rc2', 'skill':'0.2.0-rc.2',
           'source_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
           'note':'The complete historical ZIP retains original source, contracts, documentation and regression report.',
           'files':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}}
with manifest.open('x') as stream:
    stream.write(json.dumps(payload,indent=2)+'\n')
site = root.parent/'readiness-site'
asset_paths = sorted((site/'static/research/ai-readiness/rc4-candidate-2').glob('*'))
with (root/'historical/candidate-2-site-manifest.json').open('x') as stream:
    stream.write(json.dumps({'files':{str(p.relative_to(site)):hashlib.sha256(p.read_bytes()).hexdigest() for p in asset_paths if p.is_file()}},indent=2)+'\n')
def advance(text):
    return text.replace('0.1-rc.4-candidate.2','0.1-rc.4-candidate.3').replace('0.2.0rc2','0.2.0rc3').replace('0.2.0-rc.2','0.2.0-rc.3').replace('rc4-candidate-2','rc4-candidate-3')
new.mkdir()
for path in old.glob('*.md'):
    (new/path.name).write_text(advance(path.read_text()))
(root/'Pilot-Kit/rc4-candidate-3-external-packet.md').write_text(advance((root/'Pilot-Kit/rc4-candidate-2-external-packet.md').read_text()))
paths = [root/n for n in ('README.md','CITATION.cff','.zenodo.json','pyproject.toml',
    'docs/research-content.gohtml','docs/research-page-copy.md','docs/agent-tools.md',
    'docs/research-boundary.md','docs/migration-rc3-to-rc4.md',
    'scripts/build_candidate_assets.py','scripts/build_experience.py','scripts/build_pdfs.py','scripts/package_candidate.py',
    'evidence/change-manifest.json','evidence/feedback-ledger.public.json')]
paths += list((root/'src/hcai_readiness').glob('*.py')) + list((root/'tests').glob('*.py')) + list((root/'schemas').glob('*.json'))
paths += [root/'skills/ai-ready/SKILL.md',root/'skills/ai-ready/agents/openai.yaml']
for path in paths:
    if path.exists():
        path.write_text(advance(path.read_text()))
for name in ('main.go','research_test.go'):
    path=site/name
    path.write_text(advance(path.read_text()))
print('Frozen',len(payload['files']),'candidate.2 files; advanced active source references only')
