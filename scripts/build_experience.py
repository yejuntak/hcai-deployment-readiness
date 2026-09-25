"""Generate progressive HTML reading views from versioned method and criterion sources."""
import argparse
import html
import json
import re
import shutil
from pathlib import Path
import markdown
from hcai_readiness.contracts import Assessment
from hcai_readiness.reporting import render_report
from hcai_readiness.guidance import criteria_catalog
from hcai_readiness.versions import versions, public_title, PROTOCOL_FULL_NAME, RELEASE_LABEL, DISTRIBUTION_ID
from build_research_pages import STYLE

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '/static/research/ai-readiness/'+DISTRIBUTION_ID+'/'
PROTOCOL = ROOT / 'protocol' / versions()['protocol']

def page(title, body):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>'+STYLE+'\nmain{max-width:980px}p,li{max-width:80ch}td,th{text-align:left;vertical-align:top;border-bottom:1px solid #ccd6df;padding:12px}table{border-collapse:collapse;width:100%;font-size:15px}th{background:#e8eef4}.table-scroll{overflow:auto}table{min-width:540px}details{margin-block:16px}summary{padding:6px 0}li{margin-block:8px}h1{font-size:clamp(32px,5vw,48px)}.reading-nav{display:flex;gap:24px;flex-wrap:wrap;font-size:15px}code{overflow-wrap:anywhere}main>h1{margin-top:32px}@media print{.reading-nav{display:none}table{min-width:0}.table-scroll{overflow:visible}}\n</style></head><body><main><nav class="reading-nav" aria-label="Protocol navigation"><a href="/research/ai-readiness">Review guide</a><a href="'+PREFIX+'START-HERE.html">Start here</a><a href="/research/ai-readiness/updates">Update log</a></nav>'+body+'</main></body></html>'

def render_research_page():
    """Render the overview only, without rewriting frozen release artifacts."""
    catalogue = criteria_catalog()
    chunks = ['<div class="hard-legacy-anchors" aria-hidden="true">']
    for criterion in catalogue['criteria']:
        cid = html.escape(criterion['id'])
        chunks.append('<span id="'+cid+'" class="sr-only">'+cid+'</span>')
    chunks.append('</div>')
    template = (ROOT/'docs/research-content.gohtml').read_text().replace('<!-- CRITERIA -->','\n'.join(chunks))
    for key, value in {'@@HARD_TITLE@@':public_title(), '@@HARD_FULL_NAME@@':PROTOCOL_FULL_NAME, '@@HARD_STATUS@@':RELEASE_LABEL}.items():
        template = template.replace(key, html.escape(value))
    return template

def render_overview_document():
    """The repository mirror uses the same public assets, not broken root URLs."""
    origin = 'https://www.takyejun.com'
    body = render_research_page().replace('{{define "research"}}', '').replace('{{end}}', '')
    body = re.sub(r'((?:href|src)=")/', lambda m: m[1]+origin+'/', body)
    styles = ''.join('<link rel="stylesheet" href="'+origin+'/static/system/'+name+'.css">'
                     for name in ('tokens', 'reset', 'atoms', 'molecules', 'organisms', 'research'))
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<link rel="canonical" href="'+origin+'/research/ai-readiness">'
            '<title>'+html.escape(public_title())+'</title>'+styles+
            '</head><body class="site-page page-research"><main id="main">'+body+
            '</main></body></html>')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site-root',type=Path)
    args = parser.parse_args()
    output = ROOT/'docs/web'
    output.mkdir(exist_ok=True)
    sources = list(PROTOCOL.glob('*.md')) + [ROOT/'docs'/name for name in ('updates.md','agent-tools.md','migration-rc3-to-rc4.md','decision-naming-migration.md','research-boundary.md','deep-audit.md','claims-and-governance.md','editorial-review.md')]
    names = {p.name:p.stem+'.html' for p in sources}
    for source in sources:
        text = source.read_text()
        def link(match):
            label, target = match.groups()
            basename = target.rsplit('/',1)[-1]
            if not target.startswith(('https:','http:')) and basename in names:
                target = PREFIX+names[basename]
            elif target.startswith('../../docs/'):
                target = 'https://github.com/yejuntak/hcai-deployment-readiness/blob/codex/readiness-rc4-candidate/docs/'+basename
            return '['+label+']('+target+')'
        text = re.sub(r'\[([^]]+)\]\(([^)]+)\)',link,text)
        # Paper-style answer blanks are literal writing spaces, not Markdown emphasis.
        text = re.sub(r'_{3,}', lambda match: r'\_' * len(match.group()), text)
        body = markdown.markdown(text,extensions=['tables','fenced_code'])
        body = body.replace('<table>','<div class="table-scroll" tabindex="0" role="region" aria-label="Table; scroll horizontally on small screens"><table>').replace('</table>','</table></div>')
        title = next((line[2:] for line in source.read_text().splitlines() if line.startswith('# ')), source.stem)
        (output/(source.stem+'.html')).write_text(page(title,body))
    synthetic = Assessment.model_validate_json((ROOT/'examples/rc4/low-risk-quick.json').read_text())
    sample = render_report(synthetic,'html').replace('<main>','<main><p><strong>PUBLIC SYNTHETIC EXAMPLE: no real participant or pilot.</strong> The private label below describes the report default; this constructed example contains no confidential participant record.</p><p><a href="/research/ai-readiness">Return to the guide</a></p>')
    (output/'example-report.html').write_text(sample)
    for name in ('index.html','docs/index.html'):
        (ROOT/name).write_text(render_overview_document())
    if args.site_root:
        target=args.site_root/'static/research/ai-readiness'/DISTRIBUTION_ID
        target.mkdir(parents=True,exist_ok=True)
        for p in output.glob('*.html'):
            shutil.copyfile(p,target/p.name)
        # Runtime templates use shared site components. Publishing reading views
        # must not replace that composition with the standalone HTML version.
    print('Generated linked reading views, criteria, synthetic report and shared research page')

if __name__=='__main__':
    main()
