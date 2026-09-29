"""Model-only candidate on the frozen sixteen-case qualification.

Only model/runtime identity and call budget change. Cases, expected labels,
response semantics, behavior profiles, and scoring rules remain unchanged.
"""
from pathlib import Path
import hashlib

p=Path("simulator.py"); text=p.read_text()
assert hashlib.sha256(text.encode()).hexdigest()=="39169cf71fb038c026637fff567744948b081647be86bf2b13d20cea692ce3d5"
changes={
 "VERSION = '0.1.3'":"VERSION = '0.1.8'",
 "unsloth/Qwen3-4B-Instruct-2507-GGUF":"Qwen/Qwen2.5-14B-Instruct-GGUF",
 "a06e946bb6b655725eafa393f4a9745d460374c9":"2b6a96d780143b4e8e3b970394e39e3774551f29",
 "Qwen3-4B-Instruct-2507-Q4_K_M.gguf":"qwen2.5-14b-instruct-q4_k_m-00001-of-00003.gguf",
 "3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597":"a09ea5e7b1eafb1b30b241726c3cc3c905c96f14ad41e246ffa5f44e53904f68",
 "research-sim-4b-q4":"research-sim-qwen25-14b-q4",
 "timeout=240":"timeout=900",
}
for old,new in changes.items():
 assert old in text,old
 text=text.replace(old,new)
p.write_text(text)
print("SIMULATOR_SHA256",hashlib.sha256(p.read_bytes()).hexdigest())

p=Path("qualification.py"); text=p.read_text()
assert "operational-qualification-v5-defined" in text
text=text.replace("operational-qualification-v5-defined","operational-qualification-v10-qwen25-14b")
text=text.replace("'call_timeout_seconds':240","'call_timeout_seconds':900")
p.write_text(text)
print("QUALIFICATION_SHA256",hashlib.sha256(p.read_bytes()).hexdigest())
