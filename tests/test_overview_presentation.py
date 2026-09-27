"""Presentation can change without rebuilding or relabeling the protocol."""
import sys
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_experience import render_research_page, render_overview_document
from hcai_readiness.guidance import criteria_catalog
from hcai_readiness.versions import versions


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
    assert 'H.A.R.D. Protocol 0.3' in page
    assert 'Public Preview' in page
    assert 'id="hard-mcp-config"' not in page
    assert 'class="hard-legacy-anchors" aria-hidden="true"' in page


def test_overview_explains_the_missing_layer_without_claiming_a_result():
    page = render_research_page()
    assert 'Keep generation from outrunning understanding.' in page
    assert 'not an established causal effect' in page
    assert 'Research motivation' in page
    assert 'varies visual fidelity while holding content, behavior and defects constant' in page
    assert 'Separate a recorded earlier rationale from a new explanation.' in page
    assert 'A well-supported existing choice can stay.' in page
    assert 'Payment went through.' not in page
    assert 'decision compression' in page.lower()
    assert 'keep unknowns unassessed until evidence exists' in page
    for label in ('Experience and information', 'Workflow and architecture',
                  'Implementation and evidence', 'People and operation'):
        assert label in page
    protocol = (ROOT/'protocol'/versions()['protocol']/'PROTOCOL.md').read_text()
    assert 'Inspect four connected aspects' in protocol
    assert 'Do not combine them into a weighted readiness percentage.' in protocol
    assert 'The minimum artifact route cannot waive or pass any of these gates.' in protocol
    skill = (ROOT/'skills/ai-ready/SKILL.md').read_text()
    assert 'Do not introduce guided prompts, alternative suggestions, structural views or answer keys unless the study design specifies them.' in skill


def test_opening_has_seven_actual_routes_not_just_seven_labels():
    # Historical test name is retained for change-manifest links. Removal of
    # the retired integration leaves six distinct routes, with no dead label.
    hero = render_research_page().split('</section>')[0]
    links = re.findall(r'<a\b[^>]*href="([^"]+)"', hero)
    assert len(links) == len(set(links)) == 6
    assert hero.count('data-entry-route') == 6
    assert hero.count('data-primary-task') == 2
    assert '<button' not in hero
    assert 'aria-label="More ways to use H.A.R.D."' in hero
    assert all(label in hero for label in (
        'Choose a review', 'Protocol Library', 'How it works',
        'Find a rule', 'Connect MCP', 'Download Skill'))
    assert 'jev' not in hero.lower()


def test_conceptual_image_and_current_prose_keep_evidence_boundaries():
    page = render_research_page()
    assert 'hard-app-review-20260925.jpg' in page
    assert 'width="1536" height="1024"' in page
    assert 'AI-generated app concept' in page
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
    assert method.count('<li>') == 5
    assert 'role="list"' in method
    assert 'Decompress the choice.' in method
    assert 'Model only what matters.' in method
    assert 'Challenge the model.' in method
    assert 'Prove at the declared stage.' in method
    assert 'Make the next human decision.' in method
    assert 'specified, walkthrough, implemented and runtime-tested evidence separate' in method
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
    assert page.count('data-entry-route') == 6
    for name in ('index.html', 'docs/index.html'):
        assert (ROOT/name).read_text() == page


def test_three_use_paths_are_not_three_assessment_versions():
    page = render_research_page()
    for path in ('artifact', 'quick', 'independent'):
        assert f'data-use-path="{path}"' in page
    assert 'Artifact Review' in page
    assert 'A plan can support a specification handoff. It cannot establish runtime readiness.' in page
    assert 'Ineligible measures stay N/A with reasons.' in page
    assert 'Agent results remain separate from human results.' in page
    assert 'Choose a review' in page
    assert 'href="/research/ai-readiness/developers#rules"' in page
    assert 'data-open-tool="mcp"' in page
    assert 'jev' not in page.lower()
    for slug in ('artifact-review', 'quick-6', 'full-profile', 'independent-evaluation',
                 'decision-review', 'pilot', 'protocol', 'worksheet'):
        assert f'href="/research/ai-readiness/{slug}"' in page


def test_artifact_route_does_not_remove_engineering_gate_or_evidence_boundaries():
    page = render_research_page()
    assert 'Artifact Review' in page
    assert 'QUICK-6' in page and 'Full Profile' in page
    assert 'deployment requires separate evaluation' in page
    assert {item['gate'] for item in criteria_catalog()['criteria']} == {
        'G1_BASELINE', 'G2_NEED_REQUIREMENTS', 'G3_STATES_RECOVERY',
        'G4_TRACEABILITY', 'G5_OVERSIGHT', 'G6_COMMITMENT',
    }
