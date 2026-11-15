"""Build and replay one format/ecosystem/package project on its valid control."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def command(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)} failed:\n{result.stderr[-4000:]}")
    return result.stdout.strip()


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("format")
    cli.add_argument("ecosystem")
    cli.add_argument("package_slug")
    args = cli.parse_args()
    project = ROOT / "projects" / args.format / args.ecosystem / args.package_slug
    manifest = json.loads((project / "manifest.json").read_text())
    assert manifest["schema_version"] == 1
    assert (manifest["format"], manifest["ecosystem"]) == (args.format, args.ecosystem)
    parsers = json.loads((ROOT / manifest["catalog_parser"]).read_text())
    parser, = [p for p in parsers if p["name"] == manifest["package"]]
    assert parser["version"] == manifest["release"]
    assert parser["expected_output"] == manifest["expected_output"]
    lock_path = ROOT / manifest["source_lock"]
    if lock_path.suffix == ".json":
        lock = json.loads(lock_path.read_text())[manifest["package"]]
        assert lock["release"] == manifest["release"]
        assert lock["source_sha256"] == manifest["source_sha256"]
    else:
        lock = lock_path.read_text()
        assert f"{manifest['package']}=={manifest['release']}" in lock
        assert manifest["source_sha256"] in lock
    control = ROOT / manifest["control"]
    assert sha256(control.read_bytes()).hexdigest() == manifest["control_sha256"]

    image = f"parsarium/{args.format}-{args.ecosystem}-{args.package_slug}:local"
    print(f"Building {image}", flush=True)
    command(["docker", "build", "--quiet", "--platform", manifest["platform"],
             "-t", image, str(project)])
    output_dir = project / "target/coverage"
    output_dir.mkdir(parents=True, exist_ok=True)
    docker_run = ["docker", "run", "--rm", "--platform", manifest["platform"],
                  "--network", "none", "--read-only", "--cap-drop", "ALL",
                  "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
                  "-v", f"{control}:/input/control:ro",
                  "-v", f"{output_dir}:/coverage", image]
    print(command(docker_run), flush=True)
    engine = subprocess.run(["docker", "run", "--rm", "--platform", manifest["platform"],
                             "--network", "none", "--read-only", "--cap-drop", "ALL",
                             "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
                             "--entrypoint", manifest.get("fuzz_smoke_entrypoint", "/work/fuzzer"),
                             image, *manifest.get("fuzz_smoke_args", ["-help=1"])],
                            cwd=ROOT, text=True, capture_output=True)
    if engine.returncode or manifest.get("fuzz_smoke_expect", "Usage:") not in engine.stdout + engine.stderr:
        raise RuntimeError(f"fuzz engine smoke test failed:\n{engine.stderr[-2000:]}")
    summary = json.loads((output_dir / "summary.json").read_text())
    assert summary["control_pass"] and summary["output"] == manifest["expected_output"]
    assert summary["parser_source_lines_covered"] > 0
    coverage = json.loads((output_dir / "coverage.json").read_text())
    source_files = [f for f in coverage["data"][0]["files"]
                    if f["filename"].startswith(manifest["coverage_subject_prefix"])]
    assert len(source_files) == summary["parser_source_files"]
    assert sum(f["summary"]["lines"]["covered"] for f in source_files) == summary["parser_source_lines_covered"]
    receipt = {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest": f"projects/{args.format}/{args.ecosystem}/{args.package_slug}/manifest.json",
        "image_id": command(["docker", "image", "inspect", image, "--format", "{{.Id}}"]),
        "docker_server_version": command(["docker", "version", "--format", "{{.Server.Version}}"]),
        "platform": manifest["platform"],
        "toolchain": command(["docker", "run", "--rm", "--entrypoint", "cat", image, "/work/toolchain.txt"]).splitlines(),
        "source_sha256": manifest["source_sha256"],
        "control_sha256": manifest["control_sha256"],
        "project_file_sha256": {
            path.name: sha256(path.read_bytes()).hexdigest()
            for path in sorted(project.iterdir()) if path.is_file() and path.name != "verification.json"
        },
        "output": summary["output"],
        "parser_source_files": summary["parser_source_files"],
        "parser_source_lines_covered": summary["parser_source_lines_covered"],
        "fuzz_engine_smoke_pass": True,
        "coverage_output": f"projects/{args.format}/{args.ecosystem}/{args.package_slug}/target/coverage/coverage.json",
        "pass": True,
    }
    (project / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified {args.format}/{args.ecosystem}/{manifest['package']}: {receipt['parser_source_lines_covered']} library lines covered")


if __name__ == "__main__":
    main()
