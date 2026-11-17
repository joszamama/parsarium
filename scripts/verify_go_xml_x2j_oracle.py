"""Compare beego/x2j map summaries with an expat projection of the same two XML controls.

The oracle tokenizes each control with the Python standard library's expat
binding, not Go encoding/xml, then projects the events onto the fields an x2j
map can expose: local element names as path keys, '-'-prefixed attribute
local names (namespace declarations included), same-name siblings as indexed
lists, and character-data runs. A run ends at any tag, comment, processing
instruction or CDATA boundary, as Go's Decoder.Token splits them. Following
x2j's map convention, a run becomes a '#text' entry once the element already
has attributes or children; otherwise it replaces the element's string value.

Two projections are compared:
  reader: every run as decoded, matching ToMap(io.Reader).
  bytes:  the XML value after x2j's documented pre-pass that deletes whitespace
          before '<'. Runs outside CDATA lose trailing whitespace and
          whitespace-only runs disappear; CDATA content keeps its decoded value,
          so a rewrite inside CDATA shows up as a mismatch.

The oracle reuses x2j's map conventions but not its code or tokenizer.
Mismatches must equal the declared KNOWN_BYTE_PATH_DEFECTS exactly.
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from xml.parsers import expat

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/xml/go/github_com_beego_x2j"
PACKAGE = "github.com/beego/x2j"
CONTROLS = {
    "controls/xml/catalog-ns.xml": "dffe6fcacbea13d5da12b3939756d22cf0a425db8d21c8295ff6a01f8ed22928",
    "controls/xml/order-default-ns.xml": "c0ac18eb0c6e31f6cd920302ac46d9a13959caaa78f2ee7f1f01e0f9a43eccba",
}
KNOWN_BYTE_PATH_DEFECTS = {
    "controls/xml/catalog-ns.xml": {
        "oracle_only": ["catalog/item[1]/note=x < y"],
        "x2j_only": ["catalog/item[1]/note=x< y"],
    },
    "controls/xml/order-default-ns.xml": {"oracle_only": [], "x2j_only": []},
}


def local(name: str) -> str:
    return name.rpartition(":")[2]


def events(data: bytes) -> dict:
    """Return the root element as {name, attributes, content}; runs are (text, is_cdata)."""
    parser = expat.ParserCreate("UTF-8")
    parser.ordered_attributes = True
    stack, buffer, state = [], [], {"cdata": False, "root": None}

    def flush(*_):
        if buffer and stack:
            stack[-1]["content"].append(("".join(buffer), state["cdata"]))
        buffer.clear()

    def start(name, attributes):
        flush()
        element = {"name": local(name), "content": [],
                   "attributes": [(local(key), value)
                                  for key, value in zip(attributes[::2], attributes[1::2])]}
        if stack:
            stack[-1]["content"].append(element)
        else:
            state["root"] = element
        stack.append(element)

    def end(_name):
        flush()
        stack.pop()

    def cdata_start():
        flush()
        state["cdata"] = True

    def cdata_end():
        flush()
        state["cdata"] = False

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.CharacterDataHandler = buffer.append
    parser.CommentHandler = parser.ProcessingInstructionHandler = flush
    parser.StartCdataSectionHandler, parser.EndCdataSectionHandler = cdata_start, cdata_end
    parser.Parse(data, True)
    return state["root"]


def to_value(element: dict, byte_path: bool):
    nodes = [("-" + name, value) for name, value in element["attributes"]]
    value = ""
    for item in element["content"]:
        if isinstance(item, dict):
            nodes.append((item["name"], to_value(item, byte_path)))
            continue
        text, is_cdata = item
        if byte_path and not is_cdata:
            text = text.rstrip(" \t\r\n")
        if not text:
            continue
        if nodes:
            nodes.append(("#text", text))
        else:
            value = text
    if not nodes:
        return value
    counts = {}
    for key, _ in nodes:
        counts[key] = counts.get(key, 0) + 1
    result = {}
    for key, child in nodes:
        if counts[key] > 1:
            result.setdefault(key, []).append(child)
        else:
            result[key] = child
    return result


def summarize(root: dict, byte_path: bool) -> dict:
    out = {"attributes": [], "elements": [], "empty_elements": [], "lists": [], "text": []}
    depth = {"max": 0}

    def element(path, value, level):
        if isinstance(value, list):
            out["lists"].append(f"{path}={len(value)}")
            for index, item in enumerate(value):
                single(f"{path}[{index}]", item, level)
        else:
            single(path, value, level)

    def single(path, value, level):
        out["elements"].append(path)
        depth["max"] = max(depth["max"], level)
        if isinstance(value, str):
            (out["text"].append(f"{path}={value}") if value else out["empty_elements"].append(path))
            return
        for key, child in value.items():
            if key == "#text":
                if isinstance(child, list):
                    out["lists"].append(f"{path}/#text={len(child)}")
                    out["text"].extend(f"{path}/#text[{i}]={run}" for i, run in enumerate(child))
                else:
                    out["text"].append(f"{path}/#text={child}")
            elif key.startswith("-"):
                out["attributes"].append(f"{path}/{key}={child}")
            else:
                element(f"{path}/{key}", child, level + 1)

    element(root["name"], to_value(root, byte_path), 1)
    return {**{key: sorted(values) for key, values in out.items()},
            "max_depth": depth["max"], "root": root["name"]}


def compare(oracle: dict, observed: dict) -> dict:
    mismatches = {"oracle_only": [], "x2j_only": []}
    for key in sorted(oracle):
        if isinstance(oracle[key], list):
            mismatches["oracle_only"] += sorted(set(oracle[key]) - set(observed[key]))
            mismatches["x2j_only"] += sorted(set(observed[key]) - set(oracle[key]))
        elif oracle[key] != observed[key]:
            mismatches["oracle_only"].append(f"{key}={oracle[key]}")
            mismatches["x2j_only"].append(f"{key}={observed[key]}")
    return mismatches


def main() -> None:
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    record, = [item for item in json.loads((ROOT / "data/go/xml/verification.json").read_text())["third_party"]
               if item["package"] == PACKAGE]
    observed = {manifest["control"]: manifest["expected_output"],
                record["differential_control"]: record["differential_output"]}
    results = []
    for control, digest in CONTROLS.items():
        data = (ROOT / control).read_bytes()
        assert sha256(data).hexdigest() == digest, control
        root = events(data)
        reader = compare(summarize(root, False), observed[control]["reader"])
        byte_path = compare(summarize(root, True), observed[control]["bytes"])
        if reader != {"oracle_only": [], "x2j_only": []}:
            raise SystemExit(f"{control}: ToMap(io.Reader) differs from the expat projection: {reader}")
        if byte_path != KNOWN_BYTE_PATH_DEFECTS[control]:
            raise SystemExit(f"{control}: []byte path mismatches changed: {byte_path}")
        results.append({"control": control, "control_sha256": digest,
                        "reader_mismatches": reader, "bytes_mismatches": byte_path})
        print(f"{control}: reader exact; bytes mismatches {byte_path}")
    receipt = {"schema_version": 1, "package": PACKAGE,
               "checked_at_utc": datetime.now(timezone.utc).isoformat(),
               "oracle": "python3 -I scripts/verify_go_xml_x2j_oracle.py (expat, namespace-unaware, "
                         "projected onto x2j map fields)",
               "oracle_script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "manifest_sha256": sha256((PROJECT / "manifest.json").read_bytes()).hexdigest(),
               "pass": True, "results": results}
    (ROOT / "data/go/xml/x2j-oracle-check.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
