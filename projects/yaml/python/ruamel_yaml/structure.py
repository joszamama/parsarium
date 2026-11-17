"""Print the typed YAML tree for one local file through one input mode (bytes, str or stream).

The verify script compares every mode with the hand-written trees in controls/yaml/check_controls.py.
"""
import json
import sys
from pathlib import Path

from harness import parse_yaml


def main() -> None:
    mode, path = sys.argv[1], Path(sys.argv[2])
    report = parse_yaml(path.read_bytes(), mode)
    report['mode'] = mode
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
