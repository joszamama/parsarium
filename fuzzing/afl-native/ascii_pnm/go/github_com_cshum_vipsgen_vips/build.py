"""Build native libvips ppmload feedback in the pinned vipsgen Go binding."""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
from docker_slots import docker_build_slot  # noqa: E402

RELATIVE = Path("ascii_pnm/go/github_com_cshum_vipsgen_vips")
PROJECT = ROOT / "projects" / RELATIVE
OVERLAY = ROOT / "fuzzing/afl-native" / RELATIVE
IMAGE = "parsarium-afl/ascii_pnm-go-github_com_cshum_vipsgen_vips:local"
BASE = "parsarium/ascii_pnm-go-github_com_cshum_vipsgen_vips:local"
REPEATS = 5
SCOPE = ("AFL++ CLASSIC allowlist of the native libvips libvips/foreign/ppmload.c loader; "
         "Go runtime, vipsgen binding and other libvips sources excluded")


def call(args: list[str], timeout: int = 1800) -> str:
    completed = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    if completed.returncode:
        raise RuntimeError(f"{' '.join(args[:8])}: {(completed.stdout + completed.stderr)[-2000:]}")
    return completed.stdout.strip()


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def showmap(image: str, control: Path, destination: Path, platform: str) -> set[str]:
    call(["docker", "run", "--rm", "--platform", platform, "--network", "none",
          "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
          "--user", f"{os.getuid()}:{os.getgid()}",
          "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "-e", "AFL_MAP_SIZE=65536",
          "-v", f"{control}:/input/control:ro", "-v", f"{destination.parent}:/coverage",
          "--entrypoint", "afl-showmap", image,
          "-m", "none", "-t", "30000", "-o", f"/coverage/{destination.name}",
          "--", "/work/afl-target", "/input/control"], 120)
    return set(destination.read_text().splitlines()) - {""}


def main() -> None:
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    if not manifest.get("afl_native_cgo") or manifest["afl_entrypoint"] != "/work/afl-target":
        raise ValueError("native cgo AFL++ manifest is missing")
    base_receipt_path = PROJECT / "verification.json"
    base_receipt = json.loads(base_receipt_path.read_text())
    if (base_receipt.get("pass") is not True
            or base_receipt.get("parser_source_lines_covered", 0) < 5
            or base_receipt.get("underlying_source_lines_covered", 0) < 50):
        raise ValueError("Go binding and native ppmload source coverage are not verified")
    base_id = call(["docker", "image", "inspect", BASE, "--format", "{{.Id}}"])
    if base_id != base_receipt["image_id"]:
        raise ValueError("base image differs from verified receipt")
    allowlist = PROJECT / "afl-allowlist.txt"
    if allowlist.read_text().splitlines() != ["src: ppmload.c"]:
        raise ValueError("native ppmload allowlist changed")
    controls = [ROOT / manifest["control"], ROOT / manifest["differential_control"]]
    for control, expected in zip(controls, [manifest["control_sha256"],
                                           manifest["differential_control_sha256"]]):
        if digest(control) != expected:
            raise ValueError(f"control hash changed: {control}")
    with docker_build_slot():
        call(["docker", "build", "--quiet", "--platform", manifest["platform"],
              "-f", str(OVERLAY / "Dockerfile"), "-t", IMAGE, str(PROJECT)])
    image_id = call(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"])
    version = call(["docker", "run", "--rm", "--platform", manifest["platform"],
                    "--entrypoint", "dpkg-query", image_id,
                    "-W", "-f=${Version}", "afl++"])
    if version != "4.04c-4":
        raise ValueError(f"AFL++ version changed: {version}")
    with tempfile.TemporaryDirectory(prefix="parsarium-vipsgen-afl-") as directory:
        output = Path(directory)
        os.chmod(output, 0o777)
        runs = [[showmap(image_id, control, output / f"{index}-{repeat}.map",
                         manifest["platform"]) for repeat in range(REPEATS)]
                for index, control in enumerate(controls)]
    for index, group in enumerate(runs):
        if not group[0] or any(item != group[0] for item in group[1:]):
            raise ValueError(f"control {index} native AFL++ map is empty or unstable")
    ids = [{line.split(":", 1)[0] for line in group[0]} for group in runs]
    difference = len(ids[0] ^ ids[1])
    if difference < 2:
        raise ValueError("valid PNM controls do not change native ppmload feedback")
    validation = {
        "schema_version": 1, "pass": True, "project": str(RELATIVE),
        "feedback_scope": SCOPE,
        "first_control": manifest["control"], "first_sha256": manifest["control_sha256"],
        "first_control_output": manifest["expected_output"],
        "second_control": manifest["differential_control"],
        "second_sha256": manifest["differential_control_sha256"],
        "second_control_output": manifest["differential_expected_output"],
        "repeats_per_control": REPEATS,
        "first_native_tuples": len(ids[0]), "second_native_tuples": len(ids[1]),
        "native_tuple_difference": difference, "repeat_maps_identical": True,
        "mutation_campaign_run": False, "allowlist_sha256": digest(allowlist),
    }
    (OVERLAY / "feedback-validation.json").write_text(json.dumps(validation, indent=2) + "\n")
    receipt = {
        "schema_version": 1, "project": str(RELATIVE), "pass": True,
        "feedback_kind": "go_cgo_libvips_native_ppmload_edges",
        "feedback_scope": SCOPE,
        "base_project_receipt_sha256": digest(base_receipt_path),
        "base_image_id": base_id, "image_id": image_id,
        "platform": manifest["platform"], "control_sha256": manifest["control_sha256"],
        "source_sha256": manifest["source_sha256"],
        "underlying_source_sha256": manifest["underlying_source_sha256"],
        "parser_source_features": base_receipt["underlying_source_files"],
        "feedback_edges": len(ids[0]), "afl_map_size": 65536,
        "afl_package": version,
        "afl_entrypoint": manifest["afl_entrypoint"], "afl_file_input": True,
        "allowlist_sha256": digest(allowlist),
        "overlay_file_sha256": {
            name: digest(OVERLAY / name)
            for name in ("Dockerfile", "build.py", "feedback-validation.json")
        },
    }
    (OVERLAY / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified {RELATIVE}: {len(ids[0])} native ppmload tuples; "
          f"{difference} differ across controls, {REPEATS} identical repeats each")


if __name__ == "__main__":
    main()
