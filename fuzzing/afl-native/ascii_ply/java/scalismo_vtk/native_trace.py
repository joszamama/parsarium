"""Convert executed VTK IO/PLY source regions (scalismo-vtk path) into AFL++ bridge features."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


LIBRARY = "/work/native-cov/libvtkIOPLY-9.1.so"
SUBJECT = "/work/vtk/source/IO/PLY/"
# Published jars, except the impl jar whose libvtkIOPLY-9.1.so is the coverage build.
COV_CLASSPATH = ":".join(["/work/afl-java-classes", "/work/classes",
                          *sorted(str(p) for p in Path("/work/lib").glob("*.jar")
                                  if "vtkjavanativeslinuximpl" not in p.name),
                          "/work/lib-cov/vtkjavanativeslinuximpl-0.2-RC1.jar"])


def features_for(path: str) -> set[str]:
    with tempfile.TemporaryDirectory(prefix="parsarium-scalismo-vtk-trace-") as temporary:
        scratch = Path(temporary)
        environment = {
            **os.environ,
            "PARSARIUM_TARGET_CLASS": "GenericHarness",
            "LLVM_PROFILE_FILE": str(scratch / "case-%p-%m.profraw"),
        }
        # afl-showmap exports LD_BIND_NOW=1; scalismo.vtk.initialize() loads every native of
        # the impl jar, including JOGL's libnewt_head.so, whose Raspberry Pi symbols resolve
        # only lazily, so eager binding would fail before the PLY reader runs.
        environment.pop("LD_BIND_NOW", None)
        execution = subprocess.run(
            ["java", "-Duser.home=/work/home-cov", "-Djava.awt.headless=true",
             "-cp", COV_CLASSPATH,
             "JavaCase", path], env=environment, capture_output=True, text=True,
            timeout=400,
        )
        if execution.returncode:
            raise RuntimeError((execution.stdout + execution.stderr)[-1000:])
        profiles = sorted(scratch.glob("*.profraw"))
        if not profiles:
            raise RuntimeError("libvtkIOPLY did not write a native LLVM profile")
        merged = scratch / "case.profdata"
        subprocess.run(["llvm-profdata", "merge", *map(str, profiles), "-o", str(merged)],
                       check=True, capture_output=True, text=True, timeout=60)
        report = subprocess.run(
            ["llvm-cov", "export", LIBRARY, f"-instr-profile={merged}", SUBJECT],
            check=True, capture_output=True, text=True, timeout=60,
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
        raise RuntimeError("no executed VTK PLY parser regions")
    return features


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: native_trace.py INPUT FEATURE_FILE")
    features = features_for(sys.argv[1])
    Path(sys.argv[2]).write_text("\n".join(sorted(features)) + "\n")


if __name__ == "__main__":
    main()
