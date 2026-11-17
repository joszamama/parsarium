import json
import sys
from pathlib import Path
from harness import parse_xml
print(json.dumps(parse_xml(Path(sys.argv[1]).read_bytes()), ensure_ascii=False))
