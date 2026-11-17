#!/usr/bin/env python3
"""Reproduce the RapidXml 2.1.4 lead decision on both valid XML controls (no fuzzing, no malformed input)."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

PROBE = Path(__file__).resolve().parent
ROOT = PROBE.parents[3]
IMAGE = "parsarium-lead/xml-python-rapidxml:local"
CONTROLS = ("controls/xml/catalog-ns.xml", "controls/xml/order-default-ns.xml")


def run(command: list[str]) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True, timeout=900).stdout


def main() -> None:
    run(["docker", "build", "--quiet", "--platform", "linux/arm64", "-t", IMAGE, str(PROBE)])
    image_id = run(["docker", "image", "inspect", "--format", "{{.Id}}", IMAGE]).strip()
    observed = {}
    for control in CONTROLS:
        observed[control] = json.loads(run([
            "docker", "run", "--rm", "--platform", "linux/arm64", "--network", "none", "--read-only",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
            "-v", f"{ROOT / control}:/input/case:ro", IMAGE, "/input/case"]))
    receipt = {
        "schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "package": "RapidXml (PyPI rapidxml)", "release": "2.1.4",
        "sdist_sha256": "aae02d75c98c062927d1a5c40f07838c65760b144fd0d7322f097a27a081205d",
        "license": "MIT", "image_id": image_id,
        "api": "rapidxml.RapidXml(bytes) as documented in the README; parse_cdata=True is an undocumented keyword of the C extension",
        "family": "Python C++ extension over bundled RapidXML 1.13 headers (same RapidXML family as the C++ XML cell's RapidXML path)",
        "probe_file_sha256": {name: sha256((PROBE / name).read_bytes()).hexdigest()
                              for name in ("Dockerfile", "probe.py", "check.py")},
        "control_sha256": {control: sha256((ROOT / control).read_bytes()).hexdigest() for control in CONTROLS},
        "observed": observed,
    }
    (ROOT / "data/python/xml/rapidxml-lead-check.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(observed, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
