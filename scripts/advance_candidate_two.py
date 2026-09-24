"""One-time mechanical version migration; never rewrites frozen candidate-1 files."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
target = root / 'protocol/0.1-rc.4-candidate.2'
if target.exists():
    raise SystemExit('Candidate-2 sources already exist; migrate only once')
target.mkdir()
def advance(text):
    return re.sub(r'0\.1-rc\.4-candidate(?!\.2)', '0.1-rc.4-candidate.2', text).replace('0.2.0rc1', '0.2.0rc2').replace('0.2.0-rc.1', '0.2.0-rc.2')
for path in (root / 'protocol/0.1-rc.4-candidate').glob('*.md'):
    (target / path.name).write_text(advance(path.read_text()))
paths = ['CITATION.cff', '.zenodo.json', 'schemas/change-manifest.schema.json', 'evidence/change-manifest.json',
         'evidence/feedback-ledger.public.json', 'scripts/build_candidate_assets.py', 'scripts/package_candidate.py',
         'docs/research-content.gohtml', 'tests/test_mcp.py', 'tests/test_rc4.py']
for name in paths:
    path = root / name
    value = advance(path.read_text())
    if name in ('docs/research-content.gohtml', 'scripts/package_candidate.py'):
        value = value.replace('/rc4-candidate/', '/rc4-candidate-2/').replace("/rc4-candidate'", "/rc4-candidate-2'")
    path.write_text(value)
print('Advanced active version references; original candidate artifacts untouched')
