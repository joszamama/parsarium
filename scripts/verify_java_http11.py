"""Build and run pinned Java HTTP/1.1 request parsers on a valid local control.

Run from any directory: python3 scripts/verify_java_http11.py
Requires JDK 21+ and Maven 3.9+. The saved lock hashes all resolved JARs.
This verifies one ordinary request, not full protocol conformance.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/java/http11"
DATA = ROOT / "data/java/http11"
CONTROL = ROOT / "controls/http11/request.http"
CONTROL_SHA256 = "0af539fa6b7007346b95c960cbf2e0f9d34e0d53ce732e25ba44aaadaf92b7fe"
EXPECTED = {
    "method": "GET", "target": "/parsarium?x=1", "version": "HTTP/1.1",
    "host": "example.test", "x_parsarium": "yes",
}


def read(path: Path):
    return json.loads(path.read_text())


def version(command: list[str]) -> str:
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=True)
    return result.stdout.strip()


def main() -> None:
    parsers = read(DATA / "parsers.json")
    snapshot = read(DATA / "registry-snapshot.json")
    lock = read(ADAPTER / "dependencies.lock.json")["classpath"]
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    assert CONTROL.read_bytes() == (
        b"GET /parsarium?x=1 HTTP/1.1\r\nHost: example.test\r\n"
        b"X-Parsarium: yes\r\nConnection: close\r\n\r\n"
    )

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
    results = []
    for parser in parsers:
        label = parser["adapter_label"]
        command = ["java", "-cp", classpath, "org.parsarium.Http11Adapter",
                   label, str(CONTROL)]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        try:
            output = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            output = None
        passed = result.returncode == 0 and output == EXPECTED and not result.stderr.strip()
        row = {
            "package": parser["name"], "adapter_label": label,
            "control": "controls/http11/request.http", "output": output,
            "pass": passed, "exit_code": result.returncode,
            "command": "java -cp <locked classpath> org.parsarium.Http11Adapter "
                       f"{label} controls/http11/request.http",
            "version": parser["version"],
        }
        if result.stderr and not passed:
            row["stderr"] = result.stderr[-2000:]
        results.append(row)

    report = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "java": version(["java", "-version"]),
            "maven": version(["mvn", "-version"]),
            "maven_compiler_release": 21,
            "locked_classpath_jars": len(lock),
        },
        "control_sha256": CONTROL_SHA256,
        "control_meaning": "Ordinary valid HTTP/1.1 GET request with a query target and two observable headers",
        "third_party": results,
        "runtime": [],
    }
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(row["pass"] for row in results)
    print(f"{passed}/{len(results)} Java HTTP/1.1 parser paths passed")
    if passed != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
