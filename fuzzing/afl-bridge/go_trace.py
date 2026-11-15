"""Convert a raw AFL++ case to one Go fuzz corpus entry and report parser blocks."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(2)
    data = Path(sys.argv[1]).read_bytes()
    entry = os.environ["PARSARIUM_FUZZ_ENTRY"]
    prefix = os.environ["PARSARIUM_SUBJECT_PREFIX"]
    with tempfile.TemporaryDirectory(prefix="parsarium-go-") as temporary:
        workspace = Path(temporary)
        corpus = workspace / "testdata" / "fuzz" / entry
        corpus.mkdir(parents=True)
        encoded = "".join(f"\\x{value:02x}" for value in data)
        (corpus / "case").write_text(f'go test fuzz v1\n[]byte("{encoded}")\n')
        profile = workspace / "coverage.txt"
        result = subprocess.run(
            ["/work/harness.test", f"-test.run=^{entry}$",
             f"-test.coverprofile={profile}"],
            cwd=workspace, capture_output=True, text=True, timeout=30,
        )
        if result.returncode:
            raise RuntimeError(result.stdout[-1000:] + result.stderr[-1000:])
        with open(sys.argv[2], "w", encoding="utf-8") as output:
            for line in profile.read_text().splitlines()[1:]:
                fields = line.split()
                if len(fields) == 3 and fields[0].startswith(prefix) and int(fields[2]) > 0:
                    output.write(fields[0] + "\n")


if __name__ == "__main__":
    main()
