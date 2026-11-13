"""Verify JMIST Core 0.1.3's released PLY event reader."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import subprocess
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/java/ascii_ply/jmist-lock.json"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
ADAPTER = ROOT / "adapters/java/ascii_ply/jmist/src/main/java/org/parsarium/JmistPlyAdapter.java"


def download(url: str, expected_hash: str, destination: Path) -> None:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium JMIST verifier"}),
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
    with tempfile.TemporaryDirectory(prefix="parsarium-jmist-ply-") as directory:
        temp = Path(directory)
        jars = []
        for artifact in lock["artifact_pins"]:
            stem = f"{artifact['artifact']}-{artifact['version']}"
            for kind in ("jar", "pom"):
                file = temp / f"{stem}.{kind}"
                download(artifact[f"{kind}_url"], artifact[f"{kind}_sha256"], file)
                if kind == "jar":
                    jars.append(file)
        sources = temp / "jmist-core-sources.jar"
        download(lock["sources_jar_url"], lock["sources_jar_sha256"], sources)
        download(lock["parent_pom_url"], lock["parent_pom_sha256"],
                 temp / "jmist-0.1.3.pom")
        with zipfile.ZipFile(sources) as source:
            for tagged in lock["tagged_source_files"]:
                local = temp / Path(tagged["path"]).name
                download(tagged["url"], tagged["sha256"], local)
                if tagged["path"].endswith(".java"):
                    member = tagged["path"].split("/src/main/java/", 1)[1]
                    assert source.read(member) == local.read_bytes(), member

        classes = temp / "classes"
        classes.mkdir()
        cp = ":".join(str(jar) for jar in jars)
        run(["javac", "--release", "21", "-cp", cp,
             "-d", str(classes), str(ADAPTER)])
        output = json.loads(run(["java", "-cp", f"{classes}:{cp}",
                                 "org.parsarium.JmistPlyAdapter", str(CONTROL)]))
        assert output == {"vertices": 3, "faces": 1, "second_x": 1.0,
                          "indices": [0, 1, 2]}, output
        print(json.dumps({"package": "jmist-core", "version": "0.1.3",
                          "output": output, "pass": True}))


if __name__ == "__main__":
    main()
