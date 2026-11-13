"""Build the pinned BeBOP Matrix Market C reader and utility dependency."""

from hashlib import sha256
from pathlib import Path
import shlex
import subprocess
import tarfile


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def execute(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")


def download_pinned(url: str, archive: Path, expected: str) -> None:
    if not archive.exists() or digest(archive) != expected:
        execute(["curl", "--fail", "--location", "--silent", "--show-error",
                 "--output", str(archive), url])
    assert digest(archive) == expected, archive


def checked_extract(archive: Path, parent: Path, root: str, members: dict[str, str]) -> None:
    with tarfile.open(archive) as tar:
        for entry in tar.getmembers():
            path = Path(entry.name)
            if path.is_absolute() or ".." in path.parts or not (
                entry.name == root or entry.name.startswith(root + "/")
            ):
                raise ValueError(f"unsafe BeBOP archive path: {entry.name}")
        for member, expected in members.items():
            source = tar.extractfile(member)
            assert source is not None
            assert sha256(source.read()).hexdigest() == expected, member
        if not (parent / root).exists():
            tar.extractall(parent, filter="data")
    for member, expected in members.items():
        assert digest(parent / member) == expected, member


def prepare_bebop_smc(source: dict, archive: Path, cache: Path) -> tuple[Path, Path, Path, Path, dict[str, str]]:
    parent = cache / "bebop-smc-2009-12-11"
    parent.mkdir(parents=True, exist_ok=True)
    checked_extract(archive, parent, "sparse_matrix_converter", source["source_members"])
    for name, dependency in source["dependencies"].items():
        dependency_archive = cache / f"bebop-{name}-{dependency['release']}.tar.gz"
        download_pinned(dependency["source_url"], dependency_archive,
                        dependency["source_sha256"])
        checked_extract(dependency_archive, parent, dependency["archive_root"], dependency["source_members"])
    util = parent / "bebop_util"
    smc = parent / "sparse_matrix_converter"
    execute(["make", "-C", str(util / "src"), "-j4"])
    execute(["make", "-C", str(smc / "src"), "-j4"])
    smc_library = smc / "libsparse_matrix_converter.a"
    util_library = util / "libbebop_util.a"
    return (smc / "include", util / "include", smc_library, util_library,
            {"smc": digest(smc_library), "util": digest(util_library)})
