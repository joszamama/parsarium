"""Fail unless only the scoped crates' objects carry SanitizerCoverage guards."""
import json, re, subprocess, sys
from pathlib import Path

allowed, deps, binary = set(sys.argv[1].split()), Path(sys.argv[2]), sys.argv[3]
section = re.compile(r"\s__sancov_guards\s+\S+\s+\S+\s+\S+\s+([0-9a-f]+)")


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
