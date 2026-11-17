"""Replay the valid MP3 control and export Rust binding and native minimp3 C line views."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys

REGISTRY = "/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f"
RUST_PREFIX = f"{REGISTRY}/minimp3-0.6.1/"
C_SOURCE = f"{REGISTRY}/minimp3-sys-0.6.0/minimp3/minimp3.h"
COVERAGE_DIR = Path("/coverage")


def command(*args: str, env: dict[str, str] | None = None) -> str:
    run = subprocess.run(args, env=env, text=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, check=False)
    if run.returncode:
        raise RuntimeError(f"{args[0]} failed: {run.stderr[-2000:]}")
    return run.stdout


def replay(binary: str, control: str, profile: Path) -> dict:
    env = dict(os.environ, LLVM_PROFILE_FILE=str(profile))
    output = json.loads(command(binary, control, env=env))
    if not profile.is_file() or profile.stat().st_size < 100:
        raise ValueError(f"{binary} did not emit an LLVM raw profile")
    return output


def rust_files(raw: Path) -> list[dict]:
    merged = raw.with_suffix(".profdata")
    command("/work/rust-llvm-profdata", "merge", "-sparse", str(raw), "-o", str(merged))
    exported = json.loads(command("/work/rust-llvm-cov", "export", "/work/replay",
                                  f"-instr-profile={merged}"))
    return exported["data"][0]["files"]


def native_lines(raw: Path) -> tuple[dict, int]:
    merged = raw.with_suffix(".profdata")
    command("llvm-profdata", "merge", "-sparse", str(raw), "-o", str(merged))
    profile = f"-instr-profile={merged}"
    shown = command("llvm-cov", "show", "/work/native-replay", profile, C_SOURCE)
    lines = set()
    for line in shown.splitlines():
        match = re.match(r"^\s*(\d+)\|\s*([0-9.]+[kMG]?)\|", line)
        if match and float(match.group(2).rstrip("kMG")) > 0:
            lines.add(int(match.group(1)))
    exported = json.loads(command("llvm-cov", "export", "/work/native-replay", profile,
                                  "-summary-only"))
    source, = [file for file in exported["data"][0]["files"] if file["filename"] == C_SOURCE]
    official_count = source["summary"]["lines"]["covered"]
    if not lines or official_count < 100:
        raise ValueError("native minimp3 source coverage is absent")
    return ({"filename": C_SOURCE, "summary": {"lines": {"covered": len(lines)}},
             "executed_lines": sorted(lines)}, official_count)


def main() -> None:
    control = sys.argv[1] if len(sys.argv) > 1 else "/input/control"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else COVERAGE_DIR
    rust_output = replay("/work/replay", control, out / "rust.profraw")
    native_output = replay("/work/native-replay", control, out / "native.profraw")
    if rust_output != native_output:
        raise ValueError(f"coverage builds disagree: {rust_output} != {native_output}")
    binding = [file for file in rust_files(out / "rust.profraw")
               if file["filename"].startswith(RUST_PREFIX)]
    if not binding or not any(file["filename"].endswith("/src/lib.rs") for file in binding):
        raise ValueError("minimp3 Rust binding source coverage is absent")
    native_file, llvm_count = native_lines(out / "native.profraw")
    coverage = {"data": [{"files": binding + [native_file]}]}
    summary = {
        "control_pass": True,
        "output": rust_output,
        "parser_source_files": len(binding),
        "parser_source_lines_covered": sum(f["summary"]["lines"]["covered"] for f in binding),
        "underlying_source_files": 1,
        "underlying_source_lines_covered": len(native_file["executed_lines"]),
        "native_llvm_counted_lines_covered": llvm_count,
        "coverage": str(out / "coverage.json"),
    }
    (out / "coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
