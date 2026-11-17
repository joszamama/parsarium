"""Compare two fixed valid XML controls through each verified AFL overlay."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
INPUTS = {"control": ROOT / "controls/xml/two-items.xml",
          "variant": ROOT / "controls/xml/one-item.xml"}


def run(args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1500:])


def probe(slug, scratch):
    receipt_path = ROOT / f"fuzzing/afl-native/xml/python/{slug}/verification.json"
    receipt = json.loads(receipt_path.read_text())
    if not receipt.get("pass") or receipt.get("feedback_kind") != "llvm_native_parser_regions_to_afl_bitmap":
        raise ValueError(f"{slug}: no verified Expat-source AFL overlay")
    image = f"parsarium-afl/xml-python-{slug}:local"
    results = {}
    for label, source in INPUTS.items():
        mounted = ["docker", "run", "--rm", "--platform", "linux/amd64", "--network", "none",
                   "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
                   "--user", f"{os.getuid()}:{os.getgid()}",
                   "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
                   "-v", f"{source}:/input/case:ro", "-v", f"{scratch}:/coverage"]
        feature_file = Path(scratch) / f"{slug}-{label}-features.txt"
        edge_file = Path(scratch) / f"{slug}-{label}-edges.txt"
        run([*mounted, "--entrypoint", "/bin/sh", image,
             "/work/afl_trace", "/input/case", f"/coverage/{feature_file.name}"])
        run([*mounted, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap", image,
             "-m", "none", "-t", "120000", "-o", f"/coverage/{edge_file.name}", "--",
             "/work/afl_proxy", "/input/case"])
        features = set(feature_file.read_text().splitlines())
        edge_ids = {line.split(":", 1)[0] for line in edge_file.read_text().splitlines()}
        if not features or not edge_ids:
            raise ValueError(f"{slug}: empty parser feature or AFL edge set on {label}")
        results[label] = {"sha256": sha256(source.read_bytes()).hexdigest(),
                          "features": features, "edge_ids": edge_ids}
    return {"project": f"xml/python/{slug}", "feedback_scope": "source-built Expat parser regions",
            "control_sha256": results["control"]["sha256"],
            "variant_sha256": results["variant"]["sha256"],
            "control_parser_features": len(results["control"]["features"]),
            "variant_parser_features": len(results["variant"]["features"]),
            "parser_feature_symmetric_difference": len(results["control"]["features"] ^ results["variant"]["features"]),
            "control_afl_edge_ids": len(results["control"]["edge_ids"]),
            "variant_afl_edge_ids": len(results["variant"]["edge_ids"]),
            "afl_edge_id_symmetric_difference": len(results["control"]["edge_ids"] ^ results["variant"]["edge_ids"]),
            "pass": True}


def main():
    with tempfile.TemporaryDirectory(prefix="parsarium-xml-feedback-") as scratch:
        rows = [probe(slug, scratch) for slug in ("xmltodict", "stdlib_elementtree")]
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "method": "afl_trace and afl-showmap on exactly two fixed valid XML controls per path",
              "results": rows, "pass": all(row["pass"] for row in rows)}
    destination = ROOT / "data/python/xml/valid-variant-feedback.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
