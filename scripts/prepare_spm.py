"""Build the hash-pinned SPM 1.2.4 C library with its pinned CMake submodule."""

from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
import tarfile


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def prepare_spm(source: dict, archive: Path, cache: Path) -> tuple[Path, Path, str]:
    tree = cache / "spm-1.2.4-source"
    submodule = source["cmake_submodule"]
    module_archive = cache / "morse-cmake-c47785f.tar.gz"
    if not module_archive.exists() or digest(module_archive) != submodule["source_sha256"]:
        subprocess.run(["curl", "-fLsS", "--max-time", "120", "-o", str(module_archive),
                        submodule["source_url"]], check=True)
    assert digest(module_archive) == submodule["source_sha256"]
    if not tree.exists() or digest(tree / "LICENSE") != source["source_members"]["spm-v1.2.4/LICENSE"]:
        shutil.rmtree(tree, ignore_errors=True)
        with tarfile.open(archive) as tar:
            tar.extractall(cache, filter="data")
        (cache / "spm-v1.2.4").rename(tree)
    module_tree = tree / "cmake_modules/morse_cmake"
    if not (module_tree / "modules/MorseInit.cmake").exists():
        with tarfile.open(module_archive) as tar:
            tar.extractall(cache, filter="data")
        extracted = cache / "morse_cmake-c47785f30d214220e3f8bcf1591a762c02892c33"
        extracted.rename(module_tree)
    for member, expected in source["source_members"].items():
        assert digest(tree / member.removeprefix("spm-v1.2.4/")) == expected, member
    assert digest(module_tree / "modules/MorseInit.cmake") == submodule["morse_init_sha256"]
    build = cache / "spm-1.2.4-build"
    openblas = Path(source["openblas_prefix"])
    if not (build / "src/libspm.a").exists():
        subprocess.run(["cmake", "-S", str(tree), "-B", str(build),
                        "-DSPM_WITH_FORTRAN=OFF", "-DSPM_WITH_MPI=OFF",
                        "-DCMAKE_BUILD_TYPE=Release", "-DBLA_VENDOR=OpenBLAS",
                        f"-DCMAKE_PREFIX_PATH={openblas}",
                        "-DCMAKE_POLICY_VERSION_MINIMUM=3.5"], check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run(["cmake", "--build", str(build), "--target", "spm", "-j6"],
                       check=True, stdout=subprocess.DEVNULL)
    library = build / "src/libspm.a"
    return tree, build, digest(library)
