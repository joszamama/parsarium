"""Build the pinned C ZIP adapters and record valid-control observations."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import platform
import shlex
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/zip"
ADAPTER = ROOT / "adapters/c/zip"
TARGET = ADAPTER / "target"
CONTROL = ROOT / "controls/zip/hello.zip"
CONTROL_SHA256 = "c534fa083d1da92474852ca9168ba0793740c25205f828915a1d862bd78c776b"
EXPECTED = {"entries": 1, "name": "hello.txt", "content": "parsarium\n"}


def run(command: list[str], env: dict[str, str] | None = None) -> str:
    return subprocess.run(command, cwd=ROOT, env=env, check=True,
                          text=True, capture_output=True).stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    lock = json.loads((DATA / "source-lock.json").read_text())
    parsers = json.loads((DATA / "parsers.json").read_text())
    assert len(parsers) == 6 and {p["name"] for p in parsers} == set(lock)
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    local_libraries = {}
    for parser in parsers:
        name = parser["name"]
        item = lock[name]
        assert parser["version"] == item["release"]
        library = Path(item["local_library"])
        digest = sha256(library.read_bytes()).hexdigest()
        assert digest == item["local_library_sha256"], name
        env = os.environ.copy()
        if name == "libarchive":
            directory = str(library.parent / "pkgconfig")
            env["PKG_CONFIG_PATH"] = directory + os.pathsep + env.get("PKG_CONFIG_PATH", "")
        observed = run(["pkg-config", "--modversion", item["pkg_config"]], env)
        assert observed == item["release"], (name, observed)
        flags = shlex.split(run(["pkg-config", "--cflags", "--libs", item["pkg_config"]], env))
        command = ["cc", "-std=c11", "-O2", str(ROOT / parser["adapter"]),
                   *flags, "-o", str(TARGET / name)]
        run(command, env)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute, env))
        assert parser["expected_output"] == EXPECTED
        assert output == EXPECTED, (name, output)
        local_libraries[name] = {"pkg_config_version": observed,
                                 "library": str(library), "library_sha256": digest}
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "build_command": shlex.join(command),
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["cc", "--version"]).splitlines()[0],
              "local_libraries": local_libraries,
              "control": "controls/zip/hello.zip", "control_sha256": CONTROL_SHA256,
              "expected": EXPECTED, "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
