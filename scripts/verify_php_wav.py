"""Replay pinned PHP WAV package adapters on valid PCM16 RIFF/WAVE controls."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/wav"
CONTROL = ROOT / "controls/wav/256-samples.wav"


def execute(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)


def lock_is_installed(path: Path, packages: list[dict]) -> bool:
    installed_path = path.parent / "vendor/composer/installed.json"
    autoload_path = path.parent / "vendor/autoload.php"
    if not installed_path.is_file() or not autoload_path.is_file():
        return False
    installed = {item["name"]: item for item in json.loads(installed_path.read_text())["packages"]}
    return all(
        (item := installed.get(package["name"])) is not None
        and item["version"] == package["version"]
        and item["source"]["reference"] == package["source"]["reference"]
        and (path.parent / "vendor" / package["name"]).is_dir()
        for package in packages
    )


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    locks = {}
    for name in sorted({parser["composer_lock"] for parser in parsers}):
        path = ROOT / name
        packages = json.loads(path.read_text())["packages"]
        if not lock_is_installed(path, packages):
            execute(["composer", "install", "--no-interaction", "--no-progress", "--prefer-dist",
                     "--no-plugins", "--no-scripts", "--no-dev"], path.parent)
        locks[name] = {
            "packages": {package["name"]: package for package in packages},
            "sha256": sha256(path.read_bytes()).hexdigest(),
        }

    rows = []
    for parser in parsers:
        name = parser["name"]
        release = snapshot["releases"][name]
        lock = locks[parser["composer_lock"]]
        package = lock["packages"][name]
        assert parser["version"] == release["version"] == package["version"]
        assert package["source"]["reference"] == release["source_reference"]
        command = ["php", "-d", "ffi.enable=1", "-d", "display_errors=0", "-d", "log_errors=0",
                   str(ROOT / parser["adapter"]), name, str(ROOT / parser["control"])]
        output = json.loads(execute(command).stdout.strip())
        assert output == parser["expected_output"], (name, output)
        rows.append({"package": name, "version": parser["version"],
                     "composer_lock": parser["composer_lock"], "composer_lock_sha256": lock["sha256"],
                     "source_reference": release["source_reference"],
                     "control": parser["control"],
                     "control_sha256": sha256((ROOT / parser["control"]).read_bytes()).hexdigest(),
                     "command": " ".join(command), "output": output, "pass": True})
        print(f"{name}@{parser['version']}: passed")

    probe_command = ["php", str(ROOT / "adapters/php/wav/runtime_probe.php"), str(CONTROL)]
    probe = json.loads(execute(probe_command).stdout.strip())
    assert probe == {"fileinfo_loaded": True, "fileinfo_mime": "audio/x-wav", "ffi_loaded": True}
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(),
              "php_version": execute(["php", "-r", "echo PHP_VERSION;"]).stdout,
              "composer_version": execute(["composer", "--version"]).stdout.strip(),
              "mediainfo_cli_version": execute(["mediainfo", "--Version"]).stdout.strip(),
              "ffmpeg_cli_version": execute(["ffmpeg", "-version"]).stdout.splitlines()[0],
              "sox_cli_version": execute(["sox", "--version"]).stdout.strip(),
              "controls": [{"path": name, "sha256": sha256((ROOT / name).read_bytes()).hexdigest()}
                           for name in sorted({parser["control"] for parser in parsers})],
              "composer_locks": [{"path": name, "sha256": lock["sha256"]}
                                 for name, lock in locks.items()],
              "third_party": rows, "runtime": [],
              "runtime_probe": {"command": " ".join(probe_command), "output": probe, "pass": True}}
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        native = ROOT / "adapters/php/mp3/soundfile/vendor/phpmlkit/soundfile/lib/darwin-arm64/libsndfile.1.2.2.dylib"
        assert native.is_file()
        report["soundfile_native_library"] = {"path": str(native.relative_to(ROOT)),
                                               "sha256": sha256(native.read_bytes()).hexdigest()}
    (DATA / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(rows)}/{len(parsers)} PHP WAV paths passed")


if __name__ == "__main__":
    main()
