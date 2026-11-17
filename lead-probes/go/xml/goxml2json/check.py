#!/usr/bin/env python3
"""Reproduce the valid-control namespace loss in goxml2json v1.1.0."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess

PROBE = Path(__file__).resolve().parent
ROOT = PROBE.parents[3]
MODULE = "github.com/basgys/goxml2json"
VERSION = "v1.1.0"
ZIP_SHA256 = "2f7b5f64b31f00193bf1a848d2aacf9d2a555f22076d52c31957c59d7a20ca77"
CONTROL_NAMES = ("catalog-ns.xml", "order-default-ns.xml")


def command(*args: str) -> str:
    result = subprocess.run(args, cwd=PROBE, check=True, text=True,
                            capture_output=True, timeout=120)
    return result.stdout.strip()


def main() -> None:
    source = json.loads(command("go", "mod", "download", "-json", f"{MODULE}@{VERSION}"))
    if source["Version"] != VERSION or sha256(Path(source["Zip"]).read_bytes()).hexdigest() != ZIP_SHA256:
        raise RuntimeError("pinned goxml2json archive differs from source lock")
    controls = [ROOT / "controls/xml" / name for name in CONTROL_NAMES]
    records = [json.loads(line) for line in command(
        "go", "run", "-mod=readonly", ".", *(str(path) for path in controls)
    ).splitlines()]
    by_name = {record["control"]: record["converted"] for record in records}
    if set(by_name) != set(CONTROL_NAMES):
        raise RuntimeError("both valid controls were not converted")
    catalog = by_name["catalog-ns.xml"]
    order = by_name["order-default-ns.xml"]
    if (set(catalog) != {"catalog"}
            or catalog["catalog"]["-c"] != "urn:parsarium:catalog"
            or catalog["catalog"]["item"][0]["-lang"] != "es"
            or set(order) != {"order"}
            or order["order"]["line"][0]["amount"] != "12.50 €"
            or order["order"]["line"][0]["-currency"] != "EUR"):
        raise RuntimeError("observed conversion changed; review the lead decision")
    result = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "unresolved_not_selected_shared_oracle_mismatch",
        "package": MODULE, "release": VERSION, "license": "MIT",
        "api": "xml2json.Convert(io.Reader) over local XML bytes",
        "api_reference": f"https://pkg.go.dev/{MODULE}@{VERSION}#Convert",
        "source_url": f"https://github.com/basgys/goxml2json/tree/{VERSION}",
        "module_zip_sha256": ZIP_SHA256,
        "module_sum": source["Sum"],
        "go_toolchain": command("go", "version"),
        "control_sha256": {path.name: sha256(path.read_bytes()).hexdigest()
                           for path in controls},
        "observed_conversion": by_name,
        "shared_oracle_mismatch": [
            {"control": "catalog-ns.xml", "field": "root expanded name",
             "required": "{urn:parsarium:catalog}catalog", "observed": "catalog"},
            {"control": "catalog-ns.xml", "field": "c:lang attribute expanded name",
             "required": "{urn:parsarium:catalog}lang", "observed": "-lang"},
            {"control": "order-default-ns.xml", "field": "p:amount expanded name",
             "required": "{urn:parsarium:price}amount", "observed": "amount"},
            {"control": "order-default-ns.xml", "field": "p:currency attribute expanded name",
             "required": "{urn:parsarium:price}currency", "observed": "-currency"},
        ],
        "source_reason": "decoder.go labels elements with se.Name.Local and attributes with a.Name.Local; Name.Space is discarded. Node.Children is a map keyed by those labels. The JSON output cannot identify which namespace an element or attribute name used.",
        "parser_family": "XML-to-JSON tree conversion over Go encoding/xml.Decoder.Token",
        "docker_source_coverage": "not_run_after_shared_oracle_failure",
        "afl_feedback": "not_run_after_shared_oracle_failure",
        "adapter": "lead-probes/go/xml/goxml2json/main.go",
    }
    destination = ROOT / "data/go/xml/goxml2json-lead-check.json"
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"Observed namespace loss on both valid controls: {destination}")


if __name__ == "__main__":
    main()
