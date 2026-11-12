"""Fetch and verify the pinned C++ AudioFile header release."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tarfile import open as taropen
from urllib.request import Request, urlopen
import json


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/wav"
CACHE = ROOT / "adapters/cpp/wav/cache"
LOCK = json.loads((DATA / "extra-source-lock.json").read_text())


def main() -> None:
    item = LOCK["audiofile"]
    archive_path = CACHE / "audiofile.tar.gz"
    if archive_path.exists() and sha256(archive_path.read_bytes()).hexdigest() == item["source_sha256"]:
        data = archive_path.read_bytes()
    else:
        request = Request(item["source_url"], headers={"User-Agent": "Parsarium-Research"})
        with urlopen(request, timeout=90) as response:
            data = response.read()
        assert sha256(data).hexdigest() == item["source_sha256"]
        CACHE.mkdir(parents=True, exist_ok=True)
        archive_path.write_bytes(data)
    with taropen(fileobj=BytesIO(data), mode="r:gz") as archive:
        for file in item["files"]:
            name, expected = file["name"], file["sha256"]
            member = archive.getmember("AudioFile-1.1.4/" + name)
            assert member.isfile()
            stream = archive.extractfile(member)
            assert stream is not None
            contents = stream.read()
            assert sha256(contents).hexdigest() == expected
            destination = CACHE / "source/audiofile" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(contents)
    print(f"audiofile@{item['release']}: pinned source, header and license verified")


if __name__ == "__main__":
    main()
