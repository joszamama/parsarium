"""Verify AFL++ QEMU feedback inside a selected prebuilt shared object."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


def mapped_ranges(log: str, filename: str) -> list[tuple[int, int, str]]:
    result = []
    for line in log.splitlines():
        fields = line.split()
        if len(fields) < 6 or fields[-1] != filename:
            continue
        if not re.fullmatch(r"[0-9a-f]+-[0-9a-f]+", fields[0]):
            continue
        start, end = (int(value, 16) for value in fields[0].split("-"))
        result.append((start, end, fields[1]))
    return result


def address_range(start: int, end: int) -> str:
    return f"0x{start:x}-0x{end:x}"


def showmap(
    name: str,
    control: str,
    executable: str,
    harness: str,
    output_dir: Path,
    environment: dict[str, str],
) -> tuple[str, list[str]]:
    output_file = output_dir / f"{name}.map"
    command = [
        "/opt/afl/bin/afl-showmap", "-Q", "-e", "-t", "30000", "-o", str(output_file),
        "--", executable, harness, control,
    ]
    completed = subprocess.run(command, env=environment, text=True, capture_output=True)
    log = completed.stdout + completed.stderr
    if completed.returncode or "Program timed off" in log or "Captured" not in log:
        raise RuntimeError(f"{name} failed or timed out:\n{log[-4000:]}")
    return log, output_file.read_text().splitlines()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True, help="Exact path to the prebuilt parser shared object")
    parser.add_argument("--executable", default="/opt/venv/bin/python")
    parser.add_argument("--harness", default="/work/binary-run-once.py")
    parser.add_argument("--control", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--control-output", required=True)
    parser.add_argument("--variant-output", required=True)
    arguments = parser.parse_args()

    executable = os.path.realpath(arguments.executable)
    environment = os.environ.copy()
    environment["LD_PRELOAD"] = arguments.module
    environment["AFL_SKIP_CPUFREQ"] = "1"
    environment["AFL_DEBUG"] = "1"
    environment["AFL_QEMU_DEBUG_MAPS"] = "1"
    environment.pop("AFL_QEMU_INST_RANGES", None)
    # The probe needs mappings, not Python's large startup edge map.
    environment["AFL_QEMU_EXCLUDE_RANGES"] = "0x400000-0x100000000"

    with tempfile.TemporaryDirectory() as directory:
        output_dir = Path(directory)
        probe_log, _ = showmap(
            "probe", arguments.control, arguments.executable, arguments.harness,
            output_dir, environment,
        )
        if arguments.control_output not in probe_log:
            raise RuntimeError("The valid control did not produce its expected parse result")
        module_maps = mapped_ranges(probe_log, arguments.module)
        module_text = sorted({(start, end) for start, end, flags in module_maps if flags == "r-xp"})
        executable_maps = mapped_ranges(probe_log, executable)
        if len(module_text) != 1 or not executable_maps:
            raise RuntimeError("QEMU did not map the requested module and executable as expected")
        module_start, module_end = module_text[0]
        executable_start = min(start for start, _, _ in executable_maps)
        executable_end = max(end for _, end, _ in executable_maps)
        if executable_start < module_end and module_start < executable_end:
            raise RuntimeError("Module and executable address ranges overlap")

        environment.pop("AFL_DEBUG")
        environment.pop("AFL_QEMU_DEBUG_MAPS")
        environment["AFL_QEMU_INST_RANGES"] = address_range(module_start, module_end)
        environment["AFL_QEMU_EXCLUDE_RANGES"] = address_range(executable_start, executable_end)
        _, control_a = showmap(
            "control_a", arguments.control, arguments.executable, arguments.harness,
            output_dir, environment,
        )
        _, control_b = showmap(
            "control_b", arguments.control, arguments.executable, arguments.harness,
            output_dir, environment,
        )
        variant_log, variant = showmap(
            "variant", arguments.variant, arguments.executable, arguments.harness,
            output_dir, environment,
        )
        if arguments.variant_output not in variant_log:
            raise RuntimeError("The valid variant did not produce its expected parse result")
        environment["AFL_QEMU_EXCLUDE_RANGES"] += "," + address_range(module_start, module_end)
        _, excluded = showmap(
            "excluded", arguments.control, arguments.executable, arguments.harness,
            output_dir, environment,
        )

        if control_a != control_b:
            raise RuntimeError("The same valid control produced different maps")
        if control_a == variant:
            raise RuntimeError("The two valid format controls produced identical maps")
        if len(control_a) < 10 or len(excluded) > 2:
            raise RuntimeError("The target module did not produce isolated binary feedback")
        print(json.dumps({
            "feedback_kind": "native_binary_edges_not_source_coverage",
            "module": arguments.module,
            "module_sha256": hashlib.sha256(Path(arguments.module).read_bytes()).hexdigest(),
            "module_text_range": address_range(module_start, module_end),
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
