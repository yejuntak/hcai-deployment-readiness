"""Model-only development candidate; no change to cases, keys or decision rules.

This does not incorporate the unexecuted output-order grammar proposal.
"""
from pathlib import Path
import hashlib
p=Path('simulator.py');text=p.read_text()
assert hashlib.sha256(text.encode()).hexdigest()=='39169cf71fb038c026637fff567744948b081647be86bf2b13d20cea692ce3d5'
changes={"VERSION = '0.1.3'":"VERSION = '0.1.6'",'unsloth/Qwen3-4B-Instruct-2507-GGUF':'unsloth/Qwen3.5-9B-GGUF','a06e946bb6b655725eafa393f4a9745d460374c9':'3885219b6810b007914f3a7950a8d1b469d598a5','Qwen3-4B-Instruct-2507-Q4_K_M.gguf':'Qwen3.5-9B-Q4_K_M.gguf','3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597':'03b74727a860a56338e042c4420bb3f04b2fec5734175f4cb9fa853daf52b7e8','research-sim-4b-q4':'research-sim-35-9b-q4','timeout=240':'timeout=600'}
for old,new in changes.items():
 assert old in text,old
 text=text.replace(old,new)
p.write_text(text)
print('SIMULATOR_SHA256',hashlib.sha256(p.read_bytes()).hexdigest())
p=Path('qualification.py');text=p.read_text().replace('operational-qualification-v5-defined','operational-qualification-v8-modern-runtime').replace("'call_timeout_seconds':240","'call_timeout_seconds':600")
p.write_text(text)
