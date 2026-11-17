"""Reproduce JavaMP3 1.0.1's failure on an existing valid MPEG-2 control."""

from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
IMAGE = "eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d"
RELEASE = "1.0.1"
ARTIFACTS = {
    "javamp3.jar": (
        "https://repo.maven.apache.org/maven2/fr/delthas/javamp3/1.0.1/javamp3-1.0.1.jar",
        "ee259df947a4242fd03d164b2fb4c61cc42e167a0af483cc18ce0c0bfa13b1ac"),
    "javamp3-sources.jar": (
        "https://repo.maven.apache.org/maven2/fr/delthas/javamp3/1.0.1/javamp3-1.0.1-sources.jar",
        "153cb584ecc5d35ed4f39dcd5e4c8040bca8c38511afb69026066ebed4d17d8c"),
    "javamp3.pom": (
        "https://repo.maven.apache.org/maven2/fr/delthas/javamp3/1.0.1/javamp3-1.0.1.pom",
        "ad8cb4249a3ab46a04e75729e79c04ae9e749c426d94fdff031a0d617178f725"),
}
CONTROLS = ("tone-44k-mono.mp3", "tone-22k-stereo.mp3")


def docker(work: Path, *args: str, control: Path | None = None) -> subprocess.CompletedProcess:
    command = ["docker", "run", "--rm", "--platform", "linux/arm64",
               "--network", "none", "--read-only", "--cap-drop", "ALL",
               "--security-opt", "no-new-privileges",
               "--user", f"{os.getuid()}:{os.getgid()}",
               "--tmpfs", "/tmp:rw,nosuid,size=64m",
               "-v", f"{work}:/work"]
    if control:
        command += ["-v", f"{control}:/input/control:ro"]
    return subprocess.run([*command, IMAGE, *args], capture_output=True, text=True,
                          errors="replace", timeout=120)


def run() -> dict:
    oracle = runpy.run_path(str(ROOT / "controls/mp3/check_controls.py"))["walk"]
    with tempfile.TemporaryDirectory(prefix="parsarium-javamp3-probe-") as temporary:
        work = Path(temporary)
        (work / "classes").mkdir()
        (work / "Probe.java").write_bytes((HERE / "Probe.java").read_bytes())
        for name, (url, digest) in ARTIFACTS.items():
            download = subprocess.run(["curl", "--fail", "--silent", "--show-error",
                                       "--location", "--max-time", "30", url],
                                      capture_output=True, timeout=35)
            if download.returncode:
                raise RuntimeError(f"download failed: {name}: {download.stderr.decode(errors='replace')}")
            data = download.stdout
            if sha256(data).hexdigest() != digest:
                raise RuntimeError(f"artifact hash mismatch: {name}")
            (work / name).write_bytes(data)
        compile_result = docker(work, "javac", "-cp", "/work/javamp3.jar",
                                "-d", "/work/classes", "/work/Probe.java")
        if compile_result.returncode:
            raise RuntimeError(compile_result.stderr[-2000:])
        cases = []
        for name in CONTROLS:
            path = ROOT / "controls/mp3" / name
            expected = oracle(path.read_bytes())
            execution = docker(work, "java", "-cp", "/work/classes:/work/javamp3.jar",
                               "Probe", "/input/control", control=path)
            cases.append({
                "control": str(path.relative_to(ROOT)),
                "control_sha256": sha256(path.read_bytes()).hexdigest(),
                "oracle": {"sample_rate": expected["sample_rate"],
                           "channels": expected["channels"],
                           "decoded_samples": expected["frames"] * expected["samples_per_frame"]},
                "exit_code": execution.returncode,
                "output": json.loads(execution.stdout) if execution.returncode == 0 else None,
                "exception": ("ArrayIndexOutOfBoundsException: Index 2304 out of bounds for length 2304"
                              if "ArrayIndexOutOfBoundsException: Index 2304 out of bounds for length 2304"
                                 in execution.stderr else None),
                "exception_source": ("fr.delthas.javamp3.Decoder.samples_III(Decoder.java:773)"
                                     if "fr.delthas.javamp3.Decoder.samples_III(Decoder.java:773)"
                                        in execution.stderr else None),
            })
    if cases[0]["exit_code"] != 0 or cases[0]["output"] != {
            "sample_rate": 44100, "channels": 1, "pcm_bytes": 25344,
            "decoded_samples": 12672}:
        raise RuntimeError(f"mono control changed: {cases[0]}")
    if (cases[1]["exit_code"] == 0 or not cases[1]["exception"] or
            not cases[1]["exception_source"]):
        raise RuntimeError(f"stereo failure changed: {cases[1]}")
    return {"schema_version": 1, "candidate": "fr.delthas:javamp3",
            "release": RELEASE, "status": "excluded_valid_control_crash",
            "runtime_image": IMAGE, "platform": "linux/arm64",
            "source": "data/java/mp3/plain-mp3-pilot/probes/javamp3/Probe.java",
            "source_sha256": sha256((HERE / "Probe.java").read_bytes()).hexdigest(),
            "artifacts": {name: {"url": url, "sha256": digest}
                          for name, (url, digest) in ARTIFACTS.items()},
            "cases": cases,
            "limit": "Two existing valid untagged CBR Layer III controls; no malformed-input or fuzzing experiment."}


if __name__ == "__main__":
    result = run()
    serialized = json.dumps(result, indent=2) + "\n"
    if len(sys.argv) == 2 and sys.argv[1] == "--write":
        (HERE / "result.json").write_text(serialized)
    elif len(sys.argv) == 2 and sys.argv[1] == "--check":
        if (HERE / "result.json").read_text() != serialized:
            raise SystemExit("javamp3 probe result changed")
    elif len(sys.argv) != 1:
        raise SystemExit("usage: run.py [--write|--check]")
    print(serialized, end="")
