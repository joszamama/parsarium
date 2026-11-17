"""Check key JUCE SVG parser source members against the project source lock."""

from hashlib import sha256
import json
from pathlib import Path
import sys

lock = json.loads(Path(sys.argv[1]).read_text())["juce"]
source = Path(sys.argv[2])
for member, expected in lock["source_members"].items():
    actual = sha256((source / member).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"source member mismatch: {member}: {actual}")
print(f"{len(lock['source_members'])} JUCE source members verified")
