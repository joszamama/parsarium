"""Run one existing Python harness input and emit executed parser source lines."""

import os
from pathlib import Path
import sys
import trace

from harness import fuzz_one_input


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(2)
    data = Path(sys.argv[1]).read_bytes()
    tracer = trace.Trace(count=True, trace=False)
    tracer.runfunc(fuzz_one_input, data)
    prefix = os.environ["PARSARIUM_SUBJECT_PREFIX"]
    with open(sys.argv[2], "w", encoding="utf-8") as output:
        for (filename, line), hits in sorted(tracer.results().counts.items()):
            if hits > 0 and str(Path(filename).resolve()).startswith(prefix):
                output.write(f"{filename}:{line}\n")


if __name__ == "__main__":
    main()
