"""One-file external fuzzer entry point; AFL++ and generators supply input paths."""

import sys
from pathlib import Path
from harness import fuzz_one_input

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: fuzz.py FILE")
    else:
        fuzz_one_input(Path(sys.argv[1]).read_bytes())
