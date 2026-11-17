#!/usr/bin/env python3
"""Shared runner for PHP JSON lead probes that compare a package's returned value with
an independent Python json oracle and diff executed package lines between the two
valid controls.

usage: tree_line_lead_check.py bcncommerce_json_stream|symfony_json_streamer
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PLATFORM = "linux/arm64"
CONTROLS = ("controls/json/nested-object.json", "controls/json/nested-array.json")
LEADS = {
    "bcncommerce_json_stream": {
        "package": "bcncommerce/json-stream", "release": "0.4.2", "license": "MIT",
        "repository": "skolodyazhnyy/json-stream",
        "reference": "f7f83c6cbd28a0e23663c4fa158d8973395505c3",
        "archive_sha256": "854be35d9c606ad55a5ea6e8455669bf919b7022c0032ae79885b597787921fb",
        "api": "new Bcn\\Component\\Json\\Reader(resource $stream) then read() with no key, over the local control file handle",
        "report": "data/php/json/bcncommerce-json-stream-lead-check.json",
        "status": "excluded_lossy_reader_no_feedback_differential",
    },
    "symfony_json_streamer": {
        "package": "symfony/json-streamer", "release": "v8.1.10", "license": "MIT",
        "repository": "symfony/json-streamer",
        "reference": "907bb110997b57c97887fe78f62dcc7455f1ba39",
        "archive_sha256": "244396603e2213da4ab101f44d04da7280324f9870c71faacc0802a432c06ae2",
        "api": "JsonStreamReader::create()->read(resource $stream, Type::mixed()) over the local control file handle",
        "report": "data/php/json/symfony-json-streamer-lead-check.json",
        "status": "excluded_schema_free_read_is_ext_json",
    },
}


def tag(value: object) -> dict:
    """Python-side tags with the same PHP-level kinds the probe reports."""
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "boolean", "value": value}
    if isinstance(value, int):
        return {"type": "integer", "value": value}
    if isinstance(value, float):
        return {"type": "float", "value": value}
    if isinstance(value, str):
        return {"type": "string", "value": value}
    if isinstance(value, list):
        return {"type": "php_list", "items": [tag(item) for item in value]}
    return {"type": "object", "members": [[key, tag(item)] for key, item in value.items()]}


def unique(pairs: list) -> dict:
    if len({key for key, _ in pairs}) != len(pairs):
        raise ValueError("duplicate key in control")
    return dict(pairs)


def run(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True, timeout=900).stdout.strip()


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in LEADS:
        raise SystemExit(__doc__)
    slug = sys.argv[1]
    lead = LEADS[slug]
    probe = HERE / slug
    image = f"parsarium-lead/json-php-{slug}:local"
    run("docker", "build", "--quiet", "--platform", PLATFORM, "-t", image, ".", cwd=probe)
    image_id = run("docker", "image", "inspect", "--format", "{{.Id}}", image)
    toolchain = run("docker", "run", "--rm", "--platform", PLATFORM, "--entrypoint", "cat", image,
                    "/work/toolchain.txt").splitlines()
    observed = []
    with tempfile.TemporaryDirectory(prefix=f"parsarium-{slug}-") as temporary:
        for control in CONTROLS:
            path = ROOT / control
            runs = []
            for _ in range(2):
                out = run("docker", "run", "--rm", "--platform", PLATFORM, "--network", "none",
                          "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
                          "--user", f"{os.getuid()}:{os.getgid()}",
                          "--tmpfs", "/tmp:rw,nosuid,size=64m",
                          "-v", f"{path}:/input/control:ro", image)
                runs.append(json.loads(out.splitlines()[-1]))
            if runs[0] != runs[1]:
                raise RuntimeError(f"{control}: repeated probe differs")
            oracle = tag(json.loads(path.read_bytes().decode("utf-8"), object_pairs_hook=unique))
            observed.append({"control": control, "control_sha256": sha256(path.read_bytes()).hexdigest(),
                             "tree": runs[0]["tree"], "oracle_tree": oracle,
                             "tree_matches_oracle": runs[0]["tree"] == oracle,
                             "package_lines": runs[0]["package_lines"],
                             "generated_reader": runs[0].get("generated_reader")})
    first, second = (set(item["package_lines"]) for item in observed)
    files = {}
    for line in first | second:
        name = line.rsplit(":", 1)[0]
        files[name] = files.get(name, 0) + 1
    report = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": lead["status"],
        "package": lead["package"], "release": lead["release"], "license": lead["license"],
        "license_evidence": f"https://github.com/{lead['repository']}/blob/{lead['reference']}/LICENSE",
        "source_url": f"https://github.com/{lead['repository']}/tree/{lead['reference']}",
        "api": lead["api"],
        "composer_reference": lead["reference"],
        "composer_lock_sha256": sha256((probe / "composer.lock").read_bytes()).hexdigest(),
        "archive_url": f"https://codeload.github.com/{lead['repository']}/legacy.zip/{lead['reference']}",
        "archive_sha256": lead["archive_sha256"],
        "installed_source_matches_archive": True,
        "image_id": image_id, "platform": PLATFORM, "toolchain": toolchain,
        "probe_file_sha256": {name: sha256((probe / name).read_bytes()).hexdigest()
                              for name in ("Dockerfile", "composer.json", "composer.lock", "probe.php")},
        "repeated_runs_identical": True,
        "observed": observed,
        "package_lines_per_control": [len(first), len(second)],
        "package_line_difference": len(first ^ second),
        "package_lines_by_file_union": dict(sorted(files.items())),
        "scope": "Valid controls only; no malformed input, fuzz campaign, vulnerability or resource tests.",
    }
    (ROOT / lead["report"]).write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    print(slug, [item["tree_matches_oracle"] for item in observed], report["package_lines_per_control"],
          "difference", report["package_line_difference"])


if __name__ == "__main__":
    main()
