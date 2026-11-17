"""Replay the valid DNS response control through dns_messages.DnsMessage.from_bytes and trace dns-messages source."""

import json
from pathlib import Path
import trace

import dns_messages
import harness

EXPECTED = json.loads("""
{"id": 43981, "qr": 1, "opcode": 0, "aa": 0, "tc": 0, "rd": 1, "ra": 1, "z": 0, "rcode": 0,
 "qdcount": 1, "ancount": 4, "nscount": 0, "arcount": 0,
 "questions": [{"name": "www.example.test.", "type": 1, "class": 1}],
 "answers": [
  {"name": "www.example.test.", "type": 5, "class": 1, "ttl": 3600, "rdata": "example.test."},
  {"name": "example.test.", "type": 1, "class": 1, "ttl": 300, "rdata": "192.0.2.10"},
  {"name": "example.test.", "type": 28, "class": 1, "ttl": 600, "rdata": "2001:db8::10"},
  {"name": "example.test.", "type": 15, "class": 1, "ttl": 7200, "rdata": "10 mail.example.test."}],
 "authority": [], "additional": []}
""")

data = Path("/input/control").read_bytes()
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(harness.parse_dns, data)
if observed != EXPECTED:
    raise SystemExit(f"control mismatch: {observed}")
source_root = Path(dns_messages.__file__).resolve().parent
files = []
for source in sorted(source_root.rglob("*.py")):
    executed = sorted({line for (filename, line), count in tracer.results().counts.items()
                       if Path(filename).resolve() == source and count > 0})
    if executed:
        files.append({"filename": str(source), "summary": {"lines": {"covered": len(executed)}},
                      "executed_lines": executed})
for required in ("/dns_messages/dns_objects/dns_message_parser.py", "/dns_messages/utilities/name_encoder_and_decoder.py"):
    if not any(f["filename"].endswith(required) for f in files):
        raise SystemExit(f"{required} had no executed source lines")
output = Path("/coverage")
output.mkdir(exist_ok=True)
(output / "observed.json").write_text(json.dumps(observed, indent=2) + "\n")
(output / "coverage.json").write_text(json.dumps({"data": [{"files": files}]}, indent=2) + "\n")
summary = {"control_pass": True, "output": observed,
           "parser_source_files": len(files),
           "parser_source_lines_covered": sum(f["summary"]["lines"]["covered"] for f in files),
           "format_specific_source_lines_covered": sum(
               f["summary"]["lines"]["covered"] for f in files if f["filename"].endswith("/dns_messages/dns_objects/dns_message_parser.py")),
           "coverage": "/coverage/coverage.json"}
(output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
