"""Build repository research pages from the same candidate content as the website."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CONTENT = (ROOT / "docs/research-content.gohtml").read_text().replace('{{define "research"}}', '').replace('{{end}}', '')
STYLE = """body{margin:0;color:#172b43;background:#faf9f5;font:17px/1.65 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:28px}h1{font-size:clamp(38px,5vw,66px);line-height:1.08;letter-spacing:-.035em}h2{font-size:30px;line-height:1.25}h3{line-height:1.35}a{color:#244cac;text-underline-offset:4px}a:focus-visible,summary:focus-visible,button:focus-visible{outline:3px solid #b87913;outline-offset:4px}.o-section{border-top:1px solid #d6dce2;margin-top:38px;padding-top:24px}.research-hero,.ds-grid-2{display:grid;grid-template-columns:1.4fr 1fr;gap:32px}.ds-grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.research-install,.o-card-archetype,.m-callout,.research-preview,details{padding:22px;border:1px solid #d6dce2;border-radius:8px;background:#fff}.o-card-archetype{display:block;text-decoration:none}.o-card-archetype-title{font-size:23px}.o-card-archetype-head,.t-eyebrow,.o-hero-page-eyebrow,.m-eyebrow-title-eyebrow{font-size:13px;text-transform:uppercase;letter-spacing:.09em;color:#506179}.o-hero-page-lede{font-size:24px;line-height:1.4}.button{display:inline-block;border:1px solid #172b43;padding:10px 16px;border-radius:5px;text-decoration:none}.button-primary{background:#172b43;color:white}.m-cta-pair,.cluster,.research-jump{display:flex;flex-wrap:wrap;gap:12px}.tag{font-size:12px;background:#edf0f3;padding:4px 8px;border-radius:4px}.research-install-item{border-top:1px solid #d6dce2;margin-top:18px}.research-measures>div{display:grid;grid-template-columns:1fr 2fr;gap:20px;padding:18px 0;border-bottom:1px solid #d6dce2}dt{font-weight:650}dd{margin:0}dt span{display:block}.research-usage-list li{margin-bottom:18px}.research-preview-row{display:flex;justify-content:space-between;padding:15px 0;border-bottom:1px solid #d6dce2}.research-preview-note{border-left:3px solid #a26415;padding:16px;margin-top:18px}.stack>a{display:block;margin:12px 0}.u-mt-5{margin-top:24px}.t-body-s{font-size:14px;color:#506179}pre{overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}summary{cursor:pointer}footer{margin-top:40px;font-size:14px}@media(max-width:720px){.research-hero,.ds-grid-2,.ds-grid-3{grid-template-columns:1fr}main{padding:20px}.research-measures>div{grid-template-columns:1fr;gap:8px}}"""


def mapped(name, prefix):
    if name.endswith('.pdf'):
        return prefix + 'output/pdf/' + name
    mapping = {'change-manifest.json': 'evidence/change-manifest.json', 'rc4-test-results.json': 'Verification/rc4-test-results.json',
               'agent-tools.md': 'docs/agent-tools.md', 'migration-rc3-to-rc4.md': 'docs/migration-rc3-to-rc4.md'}
    return prefix + mapping.get(name, 'release/' + name)


def main():
    for filename, prefix in [('index.html', ''), ('docs/index.html', '../')]:
        content = re.sub(r'href="/static/research/ai-readiness/rc4-candidate/([^"#]+)"', lambda m: 'href="' + mapped(m.group(1), prefix) + '"', CONTENT)
        content = content.replace('href="/static/research/ai-readiness/', 'href="' + prefix)
        content = content.replace('href="/design-system#research-use"', 'href="https://www.takyejun.com/design-system#research-use"')
        page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HCAI Engineering Commitment - rc.4 Candidate</title><meta name="description" content="Current workflow, six gates and risk-tiered evidence before an engineering commitment."><style>' + STYLE + '.m-callout-icon{width:24px;height:24px;flex-shrink:0}.m-callout{display:flex;align-items:flex-start;gap:16px}</style></head><body><main>' + content + '</main><script>document.querySelectorAll("[data-copy-target]").forEach(b=>b.addEventListener("click",async()=>{try{await navigator.clipboard.writeText(document.getElementById(b.dataset.copyTarget).textContent);document.querySelector(".research-copy-status").textContent="Configuration copied."}catch{document.querySelector(".research-copy-status").textContent="Select and copy the configuration above."}}));</script></body></html>'
        (ROOT / filename).write_text(page)
    print('Research pages generated from shared candidate content')


if __name__ == '__main__':
    main()
