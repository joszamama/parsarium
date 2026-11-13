"""Verify native ASCII PLY APIs against pinned sources and a valid triangle."""

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


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
CONTROL_SHA256 = "d6f46efd47104401bef9f510970e5a3510203f947cdc6679781df60685796378"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str], timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def verify(ecosystem: str) -> None:
    assert ecosystem in ("c", "cpp")
    assert digest(CONTROL) == CONTROL_SHA256
    data = ROOT / "data" / ecosystem / "ascii_ply"
    parsers = json.loads((data / "parsers.json").read_text())
    sources = json.loads((data / "source-lock.json").read_text())
    assert len(parsers) == json.loads((data / "cell.json").read_text())["verified_third_party_count"]
    cache = Path(tempfile.gettempdir()) / "parsarium-native-ascii-ply"
    cache.mkdir(exist_ok=True)
    target = ROOT / "adapters" / ecosystem / "ascii_ply" / "target"
    target.mkdir(exist_ok=True)
    rows = []
    local_libraries = {}
    for parser in parsers:
        name = parser["name"]
        source = sources[name]
        suffix = next(s for s in (".tar.gz", ".tar.bz2", ".tar.xz") if source["source_url"].endswith(s))
        archive = cache / f"{name}-{source['release']}{suffix}"
        if not archive.exists() or digest(archive) != source["source_sha256"]:
            with urlopen(Request(source["source_url"], headers={"User-Agent": "Parsarium ASCII PLY verifier"}), timeout=120) as response, archive.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
        assert digest(archive) == source["source_sha256"]
        with tarfile.open(archive) as tar:
            for member, expected in source["source_members"].items():
                file = tar.extractfile(member)
                assert file is not None and sha256(file.read()).hexdigest() == expected, member
            if source.get("header_only"):
                header = tar.extractfile(source["header_member"])
                assert header is not None
                include_dir = cache / f"{name}-{source['release']}-include"
                include_dir.mkdir(exist_ok=True)
                (include_dir / source["header_name"]).write_bytes(header.read())
                assert digest(include_dir / source["header_name"]) == source["source_members"][source["header_member"]]
            if source.get("source_build") == "rply":
                include_dir = cache / "rply-1.1.4-src"
                include_dir.mkdir(exist_ok=True)
                for member in ("rply.h", "rplyfile.h", "rply.c"):
                    file = tar.extractfile(f"rply-1.1.4/{member}")
                    assert file is not None
                    (include_dir / member).write_bytes(file.read())
                    assert digest(include_dir / member) == source["source_members"][f"rply-1.1.4/{member}"]
            if source.get("source_build") == "libigl":
                for member in tar.getmembers():
                    member_path = Path(member.name)
                    assert not member_path.is_absolute() and ".." not in member_path.parts
                    assert member.name == "libigl-2.6.4" or member.name.startswith("libigl-2.6.4/")
                if not (cache / "libigl-2.6.4/include/igl/readPLY.h").exists():
                    tar.extractall(cache, filter="data")
                include_dir = cache / "libigl-2.6.4/include"
                for member, expected in source["source_members"].items():
                    assert digest(cache / member) == expected
            if source.get("source_build") == "plywoot":
                for member in tar.getmembers():
                    member_path = Path(member.name)
                    assert not member_path.is_absolute() and ".." not in member_path.parts
                    assert member.name == "PLYwoot-0.3.0" or member.name.startswith("PLYwoot-0.3.0/")
                if not (cache / "PLYwoot-0.3.0/include/plywoot/plywoot.hpp").exists():
                    tar.extractall(cache, filter="data")
                include_dir = cache / "PLYwoot-0.3.0/include"
                for member, expected in source["source_members"].items():
                    assert digest(cache / member) == expected
            if source.get("source_build") == "turboply":
                include_dir = cache / "turboply-1.0.6-src"
                include_dir.mkdir(exist_ok=True)
                for member in ("turboply.hpp", "turboply_util.hpp", "plyfile.cpp", "plystream.cpp"):
                    file = tar.extractfile(f"turboply-1.0.6/{member}")
                    assert file is not None
                    (include_dir / member).write_bytes(file.read())
                    assert digest(include_dir / member) == source["source_members"][f"turboply-1.0.6/{member}"]
                stream = include_dir / "plystream.cpp"
                text = stream.read_text()
                start = text.index("class FormatHandler {")
                block_start = text.index("protected:\n    template <typename F, typename StreamT>", start)
                block_end = text.index("\n};", block_start)
                block = text[block_start:block_end]
                text = text[:block_start] + text[block_end:]
                text = text[:start] + text[start:].replace("class FormatHandler {", "class FormatHandler {\n" + block + "\npublic:", 1)
                stream.write_text(text)
                assert digest(stream) == source["patched_plystream_sha256"]
            if source.get("source_build") == "geometry_central":
                for member in tar.getmembers():
                    member_path = Path(member.name)
                    assert not member_path.is_absolute() and ".." not in member_path.parts
                    assert member.name == "geometry-central-1.1.0" or member.name.startswith("geometry-central-1.1.0/")
                if not (cache / "geometry-central-1.1.0/include/geometrycentral/surface/simple_polygon_mesh.h").exists():
                    tar.extractall(cache, filter="data")
                include_dir = cache / "geometry-central-1.1.0"
                for member, expected in source["source_members"].items():
                    assert digest(cache / member) == expected
                sub = source["submodule"]
                sub_archive = cache / "geometry-central-happly.tar.gz"
                if not sub_archive.exists() or digest(sub_archive) != sub["source_sha256"]:
                    with urlopen(Request(sub["source_url"], headers={"User-Agent": "Parsarium ASCII PLY verifier"}), timeout=120) as response, sub_archive.open("wb") as output:
                        while chunk := response.read(1024 * 1024):
                            output.write(chunk)
                assert digest(sub_archive) == sub["source_sha256"]
                with tarfile.open(sub_archive) as sub_tar:
                    header = sub_tar.extractfile(sub["header_member"])
                    assert header is not None
                    header_bytes = header.read()
                    assert sha256(header_bytes).hexdigest() == sub["header_sha256"]
                (include_dir / "deps/happly/happly.h").write_bytes(header_bytes)
                assert digest(include_dir / "deps/happly/happly.h") == sub["header_sha256"]
        if not source.get("header_only") and not source.get("source_build"):
            assert source["installed_revision"] in run(["brew", "list", "--versions", source["formula"]]).split()
            for path, expected in source["installed_files"].items():
                assert digest(Path(path)) == expected, path
        for path, expected in source.get("toolchain_files", {}).items():
            assert digest(Path(path)) == expected, path
        compiler = "cc" if ecosystem == "c" else "c++"
        language = "-std=c11" if ecosystem == "c" else "-std=c++17"
        if name == "assimp":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "assimp"]))
            command = [compiler, language, "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags, "-o", str(target / name)]
        elif name == "open-mesh":
            prefix = Path(source["prefix"])
            command = [compiler, language, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(prefix / "include"), str(ROOT / parser["adapter"]),
                       "-L" + str(prefix / "lib"), "-Wl,-rpath," + str(prefix / "lib"),
                       "-lOpenMeshCore", "-lOpenMeshTools", "-o", str(target / name)]
        elif name == "cgal":
            command = [compiler, language, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", "/opt/homebrew/Cellar/cgal/6.2.1/include",
                       "-isystem", "/opt/homebrew/opt/boost/include",
                       "-isystem", "/opt/homebrew/opt/eigen/include/eigen3",
                       "-isystem", "/opt/homebrew/opt/gmp/include",
                       "-isystem", "/opt/homebrew/opt/mpfr/include",
                       str(ROOT / parser["adapter"]),
                       "-L/opt/homebrew/opt/gmp/lib", "-L/opt/homebrew/opt/mpfr/lib",
                       "-lgmp", "-lmpfr", "-o", str(target / name)]
        elif name == "pcl":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "pcl_io"]))
            command = [compiler, language, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", "/opt/homebrew/opt/boost/include",
                       str(ROOT / parser["adapter"]), *flags, "-o", str(target / name)]
        elif name == "vtk":
            prefix = Path("/opt/homebrew/Cellar/vtk/9.7.2")
            command = [compiler, language, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(prefix / "include/vtk-9.7"),
                       str(ROOT / parser["adapter"]), "-L" + str(prefix / "lib"),
                       "-Wl,-rpath," + str(prefix / "lib"),
                       "-lvtkIOPLY-9.7", "-lvtkCommonDataModel-9.7", "-lvtkCommonCore-9.7",
                       "-lvtkCommonExecutionModel-9.7", "-lvtksys-9.7",
                       "-o", str(target / name)]
        elif source.get("source_build") == "rply":
            object_path = include_dir / "rply.o"
            run(["cc", "-std=c11", "-O2", "-I" + str(include_dir),
                 "-c", str(include_dir / "rply.c"), "-o", str(object_path)])
            command = [compiler, language, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-I" + str(include_dir), str(ROOT / parser["adapter"]),
                       str(object_path), "-o", str(target / name)]
        elif source.get("source_build") == "libigl":
            command = [compiler, language, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(include_dir),
                       "-isystem", "/opt/homebrew/opt/eigen/include/eigen3",
                       str(ROOT / parser["adapter"]), "-o", str(target / name)]
        elif source.get("source_build") == "plywoot":
            assert run(["/opt/homebrew/opt/llvm/bin/clang++", "--version"]).splitlines()[0] == "Homebrew clang version 23.1.4"
            command = ["/opt/homebrew/opt/llvm/bin/clang++", language, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-nostdinc++", "-isystem", "/opt/homebrew/opt/llvm/include/c++/v1",
                       "-isystem", str(include_dir), str(ROOT / parser["adapter"]),
                       "-L/opt/homebrew/opt/llvm/lib/c++", "-Wl,-rpath,/opt/homebrew/opt/llvm/lib/c++",
                       "-stdlib=libc++", "-o", str(target / name)]
        elif source.get("source_build") == "turboply":
            assert run(["/opt/homebrew/opt/gcc/bin/g++-16", "-dumpfullversion"]) == "16.2.0"
            command = ["/opt/homebrew/opt/gcc/bin/g++-16", "-std=c++20", "-O2",
                       "-include", "algorithm", "-include", "format",
                       "-include", "charconv", "-include", "cstring",
                       "-I" + str(include_dir), "-I/opt/homebrew/opt/boost/include",
                       str(ROOT / parser["adapter"]), str(include_dir / "plyfile.cpp"),
                       str(include_dir / "plystream.cpp"), "-o", str(target / name)]
        elif source.get("source_build") == "geometry_central":
            command = [compiler, language, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-Wno-unused-parameter", "-Wno-unused-function",
                       "-ffunction-sections", "-fdata-sections",
                       "-isystem", str(include_dir / "include"),
                       "-isystem", str(include_dir / "deps/happly"),
                       "-isystem", "/opt/homebrew/opt/eigen/include/eigen3",
                       str(ROOT / parser["adapter"]),
                       str(include_dir / "src/surface/simple_polygon_mesh.cpp"),
                       "-Wl,-dead_strip", "-o", str(target / name)]
        elif source.get("header_only"):
            command = [compiler, language, "-O2", "-Wall", "-Wextra", "-Werror",
                       "-isystem", str(include_dir), str(ROOT / parser["adapter"]),
                       "-o", str(target / name)]
        else:
            raise ValueError(name)
        run(command)
        execute = [str(target / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"], "control": parser["control"],
                     "build_command": shlex.join(command), "command": shlex.join(execute),
                     "output": output, "pass": True})
        local_libraries[name] = {"source_sha256": source["source_sha256"],
                                 "installed_files": source.get("installed_files", {}),
                                 "source_header_sha256": source["source_members"].get(source.get("header_member"))}
        if source.get("source_build") == "rply":
            local_libraries[name]["built_object_sha256"] = digest(object_path)
        if source.get("source_build") == "turboply":
            local_libraries[name]["patched_plystream_sha256"] = source["patched_plystream_sha256"]
        if source.get("source_build") == "geometry_central":
            local_libraries[name]["submodule_source_sha256"] = source["submodule"]["source_sha256"]
            local_libraries[name]["submodule_header_sha256"] = source["submodule"]["header_sha256"]
        print(f"{name}@{parser['version']}: {ecosystem} ASCII PLY passed", flush=True)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["cc" if ecosystem == "c" else "c++", "--version"]).splitlines()[0],
              "source_lock": f"data/{ecosystem}/ascii_ply/source-lock.json", "local_libraries": local_libraries,
              "control": "controls/ascii_ply/triangle.ply", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (data / "verification.json").write_text(json.dumps(result, indent=2) + "\n")

