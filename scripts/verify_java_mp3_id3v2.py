"""Build pinned Java MP3/ID3v2 readers and test a valid local control.

Run from the repo root: python3 scripts/verify_java_mp3_id3v2.py
Requires JDK 21+ and Maven 3.9+. This verifies only the recorded ordinary file.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/java/mp3_id3v2"
DATA = ROOT / "data/java/mp3_id3v2"
CONTROL = ROOT / "controls/mp3_id3v2/tone-tags.mp3"
CONTROL_SHA256 = "d61e1802a52dc55b5447356a3347fa4f9e08eb706757870f65ee0776dbf5bcad"


def read(path: Path):
    return json.loads(path.read_text())


def version(command: list[str]) -> str:
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=True)
    return result.stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    assert CONTROL.read_bytes().startswith(b"ID3\x03\x00")
    parsers = read(DATA / "parsers.json")
    snapshot = read(DATA / "registry-snapshot.json")
    repository = Path.home() / ".m2/repository"
    classpaths: dict[str, str] = {}
    jar_counts: dict[str, int] = {}
    by_path: dict[str, str] = {}
    for module in ("main", "mp3spi", "bytedeco"):
        adapter = ADAPTER if module == "main" else ADAPTER / module
        lock = read(adapter / "dependencies.lock.json")["classpath"]
        build = subprocess.run([
            "mvn", "-q", "-DskipTests", "package",
            "org.apache.maven.plugins:maven-dependency-plugin:3.8.1:build-classpath",
            "-Dmdep.outputFile=target/classpath.txt",
        ], cwd=adapter, text=True, capture_output=True)
        if build.returncode:
            raise RuntimeError(f"Maven build failed ({module}):\n{build.stdout}\n{build.stderr}")
        jars = [Path(item) for item in (adapter / "target/classpath.txt").read_text().strip().split(":")]
        actual = [{"repository_path": str(jar.relative_to(repository)),
                   "sha256": sha256(jar.read_bytes()).hexdigest()} for jar in jars]
        if actual != lock:
            raise AssertionError(f"Maven classpath or resolved artifact hashes differ for {module}")
        by_path.update({row["repository_path"]: row["sha256"] for row in actual})
        classpaths[module] = str(adapter / "target/classes") + ":" + ":".join(str(jar) for jar in jars)
        jar_counts[module] = len(jars)
    for name, release in snapshot["releases"].items():
        path = (f"{release['group'].replace('.', '/')}/{release['artifact']}/"
                f"{release['version']}/{release['artifact']}-{release['version']}.jar")
        assert by_path[path] == release["jar_sha256"], name
        pom = repository / (path.removesuffix(".jar") + ".pom")
        assert sha256(pom.read_bytes()).hexdigest() == release["pom_sha256"], name

    ffprobe = Path(os.environ.get("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin")) / "ffprobe"
    ffprobe_record = snapshot["external_tools"]["ffprobe"]
    assert sha256(ffprobe.read_bytes()).hexdigest() == ffprobe_record["sha256"]
    assert subprocess.run([str(ffprobe), "-version"], text=True, capture_output=True,
                          check=True).stdout.splitlines()[0] == ffprobe_record["version"]

    results = []
    for parser in parsers:
        label = parser["adapter_label"]
        module = parser.get("adapter_module", "main")
        class_name = {"main": "org.parsarium.Mp3Id3v2Adapter",
                      "mp3spi": "org.parsarium.Mp3SpiAdapter",
                      "bytedeco": "org.parsarium.BytedecoMp3Adapter"}[module]
        assert parser["control"] == "controls/mp3_id3v2/tone-tags.mp3"
        arguments = [] if module == "mp3spi" else [label]
        command = ["java", "-cp", classpaths[module], class_name,
                   *arguments, str(CONTROL)]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        try:
            output = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            output = None
        passed = (result.returncode == 0 and output == parser["expected_output"]
                  and not result.stderr.strip())
        row = {"package": parser["name"], "adapter_label": label,
               "control": parser["control"], "output": output, "pass": passed,
               "exit_code": result.returncode,
               "command": f"java -cp <{module} locked classpath> {class_name} "
                          f"{' '.join(arguments)} {parser['control']}",
               "version": parser["version"]}
        if result.stderr and not passed:
            row["stderr"] = result.stderr[-2000:]
        results.append(row)

    runtime_dir = ADAPTER / "target/runtime-classes"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    runtime_source = ADAPTER / "runtime/JdkMp3Probe.java"
    subprocess.run(["javac", "-d", str(runtime_dir), str(runtime_source)], check=True)
    runtime_command = ["java", "-cp", str(runtime_dir), "org.parsarium.JdkMp3Probe",
                       str(CONTROL)]
    runtime_result = subprocess.run(runtime_command, cwd=ROOT, text=True,
                                    capture_output=True, timeout=30)
    runtime_output = json.loads(runtime_result.stdout.strip())
    runtime_pass = (runtime_result.returncode == 0 and runtime_output == {
        "recognized": False, "exception": "UnsupportedAudioFileException"
    } and not runtime_result.stderr.strip())
    report = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"java": version(["java", "-version"]),
                        "maven": version(["mvn", "-version"]),
                        "maven_compiler_release": 21,
                        "locked_classpath_jars": jar_counts},
        "control_sha256": CONTROL_SHA256,
        "control_meaning": "Valid mono MP3 with an ID3v2.3 tag carrying title Parsarium, artist Control and album Pilot",
        "third_party": results,
        "runtime": [],
        "runtime_probe": {"api": "AudioSystem.getAudioFileFormat(File)",
                          "control": "controls/mp3_id3v2/tone-tags.mp3",
                          "command": "java -cp <JDK-only runtime classes> org.parsarium.JdkMp3Probe controls/mp3_id3v2/tone-tags.mp3",
                          "output": runtime_output, "pass": runtime_pass},
    }
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed_count = sum(row["pass"] for row in results)
    print(f"{passed_count}/{len(results)} Java MP3/ID3v2 parser paths passed; "
          f"JDK-only MP3 probe {'passed' if runtime_pass else 'failed'}")
    if passed_count != len(results) or not runtime_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
