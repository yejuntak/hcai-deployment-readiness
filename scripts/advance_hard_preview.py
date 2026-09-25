"""Freeze the last rc.4 distribution, then mechanically advance active identities."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
site = root.parent/'readiness-site'
old = root/'protocol/0.1-rc.4-candidate.6'
new = root/'protocol/0.2-preview.1'
manifest = root/'historical/candidate-6-manifest.json'
if manifest.exists() or new.exists():
    raise SystemExit('Already advanced; do not overwrite historical artifacts')
paths = [*old.glob('*.md'), *(root/'output/pdf').glob('*v0.1-rc.4-candidate.6.pdf'),
         root/'Pilot-Kit/rc4-candidate-6-external-packet.md',
         root/'release/HCAI-v0.1-rc.4-candidate.6.zip',
         root/'release/hcai_readiness_mcp-0.2.0rc6-py3-none-any.whl',
         root/'release/ai-ready-0.2.0-rc.6.zip']
assert len(paths) == 15 and all(p.is_file() for p in paths)
payload = {'protocol': '0.1-rc.4-candidate.6', 'mcp': '0.2.0rc6', 'skill': '0.2.0-rc.6',
           'source_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
           'note': 'Original source, contracts, documentation and test reports remain in the complete historical ZIP.',
           'files': {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}}
with manifest.open('x') as f:
    f.write(json.dumps(payload,indent=2)+'\n')
assets = sorted(p for p in (site/'static/research/ai-readiness/rc4-candidate-6').glob('*') if p.is_file())
assert len(assets) == 28
with (root/'historical/candidate-6-site-manifest.json').open('x') as f:
    f.write(json.dumps({'files':{str(p.relative_to(site)):hashlib.sha256(p.read_bytes()).hexdigest() for p in assets}},indent=2)+'\n')
def advance(text):
    return text.replace('0.1-rc.4-candidate.6','0.2-preview.1').replace('0.2.0rc6','0.2.0rc7').replace('0.2.0-rc.6','0.2.0-rc.7').replace('rc4-candidate-6','hard-0.2-preview-1')
new.mkdir()
for path in old.glob('*.md'):
    (new/path.name).write_text(advance(path.read_text()))
(root/'Pilot-Kit/hard-0.2-preview-1-external-packet.md').write_text(advance((root/'Pilot-Kit/rc4-candidate-6-external-packet.md').read_text()))
names = ('README.md','CITATION.cff','.zenodo.json','pyproject.toml',
         'docs/research-content.gohtml','docs/research-page-copy.md','docs/agent-tools.md',
         'docs/research-boundary.md','docs/deep-audit.md','docs/claims-and-governance.md',
         'scripts/build_candidate_assets.py','scripts/build_experience.py','scripts/build_pdfs.py','scripts/package_candidate.py',
         'skills/ai-ready/SKILL.md')
paths = [root/name for name in names]
paths += list((root/'src/hcai_readiness').glob('*.py'))
paths += [root/'src/hcai_readiness/criteria.json']
paths += list((root/'tests').glob('*.py'))
for path in paths:
    path.write_text(advance(path.read_text()))
for name in ('main.go','research_test.go'):
    path = site/name
    path.write_text(advance(path.read_text()).replace('Review AI-built workflows - rc.4 candidate.6','HARD Protocol 0.2'))
print('Frozen 15 candidate.6 artifacts and 28 published assets; active identities advanced')
