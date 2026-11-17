"""Replay the valid YAML control through srsly.yaml_loads and trace srsly and the ruamel.yaml parser source."""

import json
from pathlib import Path
import trace

import harness


SITE = Path("/opt/venv/lib/python3.14/site-packages")
OWN = SITE / "srsly"
UNDERLYING = SITE / "ruamel/yaml"

data = Path("/input/control").read_bytes()
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(harness.parse_yaml, data)
expected = json.loads(Path("/work/expected.json").read_text(encoding="utf-8"))
if observed != expected:
    raise SystemExit(f"control mismatch: {observed}")
counts = tracer.results().counts


def executed(root: Path) -> list[dict]:
    files = []
    for source in sorted(root.glob("*.py")):
        lines = sorted({line for (filename, line), count in counts.items()
                        if Path(filename).resolve() == source and count > 0})
        if lines:
            files.append({"filename": str(source), "summary": {"lines": {"covered": len(lines)}},
                          "executed_lines": lines})
    return files


own = executed(OWN)
underlying = executed(UNDERLYING)
if not any(f["filename"].endswith("/srsly/_yaml_api.py") for f in own):
    raise SystemExit("srsly/_yaml_api.py had no executed source lines")
for required in ("scanner.py", "parser.py"):
    if not any(f["filename"].endswith("/ruamel/yaml/" + required) for f in underlying):
        raise SystemExit(f"ruamel.yaml {required} had no executed source lines")
output = Path("/coverage")
output.mkdir(exist_ok=True)
(output / "observed.json").write_text(json.dumps(observed, indent=2, ensure_ascii=False) + "\n")
(output / "coverage.json").write_text(json.dumps({"data": [{"files": own + underlying}]}, indent=2) + "\n")
summary = {"control_pass": True, "output": observed,
           "parser_source_files": len(own),
           "parser_source_lines_covered": sum(f["summary"]["lines"]["covered"] for f in own),
           "underlying_source_files": len(underlying),
           "underlying_source_lines_covered": sum(f["summary"]["lines"]["covered"] for f in underlying),
           "coverage": "/coverage/coverage.json"}
(output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(summary, ensure_ascii=False))
