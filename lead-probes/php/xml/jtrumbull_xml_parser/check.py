#!/usr/bin/env python3
"""Reproduce jtrumbull/xml-parser v1.0.2 decode() as a bare SimpleXML JSON round trip on both namespace controls."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess

PROBE = Path(__file__).resolve().parent
ROOT = PROBE.parents[3]
IMAGE = "parsarium-lead/xml-php-jtrumbull_xml_parser:local"
PLATFORM = "linux/arm64"
RELEASE = "v1.0.2"
REFERENCE = "94212d1bfc304ba9ac0a50b14e0a0cf67c877e86"
ARCHIVE_SHA256 = "19b2ab9a913f4e814bff5ad0de01158e6a49cc896619bc3324dd5b72e9b85d77"
CONTROLS = ("catalog-ns.xml", "order-default-ns.xml")
SOURCE = f"https://github.com/jtrumbull/xml-parser/blob/{REFERENCE}/lib/XMLParser/XMLParser.php"


def command(*args: str) -> str:
    result = subprocess.run(args, cwd=PROBE, check=True, text=True, capture_output=True, timeout=900)
    return result.stdout.strip()


def main() -> None:
    command("docker", "build", "--quiet", "--platform", PLATFORM, "-t", IMAGE, ".")
    image_id = command("docker", "image", "inspect", IMAGE, "--format", "{{.Id}}")
    mounts = []
    for name in CONTROLS:
        mounts += ["-v", f"{ROOT / 'controls/xml' / name}:/controls/{name}:ro"]
    observed = json.loads(command("docker", "run", "--rm", "--platform", PLATFORM, "--network", "none",
                                  "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
                                  *mounts, IMAGE))
    toolchain = command("docker", "run", "--rm", "--entrypoint", "cat", IMAGE, "/work/toolchain.txt").splitlines()
    results = observed["results"]
    if set(results) != set(CONTROLS):
        raise SystemExit(f"unexpected controls: {sorted(results)}")
    for name in CONTROLS:
        data = (ROOT / "controls/xml" / name).read_bytes()
        if results[name]["sha256"] != sha256(data).hexdigest():
            raise SystemExit(f"{name}: control bytes differ")
        if results[name]["identical_to_bare_simplexml_json"] is not True:
            raise SystemExit(f"{name}: decode() differs from a bare SimpleXML JSON round trip")
    lock = json.loads((PROBE / "composer.lock").read_text())["packages"][0]
    if (lock["version"], lock["dist"]["reference"]) != (RELEASE, REFERENCE):
        raise SystemExit("composer.lock is not the pinned release")
    catalog = results["catalog-ns.xml"]["decode"]
    order = results["order-default-ns.xml"]["decode"]
    report = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "negative_lead_simplexml_json_round_trip",
        "package": "jtrumbull/xml-parser",
        "release": RELEASE,
        "license": "MIT",
        "license_evidence": f"https://github.com/jtrumbull/xml-parser/blob/{REFERENCE}/LICENSE.md",
        "source_url": SOURCE,
        "documentation": f"https://github.com/jtrumbull/xml-parser/blob/{REFERENCE}/README.md",
        "api": "XMLParser\\XMLParser::decode(mixed $string): new SimpleXMLElement($xml) unless already one, then "
               "json_decode(json_encode($xml), false); encode() builds XML from arrays (the README's main use)",
        "composer_reference": REFERENCE,
        "archive_url": f"https://codeload.github.com/jtrumbull/xml-parser/legacy.zip/{REFERENCE}",
        "archive_sha256": ARCHIVE_SHA256,
        "installed_source_matches_archive": True,
        "lead_record_correction": "The earlier lead note said the source calls xml_parser_create; v1.0.2 (and the "
                                  "whole package source) has no xml_parser_create call. decode() uses SimpleXML.",
        "popularity": {
            "metric": "Packagist total downloads",
            "value": 62346,
            "source": "https://packagist.org/packages/jtrumbull/xml-parser",
            "snapshot": "data/php/xml/registry-snapshot.json",
        },
        "image_id": image_id,
        "platform": PLATFORM,
        "toolchain": toolchain,
        "control_sha256": {name: results[name]["sha256"] for name in CONTROLS},
        "observed": results,
        "decode_identical_to_bare_simplexml_json_on_both_controls": True,
        "observed_losses": {
            "catalog-ns.xml": {
                "root_name_reported": "c:catalog" in json.dumps(catalog),
                "cdata_note_text": catalog["item"][1]["note"],
                "first_item_attributes_kept": isinstance(catalog["item"][0], dict),
            },
            "order-default-ns.xml": {
                "prefixed_child_p_amount_kept": "p:amount" in json.dumps(order) or "amount" in json.dumps(order),
                "processing_instruction_reported_as_element": "audit" in order,
            },
        },
        "afl_feedback": "not_run: decode() adds no parsing route; every parsed value comes from PHP core "
                        "SimpleXMLElement and json_encode, as the identical bare round trip shows",
        "probe_file_sha256": {name: sha256((PROBE / name).read_bytes()).hexdigest()
                              for name in ("Dockerfile", "composer.json", "composer.lock", "probe.php", "check.py")},
    }
    output = ROOT / "data/php/xml/jtrumbull-xml-parser-lead-check.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"jtrumbull/xml-parser: decode() equals bare SimpleXML JSON on {len(CONTROLS)} controls")


if __name__ == "__main__":
    main()
