"""Source-build the tagged BTETerraRenderer Draco PLY reader and parse a control."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/java/ascii_ply/bte-draco-lock.json"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
ADAPTER = ROOT / "adapters/java/ascii_ply/bte_draco/BteDracoPlyAdapter.java"
SOURCE_PREFIX = "BTETerraRenderer-1.03.4/"
DRACO_SOURCE = "draco/src/main/java/"
COMMON_UTIL = "common/src/main/java/com/mndk/bteterrarenderer/util/"
UTIL_NAMES = {"BTRUtil.java", "IOUtil.java", "StringUtil.java"}


def fetch(url: str, expected_hash: str, destination: Path) -> None:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium BTE verifier"}),
                 timeout=90) as response:
        payload = response.read()
    assert sha256(payload).hexdigest() == expected_hash, url
    destination.write_bytes(payload)


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                            timeout=180, check=True)
    return result.stdout.strip()


def main() -> None:
    lock = json.loads(LOCK.read_text())["bteterrarenderer-draco"]
    assert sha256(CONTROL.read_bytes()).hexdigest() == lock["control_sha256"]
    with tempfile.TemporaryDirectory(prefix="parsarium-bte-draco-ply-") as folder:
        temp = Path(folder)
        archive = temp / "source.tar.gz"
        fetch(lock["source_url"], lock["source_sha256"], archive)

        sources = []
        checked = set()
        with tarfile.open(archive, "r:gz") as source:
            for member in source:
                if not member.isfile() or not member.name.startswith(SOURCE_PREFIX):
                    continue
                relative = member.name[len(SOURCE_PREFIX):]
                is_draco = relative.startswith(DRACO_SOURCE) and relative.endswith(".java")
                is_util = relative.startswith(COMMON_UTIL) and Path(relative).name in UTIL_NAMES
                is_key = relative in lock["source_members"]
                if not (is_draco or is_util or is_key):
                    continue
                handle = source.extractfile(member)
                assert handle is not None
                payload = handle.read()
                if is_key:
                    assert sha256(payload).hexdigest() == lock["source_members"][relative]
                    checked.add(relative)
                if is_draco or is_util:
                    target = temp / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(payload)
                    sources.append(target)
        assert checked == set(lock["source_members"])
        assert len(sources) == lock["expected_java_source_count"]

        jars = []
        for pin in lock["dependency_pins"]:
            for kind in ("jar", "pom"):
                target = temp / f"{pin['artifact']}-{pin['version']}.{kind}"
                fetch(pin[f"{kind}_url"], pin[f"{kind}_sha256"], target)
                if kind == "jar":
                    jars.append(target)
        lombok = next(jar for jar in jars if jar.name.startswith("lombok-"))
        classpath = ":".join(map(str, jars))
        classes = temp / "classes"
        classes.mkdir()
        run(["javac", "--release", "8", "-Xlint:-options", "-cp", classpath,
             "-processorpath", str(lombok), "-d", str(classes),
             *map(str, sources), str(ADAPTER)])
        output = json.loads(run(["java", "-cp", f"{classes}:{classpath}",
                                 "org.parsarium.BteDracoPlyAdapter", str(CONTROL)]))
        assert output == {"vertices": 3, "faces": 1, "second_x": 1.0}, output
        print(json.dumps({"package": "bteterrarenderer-draco",
                          "version": "v1.03.4", "output": output, "pass": True}))


if __name__ == "__main__":
    main()
