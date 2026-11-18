import json
import sys
from pathlib import Path
from harness import parse_dns
print(json.dumps(parse_dns(Path(sys.argv[1]).read_bytes()), ensure_ascii=False))
