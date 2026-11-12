"""Verify C++17 call sites for pinned ASCII P3 PNM readers."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess

import verify_c_ascii_pnm
import prepare_cpp_ascii_pnm


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/ascii_pnm"
TARGET = ROOT / "adapters/cpp/ascii_pnm/target"
CONTROL = ROOT / "controls/ascii_pnm/red-green.ppm"


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, check=True, text=True,
                          capture_output=True).stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == verify_c_ascii_pnm.CONTROL_SHA256
    verify_c_ascii_pnm.main()
    c_parsers = {p["name"]: p for p in json.loads((ROOT / "data/c/ascii_pnm/parsers.json").read_text())}
    c_runs = {r["package"]: r for r in json.loads((ROOT / "data/c/ascii_pnm/verification.json").read_text())["third_party"]}
    parsers = json.loads((DATA / "parsers.json").read_text())
    cell = json.loads((DATA / "cell.json").read_text())
    assert len(parsers) == cell["verified_third_party_count"]
    native = {"cimg", "boost-gil", "wxwidgets", "qtbase", "pnmpp", "openimageio"}
    assert {p["name"] for p in parsers} - native <= set(c_parsers)
    assert {p["name"] for p in parsers} & native == native
    assert set(c_parsers) == set(c_runs)
    extra_control = ROOT / "controls/ascii_pnm/red-green-inline.ppm"
    extra_control_sha256 = "782c0fd8551ce383728488dbfa0f26d2e27a6107a5a3c1793e678f2b9d87ced6"
    assert sha256(extra_control.read_bytes()).hexdigest() == extra_control_sha256
    assert extra_control.read_bytes() == b"P3\n2 1 255\n255 0 0  0 255 0\n"
    prepare_cpp_ascii_pnm.main()
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    for parser in parsers:
        name = parser["name"]
        if name == "pnmpp":
            lock = json.loads((DATA / "extra-source-lock.json").read_text())[name]
            assert parser["version"] == lock["release"]
            command = ["c++", "-std=c++17", "-O2", "-Wno-deprecated-literal-operator",
                       "-I" + str(prepare_cpp_ascii_pnm.PNMPP_INCLUDE),
                       str(ROOT / parser["adapter"]), "-o", str(TARGET / name)]
        elif name == "openimageio":
            lock = json.loads((DATA / "extra-source-lock.json").read_text())[name]
            assert parser["version"] == lock["release"]
            command = ["c++", "-std=c++17", "-O2",
                       *shlex.split(run(["pkg-config", "--cflags", "OpenImageIO"])),
                       "-I/opt/homebrew/include", str(ROOT / parser["adapter"]),
                       *shlex.split(run(["pkg-config", "--libs", "OpenImageIO"])),
                       "-o", str(TARGET / name)]
        elif name == "qtbase":
            lock = json.loads((DATA / "extra-source-lock.json").read_text())[name]
            assert parser["version"] == lock["release"]
            command = ["c++", "-std=c++17", "-O2",
                       *shlex.split(run(["pkg-config", "--cflags", "Qt6Gui", "Qt6Core"])),
                       str(ROOT / parser["adapter"]),
                       *shlex.split(run(["pkg-config", "--libs", "Qt6Gui", "Qt6Core"])),
                       "-o", str(TARGET / name)]
        elif name == "wxwidgets":
            lock = json.loads((DATA / "extra-source-lock.json").read_text())[name]
            assert parser["version"] == lock["release"]
            command = ["c++", "-std=c++17", "-O2",
                       *shlex.split(run(["wx-config", "--cxxflags"])),
                       str(ROOT / parser["adapter"]),
                       *shlex.split(run(["wx-config", "--libs"])),
                       "-o", str(TARGET / name)]
        elif name == "boost-gil":
            lock = json.loads((DATA / "extra-source-lock.json").read_text())[name]
            assert parser["version"] == lock["release"]
            command = ["c++", "-std=c++17", "-O2",
                       "-I" + str(prepare_cpp_ascii_pnm.GIL_INCLUDE),
                       "-I/opt/homebrew/include",
                       str(ROOT / parser["adapter"]), "-o", str(TARGET / name)]
        elif name == "cimg":
            lock = json.loads((DATA / "extra-source-lock.json").read_text())[name]
            assert parser["version"] == lock["release"]
            command = ["c++", "-std=c++17", "-O2",
                       "-I" + str(prepare_cpp_ascii_pnm.HEADER.parent),
                       str(ROOT / parser["adapter"]), "-o", str(TARGET / name)]
        else:
            assert parser["version"] == c_parsers[name]["version"]
            assert parser["expected_output"] == c_parsers[name]["expected_output"]
            command = shlex.split(c_runs[name]["build_command"])
            assert command[:2] == ["cc", "-std=c11"]
            command[:2] = ["c++", "-std=c++17"]
            command[command.index(str(ROOT / c_parsers[name]["adapter"]))] = str(ROOT / parser["adapter"])
            assert command[-2] == "-o"
            command[-1] = str(TARGET / name)
        run(command)
        execute = [str(TARGET / name), str(ROOT / parser["control"])]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        row = {"package": name, "version": parser["version"],
               "control": parser["control"], "build_command": shlex.join(command),
               "command": shlex.join(execute), "output": output, "pass": True}
        if name == "cimg":
            limited = parser["other_valid_control_result"]
            observed = json.loads(run([str(TARGET / name), str(CONTROL)]))
            assert observed == limited["output"]
            assert observed != parser["expected_output"]
            row["other_valid_control_result"] = limited
        rows.append(row)
        print(f"{name}@{parser['version']}: C++ P3 passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["c++", "--version"]).splitlines()[0],
              "source_lock": "data/c/png/source-lock.json",
              "extra_source_lock": "data/c/ascii_pnm/source-lock.json",
              "additional_source_lock": "data/cpp/ascii_pnm/extra-source-lock.json",
              "prerequisite_verifier": "scripts/verify_c_ascii_pnm.py",
              "control": "controls/ascii_pnm/red-green.ppm",
              "control_sha256": verify_c_ascii_pnm.CONTROL_SHA256,
              "additional_control_sha256": extra_control_sha256,
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
