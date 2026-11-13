"""Build GraphTea v1.0.0's released source reader and parse a valid control."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/java/matrix_market/graphtea-lock.json"
CONTROL = ROOT / "controls/matrix_market/real-general.mtx"
ADAPTER = ROOT / "adapters/java/matrix_market/graphtea/GraphTeaMatrixMarketAdapter.java"


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                          timeout=120, check=True).stdout.strip()


def main() -> None:
    lock = json.loads(LOCK.read_text())["graphtea"]
    assert sha256(CONTROL.read_bytes()).hexdigest() == lock["control_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-graphtea-mtx-") as directory:
        temp = Path(directory)
        archive = temp / "graphtea-source.tar.gz"
        with urlopen(Request(lock["source_url"], headers={
                "User-Agent": "Parsarium GraphTea verifier"}), timeout=120) as response:
            archive.write_bytes(response.read())
        assert sha256(archive.read_bytes()).hexdigest() == lock["source_sha256"]

        with tarfile.open(archive) as source:
            for relative_path, expected_hash in lock["source_members"].items():
                members = [member for member in source.getmembers()
                           if member.name.endswith("/" + relative_path)]
                assert len(members) == 1, relative_path
                stream = source.extractfile(members[0])
                assert stream is not None
                data = stream.read()
                assert sha256(data).hexdigest() == expected_hash, relative_path
                local = temp / relative_path
                local.parent.mkdir(parents=True, exist_ok=True)
                local.write_bytes(data)

        jama = temp / "src/scripts/lib/Jama-1.0.1.jar"
        classes = temp / "classes"
        classes.mkdir()
        run(["javac", "--release", "21", "-cp", str(jama), "-d", str(classes),
             str(temp / "src/graphtea/extensions/io/MM.java"),
             str(temp / "src/graphtea/extensions/reports/coloring/SpMat.java"),
             str(ADAPTER)])
        output = json.loads(run(["java", "-cp", f"{classes}:{jama}",
                                 "org.parsarium.GraphTeaMatrixMarketAdapter",
                                 str(CONTROL)]))
        assert output == {"rows": 2, "cols": 3, "value_0_2": -2.0}, output
        print(json.dumps({"package": "graphtea", "version": "v1.0.0",
                          "output": output, "pass": True}))


if __name__ == "__main__":
    main()
