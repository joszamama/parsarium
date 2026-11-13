"""Verify pinned C and C++ MP4 readers on a valid two-track local file."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import os
import platform
import shlex
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "controls/mp4/red-av.mp4"
CONTROL_SHA256 = "10086c39c7226726579924794cd7c0bbafe65de38021bd0f38f6da9d23d24643"


def run(command: list[str], timeout: int = 180, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout,
                            env={**os.environ, **(env or {})})
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def verify(ecosystem: str) -> None:
    assert ecosystem in ("c", "cpp")
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    data = ROOT / "data" / ecosystem / "mp4"
    parsers = json.loads((data / "parsers.json").read_text())
    lock = json.loads((data / "source-lock.json").read_text())
    assert len(parsers) == json.loads((data / "cell.json").read_text())["verified_third_party_count"]
    cache = Path(tempfile.gettempdir()) / f"parsarium-{ecosystem}-mp4"
    cache.mkdir(parents=True, exist_ok=True)
    target = ROOT / "adapters" / ecosystem / "mp4/target"
    target.mkdir(parents=True, exist_ok=True)
    rows = []
    libraries = {}
    for parser in parsers:
        name = parser["name"]
        source = lock[name]
        suffix = next(s for s in (".tar.gz", ".tar.xz", ".tar.bz2") if source["source_url"].endswith(s))
        archive = cache / f"{name}-{source['release']}{suffix}"
        if not archive.exists() or sha256(archive.read_bytes()).hexdigest() != source["source_sha256"]:
            with urlopen(Request(source["source_url"], headers={"User-Agent": "Parsarium MP4 verifier"}), timeout=120) as response:
                archive.write_bytes(response.read())
        assert sha256(archive.read_bytes()).hexdigest() == source["source_sha256"]
        with tarfile.open(archive) as tar:
            member = tar.extractfile(source["source_header_member"])
            assert member is not None
            header_bytes = member.read()
            assert sha256(header_bytes).hexdigest() == source.get("source_header_sha256", source.get("local_header_sha256"))
            member = tar.extractfile(source["license_member"])
            assert member is not None
            assert sha256(member.read()).hexdigest() == source["license_sha256"]
            if "source_engine_member" in source:
                member = tar.extractfile(source["source_engine_member"])
                assert member is not None
                assert sha256(member.read()).hexdigest() == source["source_engine_sha256"]
            for engine in source.get("source_engine_members", []):
                member = tar.extractfile(engine["member"])
                assert member is not None
                assert sha256(member.read()).hexdigest() == engine["sha256"]
        if source.get("header_only"):
            include_dir = cache / f"{name}-{source['release']}-include"
            include_dir.mkdir(exist_ok=True)
            (include_dir / "dr_mp3.h").write_bytes(header_bytes)
            flags = ["-I" + str(include_dir), "-lm"]
        else:
            if source.get("cask"):
                assert source["installed_revision"] in run(["brew", "list", "--cask", "--versions", source["cask"]]).split()
                cask_archive = Path(run(["brew", "--cache", "--cask", source["cask"]]))
                assert sha256(cask_archive.read_bytes()).hexdigest() == source["cask_sha256"]
            else:
                assert source["installed_revision"] in run(["brew", "list", "--versions", source["formula"]]).split()
            if source.get("pkg_config"):
                assert run(["pkg-config", "--modversion", source["pkg_config"]]) == source.get("pkg_config_version", source["release"])
            header = Path(source["local_header"])
            library = Path(source["local_library"])
            assert sha256(header.read_bytes()).hexdigest() == source["local_header_sha256"]
            assert sha256(library.read_bytes()).hexdigest() == source["local_library_sha256"]
            if source.get("pkg_config"):
                flags = shlex.split(run(["pkg-config", "--cflags", "--libs", source["pkg_config"]]))
            else:
                flags = ["-isystem", source["include_dir"], "-L" + str(library.parent), "-l" + source["link_name"]]
            flags.extend(source.get("extra_linker_flags", []))
        for dependency in source.get("installed_dependencies", []):
            assert sha256(Path(dependency["path"]).read_bytes()).hexdigest() == dependency["sha256"]
        compiler = "c++" if ecosystem == "cpp" else "cc"
        standard = "-std=c++17" if ecosystem == "cpp" else "-std=c11"
        command = [compiler, standard, "-O2", "-Wall", "-Wextra", "-Werror",
                   str(ROOT / parser["adapter"]), *flags, "-o", str(target / name)]
        run(command)
        execute = [str(target / name), str(CONTROL)]
        runtime_env = source.get("runtime_env", {})
        output = json.loads(run(execute, env=runtime_env))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"], "control": parser["control"],
                     "build_command": shlex.join(command),
                     "command": shlex.join(["env", *(f"{key}={value}" for key, value in runtime_env.items()), *execute]) if runtime_env else shlex.join(execute),
                     "output": output, "pass": True})
        libraries[name] = {"source_sha256": source["source_sha256"]}
        if source.get("header_only"):
            libraries[name]["source_header_sha256"] = source["source_header_sha256"]
        else:
            libraries[name]["local_header_sha256"] = source["local_header_sha256"]
            libraries[name]["local_library_sha256"] = source["local_library_sha256"]
        print(f"{name}@{parser['version']}: {ecosystem} MP4 passed", flush=True)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["c++" if ecosystem == "cpp" else "cc", "--version"]).splitlines()[0],
              "source_lock": f"data/{ecosystem}/mp4/source-lock.json", "local_libraries": libraries,
              "control": "controls/mp4/red-av.mp4", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (data / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
