import json
import sys
from pathlib import Path
from harness import parse_toml
print(json.dumps(parse_toml(Path(sys.argv[1]).read_bytes()), ensure_ascii=False, sort_keys=True))
