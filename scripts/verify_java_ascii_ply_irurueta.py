"""Verify the pinned Irurueta Java PLY reader on the valid ASCII triangle."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/java/ascii_ply/irurueta-lock.json"
SOURCE = ROOT / "adapters/java/ascii_ply/irurueta/src/main/java/org/parsarium/IruruetaPlyAdapter.java"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"


def checked_download(url: str, digest: str, destination: Path) -> None:
    with urlopen(url, timeout=45) as response:
        payload = response.read()
    assert sha256(payload).hexdigest() == digest, url
    destination.write_bytes(payload)


def main() -> None:
    lock = json.loads(LOCK.read_text())
    assert sha256(CONTROL.read_bytes()).hexdigest() == (
        "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"
    )
    with tempfile.TemporaryDirectory(prefix="parsarium-irurueta-ply-") as directory:
        tmp = Path(directory)
        jars = []
        for artifact in lock["artifact_pins"]:
            stem = f"{artifact['artifact']}-{artifact['version']}"
            for kind in ("jar", "pom"):
                path = tmp / f"{stem}.{kind}"
                checked_download(artifact[f"{kind}_url"], artifact[f"{kind}_sha256"], path)
                if kind == "jar":
                    jars.append(path)
        for source in lock["tagged_source_files"]:
            checked_download(source["url"], source["sha256"], tmp / Path(source["path"]).name)
        classes = tmp / "classes"
        classes.mkdir()
        cp = ":".join(str(path) for path in jars)
        subprocess.run(["javac", "--release", "21", "-cp", cp,
                        "-d", str(classes), str(SOURCE)], cwd=ROOT, check=True)
        completed = subprocess.run(
            ["java", "-cp", f"{classes}:{cp}", "org.parsarium.IruruetaPlyAdapter",
             str(CONTROL)], cwd=ROOT, check=True, text=True, capture_output=True
        )
        output = json.loads(completed.stdout)
        assert output == {"vertices": 3, "faces": 1, "indices": [0, 1, 2]}, output
        print(json.dumps({"package": "com.irurueta:irurueta-geometry-io",
                          "version": lock["release"], "output": output, "pass": True}))


if __name__ == "__main__":
    main()
