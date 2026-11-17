"""Verify Tk's pinned PNG decoder with source coverage and AFL++ feedback."""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


OVERLAY = Path(__file__).resolve().parent
ROOT = OVERLAY.parents[4]
PROJECT = ROOT / "projects/png/python/stdlib_tkinter_photoimage"
BASE_IMAGE = "parsarium/png-python-stdlib_tkinter_photoimage:local"
IMAGE = "parsarium-afl/png-python-stdlib_tkinter_photoimage:local"
VARIANT = ROOT / "controls/png/red-green-title.png"
sys.path.insert(0, str(ROOT / "scripts"))
from docker_slots import docker_build_slot  # noqa: E402


def command(args: list[str], timeout: int = 90) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                            errors="replace", timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)} failed: "
                           f"{(result.stdout + result.stderr)[-3000:]}")
    return result.stdout.strip()


def sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def isolated(image: str) -> list[str]:
    return ["docker", "run", "--rm", "--platform", "linux/arm64",
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=256m", "--workdir", "/tmp",
            image]


def docker_case(image: str, control: Path, *extra: str) -> list[str]:
    args = isolated(image)
    args[-1:-1] = ["-v", f"{control}:/input/file:ro", *extra]
    return args


def main() -> None:
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    base_receipt_path = PROJECT / "control-verification.json"
    base_receipt = json.loads(base_receipt_path.read_text())
    control = ROOT / manifest["control"]
    if (sha(control) != manifest["control_sha256"]
            or sha(VARIANT) != "d643731d4a91c228d705b9cf54c0d6af2c9f53ae4a2d9b2fe5035d649fad1450"):
        raise RuntimeError("valid PNG controls changed")
    if (base_receipt["status"] != "verified_control_only"
            or base_receipt["parser_source_lines_covered"] <= 0
            or base_receipt["png_reader_source_sha256"] != manifest["png_reader_source_sha256"]):
        raise RuntimeError("pinned Tk source control is not verified")
    for name, digest in base_receipt["project_file_sha256"].items():
        if sha(PROJECT / name) != digest:
            raise RuntimeError(f"base control project changed: {name}")
    base_id, platform = command(["docker", "image", "inspect", BASE_IMAGE,
                                 "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"]).split()
    if base_id != base_receipt["image_id"] or platform != manifest["platform"]:
        raise RuntimeError("local CPython/Tk control image differs from its receipt; run verify-control.py")

    print(f"Building {IMAGE}", flush=True)
    with docker_build_slot():
        command(["docker", "build", "--quiet", "--platform", manifest["platform"],
                 "-f", str(OVERLAY / "Dockerfile"), "-t", IMAGE, str(OVERLAY)],
                timeout=3600)
    image_id, overlay_platform = command(["docker", "image", "inspect", IMAGE,
                                          "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"]).split()
    if overlay_platform != manifest["platform"]:
        raise RuntimeError("AFL++ image platform differs from pinned control")
    afl_version = command(["docker", "run", "--rm", "--platform", manifest["platform"],
                           "--entrypoint", "dpkg-query", IMAGE, "-W", "-f=${Version}", "afl++"])
    if afl_version != "4.33c-1.1ubuntu1":
        raise RuntimeError(f"unexpected AFL++ version: {afl_version}")

    expected = manifest["expected_output"]
    for path in (control, VARIANT):
        result = json.loads(command(docker_case(IMAGE, path) + ["/input/file"]))
        if result != expected:
            raise RuntimeError(f"PhotoImage control mismatch: {path}: {result}")

    coverage = OVERLAY / "target/coverage"
    if coverage.exists():
        shutil.rmtree(coverage)
    coverage.mkdir(parents=True)
    observed = json.loads(command(docker_case(IMAGE, control,
        "-v", f"{coverage}:/coverage", "-e", "LLVM_PROFILE_FILE=/coverage/tk.profraw",
        "--entrypoint", "/work/with-display.sh") +
        ["/work/afl-python", "/work/replay.py", "/input/file"]))
    if observed != expected:
        raise RuntimeError("instrumented control output changed")
    command(isolated(IMAGE)[:-1] + ["-v", f"{coverage}:/coverage",
            "--entrypoint", "llvm-profdata", IMAGE, "merge", "-sparse",
            "/coverage/tk.profraw", "-o", "/coverage/tk.profdata"])
    source_json = json.loads(command(isolated(IMAGE)[:-1] +
        ["-v", f"{coverage}:/coverage", "--entrypoint", "llvm-cov", IMAGE,
         "export", "/opt/tk-afl/lib/libtk8.6.so",
         "-instr-profile=/coverage/tk.profdata", "--summary-only"]))
    png_sources = [file for file in source_json["data"][0]["files"]
                   if file["filename"] == "/work/tk-afl-source/generic/tkImgPNG.c"]
    covered = sum(file["summary"]["lines"]["covered"] for file in png_sources)
    if len(png_sources) != 1 or covered <= 0:
        raise RuntimeError("Tk PNG decoder source was not covered")

    # CLASSIC mode uses a configured 64 KiB map. Check showmap's reported size
    # as well as the decoder-only map contents below.
    map_size = 65536
    def showmap(args: list[str], label: str) -> set[str]:
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                                errors="replace", timeout=60)
        output = result.stdout + result.stderr
        if result.returncode:
            raise RuntimeError(f"afl-showmap {label} failed: {output[-3000:]}")
        reported = re.search(r"map size (\d+)", output)
        if reported is None or int(reported.group(1)) != map_size:
            raise RuntimeError(f"afl-showmap {label} map size mismatch: {output[-1000:]}")
        return set((coverage / f"{label}.map").read_text().splitlines())

    baseline_args = isolated(IMAGE)[:-1] + [
        "-v", f"{coverage}:/coverage", "-e", f"AFL_MAP_SIZE={map_size}",
        "--entrypoint", "/work/showmap.sh", IMAGE,
        "-m", "none", "-t", "15000", "-o", "/coverage/baseline.map",
        "--", "/work/afl-python", "-c", "pass"]
    if showmap(baseline_args, "baseline"):
        raise RuntimeError("unparsed Python baseline emitted AFL++ edges")
    maps: dict[str, set[str]] = {}
    for label, path in (("control1", control), ("control2", control),
                        ("variant1", VARIANT), ("variant2", VARIANT)):
        args = (docker_case(IMAGE, path,
            "-v", f"{coverage}:/coverage", "-e", f"AFL_MAP_SIZE={map_size}",
            "--entrypoint", "/work/showmap.sh") +
            ["-m", "none", "-t", "15000", "-o", f"/coverage/{label}.map",
             "--", "/work/afl-python", "/work/replay.py", "/input/file"])
        maps[label] = showmap(args, label)
        if not maps[label]:
            raise RuntimeError(f"no AFL++ decoder edges for {label}")
    if maps["control1"] != maps["control2"] or maps["variant1"] != maps["variant2"]:
        raise RuntimeError("valid PNG decoder feedback changed between identical replays")
    difference = maps["control1"] ^ maps["variant1"]
    if not difference:
        raise RuntimeError("PNG tEXt variant did not change decoder feedback")
    control_ids = {entry.split(":", 1)[0] for entry in maps["control1"]}
    variant_ids = {entry.split(":", 1)[0] for entry in maps["variant1"]}
    edge_id_difference = len(control_ids ^ variant_ids)
    if edge_id_difference <= 0:
        raise RuntimeError("PNG tEXt variant changed hit counts but no decoder edge IDs")

    file_hashes = {str(path.relative_to(OVERLAY)): sha(path)
                   for path in sorted(OVERLAY.rglob("*")) if path.is_file()
                   and path.name not in {"verification.json", "README.md"}
                   and "target" not in path.relative_to(OVERLAY).parts
                   and "__pycache__" not in path.relative_to(OVERLAY).parts}
    receipt = {
        "schema_version": 1, "project": "png/python/stdlib_tkinter_photoimage",
        "base_control_receipt_sha256": sha(base_receipt_path),
        "base_image_id": base_id, "image_id": image_id,
        "platform": manifest["platform"], "afl_package": afl_version,
        "source_sha256": manifest["source_sha256"],
        "png_reader_source_sha256": manifest["png_reader_source_sha256"],
        "control_sha256": manifest["control_sha256"],
        "variant_sha256": sha(VARIANT), "output": expected,
        "decoder_source_file": "tkImgPNG.c",
        "decoder_source_lines_covered": covered,
        "feedback_scope": "AFL++ LLVM source allowlist: tkImgPNG.c",
        "afl_map_size": map_size,
        "unparsed_baseline_edges": 0,
        "control_edges": len(maps["control1"]),
        "variant_edges": len(maps["variant1"]),
        "afl_tuple_difference": len(difference),
        "afl_edge_id_difference": edge_id_difference,
        "stable_identical_replays": True,
        "overlay_file_sha256": file_hashes,
        "pass": True,
    }
    (OVERLAY / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified Tk PNG decoder: {covered} source lines, "
          f"{len(maps['control1'])}/{len(maps['variant1'])} AFL++ edges, "
          f"{edge_id_difference} differing edge IDs", flush=True)


if __name__ == "__main__":
    main()
