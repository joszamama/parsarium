#!/usr/bin/env python3
"""Verify two valid Sonic controls and scoped, repeatable AFL++ feedback."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))

from verify_go_json_feedback import check, probe  # noqa: E402


def main() -> None:
    slug = "github_com_bytedance_sonic"
    project = ROOT / "projects/json/go" / slug
    manifest = json.loads((project / "manifest.json").read_text())
    base_image = f"parsarium/json-go-{slug}:local"
    second = ROOT / "controls/json/nested-array.json"
    subprocess.run(
        ["docker", "run", "--rm", "--platform", manifest["platform"],
         "--network", "none", "--read-only", "--cap-drop", "ALL",
         "--security-opt", "no-new-privileges",
         "--user", f"{os.getuid()}:{os.getgid()}",
         "--tmpfs", "/tmp:rw,nosuid,size=64m",
         "-v", f"{second}:/input/differential:ro",
         "--entrypoint", "/work/harness.test", base_image,
         "-test.run=^TestDifferential$", "-test.v"],
        check=True, capture_output=True, text=True, timeout=120,
    )
    result = check(slug)
    overlay = ROOT / "fuzzing/afl-native/json/go" / slug
    image = json.loads((overlay / "verification.json").read_text())["image_id"]
    with tempfile.TemporaryDirectory(prefix="parsarium-sonic-feedback-") as temporary:
        work = Path(temporary)
        first = probe(manifest, image, second, work, "second-first")
        repeated = probe(manifest, image, second, work, "second-repeated")
    if first != repeated:
        raise RuntimeError("second valid control changed parser features or AFL++ map")
    if len(first[0]) != result["differential_parser_features"] or len(first[1]) != result["differential_afl_tuples"]:
        raise RuntimeError("second valid control disagrees with differential receipt")
    result["repeated_differential_identical"] = True
    result["differential_control_pass"] = True
    result["feedback_scope"] = (
        "Sonic internal/decoder/optdec Go blocks; native NEON assembly "
        "instructions are not instrumented by Go coverpkg"
    )
    (overlay / "differential.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
