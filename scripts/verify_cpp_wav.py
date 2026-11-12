"""Build C++17 WAV call sites and record valid-control results."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess

import prepare_cpp_wav
import verify_c_wav


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cpp/wav"
ADAPTER = ROOT / "adapters/cpp/wav"
TARGET = ADAPTER / "target"
CONTROL = ROOT / "controls/wav/four-samples.wav"


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, check=True, text=True,
                          capture_output=True).stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == verify_c_wav.CONTROL_SHA256
    verify_c_wav.main()
    prepare_cpp_wav.main()
    c_parsers = {p["name"]: p for p in json.loads((ROOT / "data/c/wav/parsers.json").read_text())}
    c_runs = {r["package"]: r for r in json.loads((ROOT / "data/c/wav/verification.json").read_text())["third_party"]}
    parsers = json.loads((DATA / "parsers.json").read_text())
    extra_lock = json.loads((DATA / "extra-source-lock.json").read_text())
    cell = json.loads((DATA / "cell.json").read_text())
    assert len(parsers) == cell["verified_third_party_count"]
    assert {p["name"] for p in parsers} == set(c_parsers) | set(extra_lock)
    assert set(c_parsers) == set(c_runs)
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    local_libraries = {}
    source_builds = {}
    for parser in parsers:
        name = parser["name"]
        prerequisites = []
        if name == "sfml":
            item = extra_lock[name]
            library = Path(item["local_library"])
            digest = sha256(library.read_bytes()).hexdigest()
            assert digest == item["local_library_sha256"]
            observed = run(["pkg-config", "--modversion", item["pkg_config"]])
            assert observed == item["pkg_config_version"]
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", item["pkg_config"]]))
            command = ["c++", "-std=c++17", "-O2", str(ROOT / parser["adapter"]),
                       *flags, "-o", str(TARGET / name)]
            local_libraries[name] = {"pkg_config_version": observed,
                                     "library": str(library), "library_sha256": digest}
        elif name == "audiofile":
            item = extra_lock[name]
            source = ADAPTER / "cache/source/audiofile"
            command = ["c++", "-std=c++17", "-O2", "-I" + str(source),
                       str(ROOT / parser["adapter"]), "-o", str(TARGET / name)]
            source_builds[name] = {"source_sha256": item["source_sha256"],
                                   "files": item["files"]}
        else:
            assert parser["version"] == c_parsers[name]["version"]
            assert parser["expected_output"] == c_parsers[name]["expected_output"]
            command = shlex.split(c_runs[name]["build_command"])
            assert command[:2] == ["cc", "-std=c11"]
            command[:2] = ["c++", "-std=c++17"]
            c_adapter = str(ROOT / c_parsers[name]["adapter"])
            command[command.index(c_adapter)] = str(ROOT / parser["adapter"])
            assert command[-2] == "-o"
            command[-1] = str(TARGET / name)
            if name == "miniaudio":
                c_source = ROOT / "adapters/c/wav/cache/source/miniaudio/miniaudio.c"
                obj = TARGET / "miniaudio_c.o"
                build = ["cc", "-std=c11", "-O2", "-I" + str(c_source.parent),
                         "-c", str(c_source), "-o", str(obj)]
                run(build)
                prerequisites.append(shlex.join(build))
                command[command.index(str(c_source))] = str(obj)
        run(command)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "prerequisite_build_commands": prerequisites,
                     "build_command": shlex.join(command), "command": shlex.join(execute),
                     "output": output, "pass": True})
        print(f"{name}@{parser['version']}: C++ passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["c++", "--version"]).splitlines()[0],
              "shared_c_release_lock": "data/c/wav/source-lock.json",
              "shared_c_verification": "data/c/wav/verification.json",
              "local_libraries": local_libraries, "source_builds": source_builds,
              "control": "controls/wav/four-samples.wav",
              "control_sha256": verify_c_wav.CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
