"""Build and replay one format/ecosystem/package project on its valid control."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import re
import os
from pathlib import Path
import shutil
import subprocess
from docker_slots import docker_build_slot


ROOT = Path(__file__).resolve().parents[1]


def command(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, errors="replace", capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)} failed:\n{result.stderr[-4000:]}")
    return result.stdout.strip()


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("format")
    cli.add_argument("ecosystem")
    cli.add_argument("package_slug")
    args = cli.parse_args()
    project_root = ROOT / "projects"
    project = (project_root / args.format / args.ecosystem / args.package_slug).resolve()
    assert project.is_relative_to(project_root)
    manifest = json.loads((project / "manifest.json").read_text())
    assert manifest["schema_version"] == 1
    assert (manifest["format"], manifest["ecosystem"]) == (args.format, args.ecosystem)
    if manifest.get("kind") == "standard":
        inventory = json.loads((ROOT / manifest["standard_inventory"]).read_text())
        entry, = [item for item in inventory["verified_apis"] if item["api"] == manifest["api"]]
        assert entry["runtime"] == manifest["runtime"]
        assert entry["control"] == manifest["control"]
        assert entry["expected"] == manifest["expected_output"]
        lock_path = project / manifest["runtime_lock"]
        lock = json.loads(lock_path.read_text())
        assert lock == {"runtime": manifest["runtime"],
                        "base_image": manifest["base_image"],
                        "source_sha256": manifest["source_sha256"]}
    else:
        assert manifest.get("kind", "third_party") == "third_party"
        parsers = json.loads((ROOT / manifest["catalog_parser"]).read_text())
        parser, = [p for p in parsers if p["name"] == manifest["package"]]
        assert parser["version"] == manifest["release"]
        if "expected_output" in parser:
            expected = parser["expected_output"]
        else:
            legacy = json.loads((ROOT / manifest["catalog_parser"]).with_name("verification.json").read_text())
            records = legacy.get("third_party", legacy.get("results", []))
            record, = [item for item in records if item["package"] == manifest["package"]]
            assert record["pass"] and record["version"] == manifest["release"]
            expected = record["output"]
        assert expected == manifest["expected_output"]
        lock_path = ROOT / manifest["source_lock"]
        if lock_path.suffix == ".json":
            lock = json.loads(lock_path.read_text())[manifest["package"]]
            assert lock["release"] == manifest["release"]
            assert lock["source_sha256"] == manifest["source_sha256"]
            if "go_module_sum" in lock:
                go_sum = (project / "go.sum").read_text()
                module = lock.get("go_module", manifest["package"])
                assert f"{module} {manifest['release']} {lock['go_module_sum']}" in go_sum
            if "npm_integrity" in lock:
                npm_lock = json.loads((project / "package-lock.json").read_text())
                package = npm_lock["packages"][f"node_modules/{manifest['package']}"]
                assert package["version"] == manifest["release"]
                assert package["integrity"] == lock["npm_integrity"]
                if manifest.get("fuzz_engine") == "Jazzer.js":
                    assert npm_lock["packages"]["node_modules/@jazzer.js/core"]["version"] == manifest["fuzz_engine_release"]
            if "composer_reference" in lock:
                composer_lock = json.loads((project / "composer.lock").read_text())
                package, = [item for item in composer_lock["packages"] if item["name"] == manifest["package"]]
                assert package["version"] == manifest["release"]
                assert package["source"]["reference"] == lock["composer_reference"]
                if manifest.get("fuzz_engine") == "nikic/php-fuzzer":
                    engine, = [item for item in composer_lock["packages"] if item["name"] == "nikic/php-fuzzer"]
                    assert engine["version"] == manifest["fuzz_engine_release"]
        else:
            lock = lock_path.read_text()
            normalized_package = re.sub(r"[-_.]+", "-", manifest["package"]).lower()
            locked = {re.sub(r"[-_.]+", "-", name).lower(): version
                      for name, version in re.findall(r"(?m)^([A-Za-z0-9_.-]+)==([^\s\\]+)", lock)}
            assert locked.get(normalized_package) == manifest["release"]
            assert manifest["source_sha256"] in lock
    docker_text = (project / "Dockerfile").read_text()
    for field in ("base_image", "source_sha256", "fuzz_engine_sha256"):
        if field in manifest:
            assert manifest[field] in docker_text
    for dependency in manifest.get("dependencies", []):
        assert lock_path.suffix != ".json"
        assert f"{dependency['package']}=={dependency['release']}" in lock
        assert dependency["sha256"] in lock and dependency["sha256"] in docker_text
    control = ROOT / manifest["control"]
    assert sha256(control.read_bytes()).hexdigest() == manifest["control_sha256"]

    image = f"parsarium/{args.format}-{args.ecosystem}-{args.package_slug}:local"
    print(f"Building {image}", flush=True)
    with docker_build_slot():
        command(["docker", "build", "--quiet", "--platform", manifest["platform"],
                 "-t", image, str(project)])
    output_dir = project / "target/coverage"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    tmpfs = "/tmp:rw,exec,nosuid,size=64m" if manifest.get("tmpfs_exec") else "/tmp:rw,nosuid,size=64m"
    docker_run = ["docker", "run", "--rm", "--platform", manifest["platform"],
                  "--network", "none", "--read-only", "--cap-drop", "ALL",
                  "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
                  "--tmpfs", tmpfs,
                  "-v", f"{control}:/input/control:ro",
                  "-v", f"{output_dir}:/coverage", image]
    print(command(docker_run), flush=True)
    engine = subprocess.run(["docker", "run", "--rm", "--platform", manifest["platform"],
                             "--network", "none", "--read-only", "--cap-drop", "ALL",
                             "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
                             "--tmpfs", tmpfs,
                             "-v", f"{control}:/input/control:ro",
                             "--entrypoint", manifest.get("fuzz_smoke_entrypoint", "/work/fuzzer"),
                             image, *manifest.get("fuzz_smoke_args", ["-help=1"])],
                            cwd=ROOT, text=True, errors="replace", capture_output=True)
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
    format_specific_lines = None
    if "format_specific_coverage_file_suffix" in manifest:
        specific = [f for f in source_files
                    if f["filename"].endswith(manifest["format_specific_coverage_file_suffix"])]
        format_specific_lines = sum(f["summary"]["lines"]["covered"] for f in specific)
        assert format_specific_lines > 0
    if "underlying_coverage_subject_prefix" in manifest:
        underlying = [f for f in coverage["data"][0]["files"]
                      if f["filename"].startswith(manifest["underlying_coverage_subject_prefix"])]
        assert len(underlying) == summary["underlying_source_files"]
        assert sum(f["summary"]["lines"]["covered"] for f in underlying) == summary["underlying_source_lines_covered"]
        assert summary["underlying_source_lines_covered"] > 0
    receipt = {
        "kind": manifest.get("kind", "third_party"),
        "api": manifest.get("api"),
        "runtime": manifest.get("runtime"),
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest": f"projects/{args.format}/{args.ecosystem}/{args.package_slug}/manifest.json",
        "image_id": command(["docker", "image", "inspect", image, "--format", "{{.Id}}"]),
        "docker_server_version": command(["docker", "version", "--format", "{{.Server.Version}}"]),
        "platform": manifest["platform"],
        "toolchain": command(["docker", "run", "--rm", "--entrypoint",
                              manifest.get("toolchain_entrypoint", "cat"), image,
                              *manifest.get("toolchain_args", ["/work/toolchain.txt"])]).splitlines(),
        "source_sha256": manifest["source_sha256"],
        "control_sha256": manifest["control_sha256"],
        "project_file_sha256": {
            str(path.relative_to(project)): sha256(path.read_bytes()).hexdigest()
            for path in sorted(project.rglob("*"))
            if path.is_file() and path.name != "verification.json"
            and path.relative_to(project) != Path("README.md")
            and "target" not in path.relative_to(project).parts
        },
        "output": summary["output"],
        "parser_source_files": summary["parser_source_files"],
        "parser_source_lines_covered": summary["parser_source_lines_covered"],
        "format_specific_source_lines_covered": format_specific_lines,
        "underlying_source_files": summary.get("underlying_source_files"),
        "underlying_source_lines_covered": summary.get("underlying_source_lines_covered"),
        "fuzz_engine_smoke_pass": True,
        "coverage_output": f"projects/{args.format}/{args.ecosystem}/{args.package_slug}/target/coverage/coverage.json",
        "pass": True,
    }
    (project / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified {args.format}/{args.ecosystem}/{manifest['package']}: {receipt['parser_source_lines_covered']} library lines covered")


if __name__ == "__main__":
    main()
