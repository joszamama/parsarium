"""Verify pinned Java MP4 adapters on one valid H.264/AAC MP4 control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import platform
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/java/mp4"
DATA = ROOT / "data/java/mp4"
CONTROL = ROOT / "controls/mp4/red-av.mp4"
CONTROL_SHA256 = "10086c39c7226726579924794cd7c0bbafe65de38021bd0f38f6da9d23d24643"
JAVA_HOME = Path(os.environ.get("PARSARIUM_JAVA25_HOME", "/opt/homebrew/opt/openjdk@25"))


def read(path: Path):
    return json.loads(path.read_text())


def check_control() -> None:
    data = CONTROL.read_bytes()
    assert sha256(data).hexdigest() == CONTROL_SHA256
    offset, boxes = 0, []
    while offset < len(data):
        size = struct.unpack_from(">I", data, offset)[0]
        assert size >= 8 and offset + size <= len(data)
        boxes.append((data[offset + 4:offset + 8].decode("ascii"), size))
        offset += size
    assert boxes == [("ftyp", 32), ("moov", 1442), ("free", 8), ("mdat", 1188)]


def build(env: dict[str, str], module: str) -> tuple[str, int]:
    adapter = ADAPTER if module == "main" else ADAPTER / module
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
    assert actual == read(adapter / "dependencies.lock.json")["classpath"], "Maven classpath differs from SHA lock"
    return str(adapter / "target/classes") + ":" + ":".join(str(jar) for jar in jars), len(jars)


def check_releases(snapshot: dict) -> None:
    repository = Path.home() / ".m2/repository"
    for name, release in {**snapshot["releases"], **snapshot.get("auxiliary_releases", {})}.items():
        group, artifact, version = (release[k] for k in ("group", "artifact", "version"))
        base = repository / group.replace(".", "/") / artifact / version
        stem = f"{artifact}-{version}"
        assert sha256((base / f"{stem}.jar").read_bytes()).hexdigest() == release["jar_sha256"], name
        assert sha256((base / f"{stem}.pom").read_bytes()).hexdigest() == release["pom_sha256"], name
    for name, release in snapshot.get("native_releases", {}).items():
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
    env = {**os.environ, "JAVA_HOME": str(JAVA_HOME),
           "PATH": str(JAVA_HOME / "bin") + os.pathsep + os.environ["PATH"]}
    java = str(JAVA_HOME / "bin/java")
    modules = ("main", "ffprobe", "bramp", "jave", "imagic", "v47")
    classpaths, jar_counts = {}, {}
    for module in modules:
        classpaths[module], jar_counts[module] = build(env, module)
    parsers = read(DATA / "parsers.json")
    snapshot = read(DATA / "registry-snapshot.json")
    assert len({(p["group"], p["artifact"]) for p in parsers}) == len(parsers)
    assert set(snapshot["releases"]) == {p["name"] for p in parsers}
    check_releases(snapshot)
    ffprobe = Path(os.environ.get("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin")) / "ffprobe"
    tool = snapshot["external_tools"]["ffprobe"]
    assert sha256(ffprobe.read_bytes()).hexdigest() == tool["sha256"]
    assert subprocess.run([str(ffprobe), "-version"], text=True, capture_output=True,
                          check=True).stdout.splitlines()[0] == tool["version"]
    third_party = []
    for parser in parsers:
        module = parser.get("adapter_module", "main")
        cls = {"main": "org.parsarium.Mp4Adapter", "ffprobe": "org.parsarium.JaffreeMp4Adapter",
               "bramp": "org.parsarium.BrampMp4Adapter", "jave": "org.parsarium.JaveMp4Adapter",
               "imagic": "org.parsarium.ImagicMp4Adapter", "v47": "org.parsarium.V47Mp4Adapter"}[module]
        args = [parser["name"]] if module == "main" else []
        output = run([java, "--enable-native-access=ALL-UNNAMED", "-cp", classpaths[module], cls,
                      *args, str(ROOT / parser["control"])], parser["expected_output"])
        third_party.append({"package": parser["name"], "version": parser["version"],
                            "control": parser["control"], "output": output, "pass": True})
    runtime_classes = ADAPTER / "target/runtime"
    runtime_classes.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(JAVA_HOME / "bin/javac"), "-d", str(runtime_classes),
                    str(ADAPTER / "runtime/JdkMp4Probe.java")], check=True, env=env)
    negative = run([java, "-cp", str(runtime_classes), "JdkMp4Probe", str(CONTROL)],
                   {"imageio_reader": False, "audio_system_reader": False})
    result = {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "control_sha256": CONTROL_SHA256,
        "java": subprocess.run([java, "-version"], text=True, capture_output=True, check=True).stderr.splitlines()[0],
        "maven": subprocess.run(["mvn", "-version"], env=env, text=True, capture_output=True, check=True).stdout.splitlines()[0],
        "locked_classpath_jars_by_module": jar_counts,
        "third_party": third_party,
        "runtime": [],
        "jdk_only_probe": {"control": "controls/mp4/red-av.mp4", "output": negative,
                           "scope": "ImageIO and Java Sound bundled readers only; not an exhaustive proof of every possible provider"},
        "scope": "Valid 2x2 H.264 video and 8 kHz AAC audio MP4 control only; no malformed-input or resource-use experiment",
    }
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"Java MP4: {len(third_party)} third-party paths and no documented JDK MP4 parser verified")


if __name__ == "__main__":
    main()
