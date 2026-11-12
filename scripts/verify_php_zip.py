"""Install pinned Composer releases and verify PHP ZIP parsing on a valid control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/zip"
ADAPTER = ROOT / "adapters/php/zip"
CONTROL = ROOT / "controls/zip/hello.zip"
CONTROL_SHA256 = "c534fa083d1da92474852ca9168ba0793740c25205f828915a1d862bd78c776b"
EXPECTED = {"entries": 1, "name": "hello.txt", "content": "parsarium\n"}


def execute(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    parsers = json.loads((DATA / "parsers.json").read_text())
    standard = json.loads((DATA / "standard.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    cell = json.loads((DATA / "cell.json").read_text())
    assert len(parsers) == cell["verified_third_party_count"]
    assert len(standard["verified_apis"]) == cell["verified_standard_or_runtime_count"]

    lock_paths = sorted({parser["composer_lock"] for parser in parsers})
    locks = {}
    for lock_path in lock_paths:
        path = ROOT / lock_path
        execute(["composer", "install", "--no-interaction", "--no-progress",
                 "--prefer-dist", "--no-plugins", "--no-scripts", "--no-dev"], path.parent)
        locks[lock_path] = {item["name"]: item for item in json.loads(path.read_text())["packages"]}

    rows = []
    for parser in parsers:
        name = parser["name"]
        release = snapshot["releases"][name]
        installed = locks[parser["composer_lock"]][name]
        assert parser["version"] == release["version"] == installed["version"]
        assert release["source_reference"] == installed["source"]["reference"]
        command = ["php", "-d", "display_errors=0", str(ROOT / parser["adapter"]), str(CONTROL)]
        run = execute(command)
        output = json.loads(run.stdout)
        assert output == parser["expected_output"] == EXPECTED, name
        rows.append({"package": name, "version": parser["version"],
                     "composer_lock": parser["composer_lock"],
                     "source_reference": installed["source"]["reference"],
                     "control": parser["control"], "command": shlex.join(command),
                     "output": output, "stderr": run.stderr.strip(), "pass": True})
        print(f"{name}@{parser['version']}: passed")

    runtime_rows = []
    for api in standard["verified_apis"]:
        command = ["php", "-d", "display_errors=0", str(ROOT / api["adapter"]), str(CONTROL)]
        run = execute(command)
        output = json.loads(run.stdout)
        assert output == api["expected_output"] == EXPECTED, api["name"]
        runtime_rows.append({"name": api["name"], "control": api["control"],
                             "command": shlex.join(command), "output": output,
                             "stderr": run.stderr.strip(), "pass": True})
        print(f"{api['name']}: runtime passed")

    versions = json.loads(execute(["php", "-r", "echo json_encode([PHP_VERSION, phpversion('zip'), ZipArchive::LIBZIP_VERSION, phpversion('Phar')]);"]).stdout)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "php_version": versions[0],
              "zip_extension_version": versions[1], "libzip_version": versions[2],
              "phar_extension_version": versions[3],
              "composer_version": execute(["composer", "--version"]).stdout.strip(),
              "composer_locks": {path: sha256((ROOT / path).read_bytes()).hexdigest()
                                 for path in lock_paths},
              "control": "controls/zip/hello.zip", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": runtime_rows}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
