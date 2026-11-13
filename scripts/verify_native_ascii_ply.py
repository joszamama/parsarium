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
        suffix = ".tar.gz" if source["source_url"].endswith(".tar.gz") else ".tar.bz2"
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
        assert source["installed_revision"] in run(["brew", "list", "--versions", source["formula"]]).split()
        for path, expected in source["installed_files"].items():
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
                                 "installed_files": source["installed_files"]}
        print(f"{name}@{parser['version']}: {ecosystem} ASCII PLY passed", flush=True)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["cc" if ecosystem == "c" else "c++", "--version"]).splitlines()[0],
              "source_lock": f"data/{ecosystem}/ascii_ply/source-lock.json", "local_libraries": local_libraries,
              "control": "controls/ascii_ply/triangle.ply", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (data / "verification.json").write_text(json.dumps(result, indent=2) + "\n")

