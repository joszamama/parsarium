"""Verify pinned Java Matrix Market readers from the repo root."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import platform
from pathlib import Path
import subprocess
import tempfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/java/matrix_market"
ADAPTER = ROOT / "adapters/java/matrix_market"
CONTROL = ROOT / "controls/matrix_market/real-general.mtx"
CONTROL_SHA256 = "65614ddf08f46422a1f6f71d67bdc4490e84635b3cc61dfe089c82c41829da4c"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True, cwd=ROOT, stderr=subprocess.PIPE).strip()


def download_checked(row: dict, temp: Path) -> None:
    for kind in ("jar", "pom"):
        path = temp / f"{row['artifact']}-{row['version']}.{kind}"
        with urlopen(row[f"{kind}_url"], timeout=60) as response:
            path.write_bytes(response.read())
        assert digest(path) == row[f"{kind}_sha256"], f"{path.name} release hash mismatch"


def locked_classpath(temp: Path) -> str:
    output = temp / "classpath.txt"
    run("mvn", "-q", "-f", str(ADAPTER / "pom.xml"),
        "dependency:build-classpath", f"-Dmdep.outputFile={output}")
    paths = [Path(path) for path in output.read_text().strip().split(":")]
    repository = Path.home() / ".m2/repository"
    actual = {str(path.relative_to(repository)): digest(path) for path in paths}
    expected = json.loads((DATA / "maven-dependency-lock.json").read_text())["artifacts"]
    assert actual == expected, "Maven dependency classpath differs from the pinned hash lock"
    return ":".join(map(str, paths))


def main() -> None:
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    parsers = json.loads((DATA / "parsers.json").read_text())
    assert digest(CONTROL) == CONTROL_SHA256
    results = []
    with tempfile.TemporaryDirectory(prefix="parsarium-java-mtx-") as directory:
        temp = Path(directory)
        for parser in parsers:
            download_checked(snapshot["releases"][parser["name"]], temp)
        classpath = locked_classpath(temp)
        classes = temp / "classes"
        classes.mkdir()
        for parser in parsers:
            source = ROOT / parser["adapter"]
            run("javac", "--release", "21", "-proc:none", "-cp", classpath,
                "-d", str(classes), str(source))
            class_name = "org.parsarium." + source.stem
            raw = run("java", "--add-modules", "jdk.incubator.vector", "-cp",
                      f"{classes}:{classpath}", class_name, str(CONTROL))
            result = json.loads(raw.splitlines()[-1])
            assert result == parser["expected_output"], (parser["name"], result)
            results.append({
                "package": parser["name"], "version": parser["version"],
                "control": "controls/matrix_market/real-general.mtx",
                "output": result, "pass": True,
                "command": "python3 scripts/verify_java_matrix_market.py",
            })
    verification = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "environment": {
            "java": subprocess.run(
                ["java", "-version"], capture_output=True, text=True, check=True
            ).stderr.splitlines()[0],
            "platform": platform.platform(),
            "maven_dependency_artifacts": len(json.loads(
                (DATA / "maven-dependency-lock.json").read_text())["artifacts"]),
        },
        "control": "controls/matrix_market/real-general.mtx",
        "control_sha256": CONTROL_SHA256,
        "control_meaning": "Valid 2x3 real general coordinate matrix with three nonzero entries",
        "third_party": results,
        "runtime": [],
    }
    (DATA / "verification.json").write_text(json.dumps(verification, indent=2) + "\n")
    print(json.dumps({"verified": len(results), "packages": [r["package"] for r in results]}))


if __name__ == "__main__":
    main()
