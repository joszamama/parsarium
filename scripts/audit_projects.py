"""Audit container-harness coverage against every verified third-party parser path."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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

    completed = set()
    staged = set()
    for path in sorted((ROOT / "projects").glob("*/*/*/manifest.json")):
        parts = path.relative_to(ROOT / "projects").parts
        manifest = json.loads(path.read_text())
        key = (manifest["format"], manifest["ecosystem"], manifest["package"])
        if parts[0:2] != key[0:2] or key not in catalog:
            raise ValueError(f"project does not match catalog: {path}")
        if key in completed or key in staged:
            raise ValueError(f"duplicate project: {key}")
        parser = catalog[key]
        if manifest["release"] != parser["version"] or manifest["expected_output"] != parser["expected_output"]:
            raise ValueError(f"release or output mismatch: {path}")
        control = ROOT / manifest["control"]
        if sha256(control.read_bytes()).hexdigest() != manifest["control_sha256"]:
            raise ValueError(f"control hash mismatch: {path}")
        source = json.loads((ROOT / manifest["source_lock"]).read_text())[manifest["package"]]
        if source["release"] != manifest["release"] or source["source_sha256"] != manifest["source_sha256"]:
            raise ValueError(f"source lock mismatch: {path}")
        if not (path.parent / "Dockerfile").is_file() or not (path.parent / manifest["harness"]).is_file():
            raise ValueError(f"missing Dockerfile or harness: {path}")
        verification_path = path.parent / "verification.json"
        if not verification_path.exists():
            staged.add(key)
            continue
        result = json.loads(verification_path.read_text())
        current_files = {file.name: sha256(file.read_bytes()).hexdigest()
                         for file in sorted(path.parent.iterdir())
                         if file.is_file() and file.name != "verification.json"}
        if (result.get("pass") is not True or result.get("fuzz_engine_smoke_pass") is not True
                or result.get("output") != manifest["expected_output"]
                or result.get("parser_source_lines_covered", 0) <= 0
                or result.get("control_sha256") != manifest["control_sha256"]
                or result.get("project_file_sha256") != current_files):
            raise ValueError(f"unverified project result: {verification_path}")
        completed.add(key)

    cells = []
    for format_name, ecosystem in sorted({key[:2] for key in catalog}):
        keys = {key for key in catalog if key[:2] == (format_name, ecosystem)}
        cells.append({"format": format_name, "ecosystem": ecosystem,
                      "catalog_paths": len(keys), "containerized_verified": len(keys & completed),
                      "staged": len(keys & staged), "pending": len(keys - completed - staged)})
    report = {"schema_version": 1, "catalog_paths": len(catalog),
              "containerized_verified": len(completed), "staged": len(staged),
              "pending": len(catalog) - len(completed) - len(staged), "cells": cells}
    output = ROOT / "data/projects-coverage.json"
    serialized = json.dumps(report, indent=2) + "\n"
    if args.write:
        output.write_text(serialized)
    if args.check and output.read_text() != serialized:
        raise ValueError("data/projects-coverage.json is stale; run --write")
    print(f"{len(completed)}/{len(catalog)} containerized parser paths verified; "
          f"{len(staged)} staged; {report['pending']} pending")


if __name__ == "__main__":
    main()
