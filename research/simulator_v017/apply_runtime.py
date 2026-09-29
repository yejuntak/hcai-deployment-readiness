"""Model-only candidate on the frozen sixteen-case qualification.

Only model/runtime identity and call budget change. Cases, expected labels,
response semantics, behavior profiles, and scoring rules remain unchanged.
"""
from pathlib import Path
import hashlib

p = Path("simulator.py")
text = p.read_text()
assert hashlib.sha256(text.encode()).hexdigest() == "39169cf71fb038c026637fff567744948b081647be86bf2b13d20cea692ce3d5"

changes = {
    "VERSION = '0.1.3'": "VERSION = '0.1.7'",
    "unsloth/Qwen3-4B-Instruct-2507-GGUF": "Qwen/Qwen3-14B-GGUF",
    "a06e946bb6b655725eafa393f4a9745d460374c9": "530227a7d994db8eca5ab5ced2fb692b614357fd",
    "Qwen3-4B-Instruct-2507-Q4_K_M.gguf": "Qwen3-14B-Q4_K_M.gguf",
    "3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597": "500a8806e85ee9c83f3ae08420295592451379b4f8cf2d0f41c15dffeb6b81f0",
    "research-sim-4b-q4": "research-sim-qwen3-14b-q4",
    "timeout=240": "timeout=900",
}
for old, new in changes.items():
    assert old in text, old
    text = text.replace(old, new)
p.write_text(text)
print("SIMULATOR_SHA256", hashlib.sha256(p.read_bytes()).hexdigest())

p = Path("qualification.py")
text = p.read_text()
assert "operational-qualification-v5-defined" in text
text = text.replace("operational-qualification-v5-defined", "operational-qualification-v9-qwen3-14b")
text = text.replace("'call_timeout_seconds':240", "'call_timeout_seconds':900")
p.write_text(text)
print("QUALIFICATION_SHA256", hashlib.sha256(p.read_bytes()).hexdigest())
