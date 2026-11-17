"""Run Node's standard JSON.parse path on the JSON pilot controls in the pinned Node image.

The adapter decodes local bytes with a strict UTF-8 TextDecoder and passes the
string to JSON.parse. V8 implements JSON.parse natively, so this receipt records
the control result only; it makes no parser source-line or AFL++ feedback claim.
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
import subprocess

from run_case import ROOT


IMAGE = "node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47"
PLATFORM = "linux/arm64"
ADAPTER = "adapters/javascript/json_node.mjs"
API = "JSON.parse(text) after new TextDecoder('utf-8', {fatal: true}).decode(Buffer)"
MANIFEST = ROOT / "projects/json/javascript/stream_json/manifest.json"
REPORT = ROOT / "data/javascript/json/standard-receipt.json"


def node(*arguments: str, mounts: tuple[str, ...] = ()) -> str:
    result = subprocess.run(
        ["docker", "run", "--rm", "--platform", PLATFORM, "--network", "none", "--read-only",
         "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
         "--user", f"{os.getuid()}:{os.getgid()}", *mounts, IMAGE, *arguments],
        capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr[-2000:])
    return result.stdout.strip()


def replay(control: str) -> dict:
    adapter = ROOT / ADAPTER
    mounts = ("-v", f"{adapter}:/work/json_node.mjs:ro", "-v", f"{ROOT / control}:/input/case:ro")
    outputs = [json.loads(node("node", "/work/json_node.mjs", "/input/case", mounts=mounts))
               for _ in range(2)]
    if outputs[0] != outputs[1]:
        raise RuntimeError(f"{control}: repeated JSON.parse output differs")
    return outputs[0]


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    versions = json.loads(node("node", "-p", "JSON.stringify({node: process.version, v8: process.versions.v8})"))
    cases = [(manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
             (manifest["differential_control"], manifest["differential_control_sha256"],
              manifest["differential_expected_output"])]
    results = []
    for control, digest, expected in cases:
        if sha256((ROOT / control).read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {control}")
        output = replay(control)
        if output != expected:
            raise RuntimeError(f"{control}: JSON.parse output differs: {output}")
        results.append({"control": control, "sha256": digest, "output": output,
                        "repeated_output_identical": True})
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "kind": "standard", "api": API,
        "runtime": f"Node.js {versions['node'].removeprefix('v')}",
        "v8": versions["v8"], "base_image": IMAGE, "platform": PLATFORM,
        "adapter": ADAPTER,
        "adapter_sha256": sha256((ROOT / ADAPTER).read_bytes()).hexdigest(),
        "pass": True, "output": results[0]["output"], "controls": results,
        "parser_source_lines_covered": None, "afl_feedback": None,
        "coverage_note": "JSON.parse is a V8 builtin implemented in C++ inside the node binary; "
                         "V8 JavaScript coverage reports no script for it, so no parser source "
                         "lines or AFL++ parser feedback are attributed."}, indent=2,
        ensure_ascii=False) + "\n")
    print(f"{API}: both controls pass on Node {versions['node']} (V8 {versions['v8']})")


if __name__ == "__main__":
    main()
