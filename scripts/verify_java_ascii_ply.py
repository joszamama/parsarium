"""Reproduce pinned Java PLY parser runs using a valid ASCII triangle."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/java/ascii_ply"


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True, cwd=ROOT).strip()


def main() -> None:
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    parsers = json.loads((DATA / "parsers.json").read_text())
    control = ROOT / "controls/ascii_ply/triangle.ply"
    assert sha256(control.read_bytes()).hexdigest() == "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    with tempfile.TemporaryDirectory(prefix="parsarium-java-ply-") as directory:
        temp = Path(directory)
        jars = {}
        for parser in parsers:
            name = parser["name"]
            release = snapshot["releases"][name]
            for kind in ("jar", "pom"):
                path = temp / f"{name}.{kind}"
                with urlopen(release[f"{kind}_url"], timeout=45) as response:
                    path.write_bytes(response.read())
                assert sha256(path.read_bytes()).hexdigest() == release[f"{kind}_sha256"]
                if kind == "jar":
                    jars[name] = path
        classes = temp / "classes"
        classes.mkdir()
        classpath = ":".join(str(path) for path in jars.values())
        source = ROOT / "adapters/java/ascii_ply/src/main/java/org/parsarium/PlyAdapter.java"
        run("javac", "--release", "21", "-cp", classpath, "-d", str(classes), str(source))
        for parser in parsers:
            output = json.loads(run("java", "-cp", f"{classes}:{classpath}",
                                    "org.parsarium.PlyAdapter", parser["name"], str(control)))
            assert output == parser["expected_output"]
            print(json.dumps({"package": parser["name"], "version": parser["version"],
                              "output": output, "pass": True}))


if __name__ == "__main__":
    main()
