"""Convert executed F3D native PLY plugin and VTK PLY source regions into AFL++ bridge features."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


LIBRARY = "/work/native/libf3d-java.so"
SUBJECTS = ("/work/vtk/source/IO/PLY/", "/work/f3d/source/plugins/native/",
            "/work/f3d/build/f3d/plugins/native/")


def features_for(path: str) -> set[str]:
    with tempfile.TemporaryDirectory(prefix="parsarium-f3d-trace-") as temporary:
        scratch = Path(temporary)
        environment = {
            **os.environ,
            "PARSARIUM_TARGET_CLASS": "GenericHarness",
            "LLVM_PROFILE_FILE": str(scratch / "case-%p-%m.profraw"),
        }
        execution = subprocess.run(
            ["java", "-Djava.library.path=/work/native",
             "-cp", "/work/afl-java-classes:/work/classes:/work/lib/*",
             "JavaCase", path], env=environment, capture_output=True, text=True,
            timeout=60,
        )
        if execution.returncode:
            raise RuntimeError((execution.stdout + execution.stderr)[-1000:])
        profiles = sorted(scratch.glob("*.profraw"))
        if not profiles:
            raise RuntimeError("libf3d-java.so did not write a native LLVM profile")
        merged = scratch / "case.profdata"
        subprocess.run(["llvm-profdata", "merge", *map(str, profiles), "-o", str(merged)],
                       check=True, capture_output=True, text=True, timeout=60)
        report = subprocess.run(
            ["llvm-cov", "export", LIBRARY, f"-instr-profile={merged}", *SUBJECTS],
            check=True, capture_output=True, text=True, timeout=60,
        )
    features = set()
    for source in json.loads(report.stdout)["data"][0]["files"]:
        filename = source["filename"]
        if not filename.startswith(SUBJECTS):
            continue
        for line, column, count, has_count, region_start, *_ in source["segments"]:
            if has_count and region_start and count > 0:
                features.add(f"native:{filename}:{line}:{column}")
        for branch in source.get("branches", []):
            line, column = branch[0], branch[1]
            if branch[4] > 0:
                features.add(f"native:{filename}:{line}:{column}:true")
            if branch[5] > 0:
                features.add(f"native:{filename}:{line}:{column}:false")
    if not any(item.startswith("native:/work/vtk/source/IO/PLY/") for item in features):
        raise RuntimeError("no executed VTK PLY parser regions")
    return features


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: native_trace.py INPUT FEATURE_FILE")
    features = features_for(sys.argv[1])
    Path(sys.argv[2]).write_text("\n".join(sorted(features)) + "\n")


if __name__ == "__main__":
    main()
