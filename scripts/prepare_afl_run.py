"""Prepare an AFL++ campaign for a verified native overlay; do not start it.

The generated plan.json records the exact Docker command, seeds, image, and
source hashes. Run the printed command when ready to start a campaign.
"""

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import shlex
import subprocess

from build_afl_native import OVERLAYS
from run_case import MAX_CASE_BYTES, ROOT, project_for


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("ecosystem", choices=["c", "cpp", "rust"])
    cli.add_argument("package_slug")
    cli.add_argument("run_dir", type=Path)
    cli.add_argument("--seed", type=Path, action="append", default=[])
    cli.add_argument("--seed-dir", type=Path, action="append", default=[])
    cli.add_argument("--timeout-ms", type=int, default=1000)
    args = cli.parse_args()
    if args.timeout_ms < 1:
        cli.error("timeout-ms must be positive")
    project, manifest = project_for(args.format, args.ecosystem, args.package_slug)
    overlay = OVERLAYS / args.format / args.ecosystem / args.package_slug
    receipt_path = overlay / "verification.json"
    if not receipt_path.is_file():
        cli.error("AFL++ overlay is not verified; run scripts/build_afl_native.py first")
    receipt = json.loads(receipt_path.read_text())
    if not receipt.get("pass") or receipt["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        cli.error("AFL++ overlay receipt does not match the verified project")
    file_hashes = receipt.get("overlay_file_sha256")
    expected_dockerfile = (file_hashes or {}).get("Dockerfile", receipt.get("overlay_dockerfile_sha256"))
    if expected_dockerfile != sha256((overlay / "Dockerfile").read_bytes()).hexdigest():
        cli.error("AFL++ overlay Dockerfile changed since verification")
    if file_hashes:
        for name, expected in file_hashes.items():
            if sha256((overlay / name).read_bytes()).hexdigest() != expected:
                cli.error(f"AFL++ overlay file changed since verification: {name}")
    image = f"parsarium-afl/{args.format}-{args.ecosystem}-{args.package_slug}:local"
    inspection = subprocess.run(["docker", "image", "inspect", image, "--format", "{{.Id}}"],
                                capture_output=True, text=True)
    if inspection.returncode or inspection.stdout.strip() != receipt["image_id"]:
        cli.error("local AFL++ image does not match the verification receipt")
    run_dir = args.run_dir.resolve()
    if run_dir.exists() and any(run_dir.iterdir()):
        cli.error("run directory already contains files")
    seeds = [ROOT / manifest["control"], *args.seed]
    for directory in args.seed_dir:
        if not directory.is_dir():
            cli.error(f"seed directory does not exist: {directory}")
        seeds.extend(sorted(path for path in directory.rglob("*") if path.is_file()))
    if not seeds:
        cli.error("at least one seed is required")
    seed_data = {}
    sources = []
    for seed in seeds:
        data = seed.read_bytes()
        if not data or len(data) > MAX_CASE_BYTES:
            cli.error(f"seed is empty or exceeds {MAX_CASE_BYTES} bytes: {seed}")
        digest = sha256(data).hexdigest()
        seed_data[digest] = data
        sources.append({"path": str(seed.resolve()), "sha256": digest, "bytes": len(data)})
    seed_dir = run_dir / "seeds"
    output_dir = run_dir / "afl-out"
    seed_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir()
    for digest, data in seed_data.items():
        (seed_dir / digest).write_bytes(data)
    common = ["docker", "run", "--rm", "--pull", "never", "--platform", manifest["platform"],
              "--network", "none", "--read-only", "--cap-drop", "ALL",
              "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
              "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp",
              "-e", "AFL_SKIP_CPUFREQ=1", "-e", "AFL_NO_AFFINITY=1",
              "-e", "AFL_NO_UI=1",
              "-e", f"AFL_MAP_SIZE={receipt['afl_map_size']}",
              "-v", f"{seed_dir}:/seeds:ro", "-v", f"{output_dir}:/results",
              "--entrypoint", "afl-fuzz", receipt["image_id"]]
    target = "/work/afl_fuzzer" if args.ecosystem == "rust" else "/work/fuzzer"
    command = [*common, "-m", "none", "-t", str(args.timeout_ms), "-i", "/seeds",
               "-o", "/results", "--", target]
    resume = [*common, "-m", "none", "-t", str(args.timeout_ms), "-i", "-",
              "-o", "/results", "--", target]
    plan = {"schema_version": 1,
            "project": str(project.relative_to(ROOT / "projects")),
            "afl_package": receipt["afl_package"],
            "afl_feedback_edges_on_control": receipt["feedback_edges"],
            "afl_map_size": receipt["afl_map_size"],
            "overlay_receipt_sha256": sha256(receipt_path.read_bytes()).hexdigest(),
            "image_id": receipt["image_id"], "platform": manifest["platform"],
            "source_sha256": manifest["source_sha256"],
            "control_sha256": manifest["control_sha256"],
            "seed_sources": sources, "unique_seeds": len(seed_data),
            "timeout_ms": args.timeout_ms,
            "command": command, "resume_command": resume,
            "output_directory": str(output_dir)}
    (run_dir / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    print(f"Prepared {len(seed_data)} seeds in {run_dir}")
    print(shlex.join(command))


if __name__ == "__main__":
    main()
