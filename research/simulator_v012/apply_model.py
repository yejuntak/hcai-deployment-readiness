"""Versioned model/resource change. No semantic choice or answer is rewritten."""
from pathlib import Path
import hashlib
p=Path('simulator.py');s=p.read_text()
assert hashlib.sha256(p.read_bytes()).hexdigest()=='c1b88ff20fca49003887f76c1e0c3c7cef8e3b6835d38e31aea94145a5654349'
for a,b in [
 ("VERSION = '0.1.1'","VERSION = '0.1.2'"),
 ('unsloth/Qwen3-4B-Instruct-2507-GGUF','Qwen/Qwen3-8B-GGUF'),
 ('a06e946bb6b655725eafa393f4a9745d460374c9','7c41481f57cb95916b40956ab2f0b139b296d974'),
 ('Qwen3-4B-Instruct-2507-Q4_K_M.gguf','Qwen3-8B-Q4_K_M.gguf'),
 ('3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597','d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785'),
 ('research-sim-4b-q4','research-sim-8b-q4'),('timeout=240','timeout=600')]:
 assert a in s,a
 s=s.replace(a,b)
assert hashlib.sha256(s.encode()).hexdigest()=='a0a49cc8ba06ee45a9c609758dfdaddf5fce0d4402fab79093db02ba1162e757'
p.write_text(s)
p=Path('qualification.py');s=p.read_text().replace("'version':'operational-qualification-v3-bounded'","'version':'operational-qualification-v4-8B'").replace("'call_timeout_seconds':240","'call_timeout_seconds':600").replace("'prior_version_result':'v010:2 of 8 operational cases passed; six length truncations preserved'", "'prior_version_result':'v010: six length truncations; v011: transfer-case mixed failure misclassified. Both historical results preserved.'")
p.write_text(s)
