"""Run the C DNS standard/runtime path (glibc libresolv ns_initparse/ns_parserr) on both controls.

Builds adapters/c/dns/libresolv.Dockerfile (pinned Ubuntu image, the distribution's glibc
libresolv), replays controls/dns/response.bin and controls/dns/query.bin in a sandbox with
no network, compares each summary with the hand-written oracle's pinned summary in
controls/dns/expected.json, and writes data/c/dns/libresolv-standard-result.json.

glibc is the system runtime and is not source-instrumented here, so no parser coverage or
AFL++ feedback is claimed; the path is recorded outside the third-party ranking.

Usage: python3 scripts/run_dns_libresolv_standard.py
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
IMAGE = "parsarium-standard/dns-c-libresolv:local"
PLATFORM = "linux/arm64"


def run(command: list[str]) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def main() -> None:
    adapter = ROOT / "adapters/c/dns"
    run(["docker", "build", "--quiet", "--platform", PLATFORM, "-t", IMAGE, "-f",
         str(adapter / "libresolv.Dockerfile"), str(adapter)])
    image_id = run(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"]).strip()
    runtime = run(["docker", "run", "--rm", "--network", "none", "--entrypoint", "cat", IMAGE,
                   "/work/runtime.txt"]).strip().splitlines()
    expected = json.loads((ROOT / "controls/dns/expected.json").read_text())
    results = []
    for name in ("response.bin", "query.bin"):
        control = ROOT / "controls/dns" / name
        digest = sha256(control.read_bytes()).hexdigest()
        assert digest == expected[name]["sha256"]
        output = json.loads(run(["docker", "run", "--rm", "--platform", PLATFORM, "--network", "none",
                                 "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
                                 "-v", f"{control}:/input/case:ro", IMAGE, "/input/case"]))
        results.append({"control": f"controls/dns/{name}", "control_sha256": digest, "output": output,
                        "matches_oracle": output == expected[name]["summary"]})
    receipt = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "api": "ns_initparse(msg, msglen, &handle) + ns_parserr(&handle, section, index, &rr) (glibc libresolv, <arpa/nameser.h>)",
        "adapter": "adapters/c/dns/libresolv.c",
        "dockerfile": "adapters/c/dns/libresolv.Dockerfile",
        "adapter_sha256": sha256((adapter / "libresolv.c").read_bytes()).hexdigest(),
        "image_id": image_id, "platform": PLATFORM, "runtime": runtime,
        "control": results[0]["control"], "output": results[0]["output"],
        "differential_control": results[1]["control"], "differential_output": results[1]["output"],
        "results": results,
        "pass": all(item["matches_oracle"] for item in results),
        "coverage": None,
        "coverage_note": "System glibc is not source-instrumented; no parser coverage or AFL++ feedback is claimed.",
    }
    out = ROOT / "data/c/dns/libresolv-standard-result.json"
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(receipt["pass"], runtime)


if __name__ == "__main__":
    main()
