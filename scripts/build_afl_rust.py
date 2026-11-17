"""Build and verify source-instrumented AFL++ overlays for Rust projects.

The overlay reuses the verified parse function and pinned parser release, adds
an afl.rs byte-input entry point, and checks valid-control feedback with
afl-showmap. No mutation campaign is started.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib

from build_afl_native import AFL_PACKAGE, OVERLAYS
from run_case import ROOT, project_for
from docker_slots import docker_build_slot


AFL_RUST_RELEASE = "0.18.2"
RUST_BASE = "rust@sha256:f2c004e3d2d8b547e8cf7ffbc29205385f4e71d23e53e4e383065db5e9f822cd"
UBUNTU_BASE = "ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96"

# Optional manifest key "afl_instrumented_crates": a RUSTC_WRAPPER keeps cargo-afl's
# SanitizerCoverage flags only for the named crates, and a post-build scan fails the
# image if any other crate's object code carries __sancov_guards.
SCOPE_WRAPPER = """#!/bin/bash
# RUSTC_WRAPPER: keep cargo-afl SanitizerCoverage flags only for crates in AFL_SCOPE_CRATES.
rustc=$1; shift
log=${AFL_SCOPE_LOG:-/work/sancov-scope.log}
crate=; prev=
for arg in "$@"; do [ "$prev" = --crate-name ] && crate=$arg; prev=$arg; done
case " $AFL_SCOPE_CRATES " in *" $crate "*)
    echo "instrumented $crate" >> "$log"; exec "$rustc" "$@";; esac
args=(); held=
for arg in "$@"; do
    if [ -n "$held" ]; then
        case "$arg" in passes=sancov*|llvm-args=-sanitizer-coverage*) ;; *) args+=(-C "$arg");; esac
        held=; continue
    fi
    case "$arg" in
        -C) held=1;;
        -Cpasses=sancov*|-Cllvm-args=-sanitizer-coverage*) ;;
        *) args+=("$arg");;
    esac
done
[ -n "$crate" ] && [ "$crate" != ___ ] && echo "uninstrumented $crate" >> "$log"
exec "$rustc" "${args[@]}"
"""
SCOPE_CHECK = """\"\"\"Fail unless only the scoped crates' objects carry SanitizerCoverage guards.\"\"\"
import json, re, subprocess, sys
from pathlib import Path

allowed, deps, binary = set(sys.argv[1].split()), Path(sys.argv[2]), sys.argv[3]
section = re.compile(r"\\s__sancov_guards\\s+\\S+\\s+\\S+\\s+\\S+\\s+([0-9a-f]+)")


def guard_bytes(path):
    text = subprocess.run(["readelf", "-S", "-W", str(path)], capture_output=True, text=True,
                          check=True).stdout
    return sum(int(size, 16) for size in section.findall(text))


crates = {}
for rlib in sorted(deps.glob("*.rlib")):
    name = rlib.name[3:].rsplit("-", 1)[0]
    crates[name] = crates.get(name, 0) + guard_bytes(rlib)
instrumented = {name: size for name, size in crates.items() if size}
report = {"instrumented_crates": sorted(allowed), "rlib_guard_bytes": instrumented,
          "uninstrumented_rlibs": sorted(name for name in crates if not crates[name]),
          "binary_guards": guard_bytes(binary) // 4}
if set(instrumented) != allowed or not 0 < report["binary_guards"] * 4 <= sum(instrumented.values()):
    sys.exit(f"sancov scope violated: {report}")
print(json.dumps(report, indent=2))
"""
# Optional manifest key "afl_fixed_hashmap_keys": std's HashMap RandomState draws its
# SipHash keys from getrandom(2) once per thread. When a parser crate's own HashMaps make
# probe paths (and so SanitizerCoverage edges) depend on those keys, the overlay sets
# AFL_PRELOAD to this shim so every target process starts with the same keys. The parser
# source is unchanged; only the random seed is fixed.
FIXED_GETRANDOM = """/* AFL_PRELOAD shim: constant getrandom(2) bytes so std HashMap RandomState keys repeat
 * across target processes. Parser code is not modified; only its hash seed is fixed. */
#include <stddef.h>
#include <sys/types.h>

ssize_t getrandom(void *buf, size_t len, unsigned int flags) {
    unsigned char *out = buf;
    (void)flags;
    for (size_t i = 0; i < len; i++) out[i] = (unsigned char)(0x5a ^ i);
    return (ssize_t)len;
}
"""


def overlay_manifest(project: Path) -> str:
    source = (project / "Cargo.toml").read_text()
    if source.count("[dependencies]") != 1 or 'name = "afl_fuzzer"' in source:
        raise ValueError("unsupported Rust Cargo manifest")
    return (source.replace("[dependencies]", f'[dependencies]\nafl = "={AFL_RUST_RELEASE}"', 1)
            + '\n[[bin]]\nname = "afl_fuzzer"\npath = "src/bin/afl_fuzzer.rs"\n')


def overlay_target(project: Path) -> str:
    source = (project / "src/bin/fuzzer.rs").read_text()
    marker = "use libfuzzer_sys::fuzz_target;\n"
    if source.count(marker) != 1 or "fuzz_target!(" not in source:
        raise ValueError("unsupported Rust fuzz target")
    return source.replace("#![no_main]", "", 1).lstrip("\n").replace(marker, "", 1).replace(
        "fuzz_target!(", "fn main() { afl::fuzz!(", 1).rstrip() + "\n}\n"


def dockerfile(relative: Path, manifest: dict, afl_package: str) -> str:
    overlay = f"fuzzing/afl-native/{relative.as_posix()}"
    project = f"projects/{relative.as_posix()}"
    native_archive = relative.as_posix() == "zip/rust/libarchive2"
    librsvg = relative.as_posix() == "svg/rust/librsvg"
    build_dependencies = ("cmake libclang-dev pkg-config liblzma-dev libzstd-dev "
                          "liblz4-dev libxml2-dev libssl-dev libacl1-dev libbz2-dev zlib1g-dev "
                          if native_archive else
                          "pkg-config libglib2.0-dev libgdk-pixbuf-2.0-dev libcairo2-dev libpango1.0-dev "
                          if librsvg else "")
    runtime_dependencies = ("liblzma5 libzstd1 liblz4-1 libxml2 libssl3 "
                            "libacl1 libbz2-1.0 zlib1g " if native_archive else
                            "librsvg2-2 " if librsvg else "")
    runtime_base = (manifest["runtime_base_image"] if librsvg else
                    RUST_BASE if native_archive else UBUNTU_BASE)
    build_base = manifest["base_image"] if librsvg else RUST_BASE
    scope = " ".join(manifest.get("afl_instrumented_crates", []))
    scope_copy = (f"COPY {overlay}/rustc-scope.sh {overlay}/sancov_scope.py /work/\n"
                  if scope else "")
    scope_env = (f"AFL_SCOPE_CRATES='{scope}' RUSTC_WRAPPER=/work/rustc-scope.sh "
                 if scope else "")
    scope_check = (f" \\\n    && python3 /work/sancov_scope.py '{scope}' target/aarch64-unknown-linux-gnu/release/deps "
                   "/work/afl_fuzzer > /work/sancov-scope.json" if scope else "")
    scope_result = ("COPY --from=build /work/sancov-scope.json /work/sancov-scope.log /work/\n"
                    if scope else "")
    fixed_keys = bool(manifest.get("afl_fixed_hashmap_keys"))
    if fixed_keys:
        scope_copy += f"COPY {overlay}/fixed_getrandom.c /work/\n"
        scope_check += (" \\\n    && cc -O2 -shared -fPIC -o /work/fixed_getrandom.so "
                        "/work/fixed_getrandom.c")
        scope_result += ("COPY --from=build /work/fixed_getrandom.so /work/fixed_getrandom.so\n"
                         "ENV AFL_PRELOAD=/work/fixed_getrandom.so\n")
    return f'''# AFL++ Rust overlay generated by scripts/build_afl_rust.py
FROM {build_base} AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends clang llvm-dev g++ make python3 {build_dependencies}\\
    && rm -rf /var/lib/apt/lists/*
RUN cargo install cargo-afl --version {AFL_RUST_RELEASE} --locked
WORKDIR /work
COPY {overlay}/Cargo.toml {overlay}/Cargo.lock /work/
COPY {project}/src /work/src
COPY {overlay}/afl_fuzzer.rs /work/src/bin/afl_fuzzer.rs
{scope_copy}RUN cargo fetch --locked --target aarch64-unknown-linux-gnu
RUN cargo afl config --build --force \\
    && {scope_env}cargo afl build --locked --target aarch64-unknown-linux-gnu --release --bin afl_fuzzer \\
    && cp target/aarch64-unknown-linux-gnu/release/afl_fuzzer /work/afl_fuzzer{scope_check}
FROM {runtime_base}
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++={afl_package} libstdc++6 {runtime_dependencies}\\
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /work/afl_fuzzer /work/afl_fuzzer
{scope_result}ENTRYPOINT ["/work/afl_fuzzer"]
'''


def command(args: list[str], *, input_data: bytes | None = None, allow_failure: bool = False) -> subprocess.CompletedProcess:
    result = subprocess.run(args, cwd=ROOT, input=input_data, capture_output=True,
                            timeout=1800)
    if result.returncode and not allow_failure:
        raise RuntimeError(f"{' '.join(args[:6])} failed: {(result.stdout + result.stderr).decode(errors='replace')[-3000:]}")
    return result


def build_one(format_name: str, ecosystem: str, slug: str) -> dict:
    if ecosystem != "rust":
        raise ValueError("Rust AFL++ overlay requires the rust ecosystem")
    project, manifest = project_for(format_name, ecosystem, slug)
    relative = project.relative_to(ROOT / "projects")
    overlay = OVERLAYS / relative
    overlay.mkdir(parents=True, exist_ok=True)
    manifest_text = overlay_manifest(project)
    target_text = overlay_target(project)
    (overlay / "Cargo.toml").write_text(manifest_text)
    (overlay / "afl_fuzzer.rs").write_text(target_text)
    overlay_files = ["Cargo.toml", "Cargo.lock", "afl_fuzzer.rs", "Dockerfile"]
    if manifest.get("afl_instrumented_crates"):
        (overlay / "rustc-scope.sh").write_text(SCOPE_WRAPPER)
        (overlay / "rustc-scope.sh").chmod(0o755)
        (overlay / "sancov_scope.py").write_text(SCOPE_CHECK)
        overlay_files += ["rustc-scope.sh", "sancov_scope.py"]
    if manifest.get("afl_fixed_hashmap_keys"):
        (overlay / "fixed_getrandom.c").write_text(FIXED_GETRANDOM)
        overlay_files.append("fixed_getrandom.c")
    if not (overlay / "Cargo.lock").exists():
        with tempfile.TemporaryDirectory(prefix="parsarium-rust-lock-") as temp:
            scratch = Path(temp)
            (scratch / "Cargo.toml").write_text(manifest_text)
            shutil.copytree(project / "src", scratch / "src")
            (scratch / "src/bin/afl_fuzzer.rs").write_text(target_text)
            command(["cargo", "generate-lockfile", "--manifest-path", str(scratch / "Cargo.toml")])
            (overlay / "Cargo.lock").write_bytes((scratch / "Cargo.lock").read_bytes())
    lock = tomllib.loads((overlay / "Cargo.lock").read_text())
    parser = [item for item in lock["package"] if item["name"] == manifest["package"]
              and item["version"] == manifest["release"]]
    if len(parser) != 1 or parser[0].get("checksum") != manifest["source_sha256"]:
        raise ValueError("AFL++ lockfile changed the pinned parser source")
    afl = [item for item in lock["package"] if item["name"] == "afl"
           and item["version"] == AFL_RUST_RELEASE]
    if len(afl) != 1 or not afl[0].get("checksum"):
        raise ValueError("AFL++ Rust dependency is not locked")
    afl_package = manifest.get("afl_package_release") or (
        "4.21c-5" if relative.as_posix() == "svg/rust/librsvg" else
        "4.04c-4" if relative.as_posix() == "zip/rust/libarchive2" else AFL_PACKAGE)
    (overlay / "Dockerfile").write_text(dockerfile(relative, manifest, afl_package))
    image = f"parsarium-afl/{format_name}-rust-{slug}:local"
    print(f"Building {image}", flush=True)
    with docker_build_slot():
        command(["docker", "build", "--quiet", "--platform", manifest["platform"],
                 "-f", str(overlay / "Dockerfile"), "-t", image, str(ROOT)])
    image_id = command(["docker", "image", "inspect", image, "--format", "{{.Id}}"])
    image_id_text = image_id.stdout.decode().strip()
    map_probe = command(["docker", "run", "--rm", "--platform", manifest["platform"],
                         "-e", "AFL_DUMP_MAP_SIZE=1", "--entrypoint", "/work/afl_fuzzer", image],
                        allow_failure=True)
    if not map_probe.stdout.strip().isdigit():
        raise RuntimeError("AFL++ Rust map size probe failed")
    map_size = int(map_probe.stdout.strip())
    control = (ROOT / manifest["control"]).read_bytes()
    edges = overlay / "edges.txt"
    command([
        "docker", "run", "--rm", "-i", "--platform", manifest["platform"],
        "--network", "none", "--read-only", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
        "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp",
        "-e", f"AFL_MAP_SIZE={map_size}", "-v", f"{overlay}:/coverage",
        "--entrypoint", "afl-showmap", image, "-m", "none", "-t", "10000",
        "-o", "/coverage/edges.txt", "--", "/work/afl_fuzzer",
    ], input_data=control)
    edge_count = len([line for line in edges.read_text().splitlines() if line])
    edges.unlink()
    if edge_count == 0:
        raise RuntimeError("AFL++ Rust target produced no feedback on valid control")
    receipt = {
        "schema_version": 1, "project": str(relative), "pass": True,
        "base_project_receipt_sha256": sha256((project / "verification.json").read_bytes()).hexdigest(),
        "overlay_file_sha256": {name: sha256((overlay / name).read_bytes()).hexdigest()
                                for name in overlay_files},
        "afl_package": afl_package, "afl_rust_release": AFL_RUST_RELEASE,
        "afl_rust_checksum": afl[0]["checksum"], "parser_source_sha256": manifest["source_sha256"],
        "image_id": image_id_text, "platform": manifest["platform"],
        "control_sha256": manifest["control_sha256"],
        "feedback_edges": edge_count, "afl_map_size": map_size,
    }
    (overlay / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified {relative}: {edge_count} AFL++ feedback tuples", flush=True)
    return receipt


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format", nargs="?")
    cli.add_argument("ecosystem", nargs="?")
    cli.add_argument("package_slug", nargs="?")
    cli.add_argument("--all", action="store_true")
    cli.add_argument("--workers", type=int, default=2)
    args = cli.parse_args()
    if not args.all:
        if not all((args.format, args.ecosystem, args.package_slug)):
            cli.error("provide format, ecosystem, and slug or use --all")
        build_one(args.format, args.ecosystem, args.package_slug)
        return
    if args.workers < 1:
        cli.error("workers must be positive")
    paths = sorted((ROOT / "projects").glob("*/rust/*/manifest.json"))
    records = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        tasks = {pool.submit(build_one, *path.parent.relative_to(ROOT / "projects").parts): path
                 for path in paths}
        for future in as_completed(tasks):
            relative = str(tasks[future].parent.relative_to(ROOT / "projects"))
            try:
                receipt = future.result()
                records.append({"project": relative, "status": "verified",
                                "feedback_edges": receipt["feedback_edges"],
                                "image_id": receipt["image_id"]})
            except Exception as exc:
                records.append({"project": relative, "status": "failed", "error": str(exc)[-3000:]})
                print(f"FAILED {relative}: {exc}", flush=True)
    records.sort(key=lambda item: item["project"])
    report = {"schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "afl_rust_release": AFL_RUST_RELEASE, "projects_total": len(records),
              "projects_verified": sum(item["status"] == "verified" for item in records),
              "results": records}
    (ROOT / "data/afl-rust-smoke.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['projects_verified']}/{report['projects_total']} Rust AFL++ overlays verified")
    if report["projects_verified"] != report["projects_total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
