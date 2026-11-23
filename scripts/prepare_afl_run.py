"""Prepare an AFL++ campaign for a verified native overlay; do not start it.

The generated plan.json records the exact Docker command, seeds, image, and
source hashes. Run the printed command when ready to start a campaign.
--fandango N adds N valid inputs from the target's default Fandango route to
the control and records their provenance in the plan's seed_generation field.
"""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import uuid

from build_afl_native import OVERLAYS
import fandango_seeds
from run_case import MAX_CASE_BYTES, ROOT, project_for


def uses_afl_file_input(manifest: dict) -> bool:
    """Native C/C++ harnesses consume a file path unless explicitly overridden."""
    return manifest.get("afl_file_input", manifest["ecosystem"] in {"c", "cpp"}) is True


def commands_for(manifest: dict, receipt: dict, seed_dir: Path,
                 output_dir: Path, timeout_ms: int, container_name: str) -> tuple[list[str], list[str]]:
    binary = manifest.get("coverage_kind") == "native_binary_edges"
    tk_source_feedback = manifest.get("coverage_kind") == "native_source_afl_feedback"
    binary_env = []
    if binary:
        feedback = receipt["binary_feedback"]
        binary_env = ["-e", f"AFL_QEMU_INST_RANGES={feedback['module_text_range']}",
                      "-e", f"AFL_QEMU_EXCLUDE_RANGES={feedback['executable_excluded_range']}",
                      "-e", f"LD_PRELOAD={feedback['module']}",
                      "-e", "AFL_QEMU_MODE=trace"]
    common = ["docker", "run", "--rm", "--name", container_name,
              "--pull", "never", "--platform", manifest["platform"],
              "--network", "none", "--read-only", "--cap-drop", "ALL",
              "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
              "--tmpfs", "/tmp:rw,exec,nosuid,size=256m" if tk_source_feedback
                  else "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp",
              "-e", "AFL_SKIP_CPUFREQ=1", "-e", "AFL_NO_AFFINITY=1",
              "-e", "AFL_NO_UI=1", "-e", f"AFL_MAP_SIZE={receipt['afl_map_size']}",
              *binary_env,
              "-v", f"{seed_dir}:/seeds:ro", "-v", f"{output_dir}:/results",
              "--entrypoint", "/opt/afl/bin/afl-fuzz" if binary else
                  "/work/with-display.sh" if tk_source_feedback else "afl-fuzz",
              receipt["image_id"]]
    ecosystem = manifest["ecosystem"]
    php_native = (ecosystem == "php" and manifest.get("fuzz_engine") == "AFL++"
                  and (manifest.get("kind") == "standard" or manifest.get("afl_entrypoint")
                       or manifest.get("native_campaign_supported") is False))
    if tk_source_feedback:
        target_args = ["/work/afl-python", "/work/replay.py", "@@"]
    elif binary:
        target_args = ["/opt/venv/bin/python", "/work/binary-run-once.py", "@@"]
    elif manifest.get("afl_target"):
        # A runtime built with only its parser object instrumented runs the project adapter on one file.
        target_args = [*manifest["afl_target"], "@@"]
    elif php_native:
        target_args = ([manifest["afl_entrypoint"], "@@"] if manifest.get("afl_entrypoint")
                       else ["/opt/php/bin/php", "/work/fuzz-target.php", "@@"])
    elif ecosystem == "rust" and manifest.get("afl_native_c_binding"):
        target_args = [manifest["afl_entrypoint"], "@@"]
    elif ecosystem == "rust":
        # afl::fuzz! reads AFL shared memory, with stdin as its fallback.
        target_args = ["/work/afl_fuzzer"]
    elif ecosystem == "go" and manifest.get("afl_native_cgo"):
        target_args = [manifest["afl_entrypoint"], "@@"]
    elif ecosystem in {"go", "java", "javascript", "python", "php"}:
        target_args = ["/work/afl_proxy", "@@"]
    else:
        target_args = [manifest.get("afl_entrypoint", "/work/fuzzer")]
        if uses_afl_file_input(manifest):
            target_args.append("@@")
    mode = ["-Q"] if binary else []
    launcher = ["afl-fuzz"] if tk_source_feedback else []
    command = [*common, *launcher, *mode, "-m", "none", "-t", str(timeout_ms), "-i", "/seeds",
               "-o", "/results", "--", *target_args]
    resume = [*common, *launcher, *mode, "-m", "none", "-t", str(timeout_ms), "-i", "-",
              "-o", "/results", "--", *target_args]
    return command, resume


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("ecosystem", choices=["c", "cpp", "go", "java", "javascript", "python", "rust", "php"])
    cli.add_argument("package_slug")
    cli.add_argument("run_dir", type=Path)
    cli.add_argument("--seed", type=Path, action="append", default=[])
    cli.add_argument("--seed-dir", type=Path, action="append", default=[])
    cli.add_argument("--timeout-ms", type=int)
    fandango_seeds.add_arguments(cli)
    args = cli.parse_args()
    fandango_seeds.check_arguments(cli, args)
    project, manifest = project_for(args.format, args.ecosystem, args.package_slug)
    timeout_ms = args.timeout_ms if args.timeout_ms is not None else (
        30000 if manifest.get("coverage_kind") == "native_binary_edges"
        else 10000 if args.ecosystem in {"go", "java", "javascript", "python", "php"} else 1000)
    if timeout_ms < 1:
        cli.error("timeout-ms must be positive")
    overlay = OVERLAYS / args.format / args.ecosystem / args.package_slug
    receipt_path = overlay / "verification.json"
    if not receipt_path.is_file():
        cli.error("AFL++ overlay is not verified; run python3 parsarium.py afl build FORMAT ECOSYSTEM SLUG")
    receipt = json.loads(receipt_path.read_text())
    tk_source_feedback = manifest.get("coverage_kind") == "native_source_afl_feedback"
    base_receipt = project / ("control-verification.json" if tk_source_feedback else "verification.json")
    base_hash_field = "base_control_receipt_sha256" if tk_source_feedback else "base_project_receipt_sha256"
    if not receipt.get("pass") or receipt.get(base_hash_field) != sha256(base_receipt.read_bytes()).hexdigest():
        cli.error("AFL++ overlay receipt does not match the verified project")
    file_hashes = receipt.get("overlay_file_sha256")
    expected_dockerfile = (file_hashes or {}).get("Dockerfile", receipt.get("overlay_dockerfile_sha256"))
    if expected_dockerfile != sha256((overlay / "Dockerfile").read_bytes()).hexdigest():
        cli.error("AFL++ overlay Dockerfile changed since verification")
    if file_hashes:
        for name, expected in file_hashes.items():
            if sha256((overlay / name).read_bytes()).hexdigest() != expected:
                cli.error(f"AFL++ overlay file changed since verification: {name}")
    for name, expected in receipt.get("bridge_file_sha256", {}).items():
        if sha256((ROOT / "fuzzing/afl-bridge" / name).read_bytes()).hexdigest() != expected:
            cli.error(f"AFL++ bridge file changed since verification: {name}")
    image = f"parsarium-afl/{args.format}-{args.ecosystem}-{args.package_slug}:local"
    inspection = subprocess.run(["docker", "image", "inspect", image, "--format", "{{.Id}}"],
                                capture_output=True, text=True)
    if inspection.returncode or inspection.stdout.strip() != receipt["image_id"]:
        cli.error("local AFL++ image is missing or differs from its receipt; run python3 parsarium.py afl build FORMAT ECOSYSTEM SLUG")
    run_dir = args.run_dir.resolve()
    if run_dir.exists() and any(run_dir.iterdir()):
        cli.error("run directory already contains files")
    for directory in args.seed_dir:
        if not directory.is_dir():
            cli.error(f"seed directory does not exist: {directory}")
    seeds = [(ROOT / manifest["control"], "control"), *((path, "seed") for path in args.seed)]
    for directory in args.seed_dir:
        seeds.extend((path, "seed_dir") for path in
                     sorted(path for path in directory.rglob("*") if path.is_file()))
    seed_generation = None
    fandango_receipt = args.fandango_receipt
    if args.fandango is not None:
        try:
            fandango_receipt = fandango_seeds.generate_seeds(
                args.format, args.ecosystem, args.package_slug, run_dir, args.fandango,
                args.fandango_seed)
        except (OSError, RuntimeError, ValueError) as error:
            cli.error(str(error))
    if fandango_receipt is not None:
        try:
            _, generated, seed_generation = fandango_seeds.provenance(
                fandango_receipt, run_dir, str(project.relative_to(ROOT / "projects")))
        except (OSError, ValueError, KeyError) as error:
            cli.error(str(error))
        if args.fandango is not None:
            seed_generation["receipt_sha256"] = sha256(fandango_receipt.read_bytes()).hexdigest()
        seeds.extend((path, "fandango") for path in generated)
    seed_data = {}
    sources = []
    for seed, origin in seeds:
        data = seed.read_bytes()
        if not data or len(data) > MAX_CASE_BYTES:
            cli.error(f"seed is empty or exceeds {MAX_CASE_BYTES} bytes: {seed}")
        digest = sha256(data).hexdigest()
        seed_data[digest] = data
        sources.append({"path": str(seed.resolve()), "sha256": digest, "bytes": len(data),
                        "origin": origin})
    seed_dir = run_dir / "seeds"
    output_dir = run_dir / "afl-out"
    seed_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir()
    for digest, data in seed_data.items():
        (seed_dir / digest).write_bytes(data)
    container_name = f"parsarium-afl-{uuid.uuid4().hex[:16]}"
    command, resume = commands_for(manifest, receipt, seed_dir, output_dir,
                                   timeout_ms, container_name)
    plan = {"schema_version": 1,
            "project": str(project.relative_to(ROOT / "projects")),
            "afl_package": receipt["afl_package"],
            "afl_feedback_edges_on_control": receipt["control_edges" if tk_source_feedback
                                                     else "feedback_edges"],
            "afl_map_size": receipt["afl_map_size"],
            "overlay_receipt_sha256": sha256(receipt_path.read_bytes()).hexdigest(),
            "image_id": receipt["image_id"], "platform": manifest["platform"],
            "source_sha256": manifest["source_sha256"],
            "control_sha256": manifest["control_sha256"],
            "seed_sources": sources, "unique_seeds": len(seed_data),
            "timeout_ms": timeout_ms,
            "container_name": container_name,
            "feedback_kind": ("tk_png_decoder_source_edges" if tk_source_feedback else
                              receipt.get("feedback_kind", "source_instrumented_edges")),
            "command": command, "resume_command": resume,
            "output_directory": str(output_dir)}
    if seed_generation is not None:
        plan["seed_generation"] = seed_generation
    (run_dir / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    print(f"Prepared {len(seed_data)} seeds in {run_dir}")
    print(shlex.join(command))
    if len(seed_data) == 1:
        print("note: the only seed is the control; add --fandango N to start from N generated "
              "valid inputs as well", file=sys.stderr)


if __name__ == "__main__":
    main()
