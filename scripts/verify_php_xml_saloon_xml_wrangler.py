"""Recheck saloonphp/xml-wrangler's two valid controls, package source lines and native AFL++ feedback."""

from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from verify_php_xml_feedback import probe


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/xml/php/saloon_xml_wrangler"
OVERLAY = ROOT / "fuzzing/afl-native/xml/php/saloon_xml_wrangler"
REPORT = ROOT / "data/php/xml/saloonphp-xml-wrangler-feedback-differential.json"
PREFIX = "/work/vendor/saloonphp/xml-wrangler/"
UNDERLYING = "/work/vendor/veewee/xml/"
REPEATS = 3
# The package's own array view and the attributes of <plain xmlns=""> in order-default-ns.xml.
RAW_VIEW = ('require "/work/vendor/autoload.php"; '
            '$reader = Saloon\\XmlWrangler\\XmlReader::fromString(file_get_contents($argv[1])); '
            '$line = $reader->elements()["order"]->getContent()["line"]->getContent()[1]; '
            'echo json_encode(["values" => Saloon\\XmlWrangler\\XmlReader::fromString(file_get_contents($argv[1]))->values(), '
            '"plain_attributes" => $line->getContent()["plain"]->getAttributes()], '
            'JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);')

sys.path.insert(0, str(PROJECT))
from oracle import summarize  # noqa: E402


def sandbox(manifest: dict, control: Path) -> list[str]:
    return ["docker", "run", "--rm", "--platform", manifest["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,nosuid,size=64m", "-v", f"{control}:/input/control:ro"]


def replay(manifest: dict, image: str, control: Path, work: Path) -> dict:
    """Run the Xdebug control runner on one valid control and return its per-file line counts."""
    work.mkdir()
    result = subprocess.run([*sandbox(manifest, control), "-v", f"{work}:/coverage", image],
                            capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    summary = json.loads((work / "summary.json").read_text())
    files = json.loads((work / "coverage.json").read_text())["data"][0]["files"]
    if not summary["control_pass"] or not summary["file_and_stream_api_match"]:
        raise RuntimeError(f"{control.name}: control runner did not pass")
    if any(not item["filename"].startswith((PREFIX, UNDERLYING)) for item in files):
        raise RuntimeError("coverage outside XML Wrangler and veewee/xml source")
    lines = lambda prefix: {item["filename"].removeprefix(prefix): item["summary"]["lines"]["covered"]
                            for item in files if item["filename"].startswith(prefix)}
    return {"output": summary["output"],
            "parser_source_lines_covered": summary["parser_source_lines_covered"],
            "underlying_source_lines_covered": summary["underlying_source_lines_covered"],
            "lines_by_file": lines(PREFIX), "underlying_lines_by_file": lines(UNDERLYING)}


def raw_view(manifest: dict, image: str, control: Path) -> dict:
    result = subprocess.run([*sandbox(manifest, control), "--entrypoint", "php", image,
                             "-r", RAW_VIEW, "/input/control"], capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    return json.loads(result.stdout)


def edges(tuples: frozenset) -> set[str]:
    return {item.split(":", 1)[0] for item in tuples}


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--write", "--check"}:
        raise SystemExit("usage: verify_php_xml_saloon_xml_wrangler.py --write|--check")
    manifest = json.loads((PROJECT / "manifest.json").read_text())
    base = json.loads((PROJECT / "verification.json").read_text())
    overlay = json.loads((OVERLAY / "verification.json").read_text())
    if (manifest["coverage_subject_prefix"], manifest["underlying_coverage_subject_prefix"]) != (PREFIX, UNDERLYING):
        raise RuntimeError("coverage subjects are not the XML Wrangler and veewee/xml sources")
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
    with tempfile.TemporaryDirectory(prefix="parsarium-saloon-xml-wrangler-") as temporary:
        work = Path(temporary)
        lines = replay(manifest, base["image_id"], control, work / "control-lines")
        other_lines = replay(manifest, base["image_id"], differential, work / "differential-lines")
        raw = raw_view(manifest, base["image_id"], differential)
        image = overlay["image_id"]
        first = [probe(manifest, image, control, work, f"first{index}", False)[1] for index in range(REPEATS)]
        other = [probe(manifest, image, differential, work, f"other{index}", False)[1] for index in range(REPEATS)]
    if lines["output"] != manifest["expected_output"]:
        raise RuntimeError("catalog-ns summary differs from manifest")
    if other_lines["output"] != manifest["differential_expected_output"]:
        raise RuntimeError("order-default-ns summary differs from manifest")
    if lines["parser_source_lines_covered"] != base["parser_source_lines_covered"]:
        raise RuntimeError("control package lines differ from the project receipt")
    if len(set(first)) != 1 or len(set(other)) != 1:
        raise RuntimeError("repeated probe changed the AFL++ map")
    if len(first[0]) != overlay["feedback_edges"] or len(other[0]) != overlay["differential_feedback_edges"]:
        raise RuntimeError("control probes differ from overlay receipt")
    tuple_difference = len(edges(first[0]) ^ edges(other[0]))
    if tuple_difference != overlay["afl_tuple_difference"] or not tuple_difference:
        raise RuntimeError("differential control did not change native parser feedback as recorded")
    if raw["plain_attributes"] != []:
        raise RuntimeError(f"<plain xmlns=\"\"> attributes changed: {raw['plain_attributes']}")
    package_difference = Counter(lines["lines_by_file"])
    package_difference.subtract(other_lines["lines_by_file"])
    result = {
        "project": "xml/php/saloon_xml_wrangler", "pass": True,
        "feedback_kind": overlay["feedback_kind"],
        "overlay_receipt_sha256": sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"], "overlay_image_id": image,
        "release_source_sha256": manifest["source_sha256"],
        "underlying_package_source_sha256": manifest["underlying_package_source_sha256"],
        "parser_source_prefix": PREFIX, "underlying_source_prefix": UNDERLYING,
        "control": manifest["control"], "control_sha256": manifest["control_sha256"],
        "differential": manifest["differential_control"],
        "differential_sha256": manifest["differential_control_sha256"],
        "oracle": "projects/xml/php/saloon_xml_wrangler/oracle.py",
        "control_output_matches_oracle": True, "differential_output_matches_oracle": True,
        "file_and_stream_api_match": True,
        "control_source_lines_by_file": lines["lines_by_file"],
        "differential_source_lines_by_file": other_lines["lines_by_file"],
        "package_line_count_difference_by_file": {name: count for name, count in sorted(package_difference.items()) if count},
        "control_underlying_source_lines": lines["underlying_source_lines_covered"],
        "differential_underlying_source_lines": other_lines["underlying_source_lines_covered"],
        "control_underlying_lines_by_file": lines["underlying_lines_by_file"],
        "raw_package_view_differential": raw,
        "raw_namespace_note": "values() keys are raw qualified names; <plain xmlns=\"\"> keeps no attribute, because "
                              "veewee/xml drops declarations with an empty URI. Not repaired by the harness.",
        "repeats_per_control": REPEATS,
        "repeated_control_identical": True, "repeated_differential_identical": True,
        "control_afl_tuples": len(first[0]), "differential_afl_tuples": len(other[0]),
        "afl_tuple_difference": tuple_difference,
        "reader_pass_tuple_difference": overlay["reader_pass_tuple_difference"],
        "post_elements_edges": overlay["post_elements_edges"],
        "shared_family": overlay["shared_family"],
    }
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if sys.argv[1] == "--write":
        REPORT.write_text(output)
    elif REPORT.read_text() != output:
        raise SystemExit("saloonphp/xml-wrangler feedback receipt changed")
    print(f"verified saloonphp/xml-wrangler: {lines['parser_source_lines_covered']} package lines, "
          f"{tuple_difference} native AFL++ tuples differ")


if __name__ == "__main__":
    main()
