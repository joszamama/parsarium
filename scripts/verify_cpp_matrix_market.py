"""Verify the C++ Matrix Market cell against pinned source and a valid matrix."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import shlex
import shutil
import subprocess
import tarfile
import tempfile

from prepare_lis import prepare_lis
from prepare_lagraph import prepare_lagraph
from prepare_librsb import prepare_librsb
from prepare_superlu_dist import prepare_superlu_dist


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/matrix_market"
CONTROL = ROOT / "controls/matrix_market/real-general.mtx"
CONTROL_SHA256 = "65614ddf08f46422a1f6f71d67bdc4490e84635b3cc61dfe089c82c41829da4c"
SYMMETRIC_CONTROL = ROOT / "controls/matrix_market/real-symmetric.mtx"
SYMMETRIC_CONTROL_SHA256 = "53a869970ef0ddf0707dc5ff9a46f4a1daa380e7ff6055e79fa5314103d61cbd"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def main() -> None:
    assert digest(CONTROL) == CONTROL_SHA256
    assert digest(SYMMETRIC_CONTROL) == SYMMETRIC_CONTROL_SHA256
    parsers = json.loads((DATA / "parsers.json").read_text())
    sources = json.loads((DATA / "source-lock.json").read_text())
    assert len(parsers) == json.loads((DATA / "cell.json").read_text())["verified_third_party_count"]
    cache = Path(tempfile.gettempdir()) / "parsarium-native-matrix-market"
    cache.mkdir(exist_ok=True)
    target = ROOT / "adapters/cpp/matrix_market/target"
    target.mkdir(exist_ok=True)
    rows = []
    local_libraries = {}
    for parser in parsers:
        name = parser["name"]
        source = sources[name]
        suffix = {"zip": ".zip", "bz2": ".tar.bz2"}.get(source.get("archive_format"), ".tar.gz")
        archive = cache / f"{name}-{source['release']}{suffix}"
        if not archive.exists() or digest(archive) != source["source_sha256"]:
            if source.get("local_source_archive"):
                local_archive = ROOT / source["local_source_archive"]
                assert digest(local_archive) == source["source_sha256"]
                shutil.copyfile(local_archive, archive)
            else:
                with urlopen(Request(source["source_url"], headers={"User-Agent": "Parsarium Matrix Market verifier"}), timeout=120) as response, archive.open("wb") as output:
                    while chunk := response.read(1024 * 1024):
                        output.write(chunk)
        assert digest(archive) == source["source_sha256"]
        if source.get("source_build") == "lis":
            install, built_lib_sha256 = prepare_lis(source, archive, cache)
        elif source.get("source_build") == "lagraph":
            include, libdir, built_lib_sha256 = prepare_lagraph(source, archive, cache)
        elif source.get("source_build") == "librsb":
            install, built_lib_sha256 = prepare_librsb(source, archive, cache)
        elif source.get("source_build") == "superlu_dist":
            include, libdir, built_lib_sha256 = prepare_superlu_dist(source, archive, cache)
        else:
            with tarfile.open(archive) as tar:
                for member, expected in source["source_members"].items():
                    file = tar.extractfile(member)
                    assert file is not None and sha256(file.read()).hexdigest() == expected, member
                if source.get("source_build") in ("header_only", "taco", "trilinos"):
                    root = source["archive_root"]
                    for member in tar.getmembers():
                        member_path = Path(member.name)
                        assert not member_path.is_absolute() and ".." not in member_path.parts
                        assert member.name == root or member.name.startswith(root + "/")
                    sentinel = source.get("extract_sentinel", "include")
                    if not (cache / root / sentinel).exists():
                        tar.extractall(cache, filter="data")
                    for member, expected in source["source_members"].items():
                        assert digest(cache / member) == expected, member
        for dependency in source.get("dependencies", []):
            dep_archive = cache / f"{dependency['name']}-{dependency['release']}.tar.gz"
            if not dep_archive.exists() or digest(dep_archive) != dependency["source_sha256"]:
                with urlopen(Request(dependency["source_url"], headers={"User-Agent": "Parsarium Matrix Market verifier"}), timeout=120) as response, dep_archive.open("wb") as output:
                    while chunk := response.read(1024 * 1024):
                        output.write(chunk)
            assert digest(dep_archive) == dependency["source_sha256"]
            with tarfile.open(dep_archive) as dep_tar:
                for member, expected in dependency["source_members"].items():
                    file = dep_tar.extractfile(member)
                    assert file is not None and sha256(file.read()).hexdigest() == expected, member
                root = dependency["archive_root"]
                for member in dep_tar.getmembers():
                    member_path = Path(member.name)
                    assert not member_path.is_absolute() and ".." not in member_path.parts
                    assert member.name == root or member.name.startswith(root + "/")
                if not (cache / root / "include").exists():
                    dep_tar.extractall(cache, filter="data")
        for path, expected in source.get("installed_files", {}).items():
            assert digest(Path(path)) == expected, path
        if source.get("formula"):
            assert source["installed_revision"] in run(["brew", "list", "--versions", source["formula"]]).split()
        if name == "eigen":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", source["include_dir"], str(ROOT / parser["adapter"]),
                       "-o", str(target / name)]
        elif name == "suite-sparse":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "cholmod"]))
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags,
                       "-o", str(target / name)]
        elif name == "fast-matrix-market":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(cache / source["archive_root"] / "include"),
                       str(ROOT / parser["adapter"]), "-o", str(target / name)]
        elif name == "pigo":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(cache / source["archive_root"] / "include"),
                       str(ROOT / parser["adapter"]), "-o", str(target / name)]
        elif name == "tatami-mtx":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(cache / source["archive_root"] / "include"),
                       *[flag for dep in source["dependencies"]
                         for flag in ("-isystem", str(cache / dep["archive_root"] / "include"))],
                       str(ROOT / parser["adapter"]), "-lz", "-o", str(target / name)]
        elif name == "seldon":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-Wno-unused-parameter", "-Wno-unused-but-set-variable",
                       "-iquote", str(cache / source["archive_root"]),
                       str(ROOT / parser["adapter"]), "-o", str(target / name)]
        elif name == "hifir":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(cache / source["archive_root"] / "src"),
                       str(ROOT / parser["adapter"]), "-o", str(target / name)]
        elif name == "taco":
            taco_root = cache / source["archive_root"]
            taco_build = cache / "taco-build-v0.1"
            taco_library = taco_build / "lib/libtaco.a"
            if not taco_library.exists():
                run(["cmake", "-S", str(taco_root), "-B", str(taco_build),
                     "-DCMAKE_POLICY_VERSION_MINIMUM=3.5", "-DCMAKE_BUILD_TYPE=Release",
                     "-DTACO_SHARED_LIBRARY=OFF"])
                run(["cmake", "--build", str(taco_build), "--target", "taco", "-j4"])
            built_lib_sha256 = digest(taco_library)
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(taco_root / "include"),
                       str(ROOT / parser["adapter"]), str(taco_library),
                       "-o", str(target / name)]
        elif name == "trilinos":
            trilinos_root = cache / source["archive_root"]
            trilinos_build = cache / "trilinos-build-17.3.0"
            teuchos_library = trilinos_build / "packages/teuchos/numerics/src/libteuchosnumerics.a"
            if not teuchos_library.exists():
                run(["cmake", "-S", str(trilinos_root), "-B", str(trilinos_build),
                     "-DTrilinos_ENABLE_Teuchos=ON", "-DTrilinos_ENABLE_ALL_PACKAGES=OFF",
                     "-DTrilinos_ENABLE_TESTS=OFF", "-DTrilinos_ENABLE_EXAMPLES=OFF",
                     "-DBUILD_SHARED_LIBS=OFF", "-DCMAKE_BUILD_TYPE=Release"])
                run(["cmake", "--build", str(trilinos_build), "--target", "teuchosnumerics", "-j8"])
            built_lib_sha256 = digest(teuchos_library)
            adapter_build = cache / "trilinos-adapter-build-17.3.0"
            run(["cmake", "-S", str(ROOT / "adapters/cpp/matrix_market/trilinos"),
                 "-B", str(adapter_build),
                 "-DTeuchosNumerics_DIR=" + str(trilinos_build / "cmake_packages/TeuchosNumerics"),
                 "-DCMAKE_RUNTIME_OUTPUT_DIRECTORY=" + str(target),
                 "-DCMAKE_BUILD_TYPE=Release"])
            command = ["cmake", "--build", str(adapter_build), "--target", "parsarium_trilinos", "-j4"]
        elif name == "gsl":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "gsl"]))
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags, "-o", str(target / name)]
        elif name == "eminem":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(cache / source["archive_root"] / "include"),
                       *[flag for dep in source["dependencies"]
                         for flag in ("-isystem", str(cache / dep["archive_root"] / "include"))],
                       str(ROOT / parser["adapter"]), "-o", str(target / name)]
        elif name == "ginkgo":
            prefix = Path(source["prefix"])
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(prefix / "include"), str(ROOT / parser["adapter"]),
                       "-L" + str(prefix / "lib"), "-Wl,-rpath," + str(prefix / "lib"),
                       "-lginkgo", "-o", str(target / name)]
        elif name == "viennacl":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", source["include_dir"], str(ROOT / parser["adapter"]),
                       "-o", str(target / name)]
        elif name == "mtl5":
            command = ["c++", "-std=c++20", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(cache / source["archive_root"] / "include"),
                       str(ROOT / parser["adapter"]), "-o", str(target / name)]
        elif name == "hypre":
            prefix = Path(source["prefix"])
            command = ["mpic++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(prefix / "include"), str(ROOT / parser["adapter"]),
                       "-L" + str(prefix / "lib"), "-Wl,-rpath," + str(prefix / "lib"),
                       "-lHYPRE", "-o", str(target / name)]
        elif name == "lagraph":
            graphblas = Path(source["graphblas_prefix"])
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(include), "-I" + str(graphblas / "include/suitesparse"),
                       str(ROOT / parser["adapter"]), "-L" + str(libdir),
                       "-Wl,-rpath," + str(libdir), "-llagraph",
                       "-L" + str(graphblas / "lib"), "-lgraphblas", "-o", str(target / name)]
        elif name == "librsb":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(install / "include"), str(ROOT / parser["adapter"]),
                       str(install / "lib/librsb.a"), "-lm", "-lz",
                       "-o", str(target / name)]
        elif name == "superlu":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "superlu"]))
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags, "-o", str(target / name)]
        elif name == "superlu-dist":
            command = ["mpic++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(include), str(ROOT / parser["adapter"]),
                       "-L" + str(libdir), "-Wl,-rpath," + str(libdir),
                       "-lsuperlu_dist", "-o", str(target / name)]
        elif name == "lis":
            command = ["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(install / "include"), str(ROOT / parser["adapter"]),
                       str(install / "lib/liblis.a"), "-lm", "-o", str(target / name)]
        else:
            raise ValueError(name)
        run(command)
        execute = [str(target / name), str(ROOT / parser["control"])]
        output = json.loads(run(execute).splitlines()[-1])
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"], "control": parser["control"],
                     "build_command": shlex.join(command), "command": shlex.join(execute),
                     "output": output, "pass": True})
        local_libraries[name] = {"source_sha256": source["source_sha256"],
                                 "installed_files": source.get("installed_files", {})}
        if source.get("dependencies"):
            local_libraries[name]["dependency_source_sha256"] = {
                dep["name"]: dep["source_sha256"] for dep in source["dependencies"]}
        if source.get("source_build") in ("lis", "lagraph", "librsb", "superlu_dist", "taco", "trilinos"):
            local_libraries[name]["built_lib_sha256"] = built_lib_sha256
        print(f"{name}@{parser['version']}: C++ Matrix Market passed", flush=True)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["c++", "--version"]).splitlines()[0],
              "source_lock": "data/cpp/matrix_market/source-lock.json",
              "local_libraries": local_libraries,
              "control": "controls/matrix_market/real-general.mtx", "control_sha256": CONTROL_SHA256,
              "additional_controls": {"controls/matrix_market/real-symmetric.mtx": SYMMETRIC_CONTROL_SHA256},
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
