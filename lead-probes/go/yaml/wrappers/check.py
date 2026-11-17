#!/usr/bin/env python3
"""Reproduce the Go YAML round-2 lead decisions on the two valid controls.

1. Runs each wrapper/independent lead's documented API (main.go) on both valid
   controls and compares the result with the hand-written oracle of
   controls/yaml/check_controls.py.
2. For leads whose result matches, builds the probe with `go build -cover`
   (the probe's main package is in -coverpkg, otherwise no coverage is
   written) and compares the covered blocks of the lead's own packages and of
   the underlying go.yaml.in/yaml/v3 between the controls, three runs each.
3. Downloads the fork/predecessor/rename leads and counts distinct non-test
   source lines shared with the selected go-yaml module they derive from.

Writes data/go/yaml/lead-check.json. No malformed input, no fuzz campaign.
"""

from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

PROBE = Path(__file__).resolve().parent
ROOT = PROBE.parents[3]
G = "git" + "hub.com"
CONTROLS = ("catalog.yaml", "order.yaml")
LEADS = {
    "ghodss": {"package": f"{G}/ghodss/yaml", "version": "v1.0.0", "api": "yaml.YAMLToJSON([]byte)"},
    "sigs": {"package": "sigs.k8s.io/yaml", "version": "v1.6.0", "api": "yaml.YAMLToJSON([]byte)"},
    "apimachinery": {"package": "k8s.io/apimachinery/pkg/util/yaml", "version": "v0.37.2", "api": "yaml.ToJSON([]byte)"},
    "koanf": {"package": f"{G}/knadh/koanf/parsers/yaml", "version": "v1.1.1", "api": "yaml.Parser().Unmarshal([]byte)"},
    "gypsy": {"package": f"{G}/kylelemons/go-gypsy/yaml", "version": "v1.0.0", "api": "yaml.Parse(io.Reader)"},
    "kyaml": {"package": "sigs.k8s.io/kustomize/kyaml/yaml", "version": "v0.21.3", "api": "yaml.Parse(string) *RNode",
              "own": ["sigs.k8s.io/kustomize/kyaml/yaml/"]},
    "cue": {"package": "cuelang.org/go/encoding/yaml", "version": "v0.17.1", "api": "yaml.Extract(filename, []byte) *ast.File",
            "own": ["cuelang.org/go/encoding/yaml/", "cuelang.org/go/internal/encoding/yaml/"]},
}
UNDERLYING = "go.yaml.in/yaml/v3/"
COVERPKG = ["sigs.k8s.io/kustomize/kyaml/yaml", "cuelang.org/go/encoding/yaml",
            "cuelang.org/go/internal/encoding/yaml", "go.yaml.in/yaml/v3", "parsarium.local/yaml-go-wrapper-lead-probe"]
FORKS = [
    (f"{G}/go-yaml/yaml", "v2.1.0+incompatible", "gopkg.in/yaml.v2", "v2.4.0"),
    (f"{G}/go-yaml/yaml", "v0.0.0-20250401170010-944c86a7d293", "gopkg.in/yaml.v3", "v3.0.1"),
    ("launchpad.net/goyaml", "v0.0.0-20140305200416-000000000051", "gopkg.in/yaml.v2", "v2.4.0"),
    ("go.yaml.in/yaml/v3", "v3.0.6", "gopkg.in/yaml.v3", "v3.0.1"),
    ("go.yaml.in/yaml/v2", "v2.4.2", "gopkg.in/yaml.v2", "v2.4.0"),
    (f"{G}/coreos/yaml", "v0.0.0-20141224210557-6b16a5714269", "gopkg.in/yaml.v2", "v2.4.0"),
    (f"{G}/buildkite/yaml", "v2.1.0+incompatible", "gopkg.in/yaml.v2", "v2.4.0"),
    (f"{G}/pivotal-golang/yaml", "v0.0.0-20160414152406-8b09e4a33107", "gopkg.in/yaml.v2", "v2.4.0"),
    ("gopkg.in/coryb/yaml.v2", "v2.0.0", "gopkg.in/yaml.v2", "v2.4.0"),
    (f"{G}/zclconf/go-cty-yaml", "v1.2.0", "gopkg.in/yaml.v2", "v2.4.0"),
    (f"{G}/go-faster/yaml", "v0.4.6", "gopkg.in/yaml.v3", "v3.0.1"),
    (f"{G}/braydonk/yaml", "v0.9.0", "gopkg.in/yaml.v3", "v3.0.1"),
    ("go.yaml.in/yaml/v4", "v4.0.0", "gopkg.in/yaml.v3", "v3.0.1"),
    (f"{G}/goccy/go-yaml", "v1.19.2", "gopkg.in/yaml.v3", "v3.0.1"),
]
SKIP_PARTS = ("example", "cmd/", "util/", "testutil", "yts/", "testdata")


def command(*args: str, env: dict | None = None) -> str:
    result = subprocess.run(args, cwd=PROBE, check=True, text=True, capture_output=True,
                            timeout=600, env=env)
    return result.stdout


def oracle() -> dict:
    spec = importlib.util.spec_from_file_location("yaml_controls", ROOT / "controls/yaml/check_controls.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.EXPECTED


def first_difference(observed, expected, path="$"):
    if observed == expected:
        return None
    if (isinstance(observed, list) and isinstance(expected, list) and observed and expected
            and observed[0] == expected[0] == "map"):
        got, want = [key for key, _ in observed[1]], [key for key, _ in expected[1]]
        if got != want:
            return {"path": path, "observed_keys": got, "expected_keys": want}
        for (key, a), (_, b) in zip(observed[1], expected[1]):
            found = first_difference(a, b, f"{path}.{key}")
            if found:
                return found
    if (isinstance(observed, list) and isinstance(expected, list) and observed and expected
            and observed[0] == expected[0] == "seq" and len(observed[1]) == len(expected[1])):
        for index, (a, b) in enumerate(zip(observed[1], expected[1])):
            found = first_difference(a, b, f"{path}[{index}]")
            if found:
                return found
    return {"path": path, "observed": observed, "expected": expected}


def blocks(profile: str, prefixes: list[str]) -> frozenset:
    out = set()
    for line in profile.splitlines()[1:]:
        fields = line.split()
        if len(fields) == 3 and int(fields[2]) > 0 and any(fields[0].startswith(p) for p in prefixes):
            out.add(fields[0])
    return frozenset(out)


def covered(binary: Path, lead: str, control: Path, prefixes: list[str]) -> frozenset:
    with tempfile.TemporaryDirectory(prefix="parsarium-yaml-lead-") as temporary:
        directory = Path(temporary) / "cover"
        directory.mkdir()
        env = {**os.environ, "GOCOVERDIR": str(directory)}
        command(str(binary), lead, str(control), env=env)
        text = Path(temporary) / "profile.txt"
        command("go", "tool", "covdata", "textfmt", "-i", str(directory), "-o", str(text))
        result = blocks(text.read_text(), prefixes)
    if not result:
        raise RuntimeError(f"{lead}: no coverage under {prefixes}")
    return result


def source_lines(root: Path) -> set[str]:
    out = set()
    for path in root.rglob("*.go"):
        relative = str(path.relative_to(root))
        if path.name.endswith("_test.go") or any(part in relative for part in SKIP_PARTS):
            continue
        for line in path.read_text(errors="replace").splitlines():
            text = line.strip()
            if text and not text.startswith("//"):
                out.add(text)
    return out


def download(module: str, version: str) -> dict:
    return json.loads(command("go", "mod", "download", "-json", f"{module}@{version}"))


def main() -> None:
    expected = oracle()
    controls = {name: ROOT / "controls/yaml" / name for name in CONTROLS}
    command("go", "mod", "verify")
    with tempfile.TemporaryDirectory(prefix="parsarium-yaml-probe-") as temporary:
        plain, cover = Path(temporary) / "probe", Path(temporary) / "probe-cover"
        command("go", "build", "-mod=readonly", "-o", str(plain), ".")
        command("go", "build", "-mod=readonly", "-cover", f"-coverpkg={','.join(COVERPKG)}", "-o", str(cover), ".")
        results = {}
        for lead, spec in LEADS.items():
            observed = {name: json.loads(command(str(plain), lead, str(path))) for name, path in controls.items()}
            row = {**{key: value for key, value in spec.items() if key != "own"}, "controls": {}}
            for name, record in observed.items():
                match = record["error"] is None and record["tree"] == expected[name]
                row["controls"][name] = {
                    "oracle_match": match, "error": record["error"],
                    "first_difference": None if match or record["error"] else first_difference(record["tree"], expected[name])}
            row["oracle_match_both"] = all(item["oracle_match"] for item in row["controls"].values())
            if row["oracle_match_both"] and "own" in spec:
                feedback = {}
                for label, prefixes in (("own", spec["own"]), ("underlying_go_yaml_in_v3", [UNDERLYING])):
                    runs = {name: [covered(cover, lead, path, prefixes) for _ in range(3)]
                            for name, path in controls.items()}
                    stable = all(item == runs[name][0] for name in runs for item in runs[name])
                    a, b = runs["catalog.yaml"][0], runs["order.yaml"][0]
                    feedback[label] = {"prefixes": prefixes, "repeats_identical": stable,
                                       "catalog_blocks": len(a), "order_blocks": len(b),
                                       "block_difference": len(a ^ b)}
                row["source_block_feedback"] = feedback
            results[lead] = row
    forks = []
    for module, version, reference, reference_version in FORKS:
        info, ref = download(module, version), download(reference, reference_version)
        a, b = source_lines(Path(info["Dir"])), source_lines(Path(ref["Dir"]))
        first = Path(info["GoMod"]).read_text().splitlines()[0] if info.get("GoMod") else None
        forks.append({"module": module, "version": version, "module_sum": info.get("Sum"),
                      "go_mod_first_line": first, "reference": f"{reference}@{reference_version}",
                      "distinct_non_test_lines": len(a), "reference_distinct_non_test_lines": len(b),
                      "shared_distinct_lines": len(a & b)})
    report = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "go_toolchain": command("go", "version").strip(),
        "probe": "lead-probes/go/yaml/wrappers",
        "control_sha256": {name: sha256(path.read_bytes()).hexdigest() for name, path in controls.items()},
        "oracle": "controls/yaml/check_controls.py EXPECTED typed trees",
        "note": ("Local go toolchain probe, not a Docker harness. Go maps have no order, so map keys of "
                 "map-returning APIs are reported sorted; JSON-conversion APIs are read token by token, "
                 "so their typed tree keeps the key order of the JSON text they emit. Shared lines are "
                 "distinct stripped non-comment lines of non-test .go files (cmd/, examples, test "
                 "utilities and testdata excluded)."),
        "leads": results,
        "source_overlap": forks,
    }
    destination = ROOT / "data/go/yaml/lead-check.json"
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    for lead, row in results.items():
        print(lead, row["oracle_match_both"], json.dumps(row.get("source_block_feedback")))
    print(f"wrote {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
