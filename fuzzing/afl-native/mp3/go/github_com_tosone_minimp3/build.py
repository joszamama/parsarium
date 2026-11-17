"""Build native minimp3 C coverage in its Go binding and verify valid-control feedback."""

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

RELATIVE = Path("mp3/go/github_com_tosone_minimp3")
PROJECT = ROOT / "projects" / RELATIVE
OVERLAY = ROOT / "fuzzing/afl-native" / RELATIVE
IMAGE = "parsarium-afl/mp3-go-github_com_tosone_minimp3:local"
BASE = "parsarium/mp3-go-github_com_tosone_minimp3:local"
REPEATS = 5


def call(args: list[str], timeout: int = 1200) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-3000:])
    return result.stdout.strip()


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def showmap(image_id: str, control: Path, output: Path, platform: str) -> set[str]:
    call(["docker", "run", "--rm", "--platform", platform, "--network", "none",
          "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
          "--user", f"{os.getuid()}:{os.getgid()}",
          "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "-e", "AFL_MAP_SIZE=65536",
          "-v", f"{control}:/input/control:ro", "-v", f"{output.parent}:/coverage",
          "--entrypoint", "afl-showmap", image_id,
          "-m", "none", "-t", "30000", "-o", f"/coverage/{output.name}",
          "--", "/work/afl-target", "/input/control"], 120)
    return set(output.read_text().splitlines()) - {""}


def main() -> None:
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    if not manifest.get("afl_native_cgo") or manifest["afl_entrypoint"] != "/work/afl-target":
        raise ValueError("native cgo AFL++ manifest is missing")
    base_receipt_path = PROJECT / "verification.json"
    base_receipt = json.loads(base_receipt_path.read_text())
    if (base_receipt.get("pass") is not True or
            (base_receipt.get("underlying_source_lines_covered") or 0) < 100):
        raise ValueError("native C source coverage is not verified")
    base_id = call(["docker", "image", "inspect", BASE, "--format", "{{.Id}}"])
    if base_id != base_receipt["image_id"]:
        raise ValueError("base image differs from verified control receipt")
    allowlist = PROJECT / "afl-allowlist.txt"
    names = [line.removeprefix("fun: ") for line in allowlist.read_text().splitlines()]
    if (len(names) != 47 or len(set(names)) != len(names) or
            not all(name and " " not in name for name in names) or
            "mp3dec_decode_frame" not in names):
        raise ValueError("pinned native parser function allowlist changed")
    with docker_build_slot():
        call(["docker", "build", "--quiet", "--platform", manifest["platform"],
              "-f", str(OVERLAY / "Dockerfile"), "-t", IMAGE, str(PROJECT)])
    image_id = call(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"])
    version = call(["docker", "run", "--rm", "--platform", manifest["platform"],
                    "--entrypoint", "dpkg-query", image_id,
                    "-W", "-f=${Version}", "afl++"])
    if version != "4.04c-4":
        raise ValueError(f"AFL++ version changed: {version}")
    controls = [ROOT / manifest["control"], ROOT / manifest["differential_control"]]
    for control, expected in zip(controls, [manifest["control_sha256"],
                                           manifest["differential_control_sha256"]]):
        if digest(control) != expected:
            raise ValueError(f"control hash mismatch: {control}")
    with tempfile.TemporaryDirectory(prefix="parsarium-minimp3-afl-") as temp:
        output = Path(temp)
        runs = [[showmap(image_id, control, output / f"{index}-{attempt}.map",
                         manifest["platform"])
                 for attempt in range(REPEATS)]
                for index, control in enumerate(controls)]
    for index, group in enumerate(runs):
        if not group[0] or any(item != group[0] for item in group[1:]):
            raise ValueError(f"control {index} native AFL++ tuples are empty or unstable")
    edge_ids = [{line.split(":", 1)[0] for line in group[0]} for group in runs]
    edge_difference = len(edge_ids[0] ^ edge_ids[1])
    if edge_difference < 2:
        raise ValueError("valid controls did not yield different native parser feedback")
    validation = {
        "schema_version": 1, "pass": True, "project": str(RELATIVE),
        "feedback_scope": "AFL++ CLASSIC allowlist of 47 vendored minimp3.h C decoder functions; Go runtime and cgo glue excluded",
        "first_control": manifest["control"], "first_sha256": manifest["control_sha256"],
        "second_control": manifest["differential_control"],
        "second_sha256": manifest["differential_control_sha256"],
        "second_control_output": manifest["differential_expected_output"],
        "repeats_per_control": REPEATS,
        "first_native_tuples": len(edge_ids[0]), "second_native_tuples": len(edge_ids[1]),
        "native_tuple_difference": edge_difference,
        "repeat_maps_identical": True, "mutation_campaign_run": False,
        "allowlist_sha256": digest(allowlist),
    }
    validation_path = OVERLAY / "feedback-validation.json"
    validation_path.write_text(json.dumps(validation, indent=2) + "\n")
    receipt = {
        "schema_version": 1, "project": str(RELATIVE), "pass": True,
        "feedback_kind": "go_cgo_minimp3_native_c_parser_edges",
        "feedback_scope": validation["feedback_scope"],
        "base_project_receipt_sha256": digest(base_receipt_path),
        "base_image_id": base_id, "image_id": image_id,
        "platform": manifest["platform"], "control_sha256": manifest["control_sha256"],
        "source_sha256": manifest["source_sha256"],
        "parser_source_features": len(names),
        "feedback_edges": len(edge_ids[0]), "afl_map_size": 65536,
        "afl_package": version,
        "afl_entrypoint": "/work/afl-target", "afl_file_input": True,
        "allowlist_sha256": digest(allowlist),
        "overlay_file_sha256": {
            name: digest(OVERLAY / name)
            for name in ("Dockerfile", "build.py", "feedback-validation.json")
        },
    }
    (OVERLAY / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified {RELATIVE}: {len(edge_ids[0])} native C AFL++ tuples, "
          f"{edge_difference} differ on second valid control; {REPEATS} stable repeats each")


if __name__ == "__main__":
    main()
