"""Fetch pinned native C++ ASCII PNM reader sources."""

from hashlib import sha256
from pathlib import Path
from urllib.request import urlopen
import json
import subprocess
import tarfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "data/cpp/ascii_pnm/extra-source-lock.json").read_text())
CACHE = ROOT / "adapters/cpp/ascii_pnm/cache"
ARCHIVE = CACHE / "CImg-v.4.0.5.tar.gz"
HEADER = CACHE / "CImg-v.4.0.5/CImg.h"
GIL_ARCHIVE = CACHE / "gil-boost-1.92.0.tar.gz"
GIL_INCLUDE = CACHE / "gil-boost-1.92.0/include"
PNMPP_ARCHIVE = CACHE / "pnmpp-v1.0.1.tar.gz"
PNMPP_INCLUDE = CACHE / "pnmpp-v1.0.1-patched"


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    cimg = LOCK["cimg"]
    if not ARCHIVE.exists():
        with urlopen(cimg["source_url"], timeout=45) as response:
            ARCHIVE.write_bytes(response.read())
    assert sha256(ARCHIVE.read_bytes()).hexdigest() == cimg["source_sha256"]
    with tarfile.open(ARCHIVE, "r:gz") as archive:
        source = archive.extractfile("CImg-v.4.0.5/CImg.h")
        assert source is not None
        data = source.read()
    assert sha256(data).hexdigest() == cimg["files"][0]["sha256"]
    HEADER.parent.mkdir(parents=True, exist_ok=True)
    HEADER.write_bytes(data)

    gil = LOCK["boost-gil"]
    if not GIL_ARCHIVE.exists():
        with urlopen(gil["source_url"], timeout=45) as response:
            GIL_ARCHIVE.write_bytes(response.read())
    assert sha256(GIL_ARCHIVE.read_bytes()).hexdigest() == gil["source_sha256"]
    with tarfile.open(GIL_ARCHIVE, "r:gz") as archive:
        for member in archive:
            if not member.isfile() or not member.name.startswith("gil-boost-1.92.0/include/"):
                continue
            relative = Path(member.name).relative_to("gil-boost-1.92.0")
            assert ".." not in relative.parts
            target = CACHE / "gil-boost-1.92.0" / relative
            source = archive.extractfile(member)
            assert source is not None
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read())
    for file in gil["files"]:
        assert sha256((CACHE / "gil-boost-1.92.0" / file["path"]).read_bytes()).hexdigest() == file["sha256"]
    installed = subprocess.run(["brew", "list", "--versions", "boost"],
                               text=True, capture_output=True, check=True).stdout.strip()
    assert installed == f"boost {gil['base_boost_release']}"
    assert sha256(Path(gil["base_header"]).read_bytes()).hexdigest() == gil["base_header_sha256"]

    pnmpp = LOCK["pnmpp"]
    if not PNMPP_ARCHIVE.exists():
        with urlopen(pnmpp["source_url"], timeout=45) as response:
            PNMPP_ARCHIVE.write_bytes(response.read())
    assert sha256(PNMPP_ARCHIVE.read_bytes()).hexdigest() == pnmpp["source_sha256"]
    with tarfile.open(PNMPP_ARCHIVE, "r:gz") as archive:
        source = archive.extractfile("pnm-1.0.1/pnm.hpp")
        assert source is not None
        original = source.read()
    assert sha256(original).hexdigest() == pnmpp["files"][0]["sha256"]
    header = original.decode()
    for old, replacement in (
        ("this->iy_ <  rhs.ny_", "this->iy_ <  rhs.iy_"),
        ("this->iy_ >  rhs.ny_", "this->iy_ >  rhs.iy_"),
        ("this->iy_ <= rhs.ny_", "this->iy_ <= rhs.iy_"),
        ("this->iy_ >= rhs.ny_", "this->iy_ >= rhs.iy_"),
    ):
        assert header.count(old) == 2
        header = header.replace(old, replacement)
    patched = header.encode()
    assert sha256(patched).hexdigest() == pnmpp["patched_header_sha256"]
    PNMPP_INCLUDE.mkdir(parents=True, exist_ok=True)
    (PNMPP_INCLUDE / "pnm.hpp").write_bytes(patched)

    wx = LOCK["wxwidgets"]
    installed_wx = subprocess.run(["brew", "list", "--versions", "wxwidgets"],
                                  text=True, capture_output=True, check=True).stdout.strip()
    assert installed_wx == f"wxwidgets {wx['release']}"
    wx_config = subprocess.run(["wx-config", "--version"], text=True,
                               capture_output=True, check=True).stdout.strip()
    assert wx_config == wx["release"]
    for library in wx["local_libraries"]:
        assert sha256(Path(library["path"]).read_bytes()).hexdigest() == library["sha256"]
    qt = LOCK["qtbase"]
    installed_qt = subprocess.run(["brew", "list", "--versions", "qtbase"],
                                  text=True, capture_output=True, check=True).stdout.strip()
    assert installed_qt == f"qtbase {qt['homebrew_formula_revision']}"
    qt_version = subprocess.run(["pkg-config", "--modversion", "Qt6Gui"],
                                text=True, capture_output=True, check=True).stdout.strip()
    assert qt_version == qt["pkg_config_version"]
    for library in qt["local_libraries"]:
        assert sha256(Path(library["path"]).read_bytes()).hexdigest() == library["sha256"]
    oiio = LOCK["openimageio"]
    installed_oiio = subprocess.run(["brew", "list", "--versions", "openimageio"],
                                   text=True, capture_output=True, check=True).stdout.strip()
    assert installed_oiio == f"openimageio {oiio['homebrew_formula_revision']}"
    oiio_version = subprocess.run(["pkg-config", "--modversion", "OpenImageIO"],
                                  text=True, capture_output=True, check=True).stdout.strip()
    assert oiio_version == oiio["release"]
    for file in oiio["local_files"]:
        assert sha256(Path(file["path"]).read_bytes()).hexdigest() == file["sha256"]
    print("CImg, Boost.GIL, pnm++, wxWidgets, QtBase, and OpenImageIO release pins verified")


if __name__ == "__main__":
    main()
