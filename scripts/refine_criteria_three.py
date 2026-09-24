"""Mechanical source migration for candidate.3 criterion refinements; stable IDs retained."""
import json
from pathlib import Path
path = Path(__file__).resolve().parents[1]/'src/hcai_readiness/criteria.json'
data = json.loads(path.read_text())
data['version'] = '0.1-rc.4-candidate.3'
by_id = {c['id']:c for c in data['criteria']}
by_id['HCAI-2.2']['requirement'] = 'Each important requirement/artifact pair has an executed check bound to both its exact artifact digest and its requirement/context fingerprint. A change to acceptance criteria, scope, linked states, references, dependencies or authority invalidates the affected check.'
by_id['HCAI-2.2']['check'] = 'Compare both fingerprints with the record captured when the check ran. Repeat the affected check after a change; computing a new hash does not constitute retesting.'
by_id['HCAI-3.1']['requirement'] = 'Represent connected normal, edge and recovery paths with an entry, resolvable next-state IDs, reachable endpoints, data treatment, ownership and requirement links. Review transition conditions, dependency failures and bounded retry/exit behavior.'
by_id['HCAI-4.1']['requirement'] = 'Classify six risk dimensions and four consequential-context flags. Use the highest dimension or context floor. Safety/rights impact or irreversible external action sets high; sensitive data or untrusted input to actions sets at least moderate. Any unknown prevents QUICK6.'
by_id['HCAI-4.2']['requirement'] += ' A recorded human evidence-quality review must address relevance, completeness, authenticity and test adequacy; agent-only assertions cannot replace it.'
if 'HCAI-1.4' not in by_id:
    data['criteria'].insert(3, {'id':'HCAI-1.4','title':'Include the people who bear the consequences','gate':'G2_NEED_REQUIREMENTS',
        'requirement':'Name affected roles, including non-operators. Screen access/usability, privacy/security, unequal effects and human agency. Link applicable concerns to requirements and validation; justify inapplicable items with an owner and evidence. Human use/control cannot be excluded.',
        'check':'Ask who might be unable to use, correct, decline or challenge the workflow, and who could be affected without operating it. Inspect the linked success conditions and evidence, not just a checked box.',
        'pass_example':'A requester and an advisor can correct an intake; the requirement specifies retained data, readable error feedback and a human escalation path.',
        'failure_example':'The owner saves time, but a requester cannot correct a wrong generated record and nobody evaluated that effect.',
        'verification':'Deterministic coverage and applicability checks plus human/context-specific review; not an accessibility, fairness, privacy or security certification'})
path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
