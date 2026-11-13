"""Reproduce the pinned MonkeyWrench ASCII PLY control run."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "adapters/java/ascii_ply/monkeywrench"
DATA = ROOT / "data/java/ascii_ply"
M2 = Path.home() / ".m2/repository"


def run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args[:3])} failed: {result.stderr}")
    return result.stdout.strip()


def main() -> None:
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    release = snapshot["releases"]["MonkeyWrench"]
    parser = next(row for row in json.loads((DATA / "parsers.json").read_text())
                  if row["name"] == "MonkeyWrench")
    control = ROOT / parser["control"]
    assert sha256(control.read_bytes()).hexdigest() == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    with urlopen(release["pom_url"], timeout=45) as response:
        assert sha256(response.read()).hexdigest() == release["pom_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-monkeywrench-") as directory:
        temp = Path(directory)
        classpath_file = temp / "classpath.txt"
        run("mvn", "-q", "-f", str(MODULE / "pom.xml"), "dependency:build-classpath",
            f"-Dmdep.outputFile={classpath_file}", "-DincludeScope=runtime")
        entries = [Path(item) for item in classpath_file.read_text().strip().split(":")]
        actual = [{"repository_path": str(item.relative_to(M2)),
                   "sha256": sha256(item.read_bytes()).hexdigest()} for item in entries]
        lock = json.loads((MODULE / "dependencies.lock.json").read_text())["classpath"]
        assert actual == lock, "Resolved classpath differs from pinned jar list or hashes"
        assert lock[0]["sha256"] == release["jar_sha256"]
        classes = temp / "classes"
        classes.mkdir()
        cp = ":".join(str(item) for item in entries)
        source = MODULE / "src/main/java/org/parsarium/MonkeyWrenchPlyAdapter.java"
        run("javac", "--release", "21", "-cp", cp, "-d", str(classes), str(source))
        output = json.loads(run("java", "-Djava.awt.headless=true", "-cp", f"{classes}:{cp}",
                                "org.parsarium.MonkeyWrenchPlyAdapter", str(control)))
    assert output == parser["expected_output"]
    print(json.dumps({"package": "MonkeyWrench", "version": "1.0.1",
                      "classpath_jars": len(lock), "output": output, "pass": True}))


if __name__ == "__main__":
    main()
