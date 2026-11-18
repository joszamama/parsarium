"""Record repeat stability and colour-variant response for a generated Java PLY AFL++ bridge.

Run after scripts/build_afl_bridge.py has written this overlay's receipt. The
valid control and the valid colour variant each run twice through the parser
trace and through afl-showmap; the receipt gains the counts below only when
both repeats agree and the variant changes both the parser feature set and the map.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile


OVERLAY = Path(__file__).resolve().parent
ROOT = OVERLAY.parents[4]
RELATIVE = OVERLAY.relative_to(ROOT / "fuzzing/afl-native")
IMAGE = f"parsarium-afl/{RELATIVE.parts[0]}-{RELATIVE.parts[1]}-{RELATIVE.parts[2]}:local"
VARIANT = ROOT / "controls/ascii_ply/triangle-colour.ply"


def docker(sample: Path, scratch: Path, args: list[str]) -> None:
    command = ["docker", "run", "--rm", "--platform", "linux/arm64", "--network", "none",
               "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
               "--user", f"{os.getuid()}:{os.getgid()}",
               "--tmpfs", "/tmp:rw,exec,nosuid,size=256m", "-e", "AFL_MAP_SIZE=65536",
               "-v", f"{sample}:/input/case:ro", "-v", f"{scratch}:/coverage", *args]
    result = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])


def features(sample: Path, scratch: Path, name: str) -> set[str]:
    docker(sample, scratch, ["--entrypoint", "/bin/sh", IMAGE, "/work/afl_trace",
                             "/input/case", f"/coverage/{name}"])
    return {line for line in (scratch / name).read_text().splitlines() if line}


def edges(sample: Path, scratch: Path, name: str) -> set[str]:
    docker(sample, scratch, ["--entrypoint", "afl-showmap", IMAGE, "-m", "none", "-t", "60000",
                             "-o", f"/coverage/{name}", "--", "/work/afl_proxy", "/input/case"])
    return {line.split(":", 1)[0] for line in (scratch / name).read_text().splitlines() if line}


def main() -> None:
    receipt_path = OVERLAY / "verification.json"
    receipt = json.loads(receipt_path.read_text())
    image_id = subprocess.run(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"],
                              capture_output=True, text=True, check=True).stdout.strip()
    if not receipt.get("pass") or image_id != receipt["image_id"]:
        raise RuntimeError("overlay receipt is not current for the local AFL++ image")
    control = ROOT / "controls/ascii_ply/triangle.ply"
    with tempfile.TemporaryDirectory(prefix="parsarium-ply-variant-") as temporary:
        scratch = Path(temporary)
        control_sets = [features(control, scratch, f"control-{i}.txt") for i in range(2)]
        variant_sets = [features(VARIANT, scratch, f"variant-{i}.txt") for i in range(2)]
        control_maps = [edges(control, scratch, f"control-map-{i}.txt") for i in range(2)]
        variant_maps = [edges(VARIANT, scratch, f"variant-map-{i}.txt") for i in range(2)]
    if control_sets[0] != control_sets[1] or variant_sets[0] != variant_sets[1]:
        raise RuntimeError("parser features differ between identical runs")
    if control_maps[0] != control_maps[1] or variant_maps[0] != variant_maps[1]:
        raise RuntimeError("AFL++ maps differ between identical runs")
    if len(control_sets[0]) != receipt["parser_source_features"]:
        raise RuntimeError("control feature count differs from the bridge receipt")
    variant_only = variant_sets[0] - control_sets[0]
    control_only = control_sets[0] - variant_sets[0]
    if not (variant_only or control_only) or control_maps[0] == variant_maps[0]:
        raise RuntimeError("colour variant did not change parser feedback")
    receipt.update({
        "variant_sha256": sha256(VARIANT.read_bytes()).hexdigest(),
        "control_repeat_feature_counts": [len(item) for item in control_sets],
        "variant_repeat_feature_counts": [len(item) for item in variant_sets],
        "stable_variant_only_features": len(variant_only),
        "stable_control_only_features": len(control_only),
        "parser_feature_difference": len(variant_only) + len(control_only),
        "control_repeat_edge_counts": [len(item) for item in control_maps],
        "variant_feedback_edges": len(variant_maps[0]),
        "afl_tuple_difference": len(control_maps[0] ^ variant_maps[0]),
        "variant_check_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    })
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"{RELATIVE}: {len(control_sets[0])} stable control features, "
          f"{len(variant_only) + len(control_only)} features differ on the variant, "
          f"{receipt['afl_tuple_difference']} differing AFL++ tuples")


if __name__ == "__main__":
    main()
