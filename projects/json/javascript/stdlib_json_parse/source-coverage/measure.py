"""Replay the standard adapter on the source-built Node.js and count V8 JSON parser source lines.

Runs, each with its own LLVM profile: `node -e 0` (no JSON.parse), the adapter's read and strict UTF-8
decode of the nested-object control without JSON.parse, the nested-object control twice, and the
nested-array control twice. Only deps/v8/src/json/json-parser.cc was compiled with coverage,
so every counter here belongs to that translation unit; lines are reported for json-parser.cc and
json-parser.h. Writes /coverage/summary.json and prints it.
"""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time

NODE = "/opt/node/bin/node"
SOURCE_ROOT = "/work/node-v26.10.0/"
SOURCES = [SOURCE_ROOT + "deps/v8/src/json/json-parser.cc", SOURCE_ROOT + "deps/v8/src/json/json-parser.h"]
OUT = Path("/coverage")
EXPECTED = {
    "/controls/nested-object.json": {"arrays": 3, "booleans": 2, "max_depth": 4, "nulls": 1, "numbers": [-2.5, 1, 1, 2, 2], "objects": 5, "root": "object", "strings": ["café \"quoted\"", "go", "json", "parsarium", "rfc8259"], "top_level_keys": ["enabled", "missing", "name", "nested", "ratio", "tags", "version"]},
    "/controls/nested-array.json": {"arrays": 4, "booleans": 2, "max_depth": 3, "nulls": 1, "numbers": [0.25, 1], "objects": 2, "root": "array", "strings": ["A", "two"], "top_level_items": 5},
}
DECODE_ONLY = ("import { readFile } from 'node:fs/promises';"
               "new TextDecoder('utf-8', { fatal: true }).decode(await readFile('/controls/nested-object.json'));")
RUNS = [
    ("baseline", ["-e", "0"], None),
    ("decode-only", ["--input-type=module", "-e", DECODE_ONLY], None),
    ("object-1", ["/work/adapter.mjs", "/controls/nested-object.json"], "/controls/nested-object.json"),
    ("object-2", ["/work/adapter.mjs", "/controls/nested-object.json"], "/controls/nested-object.json"),
    ("array-1", ["/work/adapter.mjs", "/controls/nested-array.json"], "/controls/nested-array.json"),
    ("array-2", ["/work/adapter.mjs", "/controls/nested-array.json"], "/controls/nested-array.json"),
]


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def run(command, **kwargs):
    return subprocess.run(command, check=True, capture_output=True, text=True, **kwargs).stdout


def lcov(profdata):
    """Map 'file:line' -> execution count, plus executed function names, from an lcov export."""
    lines, functions, current = {}, set(), None
    text = run(["llvm-cov-20", "export", "-format=lcov", NODE, "-instr-profile=" + str(profdata), *SOURCES])
    for line in text.splitlines():
        if line.startswith("SF:"):
            current = Path(line[3:]).name
        elif line.startswith("DA:"):
            number, count = line[3:].split(",")[:2]
            lines[f"{current}:{number}"] = int(count)
        elif line.startswith("FNDA:"):
            count, name = line[5:].split(",", 1)
            if int(count):
                functions.add(name)
    return lines, functions


def fingerprint(items):
    return sha256("\n".join(items).encode()).hexdigest()


def main():
    hashes = dict(line.split()[::-1] for line in Path("/work/source-hashes.txt").read_text().splitlines())
    if digest(NODE) != hashes["/work/node"]:
        raise SystemExit("node binary differs from the build stage")
    for source in SOURCES:
        if digest(source) != hashes[source[len(SOURCE_ROOT):]]:
            raise SystemExit(f"{source} differs from the build stage")
    if digest("/controls/nested-array.json") != digest("/work/second-control.json"):
        raise SystemExit("mounted nested-array control differs from the image copy")
    raw = OUT / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    results = {}
    for name, args, control in RUNS:
        profraw = raw / f"{name}.profraw"
        started = time.monotonic()
        stdout = run([NODE, *args], env={"LLVM_PROFILE_FILE": str(profraw), "PATH": "/usr/bin:/bin"})
        seconds = time.monotonic() - started
        if control is not None and json.loads(stdout) != EXPECTED[control]:
            raise SystemExit(f"{name}: control mismatch {stdout!r}")
        profdata = raw / f"{name}.profdata"
        run(["llvm-profdata-20", "merge", "-sparse", str(profraw), "-o", str(profdata)])
        lines, functions = lcov(profdata)
        results[name] = {"lines": lines, "functions": functions, "seconds": round(seconds, 3),
                         "output": json.loads(stdout) if control else None}

    def covered(name):
        return sorted(key for key, count in results[name]["lines"].items() if count)

    def counts(name):
        return sorted(f"{key}={count}" for key, count in results[name]["lines"].items())

    def per_file(keys):
        return {file: sum(1 for key in keys if key.startswith(file + ":")) for file in ("json-parser.cc", "json-parser.h")}

    scope_lines = sorted(results["baseline"]["lines"])
    object_lines, array_lines = set(covered("object-1")), set(covered("array-1"))
    summary = {
        "feedback_kind": "llvm_source_lines",
        "instrumented_objects": Path("/work/instrumented-objects.txt").read_text().split(),
        "toolchain": Path("/work/toolchain.txt").read_text().splitlines(),
        "node_sha256": digest(NODE),
        "source_sha256": {Path(source).name: digest(source) for source in SOURCES},
        "adapter_sha256": digest("/work/adapter.mjs"),
        "control_sha256": {path: digest(path) for path in EXPECTED},
        "scope_lines": len(scope_lines),
        "scope_lines_by_file": per_file(scope_lines),
        "runs": {name: {"lines_covered": len(covered(name)), "lines_covered_by_file": per_file(covered(name)),
                        "functions_executed": len(result["functions"]), "line_set_sha256": fingerprint(covered(name)),
                        "line_counts_sha256": fingerprint(counts(name)), "seconds": result["seconds"],
                        "output_matches_expected": True if result["output"] is not None else None}
                 for name, result in results.items()},
        "object_repeat_identical_lines": covered("object-1") == covered("object-2"),
        "object_repeat_identical_counts": counts("object-1") == counts("object-2"),
        "array_repeat_identical_lines": covered("array-1") == covered("array-2"),
        "array_repeat_identical_counts": counts("array-1") == counts("array-2"),
        "object_array_lines_differ": object_lines != array_lines,
        "object_only_lines": sorted(object_lines - array_lines, key=lambda key: (key.split(":")[0], int(key.split(":")[1]))),
        "array_only_lines": sorted(array_lines - object_lines, key=lambda key: (key.split(":")[0], int(key.split(":")[1]))),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


main()
