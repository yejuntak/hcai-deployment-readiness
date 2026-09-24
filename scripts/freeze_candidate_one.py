"""One-time, non-overwriting manifest for the first public rc.4 candidate."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
target = root / 'historical/candidate-1-manifest.json'
if target.exists():
    raise SystemExit('Candidate 1 is already frozen; refusing to replace its manifest')
paths = [*sorted((root / 'protocol/0.1-rc.4-candidate').glob('*.md')),
         *sorted((root / 'output/pdf').glob('*.pdf')),
         root / 'release/HCAI-v0.1-rc.4-candidate.zip',
         root / 'release/hcai_readiness_mcp-0.2.0rc1-py3-none-any.whl',
         root / 'release/ai-ready-0.2.0-rc.1.zip']
manifest = {'protocol': '0.1-rc.4-candidate', 'mcp': '0.2.0rc1', 'skill': '0.2.0-rc.1',
            'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
            'note': 'The original complete ZIP retains all original source, schemas, reports and documentation. Named files stay byte-frozen.',
            'files': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
with target.open('x') as stream:
    json.dump(manifest, stream, indent=2)
    stream.write('\n')
print('Candidate 1 preserved:', len(paths), 'artifacts')
