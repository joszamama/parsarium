"""Trace one local input through a project's Python parser harness.

Mounted read-only into the verified control image by queue_coverage.py. This
module does not import Atheris or start a fuzz campaign.
"""

import importlib
import json
from pathlib import Path
import sys
import trace


def main() -> None:
    case, output, prefixes_json = sys.argv[1:]
    prefixes = json.loads(prefixes_json)
    if not isinstance(prefixes, list) or not prefixes or any(
            not isinstance(prefix, str) or not prefix.startswith("/") for prefix in prefixes):
        raise ValueError("expected absolute parser source prefixes")
    sys.path.insert(0, "/work")
    harness = importlib.import_module("harness")
    data = Path(case).read_bytes()
    tracer = trace.Trace(count=True, trace=False)
    outcome = "ok"
    try:
        tracer.runfunc(harness.fuzz_one_input, data)
    except Exception as error:
        # The campaign target may let a parser exception escape. Preserve
        # coverage from the path taken without treating it as a valid control.
        outcome = f"exception:{type(error).__name__}"
    files = {}
    for (filename, line), count in tracer.results().counts.items():
        if count > 0 and line > 0 and any(filename.startswith(prefix) for prefix in prefixes):
            files.setdefault(filename, set()).add(line)
    record = {"outcome": outcome, "files": [
        {"filename": name, "executed_lines": sorted(lines)}
        for name, lines in sorted(files.items())]}
    Path(output).write_text(json.dumps(record, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
