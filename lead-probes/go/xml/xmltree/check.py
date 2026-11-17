#!/usr/bin/env python3
"""Reproduce the aqwari.net/xml/xmltree lead decision on both valid XML controls."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PROBE = Path(__file__).resolve().parent
ROOT = PROBE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from verify_go_xml_feedback import probe  # noqa: E402

PACKAGE = "aqwari.net/xml/xmltree"
LOCK = json.loads((PROBE / "source-lock.json").read_text())[PACKAGE]
IMAGE = "parsarium-lead/xml-go-xmltree:local"
AFL_IMAGE = "parsarium-lead-afl/xml-go-xmltree:local"
PLATFORM = "linux/arm64"
CONTROLS = {"control": "controls/xml/catalog-ns.xml", "differential": "controls/xml/order-default-ns.xml"}
# Other valid controls from controls/xml, used only to show that xmltree feedback is
# input-dependent at all; they do not replace the cell's fixed differential.
SUPPLEMENTARY = ("controls/xml/one-item.xml", "controls/xml/two-items.xml")
REPEATS = 2
PREFIXES = {"xmltree": "aqwari.net/xml/xmltree/", "encoding_xml": "encoding/xml/"}
OUTPUT = ROOT / "data/go/xml/xmltree-lead-check.json"
SANDBOX = ["--network", "none", "--read-only", "--cap-drop", "ALL",
           "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
           "--tmpfs", "/tmp:rw,nosuid,size=64m"]


def run(command: list[str], **kwargs) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True, **kwargs).stdout


def covered(profile: Path) -> dict[str, dict[str, set]]:
    """Return covered cover blocks and source lines per prefix for one run."""
    found = {key: {"blocks": set(), "lines": set()} for key in PREFIXES}
    for line in profile.read_text().splitlines()[1:]:
        location, _, count = line.split()
        if count == "0":
            continue
        for key, prefix in PREFIXES.items():
            if not location.startswith(prefix):
                continue
            filename, span = location.rsplit(":", 1)
            start, end = span.split(",")
            first, last = int(start.split(".")[0]), int(end.split(".")[0])
            if end.split(".")[1] == "1" and last > first:
                last -= 1  # Go cover block end positions are exclusive.
            found[key]["blocks"].add(location)
            found[key]["lines"].update(f"{filename}:{number}" for number in range(first, last + 1))
    return found


def replay(name: str, control: str, work: Path, label: str) -> tuple[dict, dict]:
    test = {"control": "TestControl", "differential": "TestDifferential"}[name]
    output = run(["docker", "run", "--rm", "--platform", PLATFORM, *SANDBOX,
                  "-v", f"{ROOT / control}:/input/{name}:ro", "-v", f"{work}:/coverage",
                  IMAGE, f"-test.run=^{test}$", "-test.v",
                  f"-test.coverprofile=/coverage/{label}.cover"], timeout=120)
    observed, = [json.loads(line.removeprefix("OBSERVED_JSON:")) for line in output.splitlines()
                 if line.startswith("OBSERVED_JSON:")]
    return observed, covered(work / f"{label}.cover")


def main() -> None:
    oracle = json.loads(run([sys.executable, "-I", str(PROBE / "oracle.py"), *CONTROLS.values()]))
    run(["docker", "build", "--quiet", "--platform", PLATFORM, "-t", IMAGE, str(PROBE)], timeout=900)
    run(["docker", "build", "--quiet", "--platform", PLATFORM, "-t", AFL_IMAGE,
         "-f", str(PROBE / "afl.Dockerfile"), str(ROOT)], timeout=900)
    image_id = run(["docker", "image", "inspect", "--format", "{{.Id}}", IMAGE]).strip()
    afl_image_id = run(["docker", "image", "inspect", "--format", "{{.Id}}", AFL_IMAGE]).strip()
    toolchain = run(["docker", "run", "--rm", "--platform", PLATFORM, "--entrypoint", "go",
                     "golang@" + "sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66",
                     "version"]).strip()

    controls = {}
    afl = {}
    manifest = {"platform": PLATFORM}
    with tempfile.TemporaryDirectory(prefix="parsarium-xmltree-lead-") as temporary:
        work = Path(temporary)
        for name, control in CONTROLS.items():
            runs = [replay(name, control, work, f"{name}-{repeat}") for repeat in range(REPEATS)]
            if any(item != runs[0] for item in runs):
                raise RuntimeError(f"{control}: repeated replay changed")
            observed, cover = runs[0]
            if observed != oracle[control]:
                raise RuntimeError(f"{control}: xmltree summary differs from expat oracle: {observed}")
            controls[control] = {
                "control_sha256": sha256((ROOT / control).read_bytes()).hexdigest(),
                "observed": observed, "matches_expat_oracle": True,
                **{f"{key}_cover_blocks": len(cover[key]["blocks"]) for key in PREFIXES},
                **{f"{key}_source_lines": len(cover[key]["lines"]) for key in PREFIXES},
                "_cover": cover}
        for control in (*CONTROLS.values(), *SUPPLEMENTARY):
            for key, prefix in PREFIXES.items():
                runs = [probe(manifest, afl_image_id, ROOT / control, work,
                              f"{Path(control).stem}-{key}-{repeat}", prefix)
                        for repeat in range(REPEATS)]
                if any(item != runs[0] for item in runs):
                    raise RuntimeError(f"{control}: repeated {prefix} AFL++ probe changed")
                afl[control, key] = runs[0]

    first, second = CONTROLS.values()
    differences = {}
    for key in PREFIXES:
        blocks = sorted(controls[first]["_cover"][key]["blocks"] ^ controls[second]["_cover"][key]["blocks"])
        features = sorted(afl[first, key][0] ^ afl[second, key][0])
        tuples = ({item.split(":", 1)[0] for item in afl[first, key][1]} ^
                  {item.split(":", 1)[0] for item in afl[second, key][1]})
        differences[key] = {"replay_cover_block_difference": len(blocks),
                            "afl_parser_feature_difference": len(features),
                            "afl_tuple_difference": len(tuples),
                            "control_afl_features": len(afl[first, key][0]),
                            "control_afl_tuples": len(afl[first, key][1]),
                            "differential_afl_features": len(afl[second, key][0]),
                            "differential_afl_tuples": len(afl[second, key][1])}
        if key == "xmltree":
            differences[key]["changed_blocks"] = blocks
    supplementary = {}
    for control in SUPPLEMENTARY:
        features = sorted(afl[first, "xmltree"][0] ^ afl[control, "xmltree"][0])
        tuples = ({item.split(":", 1)[0] for item in afl[first, "xmltree"][1]} ^
                  {item.split(":", 1)[0] for item in afl[control, "xmltree"][1]})
        supplementary[control] = {"sha256": sha256((ROOT / control).read_bytes()).hexdigest(),
                                  "xmltree_afl_features": len(afl[control, "xmltree"][0]),
                                  "xmltree_feature_difference_vs_control": len(features),
                                  "xmltree_tuple_difference_vs_control": len(tuples),
                                  "changed_features": features}
    for record in controls.values():
        del record["_cover"]

    if any(record["xmltree_cover_blocks"] == 0 or record["encoding_xml_cover_blocks"] == 0
           for record in controls.values()):
        raise RuntimeError("a replay recorded no xmltree or encoding/xml coverage")
    if differences["xmltree"]["afl_parser_feature_difference"] or differences["xmltree"]["afl_tuple_difference"]:
        raise RuntimeError("xmltree feedback now differs on the fixed differential; review the lead decision")
    if not differences["encoding_xml"]["afl_parser_feature_difference"]:
        raise RuntimeError("encoding/xml feedback no longer differs; review the lead decision")

    result = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "negative_lead_no_package_feedback_differential",
        "package": PACKAGE, "module": LOCK["go_module"], "release": LOCK["release"],
        "release_commit": LOCK["upstream_commit"],
        "release_commit_time_utc": "2021-03-31T02:33:08Z",
        "source_url": "https://github.com/droyo/go-xml/tree/d9421b293817",
        "license": "MIT (LICENSE, Copyright (c) 2015 David Arroyo)",
        "source_lock": "lead-probes/go/xml/xmltree/source-lock.json",
        "module_zip_sha256": LOCK["source_sha256"], "module_sum": LOCK["go_module_sum"],
        "dependencies": LOCK["dependencies"],
        "image": "golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66",
        "platform": PLATFORM, "go_toolchain": toolchain,
        "probe_image_id": image_id, "afl_image_id": afl_image_id,
        "afl_package": "4.33c-1.1ubuntu1",
        "underlying_source": "encoding/xml/xml.go",
        "underlying_source_sha256": "41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb",
        "popularity": {
            "metric": "pkg.go.dev Imported by package count", "value": 43,
            "importing_modules": 20,
            "source": "https://pkg.go.dev/aqwari.net/xml/xmltree?tab=importedby",
            "captured_at_utc": "2026-11-17T03:16:02.492959+00:00",
            "registry_snapshot": "data/go/xml/registry-snapshot.json",
            "recheck_utc": "2026-11-17T14:30:36Z",
            "recheck_page_sha256": "b40739508ed941d915ae5eccd3a45af984bdb3cb324b53db6073aac49abcbc78",
            "caveat": "Package importers, not installations; no tagged release. Of the 70 package paths the importer page lists (including internal and invalid ones), 58 are xsd, xsdgen, wsdl, cmd/xsdparse or gentests packages inside copies of the droyo/go-xml repository itself; 12 are in other projects.",
        },
        "api_finding": {
            "local_bytes_parse_api": "xmltree.Parse([]byte) (*Element, error); no io.Reader or file entry point",
            "api_reference": f"https://pkg.go.dev/{LOCK['go_module']}@{LOCK['release']}/xmltree#Parse",
            "tokenizer": "none of its own; Parse runs encoding/xml.NewDecoder(bytes.NewReader(doc)).Token() and builds Element values from StartElement/EndElement tokens",
            "own_code": "xmltree.go tree walk (Element.parse), namespace scope stack (Scope.pushNS), Scope.Prefix/Resolve, raw Content slicing by Decoder.InputOffset, recursion limit 3000",
            "text": "No decoded character data. Element.Content is the raw source bytes between start and end tag: references stay undecoded and CDATA keeps its markup.",
            "namespace_declarations": "Removed from StartElement.Attr into an unexported Scope; Prefix and Resolve use it, but the public API cannot list or count declarations.",
        },
        "parser_family": "Go encoding/xml.Decoder (same pinned encoding/xml source as stdlib_decoder, etree, xmlquery, mxj, x2j and goxpp); xmltree adds tree building and namespace scope only. Not an independent engine.",
        "oracle": "python3 -I lead-probes/go/xml/xmltree/oracle.py (expat namespace mode with prefixes; raw leaf bytes sliced at expat byte offsets)",
        "controls": controls,
        "fixed_differential_feedback": differences,
        "supplementary_input_dependence": supplementary,
        "decision": "Not counted as a runnable parser path. xmltree.Parse([]byte) parses both valid controls and its exposed tree matches an independent expat oracle exactly, including expanded names, prefixes rebuilt by Scope.Prefix, xmlns=\"\" undeclaration and raw leaf content. Its own xmltree.go source is covered and its AFL++ feedback repeats exactly. On the cell's fixed differential pair (catalog-ns.xml vs order-default-ns.xml) the xmltree-scoped cover blocks and AFL++ map are identical; every difference is in encoding/xml, which Parsarium already counts as stdlib_decoder. This fails the same gate that excluded mellium.im/xmlstream. Other valid inputs without prefixed declarations (one-item.xml, two-items.xml) do change four xmltree.go blocks, so the feedback is input-dependent; an integrator could revisit the lead if the cell gate changes, but the fixed pair is not replaced here.",
        "probe_file_sha256": {name: sha256((PROBE / name).read_bytes()).hexdigest()
                              for name in ("Dockerfile", "afl.Dockerfile", "afl_trace", "check.py", "go.mod",
                                           "go.sum", "harness.go", "harness_test.go", "oracle.py",
                                           "source-lock.json")},
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    for key, record in differences.items():
        print(f"{key}: {record['afl_parser_feature_difference']} AFL++ features, "
              f"{record['afl_tuple_difference']} tuples differ on the fixed pair")
    for control, record in supplementary.items():
        print(f"{control}: {record['xmltree_feature_difference_vs_control']} xmltree features differ")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
