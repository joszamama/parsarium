"""Install pinned Composer releases and verify PHP PNG parsing on a valid control."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import shlex
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/png"
CONTROL = ROOT / "controls/png/red-green.png"
CONTROL_SHA256 = "5a852fbaaaecaf4cd14c01e150c7f881c5c5894b0a1e3c53be7e007c58374ee6"


def execute(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)


def main() -> None:
    assert sha256(CONTROL.read_bytes()).hexdigest() == CONTROL_SHA256
    cell = json.loads((DATA / "cell.json").read_text())
    parsers = json.loads((DATA / "parsers.json").read_text())
    standard = json.loads((DATA / "standard.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    assert len(parsers) == cell["verified_third_party_count"]
    assert len(standard["verified_apis"]) == cell["verified_standard_or_runtime_count"]

    lock_path = ROOT / "adapters/php/png/composer.lock"
    execute(["composer", "install", "--no-interaction", "--no-progress",
             "--prefer-dist", "--no-plugins", "--no-scripts", "--no-dev"], lock_path.parent)
    locked = {item["name"]: item for item in json.loads(lock_path.read_text())["packages"]}

    rows = []
    for parser in parsers:
        name = parser["name"]
        release = snapshot["releases"][name]
        installed = locked[name]
        assert parser["version"] == release["version"] == installed["version"]
        assert release["source_reference"] == installed["source"]["reference"]
        command = ["php", "-d", "display_errors=0", str(ROOT / parser["adapter"]), str(CONTROL)]
        run = execute(command)
        output = json.loads(run.stdout)
        assert output == parser["expected_output"], name
        assert output["width"] == 2 and output["height"] == 1, name
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
        assert output == api["expected_output"], api["name"]
        runtime_rows.append({"name": api["name"], "control": api["control"],
                             "command": shlex.join(command), "output": output,
                             "stderr": run.stderr.strip(), "pass": True})
        print(f"{api['name']}: runtime passed")

    versions = json.loads(execute(["php", "-r", "echo json_encode([PHP_VERSION, gd_info()['GD Version']]);"]).stdout)
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "php_version": versions[0],
              "gd_version": versions[1],
              "composer_version": execute(["composer", "--version"]).stdout.strip(),
              "composer_lock": "adapters/php/png/composer.lock",
              "composer_lock_sha256": sha256(lock_path.read_bytes()).hexdigest(),
              "control": "controls/png/red-green.png", "control_sha256": CONTROL_SHA256,
              "third_party": rows, "runtime": runtime_rows}
    (DATA / "verification.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
