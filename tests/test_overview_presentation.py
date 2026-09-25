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
    assert page.count('data-primary-task') == 5
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
    assert 'The proposed study has not established an effect.' in page
    assert 'Research motivation' in page
    assert 'how visual fidelity affects readiness judgments' in page
    assert 'Payment went through.' not in page
    assert 'review method, not an image filter' in page
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
        'Choose a review', 'Protocol Library', 'How it works',
        'Find a rule', 'Connect MCP', 'Download Skill', 'Connect Jev'))


def test_conceptual_image_and_current_prose_keep_evidence_boundaries():
    page = render_research_page()
    assert 'hard-app-review-20260925.jpg' in page
    assert 'width="1536" height="1024"' in page
    assert 'AI-generated app concept.' in page
    assert 'not a working H.A.R.D. application, a participant record or a study result' in page
    for retired in ('Where the question began.', 'An architect I knew',
                    'watercolor', "architect's actual project", 'hard-structure-20260925.jpg'):
        assert retired not in page
    assert 'class="research-output-list"' in page and '<dt>A recommendation</dt>' not in page
    assert 'alt="App concept: a request-review interface' in page
    assert 'The 15-minute target remains untested.' in page
    assert 'deployment requires separate evaluation' in page
    assert not any(char in unescape(page) for char in ('\u2013', '\u2014'))


def test_method_separates_motivation_from_three_visible_practice_steps():
    method = render_research_page().split('id="method"', 1)[1].split('</section>', 1)[0]
    assert 'hard-method-layout' in method and 'hard-feature-row' not in method
    assert method.index('hard-method-intro') < method.index('hard-method-review')
    assert '<h3 class="t-title-l">' in method
    assert method.count('<li>') == 3
    assert 'role="list"' in method
    assert 'Do not blur labels or remove information people need' in method
    assert 'In a separate view' in method
    assert 'Check the artifact against its requirements and evidence' in method
    assert 'optional review guidance, not an extra gate' in method
    assert 'Keep it separate from the proposed study design' in method
    assert not any(tag in method for tag in ('<a ', '<button', '<details'))


def test_repository_mirrors_resolve_public_assets_and_keep_shared_styles():
    page = render_overview_document()
    assert 'href="/' not in page and 'src="/' not in page
    assert 'https://www.takyejun.com/static/research/ai-readiness/visuals/hard-app-review-20260925.jpg' in page
    assert 'https://www.takyejun.com/static/system/research.css' in page
    assert 'class="site-page page-research"' in page
    assert 'href="#start"' in page and 'href="#method"' in page
    assert '{{template' not in page
    assert page.count('data-entry-route') == 7
    for name in ('index.html', 'docs/index.html'):
        assert (ROOT/name).read_text() == page


def test_three_use_paths_are_not_three_assessment_versions():
    page = render_research_page()
    for path in ('quick', 'full', 'pilot'):
        assert f'data-use-path="{path}"' in page
    assert 'not a third scoring system or a new version' in page
    assert 'actual use of either profile' in page
    assert 'The packet supports planning a pilot' in page
    assert 'Choose a review' in page
    assert 'href="/research/ai-readiness/developers#rules"' in page
    assert 'data-open-tool="mcp"' in page and 'data-open-tool="jev"' in page
    for slug in ('quick-6', 'full-profile', 'pilot', 'protocol', 'worksheet'):
        assert f'href="/research/ai-readiness/{slug}"' in page
