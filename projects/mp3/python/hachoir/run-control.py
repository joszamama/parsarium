"""Replay the untagged MP3 control and count executed hachoir package lines."""

import json
from pathlib import Path
import trace

import hachoir

from harness import parse_mp3


data = Path("/input/control").read_bytes()
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(parse_mp3, data)
expected = {"version": "1", "layer": "III", "sample_rate": 44100, "bitrate": 64000,
            "channel_mode": "Single channel", "channels": 1, "frames": 11,
            "frame_bytes": 2298}
if observed != expected:
    raise SystemExit(f"control mismatch: {observed}")
source_root = str(Path(hachoir.__file__).resolve().parent) + "/"
executed_by_file = {}
for (filename, line), count in tracer.results().counts.items():
    source = str(Path(filename).resolve())
    if source.startswith(source_root) and count > 0:
        executed_by_file.setdefault(source, set()).add(line)
mpeg_lines = executed_by_file.get(source_root + "parser/audio/mpeg_audio.py", set())
id3_lines = executed_by_file.get(source_root + "parser/audio/id3.py", set())
# Selection gate: the untagged control must reach the frame walker in
# mpeg_audio.py, not only the generic field framework or the ID3 parser.
if not mpeg_lines or id3_lines:
    raise SystemExit(f"mpeg_audio.py lines {len(mpeg_lines)}, id3.py lines {len(id3_lines)}")
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
           "mpeg_audio_lines_covered": len(mpeg_lines),
           "id3_lines_covered": len(id3_lines),
           "coverage": "/coverage/coverage.json"}
(output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
