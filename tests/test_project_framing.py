"""Keep the HCAI review's current identity separate from unrelated standards."""
import hashlib
import html
import json
from pathlib import Path

from hcai_readiness.guidance import GUIDES, criteria_catalog
from hcai_readiness.versions import versions

ROOT = Path(__file__).resolve().parents[1]


def test_current_materials_do_not_claim_unrelated_standard_origin():
    paths = list((ROOT/'protocol'/versions()['protocol']).glob('*.md'))
    paths += list((ROOT/'docs').glob('*.md'))
    paths += list((ROOT/'docs/web').glob('*.html'))
    paths += list((ROOT/'skills/ai-ready/references').glob('*.md'))
    paths += [ROOT/name for name in (
        'README.md', 'CHANGELOG.md', 'docs/research-content.gohtml',
        'skills/ai-ready/SKILL.md', 'src/hcai_readiness/protocol.md',
        'index.html', 'docs/index.html',
    )]
    tokens = ('wcag', 'w3c', 'w3.org/', 'web content accessibility guidelines')
    failures = [str(path.relative_to(ROOT)) for path in paths
                if any(token in html.unescape(path.read_text()).lower() for token in tokens)]
    assert not failures, failures
    for content in (GUIDES, criteria_catalog()):
        assert not any(token in json.dumps(content).lower() for token in tokens)
    protocol = (ROOT/'protocol'/versions()['protocol']/'PROTOCOL.md').read_text()
    assert 'HCAI' in protocol and 'engineering-commitment' in protocol
    assert 'does not certify a system or approve deployment' in protocol


def test_candidate_five_remains_byte_frozen():
    manifest = json.loads((ROOT/'historical/candidate-5-manifest.json').read_text())
    assert len(manifest['files']) == 15
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest
    site = ROOT.parent/'readiness-site'
    if site.is_dir():
        assets = json.loads((ROOT/'historical/candidate-5-site-manifest.json').read_text())
        assert len(assets['files']) == 28
        for name, digest in assets['files'].items():
            assert hashlib.sha256((site/name).read_bytes()).hexdigest() == digest
