"""Verify the tagged JVM Assimp port against the local ASCII PLY triangle."""

from hashlib import sha256
from pathlib import Path
from urllib.request import urlopen
import json
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/java/ascii_ply"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
SOURCE = ROOT / "adapters/java/ascii_ply/kotlin_assimp/KotlinAssimpPlyAdapter.java"


def download(url: str, expected: str, destination: Path) -> None:
    with urlopen(url, timeout=120) as response:
        destination.write_bytes(response.read())
    assert sha256(destination.read_bytes()).hexdigest() == expected, url


def main() -> None:
    lock = json.loads((DATA / "kotlin-assimp-lock.json").read_text())["kotlin-assimp"]
    assert sha256(CONTROL.read_bytes()).hexdigest() == (
        "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    )
    with tempfile.TemporaryDirectory(prefix="parsarium-kotlin-assimp-ply-") as directory:
        temp = Path(directory)
        archive = temp / "assimp-v4.0.tar.gz"
        jar = temp / "assimp-all.jar"
        download(lock["source_url"], lock["source_sha256"], archive)
        with tarfile.open(archive) as tar:
            for member, digest in lock["source_members"].items():
                source = tar.extractfile(member)
                assert source is not None and sha256(source.read()).hexdigest() == digest, member
        download(lock["jar_url"], lock["jar_sha256"], jar)
        classes = temp / "classes"
        classes.mkdir()
        subprocess.run(["javac", "--release", "21", "-cp", str(jar),
                        "-d", str(classes), str(SOURCE)], cwd=ROOT, check=True)
        completed = subprocess.run(
            ["java", "-cp", f"{classes}:{jar}", "org.parsarium.KotlinAssimpPlyAdapter",
             str(CONTROL)], cwd=ROOT, check=True, capture_output=True, text=True
        )
        output = json.loads(completed.stdout.splitlines()[-1])
        assert output == {"vertices": 3, "faces": 1, "indices": [0, 1, 2]}, output
        print(json.dumps({"package": "kotlin-graphics/assimp", "release": "v4.0",
                          "output": output, "pass": True}))


if __name__ == "__main__":
    main()
