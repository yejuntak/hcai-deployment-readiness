"""Change only the declared model/resource identity, not response semantics."""
from pathlib import Path
import hashlib
p=Path('simulator.py');t=p.read_text()
assert hashlib.sha256(t.encode()).hexdigest()=='39169cf71fb038c026637fff567744948b081647be86bf2b13d20cea692ce3d5'
changes={"VERSION = '0.1.3'": "VERSION = '0.1.5'", 'unsloth/Qwen3-4B-Instruct-2507-GGUF': 'Qwen/Qwen2.5-7B-Instruct-GGUF', 'a06e946bb6b655725eafa393f4a9745d460374c9': 'bb5d59e06d9551d752d08b292a50eb208b07ab1f', 'Qwen3-4B-Instruct-2507-Q4_K_M.gguf': 'qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf', '3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597': 'dfce12e3862a5283ccfb88221b48480e58745165de856439950d0f22590580db', 'research-sim-4b-q4': 'research-sim-7b-q4', 'timeout=240': 'timeout=600'}
for a,b in changes.items():
 assert a in t,a
 t=t.replace(a,b)
assert hashlib.sha256(t.encode()).hexdigest()=='9e150351ade8f224e10ee8f02d4a7be968b88cb107f69a20f4c5a8fe70531a15'
p.write_text(t)
p=Path('qualification.py');t=p.read_text().replace('operational-qualification-v5-defined','operational-qualification-v7-runtime').replace("'call_timeout_seconds':240","'call_timeout_seconds':600")
p.write_text(t)
