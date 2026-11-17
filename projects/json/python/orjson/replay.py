import json
import sys
from pathlib import Path
from harness import parse_json

print(json.dumps(parse_json(Path(sys.argv[1]).read_bytes()), ensure_ascii=False))
