"""Rebuild and run SHA-locked Java PNG parsers on the valid RGBA control.

Requires JDK 21+, Maven 3.9+, and macOS arm64 for the locked JavaFX/OpenCV
native artifacts. This establishes only the labeled control behavior.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import struct
import subprocess
import zlib

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/java/png"
DATA = ROOT / "data/java/png"
CONTROL = ROOT / "controls/png/red-green.png"
CONTROL_SHA256 = "5a852fbaaaecaf4cd14c01e150c7f881c5c5894b0a1e3c53be7e007c58374ee6"
EXPECTED_PIXELS = {"width": 2, "height": 1, "pixels": "ffff0000,ff00ff00"}


def read(path: Path):
    return json.loads(path.read_text())


def version(command: list[str]) -> str:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=True).stdout.strip()


def check_control() -> None:
    encoded = CONTROL.read_bytes()
    assert sha256(encoded).hexdigest() == CONTROL_SHA256
    assert encoded[:8] == b"\x89PNG\r\n\x1a\n"
    offset, chunks = 8, []
    while offset < len(encoded):
        length = struct.unpack_from(">I", encoded, offset)[0]
        kind = encoded[offset+4:offset+8]
        payload = encoded[offset+8:offset+8+length]
        crc = struct.unpack_from(">I", encoded, offset+8+length)[0]
        assert zlib.crc32(kind+payload) == crc
        chunks.append((kind,payload))
        offset += 12 + length
    assert offset == len(encoded)
    assert [kind for kind,_ in chunks] == [b"IHDR",b"IDAT",b"IEND"]
    assert chunks[0][1] == struct.pack(">IIBBBBB", 2,1,8,6,0,0,0)
    assert zlib.decompress(chunks[1][1]) == bytes((0,255,0,0,255,0,255,0,255))
    assert chunks[2][1] == b""


def main() -> None:
    parsers = read(DATA / "parsers.json")
    standard = read(DATA / "standard.json")["verified_apis"]
    snapshot = read(DATA / "registry-snapshot.json")
    lock = read(ADAPTER / "dependencies.lock.json")["classpath"]
    check_control()
    assert platform.system() == "Darwin" and platform.machine() == "arm64"

    build = subprocess.run([
        "mvn", "-q", "-DskipTests", "package",
        "org.apache.maven.plugins:maven-dependency-plugin:3.8.1:build-classpath",
        "-Dmdep.outputFile=target/classpath.txt",
    ], cwd=ADAPTER, text=True, capture_output=True)
    if build.returncode:
        raise RuntimeError(f"Maven build failed:\n{build.stdout}\n{build.stderr}")

    repository = Path.home() / ".m2/repository"
    jars = [Path(item) for item in (ADAPTER / "target/classpath.txt").read_text().strip().split(":")]
    actual = [{"repository_path": str(jar.relative_to(repository)),
               "sha256": sha256(jar.read_bytes()).hexdigest()} for jar in jars]
    if actual != lock:
        raise AssertionError("Maven classpath or resolved JAR hashes differ from dependencies.lock.json")
    by_path = {item["repository_path"]: item["sha256"] for item in actual}
    for name, release in snapshot["releases"].items():
        stem = f"{release['artifact']}-{release['version']}"
        if release["classifier"]:
            stem += f"-{release['classifier']}"
        path = f"{release['group'].replace('.', '/')}/{release['artifact']}/{release['version']}/{stem}.jar"
        assert by_path[path] == release["jar_sha256"], name
        local_pom = repository / release["group"].replace(".", "/") / release["artifact"] / release["version"] / f"{release['artifact']}-{release['version']}.pom"
        assert sha256(local_pom.read_bytes()).hexdigest() == release["pom_sha256"], name

    classpath = str(ADAPTER / "target/classes") + ":" + ":".join(str(jar) for jar in jars)
    def run(label: str, package: str, expected: dict, version_number: str | None = None) -> dict:
        command = ["java", "-Djava.awt.headless=true", "-cp", classpath,
                   "org.parsarium.PngAdapter", label, str(CONTROL)]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        try:
            output = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            output = None
        passed = result.returncode == 0 and output == expected and "Exception in thread" not in result.stderr
        row = {"package": package, "adapter_label": label, "control": "controls/png/red-green.png",
               "output": output, "pass": passed, "exit_code": result.returncode,
               "command": f"java -Djava.awt.headless=true -cp <locked classpath> org.parsarium.PngAdapter {label} controls/png/red-green.png"}
        if version_number is not None:
            row["version"] = version_number
        if result.stderr and not passed:
            row["stderr"] = result.stderr[-2000:]
        return row

    third_party = [run(parser["name"], parser["name"], parser["expected_output"], parser["version"])
                   for parser in parsers]
    runtime = [run(api["name"], api["name"], EXPECTED_PIXELS) for api in standard]
    results = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"java": version(["java", "-version"]), "maven": version(["mvn", "-version"]),
                        "os": platform.platform(), "arch": platform.machine(),
                        "maven_compiler_release": 21, "locked_classpath_jars": len(lock)},
        "control_sha256": CONTROL_SHA256,
        "control_meaning": "Valid 2×1 RGBA PNG; opaque red then opaque green; verified IHDR, IDAT, IEND, CRC and decoded filter-0 scanline",
        "third_party": third_party, "runtime": runtime,
    }
    (DATA / "verification.json").write_text(json.dumps(results, indent=2) + "\n")
    passed = sum(row["pass"] for row in third_party)
    runtime_passed = sum(row["pass"] for row in runtime)
    print(f"{passed}/{len(third_party)} Java PNG packages; {runtime_passed}/{len(runtime)} JDK APIs passed")
    if passed != len(third_party) or runtime_passed != len(runtime):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
