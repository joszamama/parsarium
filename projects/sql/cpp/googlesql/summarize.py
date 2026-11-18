"""Print the oracle summary of one local SQL file from the GoogleSQL parser AST.

/work/replay walks the AST that googlesql::ParseNextStatement returns for each statement and
prints the summary as one JSON line; this script runs it with the coverage profile kept
out of the working directory, or re-reads a saved line (--tree).
"""
import json
import os
import subprocess
import sys


def summary_of(path):
    environment = {**os.environ, "LLVM_PROFILE_FILE": "/tmp/summary-%p.profraw"}
    output = subprocess.run(["/work/replay", path], check=True, capture_output=True,
                            text=True, env=environment).stdout
    return json.loads(output.strip().splitlines()[-1])


if __name__ == "__main__":
    if sys.argv[1] == "--tree":
        with open(sys.argv[2], encoding="utf-8") as handle:
            print(json.dumps(json.loads(handle.read().strip().splitlines()[-1])))
    else:
        print(json.dumps(summary_of(sys.argv[1])))
