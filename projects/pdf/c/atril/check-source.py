"""Check pinned Atril and Poppler source members against the project source lock."""

from hashlib import sha256
import json
from pathlib import Path
import sys

lock = json.loads(Path(sys.argv[1]).read_text())
for name, source in (("atril", sys.argv[2]), ("poppler-glib", sys.argv[3])):
    members = lock[name]["source_members"]
    for member, expected in members.items():
        actual = sha256((Path(source) / member).read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f"{name} source member mismatch: {member}: {actual}")
    print(f"{len(members)} {name} source members verified")
