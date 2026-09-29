"""Reproducible source transformation, not a model-output repair."""
from pathlib import Path
import hashlib
p=Path('simulator.py');s=p.read_text()
assert hashlib.sha256(p.read_bytes()).hexdigest()=='bc7a1ab49a70bfdc22870ba6c9ae6f50c2f4697592cb52e364c36e357288e0b7'
changes=[
 ("VERSION = '0.1.0'","VERSION = '0.1.1'"),
 ("'rationale':{'type':'string'},'uncertainty':{'type':'string'},", "'rationale':{'type':'string','minLength':1,'maxLength':240},'uncertainty':{'type':'string','minLength':1,'maxLength':160},"),
 ("'items':{'type':'string'},'minItems':1,'maxItems':3", "'items':{'type':'string','minLength':1,'maxLength':100},'minItems':1,'maxItems':3"),
 ("'items':{'type':'string'},'minItems':1,'maxItems':5", "'items':{'type':'string','minLength':1,'maxLength':24},'minItems':1,'maxItems':5"),
 ("'case_id':{'type':'string'}", "'case_id':{'type':'string','pattern':'^K[a-f0-9]{12}$'}"),
 ("Use one short sentence for rationale and uncertainty and short next actions.", "Keep rationale at most 240 characters, uncertainty at most 160 characters, and each next action at most 100 characters. The grammar enforces these length limits, not correctness.")]
for a,b in changes:
 assert s.count(a)==1,(a,s.count(a))
 s=s.replace(a,b)
assert hashlib.sha256(s.encode()).hexdigest()=='c1b88ff20fca49003887f76c1e0c3c7cef8e3b6835d38e31aea94145a5654349'
p.write_text(s)
