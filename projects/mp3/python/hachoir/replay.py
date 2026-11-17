"""Print the parsed frame-header fields for one local MP3 file."""

import json
import sys

sys.path.insert(0, "/work")
from harness import parse_mp3  # noqa: E402

with open(sys.argv[1], "rb") as source:
    print(json.dumps(parse_mp3(source.read())))
