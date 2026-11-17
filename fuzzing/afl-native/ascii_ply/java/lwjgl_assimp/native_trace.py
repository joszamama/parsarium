"""Convert executed Assimp PLY source regions into AFL++ bridge features."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


LIBRARY = "/work/native/libassimp.so"
SUBJECT = "/work/source/code/AssetLib/Ply/"


def features_for(path: str) -> set[str]:
    with tempfile.TemporaryDirectory(prefix="parsarium-assimp-trace-") as temporary:
        scratch = Path(temporary)
        environment = {
            **os.environ,
            "PARSARIUM_TARGET_CLASS": "GenericHarness",
            "PARSARIUM_LWJGL_NATIVE_DIR": "/work/native",
            "LLVM_PROFILE_FILE": str(scratch / "case-%p-%m.profraw"),
        }
        execution = subprocess.run(
            ["java", "-cp", "/work/afl-java-classes:/work/classes:/work/lib/*",
             "JavaCase", path], env=environment, capture_output=True, text=True,
            timeout=30,
        )
        if execution.returncode:
            raise RuntimeError((execution.stdout + execution.stderr)[-1000:])
        profiles = sorted(scratch.glob("*.profraw"))
        if not profiles:
            raise RuntimeError("Assimp did not write a native LLVM profile")
        merged = scratch / "case.profdata"
        subprocess.run(["llvm-profdata", "merge", *map(str, profiles), "-o", str(merged)],
                       check=True, capture_output=True, text=True, timeout=30)
        report = subprocess.run(
            ["llvm-cov", "export", LIBRARY, f"-instr-profile={merged}", SUBJECT],
            check=True, capture_output=True, text=True, timeout=30,
        )
    features = set()
    for source in json.loads(report.stdout)["data"][0]["files"]:
        filename = source["filename"]
        if not filename.startswith(SUBJECT):
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
    if not features:
        raise RuntimeError("no executed Assimp PLY parser regions")
    return features


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: native_trace.py INPUT FEATURE_FILE")
    features = features_for(sys.argv[1])
    Path(sys.argv[2]).write_text("\n".join(sorted(features)) + "\n")


if __name__ == "__main__":
    main()
