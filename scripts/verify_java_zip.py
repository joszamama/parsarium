"""Build and run pinned Java ZIP readers on a valid one-entry control.

Run from any directory: python3 scripts/verify_java_zip.py
Requires JDK 21+ and Maven 3.9+. The saved Maven lock hashes every resolved JAR.
This verifies the documented control subset only, not full ZIP conformance.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/java/zip"
DATA = ROOT / "data/java/zip"
CONTROL = ROOT / "controls/zip/hello.zip"
CONTROL_SHA256 = "c534fa083d1da92474852ca9168ba0793740c25205f828915a1d862bd78c776b"
EXPECTED = {"name": "hello.txt", "content_base64": "cGFyc2FyaXVtCg=="}


def read(path: Path):
    return json.loads(path.read_text())


def version(command: list[str]) -> str:
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=True)
    return result.stdout.strip()


def main() -> None:
    parsers = read(DATA / "parsers.json")
    standard = read(DATA / "standard.json")["verified_apis"]
    snapshot = read(DATA / "registry-snapshot.json")
    lock = read(ADAPTER / "dependencies.lock.json")["classpath"]
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    with zipfile.ZipFile(CONTROL) as archive:
        assert archive.namelist() == ["hello.txt"]
        assert archive.read("hello.txt") == b"parsarium\n"

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
        raise AssertionError("Maven classpath or resolved artifact hashes differ from dependencies.lock.json")
    by_path = {item["repository_path"]: item["sha256"] for item in actual}
    for name, release in snapshot["releases"].items():
        path = (f"{release['group'].replace('.', '/')}/{release['artifact']}/"
                f"{release['version']}/{release['artifact']}-{release['version']}.jar")
        assert by_path[path] == release["jar_sha256"], name

    classpath = str(ADAPTER / "target/classes") + ":" + ":".join(str(jar) for jar in jars)
    def run(label: str, package: str, version_number: str | None = None) -> dict:
        command = ["java", "-cp", classpath, "org.parsarium.ZipAdapter",
                   label, str(CONTROL)]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                                timeout=30)
        try:
            output = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            output = None
        passed = result.returncode == 0 and output == EXPECTED and "Exception in thread" not in result.stderr
        row = {"package": package, "adapter_label": label, "control": "controls/zip/hello.zip",
               "output": output, "pass": passed, "exit_code": result.returncode,
               "command": "java -cp <locked classpath> org.parsarium.ZipAdapter "
                          f"{label} controls/zip/hello.zip"}
        if version_number is not None:
            row["version"] = version_number
        if result.stderr and not passed:
            row["stderr"] = result.stderr[-2000:]
        return row

    third_party = [run(parser["name"], parser["name"], parser["version"])
                   for parser in parsers]
    runtime = [run(api["name"], api["name"]) for api in standard]
    results = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "java": version(["java", "-version"]),
            "maven": version(["mvn", "-version"]),
            "maven_compiler_release": 21,
            "locked_classpath_jars": len(lock),
        },
        "control_sha256": CONTROL_SHA256,
        "control_meaning": "Valid ordinary ZIP archive with one DEFLATE-compressed hello.txt entry containing parsarium followed by a newline",
        "third_party": third_party,
        "runtime": runtime,
    }
    (DATA / "verification.json").write_text(json.dumps(results, indent=2) + "\n")
    passed = sum(row["pass"] for row in third_party)
    runtime_passed = sum(row["pass"] for row in runtime)
    print(f"{passed}/{len(third_party)} Java ZIP packages; {runtime_passed}/{len(runtime)} JDK APIs passed")
    if passed != len(third_party) or runtime_passed != len(runtime):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
