"""Audit container harnesses against third-party and standard API inventories."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def receipt_verified(path: Path, manifest: dict) -> bool:
    verification_path = path.parent / "verification.json"
    if not verification_path.exists():
        return False
    result = json.loads(verification_path.read_text())
    current_files = {str(file.relative_to(path.parent)): sha256(file.read_bytes()).hexdigest()
                     for file in sorted(path.parent.rglob("*"))
                     if file.is_file() and file.name != "verification.json"
                     and "target" not in file.relative_to(path.parent).parts}
    if (result.get("pass") is not True or result.get("fuzz_engine_smoke_pass") is not True
            or result.get("kind", "third_party") != manifest.get("kind", "third_party")
            or (manifest.get("kind") == "standard"
                and (result.get("api") != manifest["api"]
                     or result.get("runtime") != manifest["runtime"]))
            or result.get("manifest") != str(path.relative_to(ROOT))
            or result.get("source_sha256") != manifest["source_sha256"]
            or result.get("platform") != manifest["platform"]
            or not result.get("image_id", "").startswith("sha256:")
            or not result.get("toolchain")
            or result.get("output") != manifest["expected_output"]
            or result.get("parser_source_files", 0) <= 0
            or result.get("parser_source_lines_covered", 0) <= 0
            or ("format_specific_coverage_file_suffix" in manifest
                and result.get("format_specific_source_lines_covered", 0) <= 0)
            or ("underlying_coverage_subject_prefix" in manifest
                and result.get("underlying_source_lines_covered", 0) <= 0)
            or result.get("control_sha256") != manifest["control_sha256"]
            or result.get("project_file_sha256") != current_files):
        raise ValueError(f"unverified project result: {verification_path}")
    return True


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("--write", action="store_true")
    cli.add_argument("--check", action="store_true")
    args = cli.parse_args()
    if args.write and args.check:
        cli.error("choose --write or --check")

    catalog = {}
    for path in sorted((ROOT / "data").glob("*/*/parsers.json")):
        ecosystem, format_name = path.relative_to(ROOT / "data").parts[:2]
        for parser in json.loads(path.read_text()):
            key = (format_name, ecosystem, parser["name"])
            if key in catalog:
                raise ValueError(f"duplicate catalog path: {key}")
            catalog[key] = parser

    standard_by_cell = {}
    standard_catalog = {}
    for path in sorted((ROOT / "data").glob("*/*/standard.json")):
        ecosystem, format_name = path.relative_to(ROOT / "data").parts[:2]
        entries = json.loads(path.read_text())["verified_apis"]
        standard_by_cell[(format_name, ecosystem)] = len(entries)
        for entry in entries:
            identifier = entry.get("api") or entry.get("name") or entry.get("input_api")
            key = (format_name, ecosystem, identifier)
            if key in standard_catalog:
                raise ValueError(f"duplicate standard API path: {key}")
            standard_catalog[key] = entry
    if set(standard_by_cell) != {key[:2] for key in catalog}:
        raise ValueError("standard API inventory does not cover the catalog matrix")

    completed = set()
    staged = set()
    standard_completed = set()
    standard_staged = set()
    for path in sorted((ROOT / "projects").glob("*/*/*/manifest.json")):
        parts = path.relative_to(ROOT / "projects").parts
        manifest = json.loads(path.read_text())
        if manifest.get("kind") == "standard":
            key = (manifest["format"], manifest["ecosystem"], manifest["api"])
            if parts[0:2] != key[0:2] or key not in standard_catalog:
                raise ValueError(f"standard project does not match inventory: {path}")
            if key in standard_completed or key in standard_staged:
                raise ValueError(f"duplicate standard project: {key}")
            entry = standard_catalog[key]
            if (entry["runtime"] != manifest["runtime"]
                    or entry["control"] != manifest["control"]
                    or entry["expected"] != manifest["expected_output"]):
                raise ValueError(f"standard API evidence mismatch: {path}")
            lock = json.loads((path.parent / manifest["runtime_lock"]).read_text())
            if lock != {"runtime": manifest["runtime"],
                        "base_image": manifest["base_image"],
                        "source_sha256": manifest["source_sha256"]}:
                raise ValueError(f"runtime lock mismatch: {path}")
            if sha256((ROOT / manifest["control"]).read_bytes()).hexdigest() != manifest["control_sha256"]:
                raise ValueError(f"standard control hash mismatch: {path}")
            dockerfile = path.parent / "Dockerfile"
            if not dockerfile.is_file() or not (path.parent / manifest["harness"]).is_file():
                raise ValueError(f"missing standard Dockerfile or harness: {path}")
            docker_text = dockerfile.read_text()
            if any(manifest[field] not in docker_text
                   for field in ("base_image", "source_sha256", "fuzz_engine_sha256")):
                raise ValueError(f"standard Dockerfile pin mismatch: {path}")
            (standard_completed if receipt_verified(path, manifest) else standard_staged).add(key)
            continue
        if manifest.get("kind", "third_party") != "third_party":
            raise ValueError(f"unknown project kind: {path}")
        key = (manifest["format"], manifest["ecosystem"], manifest["package"])
        if parts[0:2] != key[0:2] or key not in catalog:
            raise ValueError(f"project does not match catalog: {path}")
        if key in completed or key in staged:
            raise ValueError(f"duplicate project: {key}")
        parser = catalog[key]
        if "expected_output" in parser:
            expected = parser["expected_output"]
        else:
            legacy = json.loads((ROOT / manifest["catalog_parser"]).with_name("verification.json").read_text())
            records = legacy.get("third_party", legacy.get("results", []))
            record, = [item for item in records if item["package"] == manifest["package"]]
            if record["pass"] is not True or record["version"] != manifest["release"]:
                raise ValueError(f"legacy verification mismatch: {path}")
            expected = record["output"]
        if manifest["release"] != parser["version"] or manifest["expected_output"] != expected:
            raise ValueError(f"release or output mismatch: {path}")
        control = ROOT / manifest["control"]
        if sha256(control.read_bytes()).hexdigest() != manifest["control_sha256"]:
            raise ValueError(f"control hash mismatch: {path}")
        lock_path = ROOT / manifest["source_lock"]
        if lock_path.suffix == ".json":
            source = json.loads(lock_path.read_text())[manifest["package"]]
            if source["release"] != manifest["release"] or source["source_sha256"] != manifest["source_sha256"]:
                raise ValueError(f"source lock mismatch: {path}")
            if "go_module_sum" in source and (f"{manifest['package']} {manifest['release']} "
                    f"{source['go_module_sum']}") not in (path.parent / "go.sum").read_text():
                raise ValueError(f"Go module sum mismatch: {path}")
            if "npm_integrity" in source:
                npm_lock = json.loads((path.parent / "package-lock.json").read_text())
                npm_package = npm_lock["packages"][f"node_modules/{manifest['package']}"]
                if (npm_package["version"] != manifest["release"]
                        or npm_package["integrity"] != source["npm_integrity"]):
                    raise ValueError(f"npm integrity mismatch: {path}")
                if (manifest.get("fuzz_engine") == "Jazzer.js"
                        and npm_lock["packages"]["node_modules/@jazzer.js/core"]["version"]
                        != manifest["fuzz_engine_release"]):
                    raise ValueError(f"Jazzer.js release mismatch: {path}")
            if "composer_reference" in source:
                composer_lock = json.loads((path.parent / "composer.lock").read_text())
                composer_package, = [item for item in composer_lock["packages"]
                                     if item["name"] == manifest["package"]]
                if (composer_package["version"] != manifest["release"]
                        or composer_package["source"]["reference"] != source["composer_reference"]):
                    raise ValueError(f"Composer source mismatch: {path}")
                if manifest.get("fuzz_engine") == "nikic/php-fuzzer":
                    engine, = [item for item in composer_lock["packages"]
                               if item["name"] == "nikic/php-fuzzer"]
                    if engine["version"] != manifest["fuzz_engine_release"]:
                        raise ValueError(f"PHP fuzzer release mismatch: {path}")
        else:
            lock = lock_path.read_text()
            if f"{manifest['package']}=={manifest['release']}" not in lock or manifest["source_sha256"] not in lock:
                raise ValueError(f"source lock mismatch: {path}")
        dockerfile = path.parent / "Dockerfile"
        if not dockerfile.is_file() or not (path.parent / manifest["harness"]).is_file():
            raise ValueError(f"missing Dockerfile or harness: {path}")
        docker_text = dockerfile.read_text()
        for field in ("base_image", "source_sha256", "fuzz_engine_sha256"):
            if field in manifest and manifest[field] not in docker_text:
                raise ValueError(f"Dockerfile does not pin {field}: {path}")
        for dependency in manifest.get("dependencies", []):
            if (lock_path.suffix == ".json"
                    or f"{dependency['package']}=={dependency['release']}" not in lock
                    or dependency["sha256"] not in lock
                    or dependency["sha256"] not in docker_text):
                raise ValueError(f"dependency pin mismatch: {path}")
        (completed if receipt_verified(path, manifest) else staged).add(key)

    cells = []
    for format_name, ecosystem in sorted({key[:2] for key in catalog}):
        keys = {key for key in catalog if key[:2] == (format_name, ecosystem)}
        standard_keys = {key for key in standard_catalog if key[:2] == (format_name, ecosystem)}
        standard_count = standard_by_cell[(format_name, ecosystem)]
        cells.append({"format": format_name, "ecosystem": ecosystem,
                      "catalog_paths": len(keys), "containerized_verified": len(keys & completed),
                      "staged": len(keys & staged), "pending": len(keys - completed - staged),
                      "standard_api_paths": standard_count,
                      "standard_containerized_verified": len(standard_keys & standard_completed),
                      "standard_staged": len(standard_keys & standard_staged),
                      "standard_pending": len(standard_keys - standard_completed - standard_staged)})
    standard_total = sum(standard_by_cell.values())
    report = {"schema_version": 2, "catalog_paths": len(catalog),
              "containerized_verified": len(completed), "staged": len(staged),
              "pending": len(catalog) - len(completed) - len(staged),
              "standard_api_paths": standard_total,
              "standard_containerized_verified": len(standard_completed),
              "standard_staged": len(standard_staged),
              "standard_pending": standard_total - len(standard_completed) - len(standard_staged),
              "cells": cells}
    output = ROOT / "data/projects-coverage.json"
    serialized = json.dumps(report, indent=2) + "\n"
    if args.write:
        output.write_text(serialized)
    if args.check and output.read_text() != serialized:
        raise ValueError("data/projects-coverage.json is stale; run --write")
    print(f"{len(completed)}/{len(catalog)} containerized parser paths verified; "
          f"{len(staged)} staged; {report['pending']} pending; "
          f"{len(standard_completed)}/{standard_total} standard API paths covered")


if __name__ == "__main__":
    main()
