"""Compare two fixed valid JSON controls through the standard API AFL overlay."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
IMAGE = "parsarium-afl/json-python-stdlib_json:local"
INPUTS = {"control": ROOT / "controls/json/structure.json",
          "variant": ROOT / "controls/json/one-item.json"}


def run(args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1500:])


def main():
    receipt = json.loads((ROOT / "fuzzing/afl-native/json/python/stdlib_json/verification.json").read_text())
    if not receipt.get("pass") or receipt.get("feedback_kind") != "python_parser_source_lines_to_afl_bitmap":
        raise ValueError("no verified CPython json source-line AFL overlay")
    results = {}
    with tempfile.TemporaryDirectory(prefix="parsarium-json-stdlib-feedback-") as scratch:
        for label, source in INPUTS.items():
            mounted = ["docker", "run", "--rm", "--platform", "linux/amd64", "--network", "none",
                       "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
                       "--user", f"{os.getuid()}:{os.getgid()}",
                       "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
                       "-v", f"{source}:/input/case:ro", "-v", f"{scratch}:/coverage"]
            features = Path(scratch) / f"{label}-features.txt"
            edges = Path(scratch) / f"{label}-edges.txt"
            run([*mounted, "--entrypoint", "/bin/sh", IMAGE,
                 "/work/afl_trace", "/input/case", f"/coverage/{features.name}"])
            run([*mounted, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap", IMAGE,
                 "-m", "none", "-t", "120000", "-o", f"/coverage/{edges.name}", "--",
                 "/work/afl_proxy", "/input/case"])
            results[label] = {"sha256": sha256(source.read_bytes()).hexdigest(),
                              "features": set(features.read_text().splitlines()),
                              "edges": {line.split(":", 1)[0] for line in edges.read_text().splitlines()}}
    for label in results:
        if not results[label]["features"] or not results[label]["edges"]:
            raise ValueError(f"empty parser-source feedback on {label}")
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "project": "json/python/stdlib_json",
              "method": "afl_trace and afl-showmap on exactly two fixed valid JSON controls",
              "feedback_scope": "CPython pure-Python json package source lines; built-in _json excluded",
              "control_sha256": results["control"]["sha256"],
              "variant_sha256": results["variant"]["sha256"],
              "control_parser_features": len(results["control"]["features"]),
              "variant_parser_features": len(results["variant"]["features"]),
              "parser_feature_symmetric_difference": len(results["control"]["features"] ^ results["variant"]["features"]),
              "control_afl_edge_ids": len(results["control"]["edges"]),
              "variant_afl_edge_ids": len(results["variant"]["edges"]),
              "afl_edge_id_symmetric_difference": len(results["control"]["edges"] ^ results["variant"]["edges"]),
              "pass": True}
    destination = ROOT / "data/python/json/stdlib-valid-variant-feedback.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
