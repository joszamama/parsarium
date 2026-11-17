"""Run Python's standard-library tomllib on both TOML controls and save a host receipt.

tomllib.load reads a local binary file and returns plain Python values; the
typed tree is built with the same rules as controls/toml/check_controls.py.
This is a standard/runtime API record, not a third-party path. Run with the
interpreter whose version should be recorded:

    python3.13 data/python/toml/probe-stdlib-tomllib.py
"""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import platform
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("toml_controls", ROOT / "controls/toml/check_controls.py")
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)

results = {}
for name in ("service-config.toml", "typed-scalars.toml"):
    path = ROOT / "controls/toml" / name
    with path.open("rb") as handle:
        tree = controls.typed(tomllib.load(handle))
    expected = json.loads(path.with_name(name.replace(".toml", ".expected.json")).read_text(encoding="utf-8"))
    results[name] = {"control": f"controls/toml/{name}", "control_sha256": sha256(path.read_bytes()).hexdigest(),
                     "output": tree, "pass": tree == expected}
first = results["service-config.toml"]
receipt = {"kind": "standard_host_control", "api": "tomllib.load(local binary file)",
           "runtime": f"CPython {platform.python_version()} standard library tomllib",
           "python": sys.version, "platform": platform.platform(),
           "tomllib_source_sha256": sha256(Path(tomllib.__file__).read_bytes()).hexdigest(),
           "tomllib_parser_source_sha256": sha256((Path(tomllib.__file__).parent / "_parser.py").read_bytes()).hexdigest(),
           "control": first["control"], "control_sha256": first["control_sha256"],
           "output": first["output"], "second_control": results["typed-scalars.toml"],
           "pass": all(item["pass"] for item in results.values()),
           "scope_note": "Host run, no container, no coverage or AFL++ feedback. tomllib is a vendored copy of tomli "
                         "and is also the oracle in controls/toml/check_controls.py; the hand-written expected "
                         "trees are the independent check."}
out = Path(__file__).with_name("stdlib-tomllib-control.json")
out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
print(out, receipt["pass"])
