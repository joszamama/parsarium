"""Check the json5 path on both valid JSON controls: the type-tagged tree of the value
JSON5.parse returns in the verified image must equal an independent Python json oracle
over the same bytes, and its summary must equal the pinned summaries."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import struct
import tempfile

from run_case import ROOT, project_for
from verify_javascript_json_feedback import run, sandbox


RELATIVE = Path("json/javascript/json5")
REPORT = ROOT / "data/javascript/json/json5-tree-verification.json"


class Members(list):
    """Object members in document order, from Python's json module."""


def members(pairs: list) -> Members:
    keys = [key for key, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate key in control")
    return Members(pairs)


def oracle_tree(data: bytes) -> dict:
    """Type-tagged tree computed with Python's json module, not json5."""
    def tag(value: object) -> dict:
        if value is None:
            return {"type": "null"}
        if isinstance(value, bool):
            return {"type": "boolean", "value": value}
        if isinstance(value, str):
            return {"type": "string", "value": value}
        if isinstance(value, float):
            return {"type": "number", "float64": struct.pack(">d", value).hex()}
        if isinstance(value, Members):
            return {"type": "object", "members": [[key, tag(child)] for key, child in value]}
        if isinstance(value, list):
            return {"type": "array", "items": [tag(child) for child in value]}
        raise TypeError(type(value))
    return tag(json.loads(data.decode("utf-8"), object_pairs_hook=members,
                          parse_int=float, parse_float=float))


def main() -> None:
    project, manifest = project_for(*RELATIVE.parts)
    base = json.loads((project / "verification.json").read_text())
    pinned_trees = json.loads((project / "expected-trees.json").read_text())
    results = []
    with tempfile.TemporaryDirectory(prefix="parsarium-json5-") as temporary:
        work = Path(temporary)
        for key in ("control", "differential_control"):
            path = ROOT / manifest[key]
            data = path.read_bytes()
            digest = sha256(data).hexdigest()
            if digest != manifest[f"{key}_sha256"]:
                raise ValueError(f"control hash mismatch: {path}")
            expected_summary = manifest["expected_output" if key == "control" else "differential_expected_output"]
            observed = json.loads(run([*sandbox(manifest, path, work), "--entrypoint", "node",
                                       base["image_id"], "/work/replay.js", "--tree", "/input/case"]))
            oracle = oracle_tree(data)
            if oracle != pinned_trees[digest]["tree"]:
                raise RuntimeError(f"{path.name}: pinned tree differs from the Python oracle")
            if observed["tree"] != oracle:
                raise RuntimeError(f"{path.name}: json5 tree differs from the Python oracle")
            if observed["summary"] != expected_summary:
                raise RuntimeError(f"{path.name}: json5 summary differs: {observed['summary']}")
            results.append({"control": manifest[key], "control_sha256": digest,
                            "tree_sha256": sha256(json.dumps(oracle, sort_keys=True).encode()).hexdigest(),
                            "tree_matches_oracle": True, "summary_matches_pinned": True,
                            "summary": observed["summary"]})
            print(f"{path.name}: json5 tree and summary match", flush=True)
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "project": str(RELATIVE),
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "base_image_id": base["image_id"],
        "api": "JSON5.parse(text) after TextDecoder('utf-8', {fatal: true, ignoreBOM: true})",
        "oracle": "Python json.loads of the same bytes (object_pairs_hook keeps member order and rejects "
                  "duplicate keys; every number as float), tagged by type with numbers as IEEE 754 double bits",
        "pinned_trees": f"projects/{RELATIVE}/expected-trees.json",
        "results": results, "pass": True}, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
