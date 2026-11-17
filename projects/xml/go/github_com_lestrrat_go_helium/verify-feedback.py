#!/usr/bin/env python3
"""Verify helium's two valid controls and its own pure-Go parser source feedback."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))

from verify_go_xml_feedback import check, probe  # noqa: E402


def main() -> None:
    slug = "github_com_lestrrat_go_helium"
    project = ROOT / "projects/xml/go" / slug
    manifest = json.loads((project / "manifest.json").read_text())
    second = ROOT / "controls/xml/order-default-ns.xml"
    base_image = f"parsarium/xml-go-{slug}:local"
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
    overlay = ROOT / "fuzzing/afl-native/xml/go" / slug
    image = json.loads((overlay / "verification.json").read_text())["image_id"]
    with tempfile.TemporaryDirectory(prefix="parsarium-helium-feedback-") as temporary:
        work = Path(temporary)
        first = probe(manifest, image, ROOT / "controls/xml/catalog-ns.xml", work, "first")
        other = probe(manifest, image, second, work, "other")
        repeated = probe(manifest, image, second, work, "other-repeat")
    if other != repeated:
        raise RuntimeError("second control changed helium source features or AFL++ map")
    changed = sorted(first[0] ^ other[0])
    if len(changed) != result["parser_feature_difference"]:
        raise RuntimeError("changed source blocks disagree with feedback receipt")
    files = sorted({feature.split(":", 1)[0] for feature in changed})
    if not files or any(not name.startswith("github.com/lestrrat-go/helium/") for name in files):
        raise RuntimeError(f"feedback includes non-helium source: {files}")
    result["differential_control_pass"] = True
    result["repeated_differential_identical"] = True
    result["changed_source_files"] = files
    result["family_note"] = "helium pure-Go XML parser (libxml2-style port); own tokenizer compiled and instrumented, no encoding/xml"
    (overlay / "differential.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
