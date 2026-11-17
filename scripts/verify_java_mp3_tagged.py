"""Build pinned Java MP3/ID3v2 readers and test a valid local control.

Run from the repo root: python3 scripts/verify_java_mp3_tagged.py
Requires JDK 21, JDK 25+ for taglib, Maven 3.9+, FFprobe, and macOS arm64
libmediainfo/libzen. External binary checksums are in the dated snapshot.
This verifies only the recorded valid controls.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/java/mp3"
DATA = ROOT / "data/java/mp3"
CONTROL = ROOT / "controls/mp3/id3v2-tagged-tone.mp3"
CONTROL_SHA256 = "d61e1802a52dc55b5447356a3347fa4f9e08eb706757870f65ee0776dbf5bcad"
CONTROL_44K = ROOT / "controls/mp3/id3v2-tagged-tone-44k.mp3"
CONTROL_44K_SHA256 = "c8ca0d2c5a224ceccf150f06b9ad4de9eca753f8ce4b4817b95de0aeb07fd307"
CONTROL_LONG = ROOT / "controls/mp3/id3v2-tagged-tone-long.mp3"
CONTROL_LONG_SHA256 = "2b085bb9e5bef6bb4254233a9d6bf0652ced4589373600cff3b8ddab07909dac"


def read(path: Path):
    return json.loads(path.read_text())


def version(command: list[str]) -> str:
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=True)
    return result.stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    assert CONTROL.read_bytes().startswith(b"ID3\x03\x00")
    assert sha256(CONTROL_44K.read_bytes()).hexdigest() == CONTROL_44K_SHA256
    assert CONTROL_44K.read_bytes().startswith(b"ID3\x03\x00")
    assert sha256(CONTROL_LONG.read_bytes()).hexdigest() == CONTROL_LONG_SHA256
    assert CONTROL_LONG.read_bytes().startswith(b"ID3\x03\x00") and CONTROL_LONG.stat().st_size == 72941
    parsers = read(DATA / "parsers.json")
    snapshot = read(DATA / "registry-snapshot.json")
    repository = Path.home() / ".m2/repository"
    classpaths: dict[str, str] = {}
    jar_counts: dict[str, int] = {}
    by_path: dict[str, str] = {}
    for module in ("main", "mp3spi", "bytedeco", "tianscar", "bramp", "imagic",
                   "v47", "vlcj_info", "amilesend"):
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
    native_dir = Path(os.environ.get("PARSARIUM_LIBMEDIAINFO_DIR", "/opt/homebrew/lib"))
    for name in ("libmediainfo", "libzen"):
        entry = snapshot["external_tools"][name]
        assert sha256((native_dir / entry["filename"]).read_bytes()).hexdigest() == entry["sha256"]
        installed = subprocess.run(["brew", "list", "--versions", name], text=True,
                                   capture_output=True, check=True).stdout.strip()
        assert installed == f"{name} {entry['version']}"

    results = []
    java25 = str(Path(os.environ.get("PARSARIUM_JAVA25_HOME", "/opt/homebrew/opt/openjdk@25")) / "bin/java")
    for parser in parsers:
        label = parser["adapter_label"]
        module = parser.get("adapter_module", "main")
        class_name = {"main": "org.parsarium.Mp3Id3v2Adapter",
                      "mp3spi": "org.parsarium.Mp3SpiAdapter",
                      "bytedeco": "org.parsarium.BytedecoMp3Adapter",
                      "tianscar": "org.parsarium.Mp3SpiAdapter",
                      "bramp": "org.parsarium.BrampMp3Adapter",
                      "imagic": "org.parsarium.ImagicMp3Adapter",
                      "v47": "org.parsarium.V47Mp3Adapter",
                      "vlcj_info": "org.parsarium.VlcjInfoMp3Adapter",
                      "amilesend": "org.parsarium.AmilesendMp3Adapter"}[module]
        assert parser["control"] in ("controls/mp3/id3v2-tagged-tone.mp3",
                                     "controls/mp3/id3v2-tagged-tone-44k.mp3",
                                     "controls/mp3/id3v2-tagged-tone-long.mp3")
        parser_control = ROOT / parser["control"]
        arguments = [label] if module in ("main", "bytedeco") else []
        java_binary = java25 if parser["name"] == "taglib-java" else "java"
        native_args = [f"-Djna.library.path={native_dir}"] if module == "vlcj_info" else []
        command = [java_binary, *native_args, "-cp", classpaths[module], class_name,
                   *arguments, str(parser_control)]
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
               "command": f"{'java25' if parser['name'] == 'taglib-java' else 'java'} -cp <{module} locked classpath> {class_name} "
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
                        "java25": version([java25, "-version"]),
                        "maven": version(["mvn", "-version"]),
                        "maven_compiler_release": 21,
                        "locked_classpath_jars": jar_counts},
        "control_sha256": CONTROL_SHA256,
        "additional_control_sha256": {"controls/mp3/id3v2-tagged-tone-44k.mp3": CONTROL_44K_SHA256},
        "long_control_sha256": {"controls/mp3/id3v2-tagged-tone-long.mp3": CONTROL_LONG_SHA256},
        "control_meaning": "Valid mono 8 kHz, 44.1 kHz, and 18-second 8 kHz MP3 files with ID3v2.3 tags carrying title Parsarium, artist Control and album Pilot",
        "third_party": results,
        "runtime": [],
        "runtime_probe": {"api": "AudioSystem.getAudioFileFormat(File)",
                          "control": "controls/mp3/id3v2-tagged-tone.mp3",
                          "command": "java -cp <JDK-only runtime classes> org.parsarium.JdkMp3Probe controls/mp3/id3v2-tagged-tone.mp3",
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
