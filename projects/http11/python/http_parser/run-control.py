"""Require actual bundled C HTTP parser source coverage on the valid control."""

import json
from pathlib import Path


directory = Path("/coverage")
observed = json.loads((directory / "observed.json").read_text())
expected = {"method": "GET", "target": "/parsarium?x=1", "host": "example.test"}
if observed != expected:
    raise SystemExit(f"control mismatch: {observed}")
files = json.loads((directory / "coverage.json").read_text())["data"][0]["files"]
source = [item for item in files if item["filename"].startswith("/work/source/http_parser/")]
native = [item for item in source if item["filename"].endswith("/http_parser.c")]
binding = [item for item in source if item["filename"].endswith("/parser.c")]
covered = sum(item["summary"]["lines"]["covered"] for item in source)
native_covered = sum(item["summary"]["lines"]["covered"] for item in native)
binding_covered = sum(item["summary"]["lines"]["covered"] for item in binding)
if not source or min(covered, native_covered, binding_covered) <= 0:
    raise SystemExit("no bundled C HTTP parser or binding source lines covered")
summary = {"control_pass": True, "output": observed,
           "parser_source_files": len(source), "parser_source_lines_covered": covered,
           "format_specific_source_lines_covered": native_covered,
           "binding_source_lines_covered": binding_covered,
           "coverage": "/coverage/coverage.json"}
(directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
