"""Add the SanitizerCoverage scope to the scoped DNS Rust AFL++ overlay receipts.

scripts/build_afl_rust.py builds the overlay with the rustc wrapper and writes
/work/sancov-scope.json and /work/sancov-scope.log into the image; this script
copies them into fuzzing/afl-native/dns/rust/<slug>/verification.json as
"sancov_scope" and "rustc_wrapper_log", which audit_fuzzing.py checks against
the manifest's afl_instrumented_crates. Run after build_afl_rust.py.

Usage: python3 scripts/record_dns_rust_scope.py hickory_proto
"""

import json
import subprocess
import sys

from run_case import ROOT, project_for


def read(image: str, path: str) -> str:
    return subprocess.run(["docker", "run", "--rm", "--network", "none", "--entrypoint", "cat", image, path],
                          capture_output=True, text=True, check=True).stdout


def main() -> None:
    for slug in sys.argv[1:]:
        _, manifest = project_for("dns", "rust", slug)
        receipt_path = ROOT / "fuzzing/afl-native/dns/rust" / slug / "verification.json"
        receipt = json.loads(receipt_path.read_text())
        image = f"parsarium-afl/dns-rust-{slug}:local"
        image_id = subprocess.run(["docker", "image", "inspect", image, "--format", "{{.Id}}"],
                                  capture_output=True, text=True, check=True).stdout.strip()
        if image_id != receipt["image_id"]:
            raise SystemExit(f"{slug}: overlay image differs from its receipt")
        scope = json.loads(read(image, "/work/sancov-scope.json"))
        if scope["instrumented_crates"] != sorted(manifest["afl_instrumented_crates"]):
            raise SystemExit(f"{slug}: instrumented crates differ from the manifest")
        crates = ", ".join(scope["instrumented_crates"])
        receipt.update({
            "feedback_kind": "afl_rs_rust_sancov_edges",
            "feedback_scope": f"SanitizerCoverage only in {crates}; serde_json, the harness crate, afl and the "
                              "afl_fuzzer entry point are built without coverage",
            "sancov_scope": scope,
            "rustc_wrapper_log": sorted(read(image, "/work/sancov-scope.log").split("\n")[:-1]),
        })
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
        print(slug, scope["binary_guards"], "guards")


if __name__ == "__main__":
    main()
