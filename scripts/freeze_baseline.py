"""One-time, non-overwriting capture of the inspected historical checkout."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "24ad1e1b23e4bd81fa19be3c7ecb834887139575"
TARGET = ROOT / "historical" / "rc3-baseline"


def main():
    if TARGET.exists():
        raise SystemExit("Baseline already exists; refusing to overwrite")
    TARGET.mkdir(parents=True)
    paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", COMMIT], cwd=ROOT).decode().splitlines()
    hashes = {}
    for name in paths:
        data = subprocess.check_output(["git", "show", f"{COMMIT}:{name}"], cwd=ROOT)
        dest = TARGET / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        hashes[name] = hashlib.sha256(data).hexdigest()
    archive = Path("/Users/petertak/Documents/ChatGPT/NIW/outputs/Zenodo-Ready-v0.1-rc.3")
    expected = {
        "HCAI-Deployment-Readiness-v0.1-rc.3.zip": "d0b396c72e6467997d6f18edcb1e56ab48a6fb237e6fbaa7293c1b83d2f78a43",
        "Protocol-v0.1-rc.3.pdf": "632ff0335816bba34083aa05bed5f223f0168a64237d596a8eed7043033f4fcb",
    }
    for name, digest in expected.items():
        source = archive / name
        if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
            raise SystemExit(f"Source archive changed: {name}")
        (TARGET / "archived-release").mkdir(exist_ok=True)
        shutil.copyfile(source, TARGET / "archived-release" / name)
        hashes[f"archived-release/{name}"] = digest
    tags = {}
    for tag in ("v0.1-rc.1", "v0.1-rc.2", "agent-tools-v0.1.0", "skill-v0.1.1"):
        tags[tag] = subprocess.check_output(["git", "rev-parse", f"{tag}^{{commit}}"], cwd=ROOT).decode().strip()
    manifest = {"captured_on": "2026-09-24", "source_commit": COMMIT,
                "protocol_version": "0.1-rc.3", "mcp_version": "0.1.0", "skill_version": "0.1.1",
                "historical_tags": tags, "rc3_git_tag_existed": False,
                "note": "Public rc.3 has a DOI/archive, but no rc.3 Git tag was found. Do not invent or move tags. Snapshot includes later companion software and NIST submission copy; archived-release preserves the separate rc.3 distribution.",
                "files": hashes}
    (ROOT / "historical" / "baseline-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Frozen {len(hashes)} historical files at {COMMIT}")


if __name__ == "__main__":
    main()
