"""Verify ImgLib2 Mesh 1.3.0's released local PLY reader."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import subprocess
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/java/ascii_ply/imglib2-lock.json"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
ADAPTER = ROOT / "adapters/java/ascii_ply/imglib2/src/main/java/org/parsarium/ImgLib2MeshPlyAdapter.java"


def download(url: str, expected_hash: str, destination: Path) -> None:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium ImgLib2 Mesh verifier"}),
                 timeout=60) as response:
        data = response.read()
    assert sha256(data).hexdigest() == expected_hash, url
    destination.write_bytes(data)


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                          timeout=120, check=True).stdout.strip()


def main() -> None:
    lock = json.loads(LOCK.read_text())
    assert sha256(CONTROL.read_bytes()).hexdigest() == lock["control_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-imglib2-ply-") as directory:
        temp = Path(directory)
        jars = []
        for artifact in lock["artifact_pins"]:
            stem = f"{artifact['artifact']}-{artifact['version']}"
            for kind in ("jar", "pom"):
                file = temp / f"{stem}.{kind}"
                download(artifact[f"{kind}_url"], artifact[f"{kind}_sha256"], file)
                if kind == "jar":
                    jars.append(file)
        sources = temp / "imglib2-mesh-sources.jar"
        reader = temp / "PLYMeshIO.java"
        download(lock["sources_jar_url"], lock["sources_jar_sha256"], sources)
        download(lock["tagged_reader_source_url"],
                 lock["tagged_reader_source_sha256"], reader)
        download(lock["tagged_license_url"], lock["tagged_license_sha256"],
                 temp / "LICENSE.txt")
        download(lock["parent_pom_url"], lock["parent_pom_sha256"],
                 temp / "pom-scijava-45.1.0.pom")
        with zipfile.ZipFile(sources) as source:
            assert source.read(lock["source_jar_member"]) == reader.read_bytes()

        classes = temp / "classes"
        classes.mkdir()
        cp = ":".join(str(jar) for jar in jars)
        run(["javac", "--release", "21", "-cp", cp,
             "-d", str(classes), str(ADAPTER)])
        output = json.loads(run(["java", "-cp", f"{classes}:{cp}",
                                 "org.parsarium.ImgLib2MeshPlyAdapter", str(CONTROL)]))
        assert output == {"vertices": 3, "faces": 1}, output
        print(json.dumps({"package": "imglib2-mesh", "version": "1.3.0",
                          "output": output, "pass": True}))


if __name__ == "__main__":
    main()
