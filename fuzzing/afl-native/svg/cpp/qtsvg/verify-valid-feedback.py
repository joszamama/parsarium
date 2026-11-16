"""Check QtSvg AFL++ feedback on two documented valid SVG controls only."""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
IMAGE = "parsarium-afl/svg-cpp-qtsvg:local"
BASE_IMAGE = "parsarium/svg-cpp-qtsvg:local"
RECEIPT = json.loads((HERE / "verification.json").read_text())


def run(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    return result.stdout


image_id = run(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"]).strip()
assert image_id == RECEIPT["image_id"]
one_pixel = ROOT / "projects/svg/cpp/qtsvg/one-pixel.svg"
one_pixel_output = json.loads(run([
    "docker", "run", "--rm", "--platform", "linux/arm64", "--network", "none",
    "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
    "--user", f"{os.getuid()}:{os.getgid()}",
    "--tmpfs", "/tmp:rw,nosuid,size=64m", "-e", "LLVM_PROFILE_FILE=/tmp/one.profraw",
    "-v", f"{one_pixel}:/input/one-pixel.svg:ro", "--entrypoint", "/work/replay",
    BASE_IMAGE, "/input/one-pixel.svg",
]))
assert one_pixel_output == {"width": 1, "height": 1, "first": [255, 0, 0], "second": None}
symbol_table = run(["docker", "run", "--rm", "--platform", "linux/arm64",
                    "--entrypoint", "nm", IMAGE, "-D", "/work/qt/lib/libQt6Svg.so.6"])
assert "__afl_area_ptr" in symbol_table

controls = {"control": ROOT / "controls/svg/red-green.svg",
            "repeat": ROOT / "controls/svg/red-green.svg",
            "variant": ROOT / "controls/svg/red-blue-path.svg"}
maps = {}
with tempfile.TemporaryDirectory(prefix="parsarium-qtsvg-afl-") as temp:
    output = Path(temp)
    for label, control in controls.items():
        command = [
            "docker", "run", "--rm", "--platform", "linux/arm64", "--network", "none",
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp",
            "-e", f"AFL_MAP_SIZE={RECEIPT['afl_map_size']}",
            "-v", f"{control}:/input/case:ro", "-v", f"{output}:/maps",
            "--entrypoint", "afl-showmap", IMAGE,
            "-m", "none", "-t", "10000", "-o", f"/maps/{label}.txt", "--",
            "/work/fuzzer", "/input/case",
        ]
        run(command)
        maps[label] = (output / f"{label}.txt").read_bytes()

assert maps["control"] == maps["repeat"]
edges = {label: {line.split(b":", 1)[0] for line in value.splitlines()}
         for label, value in maps.items()}
assert edges["control"] != edges["variant"]
assert len(edges["control"]) == RECEIPT["feedback_edges"]
evidence = {
    "schema_version": 1,
    "image_id": image_id,
    "parser_library": "/work/qt/lib/libQt6Svg.so.6",
    "parser_library_afl_area_symbol": "__afl_area_ptr",
    "one_pixel_control": str(one_pixel.relative_to(ROOT)),
    "one_pixel_control_sha256": sha256(one_pixel.read_bytes()).hexdigest(),
    "one_pixel_output": one_pixel_output,
    "control": str(controls["control"].relative_to(ROOT)),
    "control_sha256": sha256(controls["control"].read_bytes()).hexdigest(),
    "control_edges": len(edges["control"]),
    "repeat_map_identical": True,
    "variant": str(controls["variant"].relative_to(ROOT)),
    "variant_sha256": sha256(controls["variant"].read_bytes()).hexdigest(),
    "variant_edges": len(edges["variant"]),
    "different_edge_ids": len(edges["control"] ^ edges["variant"]),
    "control_map_sha256": sha256(maps["control"]).hexdigest(),
    "variant_map_sha256": sha256(maps["variant"]).hexdigest(),
}
(HERE / "valid-feedback.json").write_text(json.dumps(evidence, indent=2) + "\n")
print(json.dumps(evidence))
