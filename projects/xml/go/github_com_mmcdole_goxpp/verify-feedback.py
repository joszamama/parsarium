#!/usr/bin/env python3
"""Verify goxpp's two valid controls and both parser feedback scopes."""

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
    slug = "github_com_mmcdole_goxpp"
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
    with tempfile.TemporaryDirectory(prefix="parsarium-goxpp-feedback-") as temporary:
        work = Path(temporary)
        catalog = probe(manifest, image, ROOT / "controls/xml/catalog-ns.xml", work, "catalog")
        for prefix, key in ((None, "parser"), ("encoding/xml/", "underlying")):
            first = probe(manifest, image, second, work, f"{key}-first", prefix)
            repeat = probe(manifest, image, second, work, f"{key}-repeat", prefix)
            if first != repeat:
                raise RuntimeError(f"second control changed {key} features or AFL++ map")
            expected_features = (result["differential_parser_features"] if key == "parser"
                                 else result["underlying_differential_features"])
            expected_tuples = (result["differential_afl_tuples"] if key == "parser"
                               else result["underlying_differential_afl_tuples"])
            if len(first[0]) != expected_features or len(first[1]) != expected_tuples:
                raise RuntimeError(f"second control disagrees with {key} receipt")
            if key == "parser":
                changed = sorted(catalog[0] ^ first[0])
                if len(changed) != result["parser_feature_difference"]:
                    raise RuntimeError("changed goxpp blocks disagree with feedback receipt")
                result["changed_goxpp_source_blocks"] = changed
    result["differential_control_pass"] = True
    result["repeated_differential_identical"] = True
    result["underlying_repeated_differential_identical"] = True
    result["family_note"] = "goxpp cursor state over encoding/xml.Decoder.Token; feedback scopes are separate"
    (overlay / "differential.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
