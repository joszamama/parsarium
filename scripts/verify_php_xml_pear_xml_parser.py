"""Recheck pear/xml_parser's two valid controls, package and libxml2 source lines, and native AFL++ feedback."""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from verify_php_xml_feedback import probe


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/xml/php/pear_xml_parser"
OVERLAY = ROOT / "fuzzing/afl-native/xml/php/pear_xml_parser"
REPORT = ROOT / "data/php/xml/pear-xml-parser-feedback-differential.json"
PREFIX = "/work/vendor/pear/xml_parser/"
UNDERLYING = "/work/source/libxml2-2.15.4/"
EXTENSION = "/work/source/php-8.5.12/ext/xml/"
REPEATS = 3
# XML_Parser's default case folding (left on), which upper-cases element and attribute names.
DEFAULT_FOLDING_VIEW = (
    'require "/work/vendor/autoload.php"; require "/work/summary.php"; error_reporting(E_ALL & ~E_DEPRECATED); '
    '$parser = new XML_Parser(); $handler = new ParsariumXmlParserHandler(); $parser->setHandlerObj($handler); '
    '$parser->setInputString(file_get_contents($argv[1])); $result = $parser->parse(); '
    'echo json_encode(["folding_default" => (new XML_Parser())->folding, "parse_ok" => $result === true, '
    '"elements" => $handler->summary()["elements"], "attributes" => $handler->summary()["attributes"]], '
    'JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);')

sys.path.insert(0, str(PROJECT))
sys.dont_write_bytecode = True
from oracle import summarize  # noqa: E402


def sandbox(manifest: dict, control: Path) -> list[str]:
    return ["docker", "run", "--rm", "--platform", manifest["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,nosuid,size=64m", "-v", f"{control}:/input/control:ro"]


def replay(manifest: dict, image: str, control: Path, work: Path) -> dict:
    """Run the coverage image on one valid control and return its per-file line counts."""
    work.mkdir()
    result = subprocess.run([*sandbox(manifest, control), "-v", f"{work}:/coverage", image],
                            capture_output=True, text=True, timeout=300)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    summary = json.loads((work / "summary.json").read_text())
    files = json.loads((work / "coverage.json").read_text())["data"][0]["files"]
    if not summary["control_pass"] or not summary["file_and_stream_api_match"]:
        raise RuntimeError(f"{control.name}: control runner did not pass")
    if any(not item["filename"].startswith((PREFIX, UNDERLYING, EXTENSION)) for item in files):
        raise RuntimeError("coverage outside XML_Parser, ext/xml and libxml2 source")
    lines = lambda prefix: {item["filename"].removeprefix(prefix): item["summary"]["lines"]["covered"]
                            for item in files if item["filename"].startswith(prefix)}
    package_lines = {item["filename"].removeprefix(PREFIX): item["executed_lines"]
                     for item in files if item["filename"].startswith(PREFIX)}
    underlying = lines(UNDERLYING)
    return {"summary": summary, "package_lines": package_lines, "extension_lines_by_file": lines(EXTENSION),
            "underlying_parser_files": {name: underlying[name] for name in
                                        ("parser.c", "parserInternals.c", "SAX2.c") if name in underlying}}


def default_folding(manifest: dict, image: str, control: Path) -> dict:
    result = subprocess.run([*sandbox(manifest, control), "--entrypoint", "/opt/php/bin/php", image,
                             "-r", DEFAULT_FOLDING_VIEW, "/input/control"],
                            capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    return json.loads(result.stdout)


def edges(tuples: frozenset) -> set[str]:
    return {item.split(":", 1)[0] for item in tuples}


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--write", "--check"}:
        raise SystemExit("usage: verify_php_xml_pear_xml_parser.py --write|--check")
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    base = json.loads((PROJECT / "verification.json").read_text())
    overlay = json.loads((OVERLAY / "verification.json").read_text())
    if (manifest["coverage_subject_prefix"], manifest["underlying_coverage_subject_prefix"]) != (PREFIX, UNDERLYING):
        raise RuntimeError("coverage subjects are not the XML_Parser and libxml2 sources")
    if overlay["base_project_receipt_sha256"] != sha256((PROJECT / "verification.json").read_bytes()).hexdigest():
        raise RuntimeError("AFL++ overlay receipt does not match the project receipt")
    if overlay["base_image_id"] != base["image_id"]:
        raise RuntimeError("AFL++ overlay was not built from the verified project image")
    control = ROOT / manifest["control"]
    differential = ROOT / manifest["differential_control"]
    for path, digest, key in ((control, manifest["control_sha256"], "expected_output"),
                              (differential, manifest["differential_control_sha256"], "differential_expected_output")):
        data = path.read_bytes()
        if sha256(data).hexdigest() != digest:
            raise RuntimeError(f"{path.name}: control bytes changed")
        if summarize(data) != manifest[key]:
            raise RuntimeError(f"{path.name}: manifest output differs from the expat oracle")
    with tempfile.TemporaryDirectory(prefix="parsarium-pear-xml-parser-") as temporary:
        work = Path(temporary)
        lines = replay(manifest, base["image_id"], control, work / "control-lines")
        other_lines = replay(manifest, base["image_id"], differential, work / "differential-lines")
        folding = default_folding(manifest, base["image_id"], differential)
        image = overlay["image_id"]
        first = [probe(manifest, image, control, work, f"first{index}", False)[1] for index in range(REPEATS)]
        other = [probe(manifest, image, differential, work, f"other{index}", False)[1] for index in range(REPEATS)]
    if lines["summary"]["output"] != manifest["expected_output"]:
        raise RuntimeError("catalog-ns summary differs from manifest")
    if other_lines["summary"]["output"] != manifest["differential_expected_output"]:
        raise RuntimeError("order-default-ns summary differs from manifest")
    if lines["summary"]["parser_source_lines_covered"] != base["parser_source_lines_covered"]:
        raise RuntimeError("control package lines differ from the project receipt")
    if len(set(first)) != 1 or len(set(other)) != 1:
        raise RuntimeError("repeated probe changed the AFL++ map")
    if len(first[0]) != overlay["feedback_edges"] or len(other[0]) != overlay["differential_feedback_edges"]:
        raise RuntimeError("control probes differ from overlay receipt")
    tuple_difference = len(edges(first[0]) ^ edges(other[0]))
    if tuple_difference != overlay["afl_tuple_difference"] or not tuple_difference:
        raise RuntimeError("differential control did not change native parser feedback as recorded")
    if folding["folding_default"] is not True or folding["elements"][0] != "ORDER":
        raise RuntimeError(f"XML_Parser default case folding changed: {folding}")
    deprecations = lines["summary"]["php_deprecations"]
    if deprecations != other_lines["summary"]["php_deprecations"] or not deprecations:
        raise RuntimeError("PHP deprecation notices differ between controls or are missing")
    result = {
        "project": "xml/php/pear_xml_parser", "pass": True,
        "feedback_kind": overlay["feedback_kind"],
        "overlay_receipt_sha256": sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"], "overlay_image_id": image,
        "release_source_sha256": manifest["source_sha256"],
        "parser_source_prefix": PREFIX, "underlying_source_prefix": UNDERLYING, "extension_source_prefix": EXTENSION,
        "control": manifest["control"], "control_sha256": manifest["control_sha256"],
        "differential": manifest["differential_control"],
        "differential_sha256": manifest["differential_control_sha256"],
        "oracle": "projects/xml/php/pear_xml_parser/oracle.py",
        "control_output_matches_oracle": True, "differential_output_matches_oracle": True,
        "file_and_stream_api_match": True,
        "control_package_lines": lines["package_lines"],
        "differential_package_lines": other_lines["package_lines"],
        "package_lines_identical_between_controls": lines["package_lines"] == other_lines["package_lines"],
        "xdebug_eof_pseudo_lines_removed": lines["summary"]["xdebug_eof_pseudo_lines_removed"],
        "control_extension_lines_by_file": lines["extension_lines_by_file"],
        "differential_extension_lines_by_file": other_lines["extension_lines_by_file"],
        "control_underlying_parser_lines_by_file": lines["underlying_parser_files"],
        "differential_underlying_parser_lines_by_file": other_lines["underlying_parser_files"],
        "underlying_line_note": "libxml2 totals vary by a few dict.c lines between identical runs (hash-seed "
                                "dependent); parser.c, parserInternals.c and SAX2.c counts are stable.",
        "php_deprecations": deprecations,
        "default_case_folding_view_differential": folding,
        "raw_namespace_note": "XML_Parser creates xml_parser_create() without a namespace separator: names stay raw "
                              "qualified names and xmlns/xmlns:* (including xmlns=\"\") are ordinary attributes. "
                              "With the package default $folding = true every name is upper-cased; the harness "
                              "sets the documented property to false. Not repaired by the harness.",
        "repeats_per_control": REPEATS,
        "repeated_control_identical": True, "repeated_differential_identical": True,
        "control_afl_tuples": len(first[0]), "differential_afl_tuples": len(other[0]),
        "afl_tuple_difference": tuple_difference,
        "bare_baseline_tuple_difference": overlay["baseline_tuple_difference"],
        "differing_tuples_subset_of_bare_baseline": overlay["differing_tuples_subset_of_bare_baseline"],
        "differing_tuples_package_path_only": overlay["differing_tuples_package_path_only"],
        "wrapper_assessment": "XML_Parser drives the parse itself (creates and configures the ext/xml parser, binds "
                              "the handler object, feeds the bytes and frees the parser), so it is a libxml2-family "
                              "SAX package path rather than a mapping of an already parsed tree. Its interpreted "
                              "PHP adds no input-dependent native tuples: every tuple that differs between the "
                              "controls also differs under a bare xml_parser_create/xml_parse baseline with the same "
                              "handler object.",
        "shared_family": overlay["shared_family"],
    }
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if sys.argv[1] == "--write":
        REPORT.write_text(output)
    elif REPORT.read_text() != output:
        raise SystemExit("pear/xml_parser feedback receipt changed")
    print(f"verified pear/xml_parser: {lines['summary']['parser_source_lines_covered']} package lines, "
          f"{tuple_difference} native AFL++ tuples differ")


if __name__ == "__main__":
    main()
