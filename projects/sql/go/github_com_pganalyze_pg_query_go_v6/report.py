"""Replay pg_query_go and export Go binding lines and native libpg_query C source lines separately."""

import json
import os
from pathlib import Path
import re
import subprocess

OUT = Path("/coverage")
GO_PREFIX = "github.com/pganalyze/pg_query_go/v6/"
NATIVE_PREFIX = "/work/thirdparty/parser/"
TEST = "/work/harness.test"


def run(*args: str, env=None) -> str:
    result = subprocess.run(args, env=env, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed: {(result.stdout + result.stderr)[-1200:]}")
    return result.stdout


def go_lines() -> list[dict]:
    files: dict[str, set[int]] = {}
    for line in (OUT / "raw.cover").read_text().splitlines():
        if not line.startswith(GO_PREFIX):
            continue
        fields = line.split()
        if len(fields) != 3 or fields[2] == "0":
            continue
        filename, span = fields[0].rsplit(":", 1)
        start, end = span.split(",")
        first = int(start.split(".", 1)[0])
        last, last_column = (int(value) for value in end.split("."))
        if last_column == 1 and last > first:
            last -= 1
        if first < 1 or last < first or last - first > 10000:
            raise ValueError(f"invalid Go cover span: {fields[0]}")
        files.setdefault(filename, set()).update(range(first, last + 1))
    return [
        {"filename": name, "summary": {"lines": {"covered": len(lines)}},
         "executed_lines": sorted(lines)}
        for name, lines in sorted(files.items()) if lines
    ]


def native_lines() -> list[dict]:
    raw = OUT / "native.profraw"
    if not raw.is_file() or raw.stat().st_size < 100:
        raise ValueError("libpg_query emitted no LLVM profile")
    merged = OUT / "native.profdata"
    run("llvm-profdata", "merge", "-sparse", str(raw), "-o", str(merged))
    profile = f"-instr-profile={merged}"
    exported = json.loads(run("llvm-cov", "export", "-summary-only", TEST, profile))
    official = {entry["filename"]: entry["summary"]["lines"]["covered"]
                for entry in exported["data"][0]["files"]
                if entry["filename"].startswith(NATIVE_PREFIX)}
    result = []
    for source in sorted(name for name, covered in official.items() if covered > 0):
        shown = run("llvm-cov", "show", TEST, profile, source)
        lines = set()
        for line in shown.splitlines():
            match = re.match(r"^\s*(\d+)\|\s*([0-9.]+[kMG]?)\|", line)
            if match and float(match.group(2).rstrip("kMG")) > 0:
                lines.add(int(match.group(1)))
        if lines:
            result.append({"filename": source,
                           "summary": {"lines": {"covered": len(lines)}},
                           "executed_lines": sorted(lines),
                           "llvm_official_lines_covered": official[source]})
    return result


def main() -> None:
    env = dict(os.environ, LLVM_PROFILE_FILE=str(OUT / "native.profraw"))
    output = run(TEST, "-test.run=^TestControl$", "-test.v", "-test.coverprofile=/coverage/raw.cover", env=env)
    observed = None
    for line in output.splitlines():
        if line.startswith("OBSERVED_JSON:"):
            observed = json.loads(line.removeprefix("OBSERVED_JSON:"))
    if observed is None:
        raise ValueError("control replay emitted no parsed result")
    own = go_lines()
    native = native_lines()
    gram = [item for item in native if item["filename"].endswith("/src_backend_parser_gram.c")]
    if not own:
        raise ValueError("pg_query_go Go binding source uncovered")
    if not gram or gram[0]["summary"]["lines"]["covered"] < 100:
        raise ValueError("libpg_query grammar source uncovered")
    summary = {
        "control_pass": True, "output": observed,
        "parser_source_files": len(own),
        "parser_source_lines_covered": sum(item["summary"]["lines"]["covered"] for item in own),
        "underlying_source_files": len(native),
        "underlying_source_lines_covered": sum(item["summary"]["lines"]["covered"] for item in native),
        "coverage": "/coverage/coverage.json",
    }
    (OUT / "coverage.json").write_text(json.dumps({"data": [{"files": own + native}]}, indent=2) + "\n")
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
