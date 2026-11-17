"""Replay the untagged MP3 control and count executed TinyTag package lines."""

import json
from pathlib import Path
import trace

import tinytag

from harness import ID3_LINES, MPEG_LINES, parse_mp3


data = Path("/input/control").read_bytes()
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(parse_mp3, data)
expected = {"sample_rate": 44100, "channels": 1, "bitrate_kbps": 64.0,
            "duration_us": 287347}
if observed != expected:
    raise SystemExit(f"control mismatch: {observed}")
source_root = str(Path(tinytag.__file__).resolve().parent) + "/"
executed_by_file = {}
for (filename, line), count in tracer.results().counts.items():
    source = str(Path(filename).resolve())
    if source.startswith(source_root) and count > 0:
        executed_by_file.setdefault(source, set()).add(line)
module_lines = executed_by_file.get(source_root + "tinytag.py", set())
mpeg_lines = sorted(line for line in module_lines if line in MPEG_LINES)
id3_lines = sorted(line for line in module_lines if line in ID3_LINES)
# Selection gate: the untagged control must reach the frame-header walker,
# not only magic-byte dispatch or the ID3 reader.
if not mpeg_lines or id3_lines:
    raise SystemExit(f"_MPEG lines {len(mpeg_lines)}, _ID3 lines {len(id3_lines)}")
files = [{"filename": source,
          "summary": {"lines": {"covered": len(lines)}},
          "executed_lines": sorted(lines)}
         for source, lines in sorted(executed_by_file.items())]
coverage = {"data": [{"files": files}]}
output = Path("/coverage")
output.mkdir(exist_ok=True)
(output / "observed.json").write_text(json.dumps(observed, indent=2) + "\n")
(output / "coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
summary = {"control_pass": True, "output": observed,
           "parser_source_files": len(files),
           "parser_source_lines_covered": sum(len(lines) for lines in executed_by_file.values()),
           "mpeg_class_lines": [MPEG_LINES.start, MPEG_LINES.stop - 1],
           "mpeg_frame_parser_lines_covered": len(mpeg_lines),
           "id3_lines_covered": len(id3_lines),
           "coverage": "/coverage/coverage.json"}
(output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
