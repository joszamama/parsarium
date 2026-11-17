"""Check a DNS pilot project's AFL++ overlay on both valid controls.

For one dns/<ecosystem>/<slug> project:

1. The base image replays controls/dns/response.bin and controls/dns/query.bin with the
   manifest's ``summary_command`` and must print exactly the pinned summaries
   (controls/dns/expected.json, checked by the hand-written oracle check_controls.py).
2. Each control is traced REPEATS times. Parser features are source locations inside the
   library: Python/JavaScript/Java/PHP/Go line or block features from the parser-line AFL++
   bridge (``/work/afl_trace``), or for C/C++ LLVM region entries of the base image's
   ``/work/replay`` under ``coverage_subject_prefix``. AFL++ tuples come from afl-showmap on
   the overlay target (``/work/afl_proxy`` for bridges, ``/work/fuzzer`` for C/C++,
   the cargo-afl binary for Rust).
3. Repeats must be identical, and the two controls must differ in parser features and in
   AFL++ tuples.

The report is written to data/<ecosystem>/dns/<slug>-feedback-differential.json. No
campaign is run and no malformed input is used.

Usage: python3 scripts/verify_dns_feedback.py dns/<ecosystem>/<slug> [...]
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for

REPEATS = 3
BRIDGE = {"python", "javascript", "java", "php", "go"}


def run(command: list[str], timeout: int = 300) -> str:
    result = subprocess.run(command, capture_output=True, text=True, errors="replace", timeout=timeout)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def image_id(image: str) -> str:
    return run(["docker", "image", "inspect", image, "--format", "{{.Id}}"]).strip()


def sandbox(manifest: dict, case: Path, work: Path) -> list[str]:
    return ["docker", "run", "--rm", "--platform", manifest["platform"], "--network", "none",
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}", "--tmpfs", "/tmp:rw,exec,nosuid,size=64m,mode=1777",
            "--workdir", "/tmp", "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]


def summary(manifest: dict, image: str, case: Path, work: Path) -> dict:
    entrypoint, *args = manifest["summary_command"]
    output = run([*sandbox(manifest, case, work), "-e", "LLVM_PROFILE_FILE=/tmp/replay.profraw",
                  "--entrypoint", entrypoint, image, *args])
    lines = output.strip().splitlines()
    # Go test binaries print the summary on an OBSERVED_JSON: line among test output.
    marked = [line.split("OBSERVED_JSON:", 1)[1] for line in lines if "OBSERVED_JSON:" in line]
    return json.loads(marked[-1] if marked else lines[-1])


def bridge_features(manifest: dict, overlay_image: str, case: Path, work: Path, name: str,
                    prefix: str) -> set[str]:
    run([*sandbox(manifest, case, work), "--entrypoint", "/bin/sh", overlay_image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    found = set((work / f"{name}.features").read_text().splitlines()) - {""}
    outside = [item for item in found if not item.startswith(prefix)]
    if not found or outside:
        raise RuntimeError(f"bridge features empty or outside {prefix}: {sorted(outside)[:5]}")
    return found


def native_features(manifest: dict, image: str, case: Path, work: Path, name: str) -> set[str]:
    script = (f"LLVM_PROFILE_FILE=/coverage/{name}.profraw /work/replay /input/case > /dev/null && "
              f"llvm-profdata merge -sparse /coverage/{name}.profraw -o /coverage/{name}.profdata && "
              f"llvm-cov export /work/replay -instr-profile=/coverage/{name}.profdata "
              f"> /coverage/{name}.coverage.json")
    run([*sandbox(manifest, case, work), "--entrypoint", "/bin/sh", image, "-c", script])
    coverage = json.loads((work / f"{name}.coverage.json").read_text())
    prefix = manifest["coverage_subject_prefix"]
    return {f"{item['filename']}:{line}:{column}"
            for item in coverage["data"][0]["files"] if item["filename"].startswith(prefix)
            for line, column, count, has_count, entry, gap in item["segments"]
            if has_count and entry and not gap and count > 0}


def tuples(manifest: dict, overlay_image: str, target: list[str], case: Path, work: Path,
           name: str, map_size: int) -> set[str]:
    run([*sandbox(manifest, case, work), "-e", f"AFL_MAP_SIZE={map_size}", "--entrypoint", "afl-showmap",
         overlay_image, "-m", "none", "-t", "120000", "-o", f"/coverage/{name}.map", "--", *target])
    return {line.split(":", 1)[0] for line in (work / f"{name}.map").read_text().splitlines() if line}


def by_file(features: set[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in features:
        source = item.rsplit(":", 2)[0] if item.count(":") >= 2 else item.rsplit(":", 1)[0]
        counts[source] = counts.get(source, 0) + 1
    return dict(sorted(counts.items()))


def check(relative: str) -> dict:
    fmt, eco, slug = relative.split("/")
    project, manifest = project_for(fmt, eco, slug)
    overlay_dir = ROOT / "fuzzing/afl-native" / fmt / eco / slug
    overlay = json.loads((overlay_dir / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if overlay["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise RuntimeError("overlay was built against a different project receipt")
    base_image = f"parsarium/{fmt}-{eco}-{slug}:local"
    overlay_image = f"parsarium-afl/{fmt}-{eco}-{slug}:local"
    if image_id(base_image) != base["image_id"] or image_id(overlay_image) != overlay["image_id"]:
        raise RuntimeError("local images differ from their receipts")
    expected = json.loads((ROOT / "controls/dns/expected.json").read_text())
    controls = [ROOT / manifest["control"], ROOT / manifest["differential_control"]]
    pinned = [manifest["expected_output"], manifest["differential_expected_output"]]
    for path, digest, output in zip(controls, (manifest["control_sha256"], manifest["differential_control_sha256"]), pinned):
        if sha256(path.read_bytes()).hexdigest() != digest or expected[path.name]["sha256"] != digest:
            raise RuntimeError(f"control hash mismatch: {path}")
        if expected[path.name]["summary"] != output:
            raise RuntimeError(f"manifest output differs from the oracle summary: {path.name}")
    docker_text = (overlay_dir / "Dockerfile").read_text()
    prefix_match = re.search(r"^ENV PARSARIUM_SUBJECT_PREFIX=(\S+)$", docker_text, re.MULTILINE)
    map_size = int(overlay.get("afl_map_size") or 65536)
    if eco in BRIDGE:
        target = ["/work/afl_proxy", "/input/case"]
        kind = "parser-line AFL++ bridge features"
    elif eco == "rust":
        target = [manifest.get("afl_target", "/work/afl_fuzzer"), "/input/case"]
        kind = "LLVM source regions of the base replay under coverage_subject_prefix"
    else:
        target = ["/work/fuzzer", "/input/case"]
        kind = "LLVM source regions of the base replay under coverage_subject_prefix"
    with tempfile.TemporaryDirectory(prefix="parsarium-dns-feedback-") as temporary:
        work = Path(temporary)
        os.chmod(work, 0o777)
        outputs = [summary(manifest, base["image_id"], path, work) for path in controls]
        if outputs != pinned:
            raise RuntimeError(f"control summaries differ from the oracle: {outputs}")
        runs = []
        for index, control in enumerate(controls):
            attempts = []
            for attempt in range(REPEATS):
                name = f"{index}-{attempt}"
                if eco in BRIDGE:
                    found = bridge_features(manifest, overlay["image_id"], control, work, name, prefix_match.group(1))
                else:
                    found = native_features(manifest, base["image_id"], control, work, name)
                attempts.append((found, tuples(manifest, overlay["image_id"], target, control, work, name, map_size)))
            runs.append(attempts)
    for attempts in runs:
        if any(item != attempts[0] for item in attempts):
            raise RuntimeError("repeated feedback differs for one control")
    (first_features, first_tuples), (second_features, second_tuples) = runs[0][0], runs[1][0]
    feature_difference = len(first_features ^ second_features)
    tuple_difference = len(first_tuples ^ second_tuples)
    if not first_features or not first_tuples or feature_difference == 0 or tuple_difference == 0:
        raise RuntimeError("feedback does not distinguish the two valid controls")
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(), "project": relative, "pass": True,
        "input_kind": "two fixed valid DNS messages (RFC 1035 section 4)",
        "oracle": "controls/dns/check_controls.py hand-written decoder; summaries pinned in controls/dns/expected.json",
        "feature_kind": kind, "subject_prefix": prefix_match.group(1) if prefix_match else manifest["coverage_subject_prefix"],
        "base_image_id": base["image_id"], "overlay_image_id": overlay["image_id"],
        "overlay_receipt_sha256": sha256((overlay_dir / "verification.json").read_bytes()).hexdigest(),
        "control_sha256": manifest["control_sha256"], "variant_sha256": manifest["differential_control_sha256"],
        "control_output_matches": True, "variant_output_matches": True,
        "runs_per_control": REPEATS, "control_repeat_identical": True, "variant_repeat_identical": True,
        "afl_target": target[0], "afl_map_size": map_size,
        "control_parser_features": len(first_features), "variant_parser_features": len(second_features),
        "parser_feature_difference": feature_difference,
        "control_afl_tuples": len(first_tuples), "variant_afl_tuples": len(second_tuples),
        "afl_tuple_difference": tuple_difference,
        "control_features_by_file": by_file(first_features),
        "variant_features_by_file": by_file(second_features),
        "mutation_campaign_run": False,
    }
    out = ROOT / "data" / eco / fmt / f"{slug.replace('_', '-')}-feedback-differential.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    return report


def main() -> None:
    for relative in sys.argv[1:]:
        report = check(relative)
        print(relative, report["control_parser_features"], report["variant_parser_features"],
              report["parser_feature_difference"], report["control_afl_tuples"],
              report["variant_afl_tuples"], report["afl_tuple_difference"])


if __name__ == "__main__":
    main()
