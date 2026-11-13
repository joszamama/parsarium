"""Verify Gosl's released Matrix Market reader in its documented Linux environment."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/go/matrix_market/gosl"
LOCK = ROOT / "data/go/matrix_market/gosl-lock.json"
IMAGE = "parsarium-gosl-mm-v1.2.15"


def run(command: list[str], timeout: int = 900) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                            timeout=timeout)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(command[:4])} failed: {result.stderr[-2000:]}")
    return result.stdout.strip()


def docker_command(*arguments: str) -> list[str]:
    return ["docker", "run", "--rm", "--platform", "linux/arm64",
            "-v", f"{ROOT}:/repo:ro", "-w", "/repo/adapters/go/matrix_market/gosl",
            IMAGE, *arguments]


def verify(parser=None) -> tuple[dict, dict]:
    lock = json.loads(LOCK.read_text())
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
    module_text = (ADAPTER / "go.mod").read_text()
    sums_text = (ADAPTER / "go.sum").read_text()
    assert f"{lock['module']} {lock['release']}" in module_text
    assert f"{lock['module']} {lock['release']} {lock['module_sum']}" in sums_text
    assert f"{lock['module']} {lock['release']}/go.mod {lock['go_mod_sum']}" in sums_text
    dockerfile = (ADAPTER / "Dockerfile").read_text()
    assert f"FROM {lock['container_base']}" in dockerfile
    for package, version in lock["direct_dependency_versions"].items():
        assert f"{package}={version}" in dockerfile

    image_id = run(["docker", "build", "--quiet", "--platform", lock["platform"],
                    "-t", IMAGE, str(ADAPTER)])
    assert image_id.startswith("sha256:")
    go_version = run(docker_command("go", "version"), timeout=30)
    assert go_version == lock["go_version"]
    packages = list(lock["direct_dependency_versions"])
    installed = run(docker_command("dpkg-query", "-W", *packages), timeout=30)
    observed = {}
    for line in installed.splitlines():
        name, version = line.split("\t", 1)
        observed[name.removesuffix(":arm64")] = version
    assert observed == lock["direct_dependency_versions"]

    output_text = run(docker_command("go", "run", "-mod=readonly", ".",
                                     "/repo/" + lock["control"]), timeout=240)
    output = json.loads(output_text.splitlines()[-1])
    assert output == parser["expected_output"], output
    row = {
        "package": parser["name"], "module": parser["module"],
        "version": parser["version"], "scope": parser["scope"],
        "control": parser["control"],
        "command": "python3 scripts/verify_gosl_go_matrix_market.py",
        "pass": True, "output": output, "error": None,
        "environment": "Ubuntu 24.04 linux/arm64 digest-pinned base; exact direct apt package versions; Go 1.22.2; module v1.2.15 verified by go.sum",
    }
    library = {"image_id": image_id, "go_version": go_version,
               "direct_dependency_versions": observed,
               "module_sum": lock["module_sum"],
               "source_commit": lock["source_commit"]}
    return row, library


if __name__ == "__main__":
    result, library = verify()
    print(json.dumps({"result": result, "library": library}, sort_keys=True))
