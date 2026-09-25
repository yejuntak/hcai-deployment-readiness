"""One-shot, allowlisted identity migration. Published predecessors stay byte-frozen."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT.parent / 'readiness-site'
OLD = ROOT / 'protocol/0.2-preview.1'
NEW = ROOT / 'protocol/0.2-preview.2'


def advance(text):
    for old, new in (
        ('Human-centered AI Readiness Deployment Protocol', 'Human-centered AI Readiness and Decision Protocol'),
        ('hard-0.2-preview-1', 'hard-0.2-preview-2'),
        ('0.2-preview.1', '0.2-preview.2'), ('0.2.0rc7', '0.2.0rc8'),
        ('0.2.0-rc.7', '0.2.0-rc.8'), ('library-0.2', 'library-0.2-preview-2'),
        ('workspace-0.2.1', 'workspace-0.2.2'), ('0.1.0-preview.1', '0.1.0-preview.2'),
    ):
        text = text.replace(old, new)
    return text


def freeze(base, paths, destination):
    payload = {
        'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=base, text=True).strip(),
        'note': 'Frozen before the Decision naming revision. Original source remains at source_commit; never relabel historical runs.',
        'files': {str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)},
    }
    with destination.open('x') as stream:
        stream.write(json.dumps(payload, indent=2) + '\n')


def main():
    if NEW.exists() or (ROOT/'historical/hard-preview-1-manifest.json').exists():
        raise SystemExit('Already advanced. Refusing to rewrite a historical release.')
    assets = [*OLD.glob('*.md'), *(ROOT/'output/pdf').glob('HARD-*0.2-preview.1.pdf'),
              ROOT/'Pilot-Kit/hard-0.2-preview-1-external-packet.md',
              ROOT/'release/HARD-Protocol-0.2-preview.1.zip',
              ROOT/'release/hcai_readiness_mcp-0.2.0rc7-py3-none-any.whl',
              ROOT/'release/ai-ready-0.2.0-rc.7.zip']
    assert len(assets) == 15 and all(p.is_file() for p in assets)
    freeze(ROOT, assets, ROOT/'historical/hard-preview-1-manifest.json')
    freeze(SITE, [p for p in (SITE/'static/research/ai-readiness').rglob('*') if p.is_file()],
           ROOT/'historical/hard-preview-1-site-manifest.json')
    NEW.mkdir()
    for path in OLD.glob('*.md'):
        (NEW/path.name).write_text(advance(path.read_text()))
    (ROOT/'Pilot-Kit/hard-0.2-preview-2-external-packet.md').write_text(
        advance((ROOT/'Pilot-Kit/hard-0.2-preview-1-external-packet.md').read_text()))
    names = ['README.md', 'CITATION.cff', '.zenodo.json', 'pyproject.toml',
             'docs/research-content.gohtml', 'docs/research-page-copy.md', 'docs/agent-tools.md',
             'docs/research-boundary.md', 'docs/deep-audit.md', 'docs/claims-and-governance.md',
             'docs/editorial-review.md', 'docs/migration-rc3-to-rc4.md',
             'Publication/hard-0.2-release-checklist.md', 'skills/ai-ready/SKILL.md',
             'schemas/change-manifest.schema.json',
             'scripts/build_candidate_assets.py', 'scripts/build_experience.py',
             'scripts/build_pdfs.py', 'scripts/package_candidate.py']
    paths = [ROOT/n for n in names] + list((ROOT/'src/hcai_readiness').glob('*.py'))
    paths += [ROOT/'src/hcai_readiness/criteria.json'] + list((ROOT/'tests').glob('*.py'))
    for path in paths:
        original = path.read_text()
        updated = advance(original)
        if updated != original:
            path.write_text(updated)
    # Existing change entries and dates describe their original releases.
    manifest_path = ROOT/'evidence/change-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['protocol_version'] = '0.2-preview.2'
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n')
    site_names = ['templates/research.gohtml', 'templates/hard-library.gohtml',
                  'main.go', 'research_test.go', 'static/hard-workspace.js',
                  'tools/verify_hard_workspace.py', 'tools/build_hard_workspace.py',
                  'companion/hard_companion.py', 'companion/README.md',
                  'companion/hard-jev-review/SKILL.md', 'companion/test_companion.py']
    for name in site_names:
        path = SITE/name
        path.write_text(advance(path.read_text()))
    # Reuse the unchanged rubric at a new companion distribution path.
    out = SITE/'static/research/ai-readiness/workspace-0.2.2'
    out.mkdir()
    shutil.copyfile(SITE/'static/research/ai-readiness/workspace-0.2.1/rubric.json', out/'rubric.json')
    print('Preserved 15 protocol artifacts and all prior website distributions; advanced active compatibility set.')


if __name__ == '__main__':
    main()
