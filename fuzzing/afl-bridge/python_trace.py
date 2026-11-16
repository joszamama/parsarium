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
            # CPython freezes zipimport during startup. Its code object keeps
            # the frozen filename even though the matching, pinned source file
            # is present in the runtime image.
            source = (prefix if filename == "<frozen zipimport>" and
                      prefix.endswith("/zipimport.py") else
                      str(Path(filename).resolve()))
            if hits > 0 and source.startswith(prefix):
                output.write(f"{source}:{line}\n")


if __name__ == "__main__":
    main()
