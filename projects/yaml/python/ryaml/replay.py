import json
import sys
from pathlib import Path
from harness import parse_yaml
print(json.dumps(parse_yaml(Path(sys.argv[1]).read_bytes()), ensure_ascii=False))
