"""Read one local request file and emit parsed method, target, and Host."""

import json
from pathlib import Path
import sys

from harness import parse_data


if len(sys.argv) != 2 or not Path(sys.argv[1]).is_file():
    raise SystemExit("usage: replay.py LOCAL_REQUEST_FILE")
observed = parse_data(Path(sys.argv[1]).read_bytes())
if observed is None:
    raise SystemExit("request head was not parsed")
print(json.dumps(observed))
