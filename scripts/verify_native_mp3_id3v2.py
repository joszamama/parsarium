"""Verify pinned C and C++ MP3/ID3v2 readers on a valid tagged audio file."""

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
CONTROL = ROOT / "controls/mp3_id3v2/tone-tags.mp3"
CONTROL_SHA256 = "d61e1802a52dc55b5447356a3347fa4f9e08eb706757870f65ee0776dbf5bcad"


def run(command: list[str], timeout: int = 180) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def verify(ecosystem: str) -> None:
    assert ecosystem in ("c", "cpp")
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    data = ROOT / "data" / ecosystem / "mp3_id3v2"
    parsers = json.loads((data / "parsers.json").read_text())
    lock = json.loads((data / "source-lock.json").read_text())
    assert len(parsers) == json.loads((data / "cell.json").read_text())["verified_third_party_count"]
    cache = Path(tempfile.gettempdir()) / f"parsarium-{ecosystem}-mp3-id3v2"
    cache.mkdir(parents=True, exist_ok=True)
    target = ROOT / "adapters" / ecosystem / "mp3_id3v2/target"
    target.mkdir(parents=True, exist_ok=True)
    rows = []
    libraries = {}
    for parser in parsers:
        name = parser["name"]
        source = lock[name]
        suffix = next(s for s in (".tar.gz", ".tar.xz", ".tar.bz2") if source["source_url"].endswith(s))
        archive = cache / f"{name}-{source['release']}{suffix}"
        if not archive.exists() or sha256(archive.read_bytes()).hexdigest() != source["source_sha256"]:
            with urlopen(Request(source["source_url"], headers={"User-Agent": "Parsarium MP3 verifier"}), timeout=120) as response:
                archive.write_bytes(response.read())
        assert sha256(archive.read_bytes()).hexdigest() == source["source_sha256"]
        with tarfile.open(archive) as tar:
            member = tar.extractfile(source["source_header_member"])
            assert member is not None
            assert sha256(member.read()).hexdigest() == source.get("source_header_sha256", source["local_header_sha256"])
            member = tar.extractfile(source["license_member"])
            assert member is not None
            assert sha256(member.read()).hexdigest() == source["license_sha256"]
        assert source["installed_revision"] in run(["brew", "list", "--versions", source["formula"]]).split()
        if source.get("pkg_config"):
            assert run(["pkg-config", "--modversion", source["pkg_config"]]) == source.get("pkg_config_version", source["release"])
        header = Path(source["local_header"])
        library = Path(source["local_library"])
        assert sha256(header.read_bytes()).hexdigest() == source["local_header_sha256"]
        assert sha256(library.read_bytes()).hexdigest() == source["local_library_sha256"]
        for dependency in source.get("installed_dependencies", []):
            assert sha256(Path(dependency["path"]).read_bytes()).hexdigest() == dependency["sha256"]
        compiler = "c++" if ecosystem == "cpp" else "cc"
        standard = "-std=c++17" if ecosystem == "cpp" else "-std=c11"
        if source.get("pkg_config"):
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", source["pkg_config"]]))
        else:
            flags = ["-isystem", source["include_dir"], "-L" + str(library.parent), "-l" + source["link_name"]]
        command = [compiler, standard, "-O2", "-Wall", "-Wextra", "-Werror",
                   str(ROOT / parser["adapter"]), *flags, "-o", str(target / name)]
        run(command)
        execute = [str(target / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"], "control": parser["control"],
                     "build_command": shlex.join(command), "command": shlex.join(execute),
                     "output": output, "pass": True})
        libraries[name] = {"source_sha256": source["source_sha256"],
                           "local_header_sha256": source["local_header_sha256"],
                           "local_library_sha256": source["local_library_sha256"]}
        print(f"{name}@{parser['version']}: {ecosystem} MP3 with ID3v2 passed", flush=True)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["c++" if ecosystem == "cpp" else "cc", "--version"]).splitlines()[0],
              "source_lock": f"data/{ecosystem}/mp3_id3v2/source-lock.json", "local_libraries": libraries,
              "control": "controls/mp3_id3v2/tone-tags.mp3", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (data / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
