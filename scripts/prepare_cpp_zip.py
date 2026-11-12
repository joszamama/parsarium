"""Fetch SHA-256-pinned C++ ZIP wrapper releases into the ignored cache."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path, PurePosixPath
from tarfile import open as taropen
from urllib.request import Request, urlopen
import json


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "adapters/cpp/zip/cache"
LOCK = json.loads((ROOT / "data/cpp/zip/extra-source-lock.json").read_text())


def prepare(name: str, item: dict, destination_root: Path) -> None:
    archive_path = CACHE / (name + ".tar.gz")
    if archive_path.exists() and sha256(archive_path.read_bytes()).hexdigest() == item["source_sha256"]:
        data = archive_path.read_bytes()
    else:
        request = Request(item["source_url"], headers={"User-Agent": "Parsarium-Research"})
        with urlopen(request, timeout=45) as response:
            data = response.read()
        assert sha256(data).hexdigest() == item["source_sha256"], name
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_path.write_bytes(data)
    with taropen(fileobj=BytesIO(data), mode="r:gz") as archive:
        members = archive.getmembers()
        prefixes = {PurePosixPath(member.name).parts[0] for member in members}
        assert len(prefixes) == 1
        prefix = prefixes.pop()
        for member in members:
            parts = PurePosixPath(member.name).parts
            assert parts and parts[0] == prefix and ".." not in parts
            assert member.isfile() or member.isdir(), member.name
            if not member.isfile():
                continue
            destination = destination_root / Path(*parts[1:])
            destination.parent.mkdir(parents=True, exist_ok=True)
            file = archive.extractfile(member)
            assert file is not None
            destination.write_bytes(file.read())
            destination.chmod(member.mode)


def main() -> None:
    for name, item in LOCK.items():
        prepare(name, item, CACHE / name)
        for subname, subitem in item.get("submodules", {}).items():
            prepare(name + "-" + subname, subitem, CACHE / name / "external" / subname)
        print(f"{name}: pinned {item['release']} source verified")


if __name__ == "__main__":
    main()
