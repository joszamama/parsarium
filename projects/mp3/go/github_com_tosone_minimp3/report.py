"""Replay the valid MP3 control and export Go wrapper and native minimp3 line views."""

import json
import os
from pathlib import Path
import re
import subprocess

C_SOURCE = "/go/pkg/mod/github.com/tosone/minimp3@v1.1.0/minimp3.h"
GO_PREFIX = "github.com/tosone/minimp3/"
COVERAGE_DIR = Path("/coverage")


def command(*args: str, env: dict[str, str] | None = None) -> str:
    run = subprocess.run(args, env=env, text=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, check=True)
    return run.stdout


def go_lines() -> list[dict]:
    files: dict[str, set[int]] = {}
    for line in (COVERAGE_DIR / "raw.cover").read_text().splitlines():
        if not line.startswith(GO_PREFIX):
            continue
        fields = line.split()
        if len(fields) != 3 or fields[2] == "0":
            continue
        location = fields[0]
        filename, span = location.rsplit(":", 1)
        start, end = span.split(",")
        first = int(start.split(".", 1)[0])
        last, end_column = (int(x) for x in end.split("."))
        if end_column == 1 and last > first:
            last -= 1
        if first < 1 or last < first or last - first > 10000:
            raise ValueError(f"invalid Go cover span: {location}")
        files.setdefault(filename, set()).update(range(first, last + 1))
    return [
        {"filename": name, "summary": {"lines": {"covered": len(lines)}},
         "executed_lines": sorted(lines)}
        for name, lines in sorted(files.items())
    ]


def native_lines() -> tuple[dict, int]:
    raw = COVERAGE_DIR / "native.profraw"
    if not raw.is_file() or raw.stat().st_size < 100:
        raise ValueError("C decoder did not emit an LLVM raw profile")
    merged = COVERAGE_DIR / "native.profdata"
    command("llvm-profdata", "merge", "-sparse", str(raw), "-o", str(merged))
    profile = f"-instr-profile={merged}"
    shown = command("llvm-cov", "show", "/work/harness.test", profile, C_SOURCE)
    lines = set()
    for line in shown.splitlines():
        match = re.match(r"^\s*(\d+)\|\s*([0-9.]+[kM]?)\|", line)
        if match and float(match.group(2).rstrip("kM")) > 0:
            lines.add(int(match.group(1)))
    exported = json.loads(command("llvm-cov", "export", "/work/harness.test", profile))
    source, = [file for file in exported["data"][0]["files"]
               if file["filename"] == C_SOURCE]
    official_count = source["summary"]["lines"]["covered"]
    if not lines or official_count < 100:
        raise ValueError("native minimp3 source coverage is absent")
    return ({"filename": C_SOURCE, "summary": {"lines": {"covered": len(lines)}},
             "executed_lines": sorted(lines)}, official_count)


def main() -> None:
    env = dict(os.environ)
    env["LLVM_PROFILE_FILE"] = str(COVERAGE_DIR / "native.profraw")
    replay = command("/work/harness.test", "-test.run=^TestControl$", "-test.v",
                     f"-test.coverprofile={COVERAGE_DIR / 'raw.cover'}", env=env)
    outputs = [json.loads(line.removeprefix("OBSERVED_JSON:"))
               for line in replay.splitlines() if line.startswith("OBSERVED_JSON:")]
    if len(outputs) != 1:
        raise ValueError(f"valid control produced {len(outputs)} parsed outputs: {replay[-500:]}")
    go_files = go_lines()
    native_file, llvm_count = native_lines()
    if not go_files or not any(file["filename"].endswith("/decode.go") for file in go_files):
        raise ValueError("Go binding source coverage is absent")
    coverage = {"data": [{"files": go_files + [native_file]}]}
    summary = {
        "control_pass": True,
        "output": outputs[0],
        "parser_source_files": len(go_files),
        "parser_source_lines_covered": sum(f["summary"]["lines"]["covered"] for f in go_files),
        "underlying_source_files": 1,
        "underlying_source_lines_covered": len(native_file["executed_lines"]),
        "native_llvm_counted_lines_covered": llvm_count,
        "coverage": "/coverage/coverage.json",
    }
    (COVERAGE_DIR / "coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
    (COVERAGE_DIR / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
