"""Allowlisted candidate distribution; never includes private mail/pilot source files."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path
from hcai_readiness.versions import identity, versions, public_title, RELEASE_LABEL, DISTRIBUTION_ID, MCP_VERSION, SKILL_VERSION

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / 'release'
ZIP_NAME = 'HARD-Protocol-'+versions()['protocol']+'.zip'


def candidates():
    folders = (f"protocol/{versions()['protocol']}", 'src', 'skills', 'schemas', 'examples', 'evidence', 'docs', 'tests',
               'output/pdf', 'scripts', 'Templates', 'Worked-Example')
    files = [ROOT / n for n in ('README.md', 'CHANGELOG.md', 'LICENSE', 'CITATION.cff', 'versions.json', 'identity.json',
                               'pyproject.toml', 'uv.lock', 'index.html', f'Pilot-Kit/{DISTRIBUTION_ID}-external-packet.md',
                               'Source/verify_example.py', 'Source/README.md', 'Verification/current-test-results.json',
                               'Verification/current-release-readiness.json')]
    for folder in folders:
        files.extend(p for p in (ROOT / folder).rglob('*') if p.is_file())
    # Frozen releases stay separately available. Do not recursively bundle old packages,
    # obsolete root scorecards/workbooks or historical-generation scripts as current tools.
    return sorted({p for p in files if p.exists() and '__pycache__' not in p.parts and p.suffix != '.pyc'
                   and p.name != '.DS_Store'
                   and not (p.parent == ROOT/'output/pdf' and versions()['protocol'] not in p.name)
                   and not (p.parent == ROOT/'scripts' and p.name.startswith(('advance_', 'freeze_', 'record_audit', 'refine_', 'apply_structure')))
                   and not (p.suffix in ('.xlsx','.pdf') and 'Worked-Example' in p.parts)})


def zip_files(path, files, relative_to, prefix=''):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for item in files:
            archive.write(item, prefix + str(item.relative_to(relative_to)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site-root', type=Path)
    args = parser.parse_args()
    report = json.loads((ROOT / 'Verification/current-test-results.json').read_text())
    if report['exit_code'] or report['failures'] or report['errors'] or report['tests'] == 0:
        raise SystemExit('Current passing regression report required')
    for name, expected in report['input_file_sha256'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise SystemExit(f'Test report is stale for {name}; rerun verification')
    RELEASE.mkdir(exist_ok=True)
    wheel = ROOT / f'dist/hcai_readiness_mcp-{MCP_VERSION}-py3-none-any.whl'
    if not wheel.exists():
        raise SystemExit('Build candidate wheel with uv build --wheel first')
    # Ensure packaging cannot accidentally publish an earlier engine at the same version.
    with zipfile.ZipFile(wheel) as archive:
        for path in (ROOT / 'src/hcai_readiness').iterdir():
            if not path.is_file():
                continue
            if archive.read('hcai_readiness/' + path.name) != path.read_bytes():
                raise SystemExit(f'Stale wheel: {path.name}')
    shutil.copyfile(wheel, RELEASE / wheel.name)
    skill_files = [p for p in (ROOT / 'skills/ai-ready').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    skill_zip = RELEASE / f'ai-ready-{SKILL_VERSION}.zip'
    zip_files(skill_zip, sorted(skill_files), ROOT / 'skills')
    files = candidates()
    checksum_lines = ['# '+public_title()+'; '+RELEASE_LABEL+'; exact versions in versions.json; historical hashes remain under historical/.']
    checksum_lines += [hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + str(p.relative_to(ROOT)) for p in files]
    (ROOT / 'SHA256SUMS').write_text('\n'.join(checksum_lines) + '\n')
    zip_files(RELEASE / ZIP_NAME, files + [ROOT / 'SHA256SUMS', RELEASE / wheel.name, skill_zip], ROOT,
              prefix=ZIP_NAME.removesuffix('.zip')+'/')
    published = [RELEASE / ZIP_NAME, skill_zip, RELEASE / wheel.name, *(ROOT / 'output/pdf').glob(f"HARD-*{versions()['protocol']}.pdf")]
    manifest = {'protocol_version': versions()['protocol'], 'status': 'public_preview', 'identity': identity(), 'files': {
        p.name: {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size} for p in published}}
    (RELEASE / 'download-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    if args.site_root:
        site_root = args.site_root.resolve()
        if not (site_root / 'templates/research.gohtml').is_file():
            raise SystemExit('Expected existing portfolio research template')
        target = site_root / 'static/research/ai-readiness' / DISTRIBUTION_ID
        target.mkdir(parents=True, exist_ok=True)
        for path in published + [RELEASE / 'download-manifest.json']:
            shutil.copyfile(path, target / path.name)
        for source, name in (('evidence/change-manifest.json', 'change-manifest.json'),
                             ('Verification/current-test-results.json', 'current-test-results.json'),
                             ('Verification/current-release-readiness.json', 'current-release-readiness.json'),
                             ('docs/agent-tools.md', 'agent-tools.md'), ('docs/migration-0.2-to-0.3.md', 'migration-0.2-to-0.3.md')):
            shutil.copyfile(ROOT / source, target / name)
        print(f'Public Preview downloads synchronized to {target}')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
