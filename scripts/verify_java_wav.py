"""Rebuild SHA-locked Java WAV adapters and verify valid PCM/WAVE parsing.

Requires JDK 25 and Maven 3.9+. The JDK adapter is compiled and run with no
third-party classpath. This script exercises only a valid control.
"""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import platform
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/java/wav"
DATA = ROOT / "data/java/wav"
CONTROL = ROOT / "controls/wav/256-samples.wav"
CONTROL_SHA256 = "d0dd329ac475ac10d5d918633c6dd798e4fc83db5f4c6afccfaa60e405d41ea7"
JAVA_HOME = Path(os.environ.get("PARSARIUM_JAVA25_HOME", "/opt/homebrew/opt/openjdk@25"))


def read(path: Path):
    return json.loads(path.read_text())


def java_environment() -> dict[str, str]:
    return {**os.environ, "JAVA_HOME": str(JAVA_HOME),
            "PATH": str(JAVA_HOME / "bin") + os.pathsep + os.environ["PATH"]}


def check_control() -> None:
    data = CONTROL.read_bytes()
    assert sha256(data).hexdigest() == CONTROL_SHA256
    assert len(data) == 556 and data[:4] == b"RIFF" and data[8:12] == b"WAVE"
    assert struct.unpack_from("<I", data, 4)[0] + 8 == len(data)
    assert data[12:16] == b"fmt " and struct.unpack_from("<I", data, 16)[0] == 16
    assert struct.unpack_from("<HHIIHH", data, 20) == (1, 1, 8000, 16000, 2, 16)
    assert data[36:40] == b"data" and struct.unpack_from("<I", data, 40)[0] == 512
    assert struct.unpack_from("<256h", data, 44) == (0, 1000, -1000, 0) + (0,) * 252


def build_third_party(env: dict[str, str], module: str) -> tuple[str, int]:
    adapter = ADAPTER / module if module != "main" else ADAPTER
    command = ["mvn", "-q", "-DskipTests", "package",
               "org.apache.maven.plugins:maven-dependency-plugin:3.8.1:build-classpath",
               "-Dmdep.outputFile=target/classpath.txt"]
    result = subprocess.run(command, cwd=adapter, env=env, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"Maven build failed:\n{result.stdout}\n{result.stderr}")
    repository = Path.home() / ".m2/repository"
    jars = [Path(item) for item in (adapter / "target/classpath.txt").read_text().strip().split(":")]
    actual = [{"repository_path": str(jar.relative_to(repository)),
               "sha256": sha256(jar.read_bytes()).hexdigest()} for jar in jars]
    assert actual == read(adapter / "dependencies.lock.json")["classpath"], f"Maven classpath differs from SHA lock: {module}"
    return str(adapter / "target/classes") + ":" + ":".join(str(jar) for jar in jars), len(jars)


def check_releases(snapshot: dict) -> None:
    repository = Path.home() / ".m2/repository"
    for name, release in snapshot["releases"].items():
        group, artifact, version = (release[k] for k in ("group", "artifact", "version"))
        base = repository / group.replace(".", "/") / artifact / version
        stem = f"{artifact}-{version}"
        assert sha256((base / f"{stem}.jar").read_bytes()).hexdigest() == release["jar_sha256"], name
        assert sha256((base / f"{stem}.pom").read_bytes()).hexdigest() == release["pom_sha256"], name
    for name, release in snapshot["native_releases"].items():
        group, artifact, version, classifier = (release[k] for k in ("group", "artifact", "version", "classifier"))
        base = repository / group.replace(".", "/") / artifact / version
        assert sha256((base / f"{artifact}-{version}-{classifier}.jar").read_bytes()).hexdigest() == release["jar_sha256"], name
        assert sha256((base / f"{artifact}-{version}.pom").read_bytes()).hexdigest() == release["pom_sha256"], name


def run(command: list[str], expected: dict) -> dict:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"Adapter failed ({command[-2]}):\n{result.stdout}\n{result.stderr}")
    output = json.loads(result.stdout.strip())
    assert output == expected, (command[-2], output, expected)
    return output


def main() -> None:
    assert JAVA_HOME.exists() and platform.system() == "Darwin" and platform.machine() == "arm64"
    check_control()
    env = java_environment()
    java = str(JAVA_HOME / "bin/java")
    classpaths, jar_counts = {}, {}
    for module in ("main", "bytedeco"):
        classpaths[module], jar_counts[module] = build_third_party(env, module)
    parsers = read(DATA / "parsers.json")
    snapshot = read(DATA / "registry-snapshot.json")
    assert len({(p["group"], p["artifact"]) for p in parsers}) == len(parsers)
    check_releases(snapshot)
    third_party = []
    for parser in parsers:
        module = parser.get("adapter_module", "main")
        mode = {"tika-audiovideo": "tika", "bytedeco-ffmpeg": "ffmpeg",
                "jhove-modules": "jhove", "tarsosdsp-jvm": "tarsos"}.get(parser["name"], parser["name"])
        cls = "org.parsarium.BytedecoWavAdapter" if module == "bytedeco" else "org.parsarium.WavAdapter"
        native_flag = ["--enable-native-access=ALL-UNNAMED"] if module == "bytedeco" else []
        output = run([java, *native_flag, "-cp", classpaths[module], cls,
                      mode, str(ROOT / parser["control"])], parser["expected_output"])
        third_party.append({"package": parser["name"], "version": parser["version"],
                            "control": parser["control"], "output": output, "pass": True})
    runtime_source = ADAPTER / "runtime/JdkWavAdapter.java"
    runtime_classes = ADAPTER / "target/runtime"
    runtime_classes.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(JAVA_HOME / "bin/javac"), "-d", str(runtime_classes),
                    str(runtime_source)], check=True, env=env)
    runtime = []
    for api in read(DATA / "standard.json")["verified_apis"]:
        output = run([java, "-cp", str(runtime_classes), "JdkWavAdapter",
                      api["adapter_mode"], str(ROOT / api["control"])], api["expected_output"])
        runtime.append({"api": api["api"], "control": api["control"],
                        "output": output, "pass": True})
    result = {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "control_sha256": CONTROL_SHA256,
        "java": subprocess.run([java, "-version"], text=True, capture_output=True, check=True).stderr.splitlines()[0],
        "maven": subprocess.run(["mvn", "-version"], env=env, text=True, capture_output=True, check=True).stdout.splitlines()[0],
        "platform": f"{platform.system()} {platform.machine()}",
        "locked_classpath_jars": jar_counts,
        "third_party": third_party,
        "runtime": runtime,
        "scope": "Valid 256-frame PCM RIFF/WAVE control only; no malformed-input or resource-use experiment",
    }
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"Java WAV: {len(third_party)} third-party paths and {len(runtime)} JDK APIs verified")


if __name__ == "__main__":
    main()
