"""Verify the C Matrix Market cell against pinned source and a valid matrix."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import shlex
import subprocess
import tarfile
import tempfile

from prepare_lis import prepare_lis
from prepare_lagraph import prepare_lagraph
from prepare_librsb import prepare_librsb
from prepare_superlu_dist import prepare_superlu_dist
from prepare_bebop_smc import download_pinned, prepare_bebop_smc
from prepare_libmtx import prepare_libmtx
from prepare_spm import prepare_spm
from prepare_clsparse import prepare_clsparse


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/matrix_market"
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
    target = ROOT / "adapters/c/matrix_market/target"
    target.mkdir(exist_ok=True)
    rows = []
    local_libraries = {}
    for parser in parsers:
        name = parser["name"]
        source = sources[name]
        if name == "nist-mmio":
            source_dir = cache / "nist-mmio-2007-12-20"
            source_dir.mkdir(exist_ok=True)
            for filename, pinned in source["source_files"].items():
                path = source_dir / filename
                if not path.exists() or digest(path) != pinned["sha256"]:
                    run(["curl", "-fsSL", "-A", "Mozilla/5.0 Parsarium verifier",
                         "-o", str(path), pinned["url"]])
                assert digest(path) == pinned["sha256"], filename
            assert digest(source_dir / "mmio.c") == source["source_sha256"]
            object_path = source_dir / "mmio.o"
            source_command = ["cc", "-std=c11", "-O2", "-c", str(source_dir / "mmio.c"),
                              "-o", str(object_path)]
            run(source_command)
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(source_dir), str(ROOT / parser["adapter"]),
                       str(object_path), "-o", str(target / name)]
            run(command)
            execute = [str(target / name), str(ROOT / parser["control"])]
            output = json.loads(run(execute))
            assert output == parser["expected_output"], (name, output)
            rows.append({"package": name, "version": parser["version"], "control": parser["control"],
                         "build_command": shlex.join(source_command) + " && " + shlex.join(command),
                         "command": shlex.join(execute), "output": output, "pass": True})
            local_libraries[name] = {"source_sha256": source["source_sha256"],
                                     "header_sha256": source["source_files"]["mmio.h"]["sha256"],
                                     "built_object_sha256": digest(object_path)}
            print(f"{name}@{parser['version']}: C Matrix Market passed", flush=True)
            continue
        archive = cache / f"{name}-{source['release']}{'.zip' if source.get('source_build') == 'lis' else '.tar.gz'}"
        if source.get("source_build") == "bebop_smc":
            download_pinned(source["source_url"], archive, source["source_sha256"])
        elif not archive.exists() or digest(archive) != source["source_sha256"]:
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
        elif source.get("source_build") == "bebop_smc":
            smc_include, util_include, smc_library, util_library, built_lib_sha256 = prepare_bebop_smc(source, archive, cache)
        elif source.get("source_build") == "libmtx":
            libmtx_tree, libmtx_build, libmtx_install, built_lib_sha256 = prepare_libmtx(source, archive, cache)
        elif source.get("source_build") == "spm":
            spm_tree, spm_build, built_lib_sha256 = prepare_spm(source, archive, cache)
        elif source.get("source_build") == "clsparse":
            clsparse_tree, clsparse_build, built_lib_sha256 = prepare_clsparse(source, archive, cache)
        else:
            with tarfile.open(archive) as tar:
                for member, expected in source["source_members"].items():
                    file = tar.extractfile(member)
                    assert file is not None and sha256(file.read()).hexdigest() == expected, member
        for path, expected in source.get("installed_files", {}).items():
            assert digest(Path(path)) == expected, path
        if source.get("formula"):
            assert source["installed_revision"] in run(["brew", "list", "--versions", source["formula"]]).split()
        if name == "suite-sparse":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "cholmod"]))
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags,
                       "-o", str(target / name)]
        elif name == "lis":
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(install / "include"), str(ROOT / parser["adapter"]),
                       str(install / "lib/liblis.a"), "-lm", "-o", str(target / name)]
        elif name == "hypre":
            prefix = Path(source["prefix"])
            command = ["mpicc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(prefix / "include"), str(ROOT / parser["adapter"]),
                       "-L" + str(prefix / "lib"), "-Wl,-rpath," + str(prefix / "lib"),
                       "-lHYPRE", "-o", str(target / name)]
        elif name == "lagraph":
            graphblas = Path(source["graphblas_prefix"])
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(include), "-I" + str(graphblas / "include/suitesparse"),
                       str(ROOT / parser["adapter"]), "-L" + str(libdir),
                       "-Wl,-rpath," + str(libdir), "-llagraph",
                       "-L" + str(graphblas / "lib"), "-lgraphblas", "-o", str(target / name)]
        elif name == "librsb":
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(install / "include"), str(ROOT / parser["adapter"]),
                       str(install / "lib/librsb.a"), "-lc++", "-lm", "-lz",
                       "-o", str(target / name)]
        elif name == "superlu":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "superlu"]))
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags, "-o", str(target / name)]
        elif name == "superlu-dist":
            command = ["mpicc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(include), str(ROOT / parser["adapter"]),
                       "-L" + str(libdir), "-Wl,-rpath," + str(libdir),
                       "-lsuperlu_dist", "-o", str(target / name)]
        elif name == "gsl":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "gsl"]))
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags, "-o", str(target / name)]
        elif name == "bebop-smc":
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(smc_include), "-I" + str(util_include),
                       str(ROOT / parser["adapter"]), str(smc_library),
                       str(util_library), "-lm", "-lpthread", "-o", str(target / name)]
        elif name == "libmtx":
            openblas = Path(source["openblas_prefix"])
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(libmtx_build), "-I" + str(libmtx_tree),
                       str(ROOT / parser["adapter"]),
                       "-L" + str(libmtx_install / "lib"), "-lmtx",
                       "-L" + str(openblas / "lib"), "-lopenblas",
                       "-o", str(target / name)]
        elif name == "spm":
            openblas = Path(source["openblas_prefix"])
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(spm_tree / "include"), "-I" + str(spm_build / "include"),
                       str(ROOT / parser["adapter"]), str(spm_build / "src/libspm.a"),
                       "-L" + str(openblas / "lib"), "-lopenblas", "-lm",
                       "-o", str(target / name)]
        elif name == "clsparse":
            libdir = clsparse_build / "library"
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       "-Wno-deprecated-declarations", "-DBUILD_CLVERSION=120",
                       "-DCLSPARSE_INDEX_SIZEOF=4",
                       "-I" + str(clsparse_tree / "src/include"),
                       "-I" + str(libdir), str(ROOT / parser["adapter"]),
                       "-L" + str(libdir), "-Wl,-rpath," + str(libdir),
                       "-lclSPARSE", "-framework", "OpenCL", "-o", str(target / name)]
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
        if source.get("source_build") in ("lis", "lagraph", "librsb", "superlu_dist", "bebop_smc", "libmtx", "spm", "clsparse"):
            local_libraries[name]["built_lib_sha256"] = built_lib_sha256
        print(f"{name}@{parser['version']}: C Matrix Market passed", flush=True)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["cc", "--version"]).splitlines()[0],
              "source_lock": "data/c/matrix_market/source-lock.json",
              "local_libraries": local_libraries,
              "control": "controls/matrix_market/real-general.mtx", "control_sha256": CONTROL_SHA256,
              "additional_controls": {"controls/matrix_market/real-symmetric.mtx": SYMMETRIC_CONTROL_SHA256},
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
