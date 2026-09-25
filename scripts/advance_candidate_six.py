"""Freeze candidate.5, then advance active copies for an editorial-only candidate."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
site = root.parent / 'readiness-site'
old = root / 'protocol/0.1-rc.4-candidate.5'
new = root / 'protocol/0.1-rc.4-candidate.6'
manifest = root / 'historical/candidate-5-manifest.json'
if manifest.exists() or new.exists():
    raise SystemExit('Already advanced; historical artifacts will not be overwritten')
paths = [*old.glob('*.md'), *(root/'output/pdf').glob('*v0.1-rc.4-candidate.5.pdf'),
         root/'Pilot-Kit/rc4-candidate-5-external-packet.md',
         root/'release/HCAI-v0.1-rc.4-candidate.5.zip',
         root/'release/hcai_readiness_mcp-0.2.0rc5-py3-none-any.whl',
         root/'release/ai-ready-0.2.0-rc.5.zip']
payload = {'protocol': '0.1-rc.4-candidate.5', 'mcp': '0.2.0rc5', 'skill': '0.2.0-rc.5',
           'source_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
           'note': 'The complete historical ZIP retains the original source, contracts, documentation and test report.',
           'files': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}}
with manifest.open('x') as stream:
    stream.write(json.dumps(payload, indent=2)+'\n')
assets = sorted((site/'static/research/ai-readiness/rc4-candidate-5').glob('*'))
with (root/'historical/candidate-5-site-manifest.json').open('x') as stream:
    stream.write(json.dumps({'files': {str(p.relative_to(site)): hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in assets if p.is_file()}}, indent=2)+'\n')

def advance(text):
    return text.replace('0.1-rc.4-candidate.5','0.1-rc.4-candidate.6').replace('0.2.0rc5','0.2.0rc6').replace('0.2.0-rc.5','0.2.0-rc.6').replace('rc4-candidate-5','rc4-candidate-6')

new.mkdir()
for path in old.glob('*.md'):
    (new/path.name).write_text(advance(path.read_text()))
(root/'Pilot-Kit/rc4-candidate-6-external-packet.md').write_text(advance((root/'Pilot-Kit/rc4-candidate-5-external-packet.md').read_text()))
names = ('README.md','CITATION.cff','.zenodo.json','pyproject.toml',
         'docs/research-content.gohtml','docs/research-page-copy.md','docs/agent-tools.md',
         'docs/research-boundary.md','docs/deep-audit.md','docs/claims-and-governance.md',
         'scripts/build_candidate_assets.py','scripts/build_experience.py','scripts/build_pdfs.py','scripts/package_candidate.py',
         'skills/ai-ready/SKILL.md','skills/ai-ready/agents/openai.yaml')
paths = [root/name for name in names]
paths += list((root/'src/hcai_readiness').glob('*.py'))
paths += [root/'src/hcai_readiness/criteria.json']
paths += list((root/'tests').glob('*.py'))
for path in paths:
    if path.exists():
        path.write_text(advance(path.read_text()))
for name in ('main.go','research_test.go'):
    path = site/name
    path.write_text(advance(path.read_text()).replace('rc.4 candidate.5','rc.4 candidate.6'))
print('Frozen', len(payload['files']), 'candidate.5 artifacts and', len(assets), 'website assets')
