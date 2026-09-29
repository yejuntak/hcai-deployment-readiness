"""Deterministically select six diverse public MatrAIx personas without outcome data.

Selection uses only non-sensitive task-relevant behavioral/cognitive dimensions.
No case labels, H.A.R.D. answers, model outputs, political/religious/gender fields,
or other protected/sensitive dimensions are inputs to selection.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import yaml

SEED = 20260928
FIELDS = [
    "tech_savviness",
    "risk_tolerance",
    "decision_style",
    "trust_level",
    "time_pressure",
    "cog_detail_orientation",
    "cog_skepticism",
    "cog_patience",
    "cog_ambiguity_tolerance",
    "cog_attention_span",
    "cog_decision_speed",
    "cog_confidence_calibration",
    "cog_question_asking",
    "cog_big_picture_vs_detail",
    "cog_directness",
]
SENSITIVE_EXCLUDED = [
    "political_lean","religiosity","gender_identity","cultural_background",
    "neurotype","health_mental_health","health_chronic_condition",
]
N = 6

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def tie_key(pid: str) -> str:
    return hashlib.sha256(f"{SEED}:{pid}".encode()).hexdigest()

def vector(payload):
    d = payload.get("dimensions") or {}
    return tuple(str(d.get(f, "__MISSING__")) for f in FIELDS)

def dist(a, b):
    assert len(a) == len(b)
    return sum(x != y for x,y in zip(a,b)) / len(a)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--out", required=True)
    args=ap.parse_args()
    root=Path(args.dataset)
    files=sorted(root.glob("persona_*.yaml"))
    if len(files) != 200:
        raise SystemExit(f"EXPECTED_200_PERSONAS_GOT_{len(files)}")
    rows=[]
    for p in files:
        raw=p.read_bytes()
        obj=yaml.safe_load(raw)
        if not isinstance(obj,dict) or not obj.get("persona_id"):
            raise SystemExit(f"BAD_PERSONA:{p.name}")
        dims=obj.get("dimensions") or {}
        if any(k in FIELDS for k in SENSITIVE_EXCLUDED):
            raise SystemExit("SENSITIVE_FIELD_SELECTION_BUG")
        rows.append({
            "persona_id":str(obj["persona_id"]),
            "display_name":str(obj.get("display_name","")),
            "path":str(p.relative_to(root.parent.parent.parent)),
            "sha256":sha256_bytes(raw),
            "vector":vector(obj),
            "origin_persona_id":str((obj.get("provenance") or {}).get("origin_persona_id","")),
            "origin_source_row_index":(obj.get("provenance") or {}).get("origin_source_row_index"),
        })
    # coverage audit
    coverage={}
    for idx,f in enumerate(FIELDS):
        vals=[r["vector"][idx] for r in rows]
        coverage[f]={"nonmissing":sum(v!="__MISSING__" for v in vals),"distinct_nonmissing":len({v for v in vals if v!="__MISSING__"})}
    usable=[f for f,v in coverage.items() if v["nonmissing"]>=20 and v["distinct_nonmissing"]>=2]
    if len(usable)<5:
        raise SystemExit(f"INSUFFICIENT_BEHAVIORAL_COVERAGE:{usable}")
    use_idx=[FIELDS.index(f) for f in usable]
    def d2(a,b):
        return sum(a[i]!=b[i] for i in use_idx)/len(use_idx)
    selected=[]
    first=min(rows,key=lambda r:tie_key(r["persona_id"]))
    selected.append(first)
    while len(selected)<N:
        remaining=[r for r in rows if r not in selected]
        def score(r):
            minimum=min(d2(r["vector"],s["vector"]) for s in selected)
            return (minimum, -int(tie_key(r["persona_id"]),16))
        selected.append(max(remaining,key=score))
    pairs=[]
    for i,a in enumerate(selected):
        for b in selected[i+1:]:
            pairs.append(d2(a["vector"],b["vector"]))
    out={
        "schema_version":"hard-persona-selection/1.0",
        "source_repo":"MatrAIx-ai/MatrAIx-Persona-8B",
        "source_commit":"3633d8dab149a9482a71b024418a49ae828cc941",
        "source_dataset":"persona/datasets/matraix-persona-dev-sample",
        "source_count":len(rows),
        "seed":SEED,
        "method":"deterministic maximin categorical distance",
        "selection_fields":usable,
        "excluded_sensitive_fields":SENSITIVE_EXCLUDED,
        "coverage":coverage,
        "selected":[{k:r[k] for k in ("persona_id","display_name","path","sha256","origin_persona_id","origin_source_row_index")} for r in selected],
        "pairwise_distance":{"min":min(pairs),"max":max(pairs),"mean":sum(pairs)/len(pairs)},
        "outcome_blinding":"No H.A.R.D. case labels, expected answers, qualification outputs or model responses were read by this selector.",
        "representativeness":"NOT_ESTABLISHED",
        "human_equivalence":"NOT_ESTABLISHED",
    }
    Path(args.out).write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print(json.dumps(out,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
