"""Reproduce the pinned EJML Matrix Market control run from the repo root."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/java/matrix_market"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True, cwd=ROOT).strip()


def main() -> None:
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    row = snapshot["releases"]["ejml-core"]
    expected = json.loads((DATA / "parsers.json").read_text())[0]["expected_output"]
    control = ROOT / "controls/matrix_market/real-general.mtx"
    assert digest(control) == "65614ddf08f46422a1f6f71d67bdc4490e84635b3cc61dfe089c82c41829da4c"
    with tempfile.TemporaryDirectory(prefix="parsarium-java-mtx-") as directory:
        temp = Path(directory)
        for kind in ("jar", "pom"):
            path = temp / f"ejml-core-0.46.1.{kind}"
            with urlopen(row[f"{kind}_url"], timeout=45) as response:
                path.write_bytes(response.read())
            assert digest(path) == row[f"{kind}_sha256"], f"{kind} release hash mismatch"
        jar = temp / "ejml-core-0.46.1.jar"
        classes = temp / "classes"
        classes.mkdir()
        source = ROOT / "adapters/java/matrix_market/src/main/java/org/parsarium/MatrixMarketAdapter.java"
        run("javac", "--release", "21", "-cp", str(jar), "-d", str(classes), str(source))
        output = json.loads(run("java", "-cp", f"{classes}:{jar}",
                                "org.parsarium.MatrixMarketAdapter", str(control)))
    assert output == expected, (output, expected)
    print(json.dumps({"package": "ejml-core", "version": "0.46.1", "output": output, "pass": True}))


if __name__ == "__main__":
    main()
