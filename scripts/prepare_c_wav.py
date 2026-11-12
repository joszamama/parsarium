"""Download pinned C WAV sources and verify the extracted public headers."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tarfile import open as taropen
from urllib.request import Request, urlopen
import json


ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "data/c/wav/source-lock.json").read_text())
CACHE = ROOT / "adapters/c/wav/cache"


def main() -> None:
    for name in ("dr_wav", "miniaudio"):
        item = LOCK[name]
        archive_path = CACHE / (name + ".tar.gz")
        if archive_path.exists() and sha256(archive_path.read_bytes()).hexdigest() == item["source_sha256"]:
            data = archive_path.read_bytes()
        else:
            request = Request(item["source_url"], headers={"User-Agent": "Parsarium-Research"})
            with urlopen(request, timeout=60) as response:
                data = response.read()
            assert sha256(data).hexdigest() == item["source_sha256"], name
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            archive_path.write_bytes(data)
        with taropen(fileobj=BytesIO(data), mode="r:gz") as archive:
            members = [member for member in archive.getmembers() if member.isfile()]
            for file in item["files"]:
                matches = [member for member in members if
                           member.name.count("/") == 1 and member.name.endswith("/" + file["name"])]
                assert len(matches) == 1, (name, file["name"])
                stream = archive.extractfile(matches[0])
                assert stream is not None
                contents = stream.read()
                assert sha256(contents).hexdigest() == file["sha256"], (name, file["name"])
                destination = CACHE / "source" / name / file["name"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(contents)
        print(f"{name}@{item['release']}: pinned source and files verified")
    prepare_libaudiofile()
    prepare_sdl2()


def prepare_libaudiofile() -> None:
    item = LOCK["libaudiofile"]
    archive_path = CACHE / "libaudiofile.tar.xz"
    if archive_path.exists() and sha256(archive_path.read_bytes()).hexdigest() == item["source_sha256"]:
        data = archive_path.read_bytes()
    else:
        request = Request(item["source_url"], headers={"User-Agent": "Parsarium-Research"})
        with urlopen(request, timeout=60) as response:
            data = response.read()
        assert sha256(data).hexdigest() == item["source_sha256"]
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_path.write_bytes(data)
    destination_root = CACHE / "source/audiofile"
    with taropen(fileobj=BytesIO(data), mode="r:xz") as archive:
        for member in archive:
            parts = Path(member.name).parts
            assert parts and parts[0] == "audiofile-0.3.6" and ".." not in parts
            assert member.isfile() or member.isdir(), member.name
            if not member.isfile():
                continue
            stream = archive.extractfile(member)
            assert stream is not None
            destination = destination_root.joinpath(*parts[1:])
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(stream.read())
            destination.chmod(member.mode)
    source = destination_root / "libaudiofile/modules/SimpleModule.h"
    original = "static const int kMinSignedValue = -1 << kScaleBits;"
    patched = "static const int kMinSignedValue = static_cast<int>(~((1U << kScaleBits) - 1U));"
    contents = source.read_text()
    assert contents.count(original) == 1
    source.write_text(contents.replace(original, patched))
    print(f"libaudiofile@{item['release']}: pinned source verified; signed-shift build patch applied")


def prepare_sdl2() -> None:
    item = LOCK["sdl2"]
    archive_path = CACHE / "sdl2.tar.gz"
    if archive_path.exists() and sha256(archive_path.read_bytes()).hexdigest() == item["source_sha256"]:
        data = archive_path.read_bytes()
    else:
        request = Request(item["source_url"], headers={"User-Agent": "Parsarium-Research"})
        with urlopen(request, timeout=60) as response:
            data = response.read()
        assert sha256(data).hexdigest() == item["source_sha256"]
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_path.write_bytes(data)
    destination_root = CACHE / "source/sdl2"
    skipped = []
    with taropen(fileobj=BytesIO(data), mode="r:gz") as archive:
        for member in archive:
            parts = Path(member.name).parts
            assert parts and parts[0] == "SDL2-2.32.10" and ".." not in parts
            if member.issym():
                skipped.append("/".join(parts[1:]))
                continue
            assert member.isfile(), member.name
            stream = archive.extractfile(member)
            assert stream is not None
            destination = destination_root.joinpath(*parts[1:])
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(stream.read())
            destination.chmod(member.mode)
    assert sorted(skipped) == ["android-project-ant/AndroidManifest.xml",
                               "android-project-ant/src"]
    print(f"sdl2@{item['release']}: pinned source verified; two Android-only symlinks skipped")


if __name__ == "__main__":
    main()
