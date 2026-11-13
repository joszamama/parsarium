"""Verify Vofxel v0.0.2's released parser on a valid colored ASCII PLY."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/java/ascii_ply/vofxel-lock.json"
CONTROL = ROOT / "controls/ascii_ply/voxel-rgb.ply"
ADAPTER = ROOT / "adapters/java/ascii_ply/vofxel/VofxelPlyAdapter.java"


def download(url: str, expected_hash: str, destination: Path) -> None:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium Vofxel verifier"}),
                 timeout=90) as response:
        destination.write_bytes(response.read())
    assert sha256(destination.read_bytes()).hexdigest() == expected_hash, url


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                          timeout=120, check=True).stdout.strip()


def main() -> None:
    lock = json.loads(LOCK.read_text())["vofxel"]
    assert sha256(CONTROL.read_bytes()).hexdigest() == lock["control_sha256"]

    with tempfile.TemporaryDirectory(prefix="parsarium-vofxel-ply-") as directory:
        temp = Path(directory)
        archive = temp / "vofxel-source.tar.gz"
        jar = temp / "vofxel.jar"
        pom = temp / "vofxel.pom"
        download(lock["source_url"], lock["source_sha256"], archive)
        download(lock["jar_url"], lock["jar_sha256"], jar)
        download(lock["pom_url"], lock["pom_sha256"], pom)
        with tarfile.open(archive) as source:
            for member_name, expected_hash in lock["source_members"].items():
                member = source.extractfile(member_name)
                assert member is not None
                assert sha256(member.read()).hexdigest() == expected_hash

        classes = temp / "classes"
        classes.mkdir()
        run(["javac", "-cp", str(jar), "-d", str(classes), str(ADAPTER)])
        output = json.loads(run(["java", "-cp", f"{classes}:{jar}",
                                 "org.parsarium.VofxelPlyAdapter", str(CONTROL)]))
        assert output == {"vertices": 8, "first_x": 0.0, "first_red": 255,
                          "last_z": 1.0}, output
        print(json.dumps({"package": "vofxel", "version": "v0.0.2",
                          "output": output, "pass": True}))


if __name__ == "__main__":
    main()
