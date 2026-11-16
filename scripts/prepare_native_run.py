"""Prepare a coverage-guided campaign with each project's existing fuzz engine.

This writes seeds and an exact Docker command. It never starts a campaign.
For AFL++ C/C++ campaigns, use prepare_afl_run.py instead.
"""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import shlex
import uuid

from run_case import MAX_CASE_BYTES, ROOT, image_for, project_for


ENGINE = {
    "c": "libFuzzer", "cpp": "libFuzzer", "go": "Go native fuzzing",
    "java": "Jazzer", "javascript": "Jazzer.js", "python": "Atheris",
    "rust": "Rust libFuzzer", "php": "PHP-Fuzzer",
}


def command_for(manifest: dict, image_id: str, corpus: Path, artifacts: Path,
                duration: int, go_cache: Path | None) -> list[str]:
    ecosystem = manifest["ecosystem"]
    platform = manifest["platform"]
    args = ["docker", "run", "--rm", "--pull", "never", "--platform", platform,
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/" if ecosystem == "go" else "/tmp",
            "-v", f"{corpus}:/corpus", "-v", f"{artifacts}:/artifacts"]
    if ecosystem == "go":
        entry = manifest["fuzz_entry"]
        assert go_cache is not None
        args += ["-v", f"{corpus}:/testdata/fuzz/{entry}",
                 "-v", f"{go_cache}:/go-fuzz-cache",
                 "--entrypoint", "/work/harness.test", image_id,
                 f"-test.fuzz=^{entry}$", "-test.run=^$",
                 f"-test.fuzztime={duration}s", "-test.parallel=1",
                 "-test.fuzzcachedir=/go-fuzz-cache"]
    elif ecosystem in {"c", "cpp", "rust"} or (ecosystem == "python" and
            manifest.get("fuzz_engine", "").startswith("libFuzzer")):
        args += ["--entrypoint", manifest.get("fuzz_smoke_entrypoint", "/work/fuzzer"), image_id, "/corpus",
                 f"-max_total_time={duration}", f"-max_len={MAX_CASE_BYTES}",
                 "-artifact_prefix=/artifacts/"]
    elif ecosystem == "java":
        engine_args = [arg for arg in manifest["fuzz_smoke_args"] if arg != "-help=1"]
        args += ["--entrypoint", manifest["fuzz_smoke_entrypoint"], image_id,
                 *engine_args, "/corpus", f"-max_total_time={duration}",
                 f"-max_len={MAX_CASE_BYTES}", "-artifact_prefix=/artifacts/",
                 "--reproducer_path=/artifacts"]
    elif ecosystem == "javascript":
        engine_args = manifest["fuzz_smoke_args"]
        engine_args = engine_args[:engine_args.index("--")]
        args += ["--entrypoint", manifest["fuzz_smoke_entrypoint"], image_id,
                 *engine_args, "/corpus", "--", f"-max_total_time={duration}",
                 f"-max_len={MAX_CASE_BYTES}", "-artifact_prefix=/artifacts/"]
    elif ecosystem == "python":
        args += ["--entrypoint", manifest["fuzz_smoke_entrypoint"], image_id,
                 "/work/fuzz.py", "/corpus", f"-max_total_time={duration}",
                 f"-max_len={MAX_CASE_BYTES}", "-artifact_prefix=/artifacts/"]
    elif (ecosystem == "php" and manifest.get("fuzz_engine") == "AFL++"
          and (manifest.get("kind") == "standard" or manifest.get("afl_entrypoint"))):
        target_args = ([manifest["afl_entrypoint"], "@@"] if manifest.get("afl_entrypoint")
                       else ["/opt/php/bin/php", "/work/fuzz-target.php", "@@"])
        args += ["-e", "AFL_SKIP_CPUFREQ=1", "-e", "AFL_NO_AFFINITY=1",
                 "-e", "AFL_NO_UI=1", "--entrypoint", "afl-fuzz", image_id,
                 "-m", "none", "-t", "10000", "-i", "/corpus", "-o", "/artifacts",
                 "--", *target_args]
    elif ecosystem == "php":
        args += ["--entrypoint", manifest["fuzz_smoke_entrypoint"], image_id,
                 "-d", "xdebug.mode=coverage", "/work/vendor/bin/php-fuzzer",
                 "fuzz", "/work/fuzz-target.php", "/corpus"]
    else:
        raise ValueError(f"unsupported ecosystem: {ecosystem}")
    return args


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("ecosystem", choices=sorted(ENGINE))
    cli.add_argument("package_slug")
    cli.add_argument("run_dir", type=Path)
    cli.add_argument("--seed", type=Path, action="append", default=[])
    cli.add_argument("--seed-dir", type=Path, action="append", default=[])
    cli.add_argument("--duration-seconds", type=int, default=3600)
    args = cli.parse_args()
    if args.duration_seconds < 1:
        cli.error("duration-seconds must be positive")
    project, manifest = project_for(args.format, args.ecosystem, args.package_slug)
    image, image_id = image_for(project, manifest)
    project_receipt = (project / "verification.json").read_bytes()
    if image_id != json.loads(project_receipt)["image_id"]:
        cli.error("local project image differs from its verification receipt; run python3 parsarium.py build FORMAT ECOSYSTEM SLUG")
    php_native = (args.ecosystem == "php" and manifest.get("fuzz_engine") == "AFL++"
                  and (manifest.get("kind") == "standard" or manifest.get("afl_entrypoint")))
    if php_native:
        overlay = ROOT / "fuzzing/afl-native" / args.format / args.ecosystem / args.package_slug
        overlay_receipt = json.loads((overlay / "verification.json").read_text())
        if (not overlay_receipt.get("pass") or overlay_receipt.get("base_project_receipt_sha256")
                != sha256(project_receipt).hexdigest()):
            cli.error("native PHP AFL++ overlay differs from the base receipt")
        image = f"parsarium-afl/{args.format}-{args.ecosystem}-{args.package_slug}:local"
        image_id = overlay_receipt["image_id"]
    run_dir = args.run_dir.resolve()
    if run_dir.exists() and any(run_dir.iterdir()):
        cli.error("run directory already contains files")
    seeds = [ROOT / manifest["control"], *args.seed]
    for directory in args.seed_dir:
        if not directory.is_dir():
            cli.error(f"seed directory does not exist: {directory}")
        seeds.extend(sorted(path for path in directory.rglob("*") if path.is_file()))
    data_by_sha = {}
    sources = []
    for seed in seeds:
        data = seed.read_bytes()
        if not data or len(data) > MAX_CASE_BYTES:
            cli.error(f"seed is empty or exceeds {MAX_CASE_BYTES} bytes: {seed}")
        digest = sha256(data).hexdigest()
        data_by_sha[digest] = data
        sources.append({"path": str(seed.resolve()), "sha256": digest, "bytes": len(data)})
    corpus = run_dir / "corpus"
    artifacts = run_dir / "artifacts"
    corpus.mkdir(parents=True, exist_ok=True)
    artifacts.mkdir()
    go_cache = None
    if args.ecosystem == "go":
        go_cache = run_dir / "go-cache"
        go_cache.mkdir()
    for digest, data in data_by_sha.items():
        if args.ecosystem == "go":
            encoded = "".join(f"\\x{byte:02x}" for byte in data)
            (corpus / digest).write_text(f'go test fuzz v1\n[]byte("{encoded}")\n')
        else:
            (corpus / digest).write_bytes(data)
    corpus_files = [{"name": path.name, "sha256": sha256(path.read_bytes()).hexdigest(),
                     "bytes": path.stat().st_size} for path in sorted(corpus.iterdir())]
    command = command_for(manifest, image_id, corpus, artifacts,
                          args.duration_seconds, go_cache)
    container_name = f"parsarium-native-{uuid.uuid4().hex[:16]}"
    command[3:3] = ["--name", container_name]
    engine = ("AFL++ PHP parser source bridge" if php_native and
              manifest.get("afl_entrypoint") == "/work/afl_proxy" else
              "AFL++ native PHP" if php_native else ENGINE[args.ecosystem])
    plan = {"schema_version": 1, "project": str(project.relative_to(ROOT / "projects")),
            "engine": engine, "image": image, "image_id": image_id,
            "project_receipt_sha256": sha256(project_receipt).hexdigest(),
            "platform": manifest["platform"], "source_sha256": manifest["source_sha256"],
            "control_sha256": manifest["control_sha256"], "seed_sources": sources,
            "unique_seeds": len(data_by_sha), "corpus_files": corpus_files,
            "duration_seconds": args.duration_seconds, "container_name": container_name,
            "duration_enforced_by_engine": args.ecosystem != "php",
            "command": command, "corpus_directory": str(corpus),
            "artifacts_directory": str(artifacts),
            "go_cache_directory": str(go_cache) if go_cache else None}
    (run_dir / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    print(f"Prepared {len(data_by_sha)} seeds for {engine} in {run_dir}")
    print(shlex.join(command))
    if args.ecosystem == "php":
        print(f"{engine} uses the prepared duration as the run limit.")


if __name__ == "__main__":
    main()
