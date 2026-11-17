import json
import sys
from pathlib import Path
from harness import parse_sql
print(json.dumps(parse_sql(Path(sys.argv[1]).read_bytes()), ensure_ascii=False))
