"""Verify MeteoInfo Math 4.3.0's released Matrix Market reader."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import subprocess
import tarfile
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/java/matrix_market/meteoinfo-lock.json"
CONTROL = ROOT / "controls/matrix_market/real-general.mtx"
ADAPTER = ROOT / "adapters/java/matrix_market/meteoinfo/MeteoInfoMatrixMarketAdapter.java"


def download(url: str, expected_hash: str, destination: Path) -> None:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium MeteoInfo verifier"}),
                 timeout=90) as response:
        destination.write_bytes(response.read())
    assert sha256(destination.read_bytes()).hexdigest() == expected_hash, url


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                          timeout=120, check=True).stdout.strip()


def main() -> None:
    lock = json.loads(LOCK.read_text())["meteoinfo-math"]
    assert sha256(CONTROL.read_bytes()).hexdigest() == lock["control_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-meteoinfo-mtx-") as directory:
        temp = Path(directory)
        archive = temp / "meteoinfo-source.tar.gz"
        jar = temp / "meteoinfo-math.jar"
        pom = temp / "meteoinfo-math.pom"
        sources_jar = temp / "meteoinfo-math-sources.jar"
        for url_key, hash_key, path in (
            ("source_url", "source_sha256", archive),
            ("jar_url", "jar_sha256", jar),
            ("pom_url", "pom_sha256", pom),
            ("sources_jar_url", "sources_jar_sha256", sources_jar),
        ):
            download(lock[url_key], lock[hash_key], path)
        with tarfile.open(archive) as source:
            members = {}
            for member_name, expected_hash in lock["source_members"].items():
                member = source.extractfile(member_name)
                assert member is not None
                content = member.read()
                assert sha256(content).hexdigest() == expected_hash
                members[member_name] = content
        tagged_java = members[next(name for name in members if name.endswith("DMatrix.java"))]
        with zipfile.ZipFile(sources_jar) as source_zip:
            published_java = source_zip.read(lock["source_jar_member"])
        assert sha256(published_java).hexdigest() == lock["source_jar_member_sha256"]
        assert published_java.replace(b"\r\n", b"\n") == tagged_java.replace(b"\r\n", b"\n")

        classes = temp / "classes"
        classes.mkdir()
        run(["javac", "--release", "21", "-cp", str(jar),
             "-d", str(classes), str(ADAPTER)])
        output = json.loads(run(["java", "-cp", f"{classes}:{jar}",
                                 "org.parsarium.MeteoInfoMatrixMarketAdapter", str(CONTROL)]))
        assert output == {"rows": 2, "cols": 3, "value_0_2": -2.0}, output
        print(json.dumps({"package": "meteoinfo-math", "version": "4.3.0",
                          "output": output, "pass": True}))


if __name__ == "__main__":
    main()
