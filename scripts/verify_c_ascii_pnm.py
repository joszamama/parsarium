"""Verify pinned C image readers on a valid ASCII P3 PNM control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess
import tarfile
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/ascii_pnm"
TARGET = ROOT / "adapters/c/ascii_pnm/target"
CONTROL = ROOT / "controls/ascii_pnm/red-green.ppm"
CONTROL_SHA256 = "f1e86f7bc611601fed6f44a263d8c1f026dd1d0fd66a7dbc8530e245f5561bf1"


def run(command: list[str]) -> str:
    return subprocess.run(command, cwd=ROOT, check=True, text=True,
                          capture_output=True).stdout.strip()


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    parsers = json.loads((DATA / "parsers.json").read_text())
    cell = json.loads((DATA / "cell.json").read_text())
    lock = json.loads((ROOT / "data/c/png/source-lock.json").read_text())
    lock.update(json.loads((DATA / "source-lock.json").read_text()))
    assert len(parsers) == cell["verified_third_party_count"]
    TARGET.mkdir(parents=True, exist_ok=True)
    rows, local_libraries = [], {}
    for parser in parsers:
        name = parser["name"]
        item = lock[name]
        assert parser["version"] == item["release"]
        if name == "libpnmrw":
            cache = ROOT / "adapters/c/ascii_pnm/cache"
            cache.mkdir(parents=True, exist_ok=True)
            archive = cache / "libpnmrw_14Aug2014.tar.gz"
            if not archive.exists():
                run(["curl", "-L", "--fail", "--silent", "--show-error",
                     item["source_url"], "-o", str(archive)])
            assert sha256(archive.read_bytes()).hexdigest() == item["source_sha256"]
            source = cache / "libpnmrw"
            source.mkdir(exist_ok=True)
            with tarfile.open(archive) as tar:
                for filename in ("libpnmrw.c", "libpnmrw.h"):
                    member = tar.extractfile(f"libpnmrw/{filename}")
                    assert member is not None
                    (source / filename).write_bytes(member.read())
            object_file = TARGET / "libpnmrw-lib.o"
            source_build = ["cc", "-std=c11", "-O2", "-I" + str(source),
                            "-c", str(source / "libpnmrw.c"), "-o", str(object_file)]
            run(source_build)
            command = ["cc", "-std=c11", "-O2", "-I" + str(source),
                       str(ROOT / parser["adapter"]), str(object_file),
                       "-o", str(TARGET / name)]
            run(command)
            execute = [str(TARGET / name), str(CONTROL)]
            output = json.loads(run(execute))
            assert output == parser["expected_output"], (name, output)
            local_libraries[name] = {"source_archive": str(archive),
                                     "source_sha256": item["source_sha256"],
                                     "source_build_command": shlex.join(source_build)}
            rows.append({"package": name, "version": parser["version"],
                         "control": parser["control"], "build_command": shlex.join(command),
                         "command": shlex.join(execute), "output": output, "pass": True})
            print(f"{name}@{parser['version']}: P3 passed")
            continue
        if name == "netpbm":
            version_bytes = urllib.request.urlopen(item["version_file_url"], timeout=20).read()
            assert sha256(version_bytes).hexdigest() == item["version_file_sha256"]
            assert b"NETPBM_MAJOR_RELEASE = 11\nNETPBM_MINOR_RELEASE = 2\nNETPBM_POINT_RELEASE = 30\n" == version_bytes
        library = Path(item["local_library"])
        digest = sha256(library.read_bytes()).hexdigest()
        assert digest == item["local_library_sha256"], name
        additional_libraries = []
        for extra in item.get("additional_libraries", []):
            extra_path = Path(extra["path"])
            extra_digest = sha256(extra_path.read_bytes()).hexdigest()
            assert extra_digest == extra["sha256"], name
            additional_libraries.append({"library": str(extra_path), "library_sha256": extra_digest})
        if name == "netpbm":
            receipt = json.loads((library.parents[1] / "INSTALL_RECEIPT.json").read_text())
            assert receipt["source"]["scm_revision"] == str(item["svn_revision"])
            assert receipt["source"]["versions"]["stable"] == item["release"]
        if name == "freeimage":
            observed = item["release"]
            prefix = library.parents[1]
            command = ["cc", "-std=c11", "-O2", "-I" + str(prefix / "include"),
                       str(ROOT / parser["adapter"]), "-L" + str(prefix / "lib"),
                       "-lfreeimage", "-o", str(TARGET / name)]
        else:
            observed = run(["pkg-config", "--modversion", item["pkg_config"]])
            if name == "imagemagick":
                assert observed == item["release"].rsplit("-", 1)[0]
                assert item["release"] in run(["magick", "-version"])
            elif name == "devil":
                assert observed == ""  # Installed IL.pc leaves Version blank.
            elif name == "netpbm":
                assert observed == "11.2.30"
            elif name == "ffmpeg":
                assert observed == item["pkg_config_version"]
            else:
                assert observed == item["release"], (name, observed)
            packages = ([item["pkg_config"], "x11"] if name == "imlib2" else
                        item.get("pkg_configs", [item["pkg_config"]]))
            flags = shlex.split(run(["pkg-config", "--cflags", "--libs", *packages]))
            command = ["cc", "-std=c11", "-O2", str(ROOT / parser["adapter"]),
                       *flags, "-o", str(TARGET / name)]
        run(command)
        execute = [str(TARGET / name), str(CONTROL)]
        output = json.loads(run(execute))
        assert output == parser["expected_output"], (name, output)
        local_libraries[name] = {"pkg_config_version": observed,
                                 "library": str(library), "library_sha256": digest,
                                 "additional_libraries": additional_libraries}
        rows.append({"package": name, "version": parser["version"],
                     "control": parser["control"], "build_command": shlex.join(command),
                     "command": shlex.join(execute), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: P3 passed")
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "compiler": run(["cc", "--version"]).splitlines()[0],
              "source_lock": "data/c/png/source-lock.json",
              "extra_source_lock": "data/c/ascii_pnm/source-lock.json",
              "local_libraries": local_libraries,
              "control": "controls/ascii_pnm/red-green.ppm",
              "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": []}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
