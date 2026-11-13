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


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/matrix_market"
CONTROL = ROOT / "controls/matrix_market/real-general.mtx"
CONTROL_SHA256 = "65614ddf08f46422a1f6f71d67bdc4490e84635b3cc61dfe089c82c41829da4c"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def main() -> None:
    assert digest(CONTROL) == CONTROL_SHA256
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
        archive = cache / f"{name}-{source['release']}.tar.gz"
        if not archive.exists() or digest(archive) != source["source_sha256"]:
            with urlopen(Request(source["source_url"], headers={"User-Agent": "Parsarium Matrix Market verifier"}), timeout=120) as response, archive.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
        assert digest(archive) == source["source_sha256"]
        with tarfile.open(archive) as tar:
            for member, expected in source["source_members"].items():
                file = tar.extractfile(member)
                assert file is not None and sha256(file.read()).hexdigest() == expected, member
        for path, expected in source["installed_files"].items():
            assert digest(Path(path)) == expected, path
        assert source["installed_revision"] in run(["brew", "list", "--versions", source["formula"]]).split()
        if name == "suite-sparse":
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", "cholmod"]))
            command = ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                       str(ROOT / parser["adapter"]), *flags,
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
                                 "installed_files": source["installed_files"]}
        print(f"{name}@{parser['version']}: C Matrix Market passed", flush=True)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "compiler": run(["cc", "--version"]).splitlines()[0],
              "source_lock": "data/c/matrix_market/source-lock.json",
              "local_libraries": local_libraries,
              "control": "controls/matrix_market/real-general.mtx", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
