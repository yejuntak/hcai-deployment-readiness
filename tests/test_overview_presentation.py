"""Presentation can change without rebuilding or relabeling the protocol."""
import sys
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_experience import render_research_page, render_overview_document
from hcai_readiness.guidance import criteria_catalog


def test_overview_links_to_all_canonical_rules_without_duplicating_them():
    page = render_research_page()
    assert page.count('href="/research/ai-readiness/developers"') == 1
    assert page.count('data-primary-task') == 4
    assert page.split('</section>')[0].count('data-primary-task') == 2
    assert 'class="research-criterion"' not in page
    assert '<!-- CRITERIA -->' not in page
    assert '@@HARD_' not in page
    for criterion in criteria_catalog()['criteria']:
        assert 'id="'+criterion['id']+'"' in page
        assert criterion['requirement'] not in page
    assert 'H.A.R.D. Protocol 0.2' in page
    assert 'Public Preview' in page
    assert 'id="hard-mcp-config"' not in page
    assert 'class="hard-legacy-anchors" aria-hidden="true"' in page


def test_overview_explains_the_missing_layer_without_claiming_a_result():
    page = render_research_page()
    assert 'Look beneath the finished screen.' in page
    assert 'origin anecdote, not evidence of a measured effect' in page
    assert 'Payment went through.<br>The booking did not.' in page
    assert 'Do not blur labels or remove information people need' in page
    for label in ('Experience and information', 'Workflow and architecture',
                  'Implementation and evidence', 'People and operation'):
        assert label in page
    protocol = (ROOT/'protocol/0.2-preview.2/PROTOCOL.md').read_text()
    assert 'not four scores or additional gates' in protocol
    skill = (ROOT/'skills/ai-ready/SKILL.md').read_text()
    assert 'Never introduce this view into a research session' in skill


def test_opening_has_seven_actual_routes_not_just_seven_labels():
    hero = render_research_page().split('</section>')[0]
    links = re.findall(r'<a\b[^>]*href="([^"]+)"', hero)
    assert len(links) == len(set(links)) == 7
    assert hero.count('data-entry-route') == 7
    assert hero.count('data-primary-task') == 2
    assert '<button' not in hero
    assert 'aria-label="More ways to use H.A.R.D."' in hero
    assert all(label in hero for label in (
        'Read the protocol', 'Developer Library', 'Start with QUICK-6',
        'See an example', 'Connect MCP', 'Add the Skill', 'Try Jev'))


def test_conceptual_image_and_current_prose_keep_evidence_boundaries():
    page = render_research_page()
    assert 'hard-structure-20260925.jpg' in page
    assert 'width="1536" height="1024"' in page
    assert 'AI-generated conceptual illustration, not a study result.' in page
    assert 'alt="A finished-looking interface' in page
    assert 'The 15-minute target remains untested.' in page
    assert 'deployment requires separate evaluation' in page
    assert not any(char in unescape(page) for char in ('\u2013', '\u2014'))


def test_repository_mirrors_resolve_public_assets_and_keep_shared_styles():
    page = render_overview_document()
    assert 'href="/' not in page and 'src="/' not in page
    assert 'https://www.takyejun.com/static/research/ai-readiness/visuals/hard-structure-20260925.jpg' in page
    assert 'https://www.takyejun.com/static/system/research.css' in page
    assert 'class="site-page page-research"' in page
    assert 'href="#start"' in page and 'href="#scenarios"' in page
    assert page.count('data-entry-route') == 7
    for name in ('index.html', 'docs/index.html'):
        assert (ROOT/name).read_text() == page
