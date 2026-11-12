"""Build C++ call sites for pinned PNG libraries and record valid-control results."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess

import verify_c_png


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/png"
ADAPTER = ROOT / "adapters/cpp/png"
TARGET = ADAPTER / "target"
CONTROL = ROOT / "controls/png/red-green.png"


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, check=True, text=True,
                          capture_output=True).stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == verify_c_png.CONTROL_SHA256
    # This checks every source and local binary pin before using the same packages from C++.
    verify_c_png.main()
    c_parsers = {p["name"]: p for p in json.loads((ROOT / "data/c/png/parsers.json").read_text())}
    c_runs = {r["package"]: r for r in json.loads((ROOT / "data/c/png/verification.json").read_text())["third_party"]}
    parsers = json.loads((DATA / "parsers.json").read_text())
    assert len(parsers) == 20 and {p["name"] for p in parsers} == set(c_parsers) == set(c_runs)
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    for parser in parsers:
        name = parser["name"]
        assert parser["version"] == c_parsers[name]["version"]
        assert parser["expected_output"] == c_parsers[name]["expected_output"]
        command = shlex.split(c_runs[name]["build_command"])
        assert command[0] == "cc" and command[1] == "-std=c11"
        command[0:2] = ["c++", "-std=c++17"]
        c_adapter = str(ROOT / c_parsers[name]["adapter"])
        command[command.index(c_adapter)] = str(ROOT / parser["adapter"])
        assert command[-2] == "-o"
        command[-1] = str(TARGET / name)
        prebuild_command = None
        if name == "libspng":
            source = ROOT / "adapters/c/png/cache/source/libspng/spng.c"
            object_file = TARGET / "spng.o"
            prebuild_command = ["cc", "-std=c11", "-O2", "-I" + str(source.parent),
                                "-c", str(source), "-o", str(object_file)]
            run(prebuild_command)
            command[command.index(str(source))] = str(object_file)
        run(command)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "build_command": shlex.join(command),
                     "prebuild_command": shlex.join(prebuild_command) if prebuild_command else None,
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: C++ passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["c++", "--version"]).splitlines()[0],
              "source_lock": "data/c/png/source-lock.json",
              "prerequisite_verifier": "scripts/verify_c_png.py",
              "control": "controls/png/red-green.png",
              "control_sha256": verify_c_png.CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
