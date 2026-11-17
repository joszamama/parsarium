"""Verify AFL++ feedback from the source-built Assimp PLY importer used by LWJGL."""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
RELATIVE = Path("ascii_ply/java/lwjgl_assimp")
PROJECT = ROOT / "projects" / RELATIVE
BRIDGE = ROOT / "fuzzing/afl-bridge"
IMAGE = "parsarium-afl/ascii_ply-java-lwjgl_assimp:local"
BASE_IMAGE = "parsarium/ascii_ply-java-lwjgl_assimp:local"
AFL_PACKAGE = "4.09c-1ubuntu3"
sys.path.insert(0, str(ROOT / "scripts"))
from docker_slots import docker_build_slot


def command(args: list[str], timeout: int = 180) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{args[:6]} failed: {(result.stdout + result.stderr)[-2500:]}")
    return result.stdout.strip()


def docker_case(sample: Path, destination: Path, name: str, target: list[str]) -> set[str]:
    output = destination / name
    args = ["docker", "run", "--rm", "--platform", "linux/arm64", "--network", "none",
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=256m", "--workdir", "/tmp",
            "-v", f"{sample}:/input/case:ro", "-v", f"{destination}:/coverage",
            "--entrypoint", target[0], IMAGE, *target[1:], f"/coverage/{name}"]
    command(args, timeout=120)
    return {line for line in output.read_text().splitlines() if line}


def features(sample: Path, destination: Path, name: str) -> set[str]:
    return docker_case(sample, destination, name,
                       ["/bin/sh", "/work/afl_trace", "/input/case"])


def edges(sample: Path, destination: Path, name: str) -> set[str]:
    output = destination / name
    args = ["docker", "run", "--rm", "--platform", "linux/arm64", "--network", "none",
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=256m", "--workdir", "/tmp",
            "-e", "AFL_MAP_SIZE=65536", "-v", f"{sample}:/input/case:ro",
            "-v", f"{destination}:/coverage", "--entrypoint", "afl-showmap", IMAGE,
            "-m", "none", "-t", "60000", "-o", f"/coverage/{name}", "--",
            "/work/afl_proxy", "/input/case"]
    command(args, timeout=120)
    return {line.split(":", 1)[0] for line in output.read_text().splitlines() if line}


def main() -> None:
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    receipt_path = PROJECT / "verification.json"
    base_receipt = json.loads(receipt_path.read_text())
    if not base_receipt.get("pass") or base_receipt.get("underlying_source_lines_covered", 0) < 1:
        raise RuntimeError("source-covered Assimp PLY base project is not verified")
    base_id = command(["docker", "image", "inspect", BASE_IMAGE, "--format", "{{.Id}}"])
    if base_id != base_receipt["image_id"]:
        raise RuntimeError("local base image differs from its verification receipt")
    with docker_build_slot():
        command(["docker", "build", "--quiet", "--platform", manifest["platform"],
                 "-f", str(OVERLAY / "Dockerfile"), "-t", IMAGE, str(ROOT)], timeout=1800)
    image_id = command(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"])
    version = command(["docker", "run", "--rm", "--platform", manifest["platform"],
                       "--entrypoint", "dpkg-query", IMAGE, "-W", "-f=${Version}", "afl++"])
    if version != AFL_PACKAGE:
        raise RuntimeError(f"AFL++ package changed: {version}")
    control = ROOT / manifest["control"]
    variant = ROOT / "controls/ascii_ply/triangle-colour.ply"
    with tempfile.TemporaryDirectory(prefix="parsarium-assimp-afl-") as temporary:
        scratch = Path(temporary)
        control_sets = [features(control, scratch, f"control-features-{i}.txt") for i in range(2)]
        variant_sets = [features(variant, scratch, f"variant-features-{i}.txt") for i in range(2)]
        all_features = set.union(*(control_sets + variant_sets))
        if not all_features or any(not item.startswith("native:/work/source/code/AssetLib/Ply/")
                                   for item in all_features):
            raise RuntimeError("feedback includes no native PLY source or includes wrapper features")
        stable_control = set.intersection(*control_sets)
        stable_variant = set.intersection(*variant_sets)
        control_union = set.union(*control_sets)
        stable_variant_only = stable_variant - control_union
        if not stable_variant_only:
            raise RuntimeError("valid colour PLY produced no stable new native parser regions")
        control_edges = edges(control, scratch, "control-map.txt")
        variant_edges = edges(variant, scratch, "variant-map.txt")
        if len(control_edges) < 2 or control_edges == variant_edges:
            raise RuntimeError("AFL++ map did not respond to native PLY features")
    overlay_files = ("Dockerfile", "afl_trace", "native_trace.py", "build.py")
    bridge_files = ("afl_proxy.c", "JavaCase.java")
    receipt = {
        "schema_version": 1, "project": str(RELATIVE), "pass": True,
        "feedback_kind": "java_native_assimp_ply_regions_to_afl_bitmap",
        "feedback_scope": "LLVM source regions in pinned Assimp PLY importer; Java wrapper excluded",
        "base_project_receipt_sha256": sha256(receipt_path.read_bytes()).hexdigest(),
        "base_image_id": base_id, "image_id": image_id, "platform": manifest["platform"],
        "source_sha256": manifest["source_sha256"],
        "underlying_source_sha256": manifest["underlying_source_sha256"],
        "control_sha256": manifest["control_sha256"],
        "variant_sha256": sha256(variant.read_bytes()).hexdigest(),
        "parser_source_features": len(control_sets[0]),
        "control_repeat_feature_counts": [len(item) for item in control_sets],
        "stable_control_features": len(stable_control),
        "variant_repeat_feature_counts": [len(item) for item in variant_sets],
        "stable_variant_only_features": len(stable_variant_only),
        "feedback_edges": len(control_edges),
        "variant_feedback_edges": len(variant_edges),
        "afl_map_size": 65536, "afl_package": version,
        "overlay_file_sha256": {name: sha256((OVERLAY / name).read_bytes()).hexdigest()
                                for name in overlay_files},
        "bridge_file_sha256": {name: sha256((BRIDGE / name).read_bytes()).hexdigest()
                               for name in bridge_files},
    }
    (OVERLAY / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified {RELATIVE}: {len(control_sets[0])} native PLY features, "
          f"{len(control_edges)} AFL++ edges")


if __name__ == "__main__":
    main()
