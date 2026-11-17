"""Check Go XML AFL++ bridges: repeated control probes match and a second valid input differs."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


PROJECTS = ("github_com_beevik_etree", "github_com_antchfx_xmlquery", "github_com_clbanning_mxj",
            "github_com_beego_x2j", "stdlib_decoder")
CONTROL = "controls/xml/catalog-ns.xml"
DIFFERENTIAL = "controls/xml/order-default-ns.xml"
REPORT = ROOT / "data/go/xml/afl-feedback.json"


def run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])


def probe(manifest: dict, image: str, case: Path, work: Path, name: str,
          prefix: str | None = None) -> tuple[set, set]:
    # prefix replaces the overlay's PARSARIUM_SUBJECT_PREFIX, e.g. to map encoding/xml blocks.
    override = ["-e", f"PARSARIUM_SUBJECT_PREFIX={prefix}"] if prefix else []
    common = ["docker", "run", "--rm", "--platform", manifest["platform"], *override,
              "--network", "none", "--read-only", "--cap-drop", "ALL",
              "--security-opt", "no-new-privileges",
              "--user", f"{os.getuid()}:{os.getgid()}",
              "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
              "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]
    run([*common, "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
         image, "-m", "none", "-t", "10000", "-o", f"/coverage/{name}.map",
         "--", "/work/afl_proxy", "/input/case"])
    features = set((work / f"{name}.features").read_text().splitlines()) - {""}
    tuples = set((work / f"{name}.map").read_text().splitlines()) - {""}
    return features, tuples


def check(slug: str) -> dict:
    relative = Path("xml/go") / slug
    _, manifest = project_for("xml", "go", slug)
    if manifest["control"] != CONTROL:
        raise ValueError(f"{relative}: unexpected control")
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    image = receipt["image_id"]
    with tempfile.TemporaryDirectory(prefix="parsarium-xml-go-") as temporary:
        work = Path(temporary)
        first = probe(manifest, image, ROOT / CONTROL, work, "first")
        repeat = probe(manifest, image, ROOT / CONTROL, work, "repeat")
        other = probe(manifest, image, ROOT / DIFFERENTIAL, work, "other")
        underlying = manifest.get("afl_underlying_subject_prefix")
        if underlying:
            tokenizer = [probe(manifest, image, ROOT / case, work, f"tokenizer-{label}", underlying)
                         for label, case in (("first", CONTROL), ("repeat", CONTROL),
                                             ("other", DIFFERENTIAL))]
    if first != repeat:
        raise RuntimeError(f"{relative}: repeated control probe changed parser features or AFL++ map")
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len({item.split(":", 1)[0] for item in first[1]} ^
                           {item.split(":", 1)[0] for item in other[1]})
    if not feature_difference or not tuple_difference:
        raise RuntimeError(f"{relative}: differential input did not change parser feedback")
    print(f"{relative}: stable repeat; {feature_difference} parser features, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)
    extra = {}
    if underlying:
        if tokenizer[0] != tokenizer[1]:
            raise RuntimeError(f"{relative}: repeated {underlying} probe changed")
        if tokenizer[0][0] & first[0]:
            raise RuntimeError(f"{relative}: {underlying} features overlap package features")
        underlying_features = len(tokenizer[0][0] ^ tokenizer[2][0])
        underlying_tuples = len({item.split(":", 1)[0] for item in tokenizer[0][1]} ^
                                {item.split(":", 1)[0] for item in tokenizer[2][1]})
        if not underlying_features or not underlying_tuples:
            raise RuntimeError(f"{relative}: differential input did not change {underlying} feedback")
        print(f"{relative}: {underlying} stable repeat; {underlying_features} features, "
              f"{underlying_tuples} AFL++ tuples differ", flush=True)
        extra = {"underlying_subject_prefix": underlying,
                 "underlying_repeated_control_identical": True,
                 "underlying_control_features": len(tokenizer[0][0]),
                 "underlying_control_afl_tuples": len(tokenizer[0][1]),
                 "underlying_differential_features": len(tokenizer[2][0]),
                 "underlying_differential_afl_tuples": len(tokenizer[2][1]),
                 "underlying_feature_difference": underlying_features,
                 "underlying_afl_tuple_difference": underlying_tuples}
    return {"project": str(relative), "pass": True,
            "feedback_kind": receipt["feedback_kind"],
            "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
            "control": CONTROL,
            "control_sha256": sha256((ROOT / CONTROL).read_bytes()).hexdigest(),
            "differential": DIFFERENTIAL,
            "differential_sha256": sha256((ROOT / DIFFERENTIAL).read_bytes()).hexdigest(),
            "repeated_control_identical": True,
            "control_parser_features": len(first[0]),
            "control_afl_tuples": len(first[1]),
            "differential_parser_features": len(other[0]),
            "differential_afl_tuples": len(other[1]),
            "parser_feature_difference": feature_difference,
            "afl_tuple_difference": tuple_difference, **extra}


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("projects", nargs="*", choices=PROJECTS,
                     help="verify only these projects and retain existing other receipts")
    args = cli.parse_args()
    selected = args.projects or PROJECTS
    checked = {item["project"]: item for item in (check(slug) for slug in selected)}
    if args.projects and REPORT.exists():
        existing = json.loads(REPORT.read_text())
        for item in existing.get("results", []):
            if item["project"] not in checked:
                checked[item["project"]] = item
    results = [checked[f"xml/go/{slug}"] for slug in PROJECTS
               if f"xml/go/{slug}" in checked]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_default_namespace_order",
        "results": results}, indent=2) + "\n")


if __name__ == "__main__":
    main()
