"""Build the hash-pinned clSPARSE release for the C Matrix Market adapter."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import shutil
import subprocess
import tarfile


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def download(url: str, destination: Path, expected: str) -> None:
    if not destination.exists() or digest(destination) != expected:
        with urlopen(Request(url, headers={"User-Agent": "Parsarium verifier"}), timeout=120) as source:
            with destination.open("wb") as output:
                shutil.copyfileobj(source, output)
    assert digest(destination) == expected, destination


def prepare_clsparse(source: dict, archive: Path, cache: Path) -> tuple[Path, Path, str]:
    tree = cache / "clSPARSE-0.10.2.0"
    build = cache / "clSPARSE-0.10.2.0-build"
    if not tree.exists():
        with tarfile.open(archive) as tar:
            tar.extractall(cache, filter="data")
    for member, expected in source["source_members"].items():
        assert digest(cache / member) == expected, member

    dependency = source["clhpp"]
    clhpp_archive = cache / "OpenCL-CLHPP-75bb7d0.tar.gz"
    download(dependency["source_url"], clhpp_archive, dependency["source_sha256"])
    include = cache / "clSPARSE-0.10.2.0-clhpp" / "CL"
    include.mkdir(parents=True, exist_ok=True)
    with tarfile.open(clhpp_archive) as tar:
        member = tar.extractfile(dependency["archive_member"])
        assert member is not None
        header = member.read()
    assert sha256(header).hexdigest() == dependency["header_sha256"]
    (include / "cl2.hpp").write_bytes(header)

    configure = [
        "cmake", "-S", str(tree / "src"), "-B", str(build),
        "-DCMAKE_POLICY_VERSION_MINIMUM=3.5", "-DCMAKE_BUILD_TYPE=Release",
        "-DBUILD_TESTS=OFF", "-DBUILD_BENCHMARKS=OFF",
        "-DBUILD_CLVERSION=1.2", "-DUSE_SYSTEM_CL2HPP=ON",
        f"-DCL2HPP_INCLUDE_DIRECTORY={include.parent}",
    ]
    subprocess.run(configure, check=True, capture_output=True, text=True, timeout=120)
    subprocess.run(["cmake", "--build", str(build), "--target", "clSPARSE", "-j", "4"],
                   check=True, capture_output=True, text=True, timeout=600)
    library = build / "library/libclSPARSE.1.dylib"
    assert library.is_file()
    return tree, build, digest(library)
