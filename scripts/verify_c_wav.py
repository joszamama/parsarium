"""Build the pinned C WAV adapters and record valid-control observations."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess

import prepare_c_wav


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/wav"
ADAPTER = ROOT / "adapters/c/wav"
SOURCE = ADAPTER / "cache/source"
TARGET = ADAPTER / "target"
CONTROL = ROOT / "controls/wav/four-samples.wav"
CONTROL_SHA256 = "6154e1a5105d7b8b35a7ac228d50907c2fed58ea63577391b34957cc538966ce"
EXPECTED = {"sample_rate": 8000, "channels": 1, "frames": 4,
            "samples": [0, 1000, -1000, 0]}
EXPECTED_METADATA = {"sample_rate": 8000, "channels": 1, "frames": 4}


def run(command: list[str], cwd: Path = ROOT) -> str:
    return subprocess.run(command, cwd=cwd, check=True, text=True,
                          capture_output=True).stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    lock = json.loads((DATA / "source-lock.json").read_text())
    parsers = json.loads((DATA / "parsers.json").read_text())
    cell = json.loads((DATA / "cell.json").read_text())
    assert len(parsers) == cell["verified_third_party_count"]
    assert {p["name"] for p in parsers} == set(lock)
    prepare_c_wav.main()
    TARGET.mkdir(parents=True, exist_ok=True)
    rows = []
    installed = {}
    sources = {}
    for parser in parsers:
        name = parser["name"]
        item = lock[name]
        assert parser["version"] == item["release"]
        if item.get("source_build"):
            if name == "dr_wav":
                command = ["cc", "-std=c11", "-O2", "-I" + str(SOURCE / name),
                           str(ROOT / parser["adapter"]), "-o", str(TARGET / name)]
            elif name == "miniaudio":
                command = ["cc", "-std=c11", "-O2", "-I" + str(SOURCE / name),
                           str(ROOT / parser["adapter"]), str(SOURCE / name / "miniaudio.c"),
                           "-o", str(TARGET / name)]
            elif name == "libaudiofile":
                source = SOURCE / "audiofile"
                install = TARGET / "audiofile-install"
                configure = ["./configure", "--prefix=" + str(install), "--disable-static"]
                run(configure, cwd=source)
                run(["make", "-C", str(source), "-j4"])
                run(["make", "-C", str(source), "install"])
                library = install / "lib/libaudiofile.1.dylib"
                command = ["cc", "-std=c11", "-O2", "-I" + str(install / "include"),
                           str(ROOT / parser["adapter"]), "-L" + str(install / "lib"),
                           "-laudiofile", "-o", str(TARGET / name)]
                sources[name] = {"source_sha256": item["source_sha256"],
                                 "build_patch": "replace signed left shift of -1 in SimpleModule.h with equivalent unsigned mask expression",
                                 "configure_command": shlex.join(configure),
                                 "library_sha256": sha256(library.read_bytes()).hexdigest()}
            else:
                raise AssertionError(name)
            if name != "libaudiofile":
                sources[name] = {"source_sha256": item["source_sha256"],
                                 "files": {f["name"]: f["sha256"] for f in item["files"]}}
        else:
            library = Path(item["local_library"])
            digest = sha256(library.read_bytes()).hexdigest()
            assert digest == item["local_library_sha256"], name
            for extra in item.get("additional_libraries", []):
                assert sha256(Path(extra["path"]).read_bytes()).hexdigest() == extra["sha256"]
            if name == "csfml":
                version = run(["brew", "list", "--versions", "csfml"])
                assert version == "csfml " + item["release"]
                command = ["cc", "-std=c11", "-O2",
                           "-I" + str(library.parents[1] / "include"),
                           str(ROOT / parser["adapter"]), str(library),
                           "-o", str(TARGET / name)]
                installed[name] = {"brew_version": version, "library": str(library),
                                   "library_sha256": digest,
                                   "additional_libraries": item.get("additional_libraries", [])}
            else:
                version = run(["pkg-config", "--modversion", item["pkg_config"]])
                assert version == item["pkg_config_version"], (name, version)
                flags = shlex.split(run(["pkg-config", "--cflags", "--libs", *item["pkg_configs"]]))
                command = ["cc", "-std=c11", "-O2", str(ROOT / parser["adapter"]),
                           *flags, *item.get("extra_link_flags", []), "-o", str(TARGET / name)]
                installed[name] = {"pkg_config_version": version, "library": str(library),
                                   "library_sha256": digest,
                                   "additional_libraries": item.get("additional_libraries", [])}
        run(command)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute))
        expected = EXPECTED_METADATA if name == "sdl3_mixer" else EXPECTED
        assert parser["expected_output"] == expected
        assert output == expected, (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "build_command": shlex.join(command),
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["cc", "--version"]).splitlines()[0],
              "installed_libraries": installed, "source_builds": sources,
              "control": "controls/wav/four-samples.wav", "control_sha256": CONTROL_SHA256,
              "expected": EXPECTED, "expected_metadata": EXPECTED_METADATA,
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
