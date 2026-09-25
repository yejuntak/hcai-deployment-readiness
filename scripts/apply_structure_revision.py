"""Apply dotted public branding to the unpublished preview.2 only."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT.parent/'readiness-site'

def main():
    paths = list((ROOT/'protocol/0.2-preview.2').glob('*.md'))
    paths += [ROOT/name for name in ['README.md', 'CITATION.cff', '.zenodo.json',
              'Publication/hard-0.2-release-checklist.md', 'Pilot-Kit/hard-0.2-preview-2-external-packet.md',
              'skills/ai-ready/SKILL.md', 'src/hcai_readiness/versions.py',
              'src/hcai_readiness/server.py', 'scripts/build_candidate_assets.py']]
    paths += [p for p in (ROOT/'docs').glob('*.md') if p.name != 'updates.md']
    paths += list((ROOT/'tests').glob('*.py'))
    paths += [SITE/name for name in ['main.go', 'templates/base.gohtml', 'templates/hard-library.gohtml',
              'companion/README.md', 'companion/hard-jev-review/SKILL.md', 'tools/build_hard_workspace.py',
              'static/research/ai-readiness/workspace-0.2.2/updates.html']]
    paths += list(SITE.glob('*test.go'))
    for path in paths:
        old = path.read_text()
        updated = old.replace('HARD Protocol', 'H.A.R.D. Protocol')
        if old != updated:
            path.write_text(updated)
    # Preserve the already published historical sections verbatim.
    for name, boundary in [('CHANGELOG.md', '# HARD Protocol 0.2: Public Preview, September 24, 2026'),
                           ('docs/updates.md', '## September 24, 2026: HARD Protocol 0.2 Public Preview')]:
        path = ROOT/name
        head, tail = path.read_text().split(boundary, 1)
        path.write_text(head.replace('HARD Protocol', 'H.A.R.D. Protocol')+boundary+tail)
    path = SITE/'templates/hard-updates.gohtml'
    head, tail = path.read_text().split('<p class="t-eyebrow">September 24, 2026 / Website layout update</p>', 1)
    path.write_text(head.replace('HARD Protocol', 'H.A.R.D. Protocol')+'<p class="t-eyebrow">September 24, 2026 / Website layout update</p>'+tail)
    print('Current display labels dotted. Frozen files and historical log sections untouched.')

if __name__ == '__main__':
    main()
