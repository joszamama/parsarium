"""Pin an AFL++ QEMU overlay for a verified prebuilt parser library."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from audit_projects import receipt_verified
from binary_feedback import check_binary_feedback
from docker_slots import docker_build_slot
from run_case import ROOT, project_for


def command(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)} failed:\n{result.stderr[-4000:]}")
    return result.stdout.strip()


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("ecosystem")
    cli.add_argument("package_slug")
    args = cli.parse_args()
    project, manifest = project_for(args.format, args.ecosystem, args.package_slug)
    manifest_path = project / "manifest.json"
    if not receipt_verified(manifest_path, manifest):
        raise RuntimeError("native binary base receipt is absent or stale")
    base_receipt_path = project / "verification.json"
    base_receipt = json.loads(base_receipt_path.read_text())
    feedback = base_receipt["binary_feedback"]
    check_binary_feedback(project, ROOT, manifest, feedback)
    source_image = f"parsarium/{args.format}-{args.ecosystem}-{args.package_slug}-binary-feedback:local"
    source_image_id = command(["docker", "image", "inspect", source_image, "--format", "{{.Id}}"])
    if source_image_id != base_receipt["binary_feedback_image_id"]:
        raise RuntimeError("binary feedback image differs from the base receipt")

    relative = project.relative_to(ROOT / "projects")
    overlay = ROOT / "fuzzing/afl-native" / relative
    overlay.mkdir(parents=True, exist_ok=True)
    dockerfile = overlay / "Dockerfile"
    dockerfile.write_bytes((project / "binary-feedback/Dockerfile").read_bytes())
    image = f"parsarium-afl/{args.format}-{args.ecosystem}-{args.package_slug}:local"
    with docker_build_slot():
        command(["docker", "build", "--quiet", "--platform", manifest["platform"],
                 "-f", str(dockerfile), "-t", image, str(project / "binary-feedback")])
    image_id = command(["docker", "image", "inspect", image, "--format", "{{.Id}}"])
    if image_id != source_image_id:
        raise RuntimeError("AFL++ overlay does not match the QEMU-tested image")
    receipt = {
        "schema_version": 1,
        "project": str(relative),
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "pass": True,
        "coverage_kind": "native_binary_edges",
        "feedback_kind": "underlying_shared_library_binary_edges",
        "afl_package": "AFL++ 5.04a QEMU",
        "afl_map_size": 65536,
        "feedback_edges": feedback["control_tuples"],
        "binary_feedback": feedback,
        "source_lines_covered": None,
        "base_project_receipt_sha256": sha256(base_receipt_path.read_bytes()).hexdigest(),
        "source_sha256": manifest["source_sha256"],
        "control_sha256": manifest["control_sha256"],
        "image_id": image_id,
        "overlay_file_sha256": {"Dockerfile": sha256(dockerfile.read_bytes()).hexdigest()},
    }
    (overlay / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified AFL++ native binary feedback for {relative}: {feedback['control_tuples']} tuples")


if __name__ == "__main__":
    main()
