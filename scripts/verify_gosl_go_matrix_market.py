"""Verify Gosl's released Matrix Market reader in its documented Linux environment."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/go/matrix_market/gosl"
LOCK = ROOT / "data/go/matrix_market/gosl-lock.json"
ATI_ADAPTER = ROOT / "adapters/go/matrix_market/gosl_ati"
ATI_LOCK = ROOT / "data/go/matrix_market/gosl-ati-lock.json"
IMAGE = "parsarium-gosl-mm-v1.2.15"


def run(command: list[str], timeout: int = 900) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                            timeout=timeout)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(command[:4])} failed: {result.stderr[-2000:]}")
    return result.stdout.strip()


def docker_command(adapter: Path, *arguments: str) -> list[str]:
    return ["docker", "run", "--rm", "--platform", "linux/arm64",
            "-v", f"{ROOT}:/repo:ro", "-w", "/repo/" + str(adapter.relative_to(ROOT)),
            IMAGE, *arguments]


def verify(parser=None) -> tuple[dict, dict]:
    ati = parser is not None and parser["name"] == "github.com/ATIinc/gosl-ati/la"
    adapter = ATI_ADAPTER if ati else ADAPTER
    lock = json.loads((ATI_LOCK if ati else LOCK).read_text())
    container = json.loads(LOCK.read_text())
    parser = parser or {
        "name": lock["package"], "module": lock["module"],
        "version": lock["release"], "scope": "Coordinate real matrix dimensions, entries and value",
        "control": lock["control"],
        "expected_output": {"rows": 2, "cols": 3, "entries": 3,
                            "value_0_2": -2, "symmetric": False},
    }
    assert parser["name"] == lock["package"]
    assert parser["version"] == lock["release"]
    assert parser["control"] == lock["control"]
    control = ROOT / lock["control"]
    assert hashlib.sha256(control.read_bytes()).hexdigest() == lock["control_sha256"]
    module_text = (adapter / "go.mod").read_text()
    sums_text = (adapter / "go.sum").read_text()
    assert f"{lock['module']} {lock['release']}" in module_text
    assert f"{lock['module']} {lock['release']} {lock['module_sum']}" in sums_text
    assert f"{lock['module']} {lock['release']}/go.mod {lock['go_mod_sum']}" in sums_text
    if ati:
        assert lock["container_lock"] == str(LOCK.relative_to(ROOT))
    dockerfile = (ADAPTER / "Dockerfile").read_text()
    assert f"FROM {container['container_base']}" in dockerfile
    for package, version in container["direct_dependency_versions"].items():
        assert f"{package}={version}" in dockerfile

    image_id = run(["docker", "build", "--quiet", "--platform", container["platform"],
                    "-t", IMAGE, str(ADAPTER)])
    assert image_id.startswith("sha256:")
    go_version = run(docker_command(adapter, "go", "version"), timeout=30)
    assert go_version == container["go_version"]
    packages = list(container["direct_dependency_versions"])
    installed = run(docker_command(adapter, "dpkg-query", "-W", *packages), timeout=30)
    observed = {}
    for line in installed.splitlines():
        name, version = line.split("\t", 1)
        observed[name.removesuffix(":arm64")] = version
    assert observed == container["direct_dependency_versions"]

    output_text = run(docker_command(adapter, "go", "run", "-mod=readonly", ".",
                                     "/repo/" + lock["control"]), timeout=240)
    output = json.loads(output_text.splitlines()[-1])
    assert output == parser["expected_output"], output
    row = {
        "package": parser["name"], "module": parser["module"],
        "version": parser["version"], "scope": parser["scope"],
        "control": parser["control"],
        "command": "python3 scripts/verify_gosl_go_matrix_market.py" +
                   (" --package github.com/ATIinc/gosl-ati/la" if ati else ""),
        "pass": True, "output": output, "error": None,
        "environment": "Ubuntu 24.04 linux/arm64 digest-pinned base; exact direct apt package versions; Go 1.22.2; released Go module verified by go.sum",
    }
    library = {"image_id": image_id, "go_version": go_version,
               "direct_dependency_versions": observed,
               "module_sum": lock["module_sum"],
               "source_commit": lock["source_commit"]}
    return row, library


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--package":
        catalog = json.loads((ROOT / "data/go/matrix_market/parsers.json").read_text())
        selected = next(p for p in catalog if p["name"] == sys.argv[2])
    elif len(sys.argv) == 1:
        selected = None
    else:
        raise SystemExit("usage: verify_gosl_go_matrix_market.py [--package PACKAGE]")
    result, library = verify(selected)
    print(json.dumps({"result": result, "library": library}, sort_keys=True))
