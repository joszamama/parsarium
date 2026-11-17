"""Build the mp3/rust/symphonia AFL++ overlay and check its feedback.

The overlay is the afl.rs build from scripts/build_afl_rust.py over the symphonia
facade harness, with SanitizerCoverage limited to the symphonia-bundle-mp3 crate
(manifest key afl_instrumented_crates). The harness still calls the facade
probe and codec registry; only their code is left uninstrumented.

Why: with every crate instrumented, separate processes on the same input gave
different maps. The varying guards all sit in the facade crate's instance of
symphonia_core InnerCodecRegistry::register_at_tier, three std HashMap inserts
whose probe loops depend on per-process random SipHash keys.

This script checks both valid controls' decoded results in the verified base
image, then runs afl-showmap in REPEATS separate containers per control and
requires byte-identical map files. No mutation campaign and no malformed input
is run.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
from build_afl_rust import build_one, command  # noqa: E402

FORMAT, ECOSYSTEM, SLUG = "mp3", "rust", "symphonia"
OVERLAY = Path(__file__).resolve().parent
REPEATS = 5
NONDETERMINISM_NOTE = (
    "Previous overlay (image sha256:3104024d6bdf..., every crate instrumented) gave different maps "
    "for separate processes on the same control: 1881-1887 tuples, hit-count buckets differing in "
    "tuple IDs 7544-7561. The AFL++ runtime numbers guards from 5 (map size 89259 = 89254 guards + 5), "
    "so these are guard slots 7539-7556. Mapping each __sanitizer_cov_trace_pc_guard call site in that "
    "binary to its slot puts every one of them in symphonia_core::codecs::registry::InnerCodecRegistry"
    "<AudioCodecId, RegisteredAudioDecoder>::register_at_tier, monomorphized in the symphonia facade "
    "crate (symphonia-core 0.6.1 src/codecs/registry.rs:164: three std HashMap::insert calls whose "
    "probe loops depend on per-process random SipHash keys). This overlay leaves the facade, "
    "symphonia-core and all other crates uninstrumented.")


def docker_base(platform: str) -> list[str]:
    return ["docker", "run", "--rm", "-i", "--platform", platform, "--network", "none",
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp"]


def showmap(image: str, platform: str, map_size: int, data: bytes) -> bytes:
    """afl-showmap tuple:bucket output for one input in a fresh container."""
    out = OVERLAY / "edges.txt"
    command([*docker_base(platform), "-e", f"AFL_MAP_SIZE={map_size}",
             "-v", f"{OVERLAY}:/coverage", "--entrypoint", "afl-showmap", image,
             "-m", "none", "-t", "10000", "-o", "/coverage/edges.txt", "--", "/work/afl_fuzzer"],
            input_data=data)
    found = out.read_bytes()
    out.unlink()
    return found


def tuples(map_text: bytes) -> set[str]:
    return {line.split(":", 1)[0] for line in map_text.decode().splitlines() if line}


def parser_lines(base_image: str, platform: str, path: Path, prefix: str) -> dict[str, int]:
    """Covered source lines per file under one crate prefix for one input, from the base image."""
    script = ("LLVM_PROFILE_FILE=/tmp/c.profraw /work/replay /input/case >/dev/null"
              " && /work/llvm-profdata merge -sparse /tmp/c.profraw -o /tmp/c.profdata"
              " && /work/llvm-cov export /work/replay -instr-profile=/tmp/c.profdata -summary-only")
    run = command([*docker_base(platform), "-v", f"{path}:/input/case:ro",
                   "--entrypoint", "/bin/sh", base_image, "-c", script])
    files = json.loads(run.stdout)["data"][0]["files"]
    return {f["filename"][len(prefix):]: f["summary"]["lines"]["covered"]
            for f in files if f["filename"].startswith(prefix)}


def repeat_record(runs: list[bytes]) -> dict:
    return {"repeat_map_sha256": [sha256(run).hexdigest() for run in runs],
            "repeat_tuple_counts": [len(tuples(run)) for run in runs],
            "all_repeats_identical": all(run == runs[0] for run in runs)}


def main() -> None:
    receipt = build_one(FORMAT, ECOSYSTEM, SLUG)
    manifest = json.loads((ROOT / "projects" / FORMAT / ECOSYSTEM / SLUG / "manifest.json").read_text())
    platform, image = manifest["platform"], f"parsarium-afl/{FORMAT}-{ECOSYSTEM}-{SLUG}:local"
    control = (ROOT / manifest["control"]).read_bytes()
    variant = (ROOT / manifest["afl_variant"]).read_bytes()
    if sha256(variant).hexdigest() != manifest["afl_variant_sha256"]:
        raise RuntimeError("second control changed")
    base_image = f"parsarium/{FORMAT}-{ECOSYSTEM}-{SLUG}:local"
    base_id = command(["docker", "image", "inspect", base_image, "--format", "{{.Id}}"]).stdout.decode().strip()
    project_receipt = json.loads((ROOT / "projects" / FORMAT / ECOSYSTEM / SLUG / "verification.json").read_text())
    if base_id != project_receipt["image_id"]:
        raise RuntimeError("base image differs from the project receipt; run parsarium.py build first")
    outputs = {}
    for name, data in (("control", control), ("variant", variant)):
        run = command([*docker_base(platform), "-e", "LLVM_PROFILE_FILE=/tmp/replay.profraw",
                       "-v", f"{ROOT / manifest[name if name == 'control' else 'afl_variant']}:/input/case:ro",
                       "--entrypoint", "/work/replay", base_image, "/input/case"])
        outputs[name] = json.loads(run.stdout)
    if outputs["control"] != manifest["expected_output"]:
        raise RuntimeError(f"control mismatch: {outputs['control']}")
    if outputs["variant"] != manifest["afl_variant_expected_output"]:
        raise RuntimeError(f"second control mismatch: {outputs['variant']}")
    scope = json.loads(command(["docker", "run", "--rm", "--platform", platform, "--entrypoint", "cat",
                                image, "/work/sancov-scope.json"]).stdout)
    scope_log = command(["docker", "run", "--rm", "--platform", platform, "--entrypoint", "cat",
                         image, "/work/sancov-scope.log"]).stdout.decode().split("\n")
    instrumented = sorted({line.split()[1] for line in scope_log if line.startswith("instrumented ")})
    if instrumented != sorted(manifest["afl_instrumented_crates"]) or scope["instrumented_crates"] != instrumented:
        raise RuntimeError(f"unexpected instrumentation scope: {instrumented} {scope}")
    map_size = receipt["afl_map_size"]
    control_runs = [showmap(image, platform, map_size, control) for _ in range(REPEATS)]
    variant_runs = [showmap(image, platform, map_size, variant) for _ in range(REPEATS)]
    if any(run != control_runs[0] for run in control_runs) or any(run != variant_runs[0] for run in variant_runs):
        raise RuntimeError("AFL++ maps differ between separate processes on the same control")
    control_tuples, variant_tuples = tuples(control_runs[0]), tuples(variant_runs[0])
    if not control_tuples or not variant_tuples:
        raise RuntimeError("a valid control produced no feedback")
    if not (control_tuples - variant_tuples) or not (variant_tuples - control_tuples):
        raise RuntimeError("AFL++ feedback does not depend on the control")
    differentials = {}
    for key, prefix in (("own", manifest["coverage_subject_prefix"]),
                        ("underlying", manifest["underlying_coverage_subject_prefix"])):
        control_lines = parser_lines(base_image, platform, ROOT / manifest["control"], prefix)
        variant_lines = parser_lines(base_image, platform, ROOT / manifest["afl_variant"], prefix)
        if not sum(control_lines.values()) or not sum(variant_lines.values()):
            raise RuntimeError(f"no {key} source lines covered by a valid control")
        differentials[key] = {
            "prefix": prefix, "control_lines": control_lines, "variant_lines": variant_lines,
            "files_with_different_line_counts": sorted(name for name in control_lines
                if control_lines[name] != variant_lines.get(name)),
        }
    if not differentials["underlying"]["files_with_different_line_counts"]:
        raise RuntimeError("underlying parser source lines do not depend on the control")
    afl_version = command(["docker", "run", "--rm", "--platform", platform, "--entrypoint", "dpkg-query",
                           image, "-W", "-f=${Version}", "afl++"]).stdout.decode().strip()
    receipt.update({
        "feedback_kind": "afl_rs_rust_sancov_edges",
        "feedback_scope": ("SanitizerCoverage only in the symphonia-bundle-mp3 0.6.1 crate's object code "
                           "(including generic code it instantiates); the symphonia facade, symphonia-core, "
                           "the other default-feature symphonia crates, serde_json, afl and the harness are "
                           "built without coverage. The target still runs the facade probe and codec "
                           "registry; the map counts only the underlying Symphonia MP3 demuxer/decoder"),
        "sancov_scope": scope,
        "rustc_wrapper_log": sorted(line for line in scope_log if line),
        "afl_version_output": afl_version,
        "base_image_id": base_id,
        "variant_sha256": manifest["afl_variant_sha256"],
        "control_output": outputs["control"], "variant_output": outputs["variant"],
        "repeats": REPEATS,
        "repeat_rule": "each repeat is a separate docker run of afl-showmap; map files (tuple:bucket) must be byte-identical",
        "feedback_edges": len(control_tuples),
        "variant_feedback_edges": len(variant_tuples),
        "control_map_sha256": sha256(control_runs[0]).hexdigest(),
        "variant_map_sha256": sha256(variant_runs[0]).hexdigest(),
        "edges_only_in_control": len(control_tuples - variant_tuples),
        "edges_only_in_variant": len(variant_tuples - control_tuples),
        "own_source_differential": differentials["own"],
        "underlying_source_differential": differentials["underlying"],
        "underlying_package": manifest["underlying_package"],
        "underlying_source_sha256": manifest["underlying_source_sha256"],
        "nondeterminism_finding": NONDETERMINISM_NOTE,
        "mutation_campaign_run": False,
        "control_stability": repeat_record(control_runs),
        "variant_stability": repeat_record(variant_runs),
    })
    receipt["overlay_file_sha256"]["build.py"] = sha256(Path(__file__).read_bytes()).hexdigest()
    (OVERLAY / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified {FORMAT}/{ECOSYSTEM}/{SLUG}: {len(control_tuples)} control and "
          f"{len(variant_tuples)} second-control AFL++ tuples, identical over {REPEATS} processes each")


if __name__ == "__main__":
    main()
