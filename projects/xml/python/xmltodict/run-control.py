"""Replay the control and export Python wrapper plus Expat source coverage."""

import json
import os
from pathlib import Path
import subprocess
import sys
import trace


CONFIG = json.loads(Path("/work/target.json").read_text())
OUT = Path("/coverage")


def child() -> None:
    from harness import parse_xml

    data = Path("/input/control").read_bytes()
    tracer = trace.Trace(count=True, trace=False)
    observed = tracer.runfunc(parse_xml, data)
    if observed != CONFIG["expected_output"]:
        raise SystemExit(f"control mismatch: {observed}")
    covered = {}
    for (filename, line), hits in tracer.results().counts.items():
        source = str(Path(filename).resolve())
        if hits > 0 and source.startswith(CONFIG["trace_subject_prefix"]):
            covered.setdefault(source, set()).add(line)
    files = [{"filename": source, "summary": {"lines": {"covered": len(lines)}},
              "executed_lines": sorted(lines)}
             for source, lines in sorted(covered.items())]
    if not files:
        raise SystemExit("no Python XML API source lines covered")
    OUT.mkdir(exist_ok=True)
    (OUT / "observed.json").write_text(json.dumps(observed, indent=2) + "\n")
    (OUT / "python-files.json").write_text(json.dumps(files, indent=2) + "\n")


def parent() -> None:
    OUT.mkdir(exist_ok=True)
    env = {**os.environ, "LLVM_PROFILE_FILE": str(OUT / "control.profraw")}
    subprocess.run([sys.executable, "/work/run-control.py", "--child"], env=env, check=True)
    subprocess.run(["llvm-profdata", "merge", str(OUT / "control.profraw"),
                    "-o", str(OUT / "control.profdata")], check=True)
    report = subprocess.run(["llvm-cov", "export", CONFIG["native_module"],
                             f"-instr-profile={OUT / 'control.profdata'}"],
                            capture_output=True, text=True, check=True)
    native = [f for f in json.loads(report.stdout)["data"][0]["files"]
              if f["filename"].startswith(CONFIG["native_subject_prefix"])]
    if not any(f["filename"].endswith(CONFIG["native_parser_file_suffix"])
               and f["summary"]["lines"]["covered"] > 0 for f in native):
        raise SystemExit("no Expat XML parser source lines covered")
    python_files = json.loads((OUT / "python-files.json").read_text())
    observed = json.loads((OUT / "observed.json").read_text())
    coverage = {"data": [{"files": python_files + native}]}
    (OUT / "coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
    summary = {"control_pass": True, "output": observed,
               "parser_source_files": len(python_files),
               "parser_source_lines_covered": sum(f["summary"]["lines"]["covered"] for f in python_files),
               "underlying_source_files": len(native),
               "underlying_source_lines_covered": sum(f["summary"]["lines"]["covered"] for f in native),
               "coverage": "/coverage/coverage.json"}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    child() if sys.argv[1:] == ["--child"] else parent()
