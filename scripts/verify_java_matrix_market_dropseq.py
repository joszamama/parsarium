"""Verify Drop-seq v3.0.2's released Matrix Market reader on a local control."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import shutil
import subprocess
import tarfile
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/java/matrix_market/dropseq-lock.json"
CONTROL = ROOT / "controls/matrix_market/real-general.mtx"
ADAPTER = ROOT / "adapters/java/matrix_market/dropseq/DropSeqMatrixMarketAdapter.java"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def download(url: str, expected_hash: str, destination: Path) -> None:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium Drop-seq verifier"}),
                 timeout=120) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)
    assert digest(destination) == expected_hash, url


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                          timeout=120, check=True).stdout.strip()


def main() -> None:
    lock = json.loads(LOCK.read_text())["dropseq"]
    assert digest(CONTROL) == lock["control_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-dropseq-mtx-") as directory:
        temp = Path(directory)
        archive = temp / "dropseq-source.tar.gz"
        distribution = temp / "dropseq-distribution.zip"
        download(lock["source_url"], lock["source_sha256"], archive)
        download(lock["distribution_url"], lock["distribution_sha256"], distribution)

        with tarfile.open(archive) as source:
            for member_name, expected_hash in lock["source_members"].items():
                member = source.extractfile(member_name)
                assert member is not None
                assert sha256(member.read()).hexdigest() == expected_hash
        with zipfile.ZipFile(distribution) as released:
            jar = temp / "dropseq.jar"
            htsjdk = temp / "htsjdk.jar"
            jar.write_bytes(released.read(lock["jar_member"]))
            htsjdk.write_bytes(released.read(lock["htsjdk_member"]))
        assert digest(jar) == lock["jar_sha256"]
        assert digest(htsjdk) == lock["htsjdk_sha256"]

        classes = temp / "classes"
        classes.mkdir()
        classpath = f"{jar}:{htsjdk}"
        run(["javac", "--release", "21", "-cp", classpath,
             "-d", str(classes), str(ADAPTER)])
        output = json.loads(run(["java", "-cp", f"{classes}:{classpath}",
                                 "org.parsarium.DropSeqMatrixMarketAdapter", str(CONTROL)]))
        assert output == {"rows": 2, "cols": 3, "entries": 3,
                          "value_0_2": -2.0}, output
        print(json.dumps({"package": "dropseq", "version": "v3.0.2",
                          "output": output, "pass": True}))


if __name__ == "__main__":
    main()
