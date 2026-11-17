"""Check AFL++ edges inside Open3D's exported PLY triangle-mesh reader."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

# nm -D -S -C on the pinned libOpen3D.so.0.20 reports this exported symbol.
SYMBOL = "open3d::io::ReadTriangleMeshFromPLY"
SYMBOL_ELF_VALUE = 0x40132D0
SYMBOL_SIZE = 0x6D7
# QEMU uses a deterministic load base for this pinned linux/amd64 image.
EXPECTED_FUNCTION_RANGE = "0x40048572d0-0x40048579a7"


def address_range(start: int, end: int) -> str:
    return f"0x{start:x}-0x{end:x}"


def mapped_ranges(log: str, filename: str) -> list[tuple[int, int, str, int]]:
    rows = []
    for line in log.splitlines():
        fields = line.split()
        if len(fields) < 6 or fields[-1] != filename:
            continue
        if not re.fullmatch(r"[0-9a-f]+-[0-9a-f]+", fields[0]):
            continue
        start, end = (int(part, 16) for part in fields[0].split("-"))
        rows.append((start, end, fields[1], int(fields[2], 16)))
    return rows


def showmap(name: str, control: str, output_dir: Path,
            executable: str, harness: str, environment: dict[str, str],
            expected_output: str) -> tuple[str, list[str]]:
    output = output_dir / f"{name}.map"
    command = ["/opt/afl/bin/afl-showmap", "-Q", "-t", "180000",
               "-o", str(output), "--", executable, harness, control]
    result = subprocess.run(command, env=environment, text=True,
                            errors="replace", capture_output=True, timeout=260)
    log = result.stdout + result.stderr
    if (result.returncode or "Program timed off" in log or "Captured" not in log
            or expected_output not in log):
        raise RuntimeError(f"{name} did not complete the valid parse:\n{log[-1500:]}")
    return log, output.read_text().splitlines()


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("--module", required=True)
    cli.add_argument("--executable", default="/opt/venv/bin/python")
    cli.add_argument("--harness", default="/work/binary-run-once.py")
    cli.add_argument("--control", required=True)
    cli.add_argument("--variant", required=True)
    cli.add_argument("--control-output", required=True)
    cli.add_argument("--variant-output", required=True)
    args = cli.parse_args()

    executable = os.path.realpath(args.executable)
    environment = os.environ.copy()
    environment.update({
        "LD_PRELOAD": args.module,
        "AFL_SKIP_CPUFREQ": "1",
        "AFL_FORKSRV_INIT_TMOUT": "180000",
        "AFL_QEMU_INST_RANGES": EXPECTED_FUNCTION_RANGE,
        "AFL_QEMU_EXCLUDE_RANGES": "0x400000-0xb22000",
    })
    environment.pop("AFL_DEBUG", None)
    environment.pop("AFL_QEMU_DEBUG_MAPS", None)

    with tempfile.TemporaryDirectory() as temporary:
        output_dir = Path(temporary)
        cases = {
            "control_a": (args.control, args.control_output, False, True),
            "control_b": (args.control, args.control_output, False, False),
            "variant": (args.variant, args.variant_output, False, False),
            "excluded": (args.control, args.control_output, True, False),
        }

        def run_case(name: str) -> tuple[str, list[str]]:
            path, expected, excluded, debug = cases[name]
            env = environment.copy()
            if excluded:
                env["AFL_QEMU_EXCLUDE_RANGES"] += "," + EXPECTED_FUNCTION_RANGE
            if debug:
                env["AFL_DEBUG"] = "1"
                env["AFL_QEMU_DEBUG_MAPS"] = "1"
            return showmap(name, path, output_dir, args.executable,
                           args.harness, env, expected)

        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = {name: pool.submit(run_case, name) for name in cases}
            results = {name: future.result() for name, future in futures.items()}

        probe_log, control_a = results["control_a"]
        _, control_b = results["control_b"]
        _, variant = results["variant"]
        _, excluded = results["excluded"]
        module_maps = mapped_ranges(probe_log, args.module)
        text_maps = {(start, end, offset) for start, end, flags, offset
                     in module_maps if flags == "r-xp"}
        executable_maps = mapped_ranges(probe_log, executable)
        if len(text_maps) != 1 or not executable_maps:
            raise RuntimeError("QEMU did not map the Open3D library and Python executable")
        module_start, module_end, file_offset = text_maps.pop()
        function_start = module_start - file_offset + SYMBOL_ELF_VALUE
        function_end = function_start + SYMBOL_SIZE
        if (not module_start <= function_start < function_end <= module_end
                or address_range(function_start, function_end) != EXPECTED_FUNCTION_RANGE):
            raise RuntimeError("Pinned PLY symbol range differs from QEMU's mapped library")
        executable_start = min(start for start, _, _, _ in executable_maps)
        executable_end = max(end for _, end, _, _ in executable_maps)
        if (address_range(executable_start, executable_end) != "0x400000-0xb22000"
                or function_start < executable_end and executable_start < function_end):
            raise RuntimeError("Python executable range differs from the pinned QEMU mapping")
        if (control_a != control_b or control_a == variant
                or len(control_a) < 10 or len(variant) < 10 or len(excluded) > 2):
            raise RuntimeError("PLY parser feedback was not stable, input-sensitive and isolated")

        with Path(args.module).open("rb") as source:
            module_hash = hashlib.file_digest(source, "sha256").hexdigest()
        print(json.dumps({
            "feedback_kind": "native_binary_edges_not_source_coverage",
            "module": args.module,
            "module_sha256": module_hash,
            "symbol": SYMBOL,
            "symbol_elf_value": f"0x{SYMBOL_ELF_VALUE:x}",
            "symbol_size_bytes": SYMBOL_SIZE,
            "module_full_text_range": address_range(module_start, module_end),
            "module_text_range": EXPECTED_FUNCTION_RANGE,
            "executable_excluded_range": address_range(executable_start, executable_end),
            "control_tuples": len(control_a),
            "control_map_sha256": hashlib.sha256((output_dir / "control_a.map").read_bytes()).hexdigest(),
            "repeat_identical": True,
            "variant_tuples": len(variant),
            "variant_differs": True,
            "excluded_module_tuples": len(excluded),
        }, indent=2))


if __name__ == "__main__":
    main()
