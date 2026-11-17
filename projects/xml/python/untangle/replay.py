import json
import sys
from harness import parse_xml
print(json.dumps(parse_xml(sys.argv[1]), ensure_ascii=False))
