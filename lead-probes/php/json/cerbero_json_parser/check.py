#!/usr/bin/env python3
"""Reproduce the cerbero/json-parser 1.1.1 lead check: own lazy parser path, no parser feedback differential."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

PROBE = Path(__file__).resolve().parent
ROOT = PROBE.parents[3]
IMAGE = "parsarium-lead/json-php-cerbero_json_parser:local"
AFL_IMAGE = "parsarium-lead-afl/json-php-cerbero_json_parser:local"
PLATFORM = "linux/arm64"
PACKAGE = "cerbero/json-parser"
RELEASE = "1.1.1"
REFERENCE = "02af3cd5396b50b05d287b6e6964bc5c42d40e8a"
ARCHIVE_SHA256 = "4c720bc106777d26e85c4fd32d53dda82cab22baf9c2526b4e1d0f068ad6df65"
AFL_PACKAGE = "4.33c-1.1ubuntu1"
CONTROL_NAMES = ("nested-object.json", "nested-array.json")
REPEATS = 2
# Packagist package API total downloads, read again after the registry snapshot.
RECHECK = {"value": 828834, "captured_at_utc": "2026-11-17T14:19:42Z",
           "source": "https://packagist.org/packages/cerbero/json-parser.json"}
PROBE_FILES = ("Dockerfile", "Dockerfile.afl", "afl_trace", "composer.json", "composer.lock",
               "harness.php", "probe.php", "call-trace.php")


def command(*args: str, cwd: Path = PROBE, env: dict | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True,
                            timeout=1800, env=env)
    return result.stdout.strip()


def sandbox(*mounts: str) -> list[str]:
    volumes = [part for mount in mounts for part in ("-v", mount)]
    return ["docker", "run", "--rm", "--platform", PLATFORM, "--network", "none", "--read-only",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", *volumes]


def unique_members(pairs: list) -> list:
    if len({key for key, _ in pairs}) != len(pairs):
        raise ValueError("duplicate key in control")
    return pairs


def oracle(data: bytes) -> dict:
    # Ordered members keep empty {} and [] distinct; integers and floats stay distinct.
    class ObjectPairs(list):
        pass

    def convert(value: object) -> dict:
        if isinstance(value, ObjectPairs):
            return {"type": "object", "members": [[key, convert(item)] for key, item in value]}
        if isinstance(value, list):
            return {"type": "array", "items": [convert(item) for item in value]}
        if value is None:
            return {"type": "null"}
        if isinstance(value, bool):
            return {"type": "boolean", "value": value}
        if isinstance(value, int):
            return {"type": "integer", "value": str(value)}
        if isinstance(value, float):
            return {"type": "float", "value": value}
        if isinstance(value, str):
            return {"type": "string", "value": value}
        raise TypeError(type(value).__name__)

    return convert(json.loads(data.decode("utf-8"),
                              object_pairs_hook=lambda pairs: ObjectPairs(unique_members(pairs))))


def afl_bucket(count: int) -> int:
    """AFL++ hit-count class for a map byte."""
    for bucket, limit in ((1, 1), (2, 2), (4, 3), (8, 7), (16, 15), (32, 31), (64, 127)):
        if count <= limit:
            return bucket
    return 128


def bridge(control: Path, work: Path, name: str, function: str) -> tuple[set, set]:
    """Run the parser-line tracer and afl-showmap over the proxy; return (features, map tuples)."""
    common = [*sandbox(f"{control}:/input/case:ro", f"{work}:/coverage"),
              "-e", f"PARSARIUM_PARSE_FUNCTION={function}"]
    command(*common, "--entrypoint", "/bin/sh", AFL_IMAGE,
            "/work/afl_trace", "/input/case", f"/coverage/{name}.features")
    command(*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap", AFL_IMAGE,
            "-m", "none", "-t", "30000", "-o", f"/coverage/{name}.map", "--",
            "/work/afl_proxy", "/input/case")
    features = set((work / f"{name}.features").read_text().splitlines()) - {""}
    tuples = set((work / f"{name}.map").read_text().splitlines()) - {""}
    return features, tuples


def calls(control: Path, function: str) -> dict:
    return json.loads(command(
        *sandbox(f"{control}:/input/case:ro"), "--entrypoint", "php", IMAGE,
        "-d", "xdebug.mode=trace", "-d", "xdebug.use_compression=0",
        "/work/call-trace.php", "/input/case", function))


def ids(tuples: set) -> set:
    return {item.split(":", 1)[0] for item in tuples}


def main() -> None:
    lock, = json.loads((PROBE / "composer.lock").read_text())["packages"]
    if (lock["name"], lock["version"], lock["source"]["reference"], lock["license"]) != \
            (PACKAGE, RELEASE, REFERENCE, ["MIT"]):
        raise RuntimeError("composer.lock differs from the pinned release")
    command("docker", "build", "--quiet", "--platform", PLATFORM, "-t", IMAGE, ".")
    command("docker", "build", "--quiet", "--platform", PLATFORM, "-t", AFL_IMAGE,
            "-f", str(PROBE / "Dockerfile.afl"), ".", cwd=ROOT)
    image_id = command("docker", "image", "inspect", "--format", "{{.Id}}", IMAGE)
    afl_image_id = command("docker", "image", "inspect", "--format", "{{.Id}}", AFL_IMAGE)
    afl_version = command("docker", "run", "--rm", "--platform", PLATFORM, "--entrypoint",
                          "dpkg-query", AFL_IMAGE, "-W", "-f=${Version}", "afl++")
    if afl_version != AFL_PACKAGE:
        raise RuntimeError(f"AFL++ package changed: {afl_version}")
    controls = [ROOT / "controls/json" / name for name in CONTROL_NAMES]

    observed, lines, runtime = [], {}, {}
    for path in controls:
        runs = [json.loads(command(*sandbox(f"{path}:/input/control:ro"), IMAGE))
                for _ in range(REPEATS)]
        first = runs[0]
        runtime = {key: first[key] for key in ("php", "xdebug", "toolchain")}
        if any(run != first for run in runs[1:]):
            raise RuntimeError(f"{path.name}: repeated probe changed tree or source lines")
        if first["tree"] != oracle(path.read_bytes()):
            raise RuntimeError(f"{path.name}: type-tagged tree differs from oracle")
        if not (first["file_source_tree_identical"] and first["stream_source_tree_identical"]):
            raise RuntimeError(f"{path.name}: file or stream source tree differs from string source")
        decoder = first["decoder"]
        if decoder["lazy_compound_inputs"] or not decoder["lazy_tree_identical"]:
            raise RuntimeError(f"{path.name}: lazy mode handed a compound value to json_decode")
        if not decoder["eager_compound_inputs"]:
            raise RuntimeError(f"{path.name}: eager mode no longer delegates subtrees; review the family note")
        lines[path.name] = {(name, line) for name, executed in first["package_lines_executed"].items()
                            for line in executed}
        observed.append({"control": path.name, "control_sha256": first["control_sha256"],
                         "tree": first["tree"], "decoder": decoder,
                         "package_lines_by_file": {name: len(executed) for name, executed
                                                   in first["package_lines_executed"].items()},
                         "package_lines_covered": len(lines[path.name])})
    first_name, second_name = CONTROL_NAMES

    with tempfile.TemporaryDirectory(prefix="parsarium-cerbero-lead-") as temporary:
        work = Path(temporary)
        maps = {}
        for path in controls:
            for function, label in (("parsarium_parse", "parse"), ("parsarium_no_parse", "no_parse")):
                results = [bridge(path, work, f"{path.stem}-{label}-{repeat}", function)
                           for repeat in range(REPEATS)]
                if any(result != results[0] for result in results[1:]):
                    raise RuntimeError(f"{path.name} {label}: repeated bridge probe changed")
                maps[path.name, label] = results[0]
    for name in CONTROL_NAMES:
        features, _ = maps[name, "parse"]
        prefix = "/work/vendor/cerbero/json-parser/"
        as_lines = {(item.removeprefix(prefix).rsplit(":", 1)[0], int(item.rsplit(":", 1)[1]))
                    for item in features}
        if not features or not as_lines <= lines[name]:
            raise RuntimeError(f"{name}: bridge features are not package lines seen by the probe")
        if maps[name, "no_parse"][0]:
            raise RuntimeError(f"{name}: no-parse baseline executed package lines")
    (first_features, first_tuples), (second_features, second_tuples) = \
        maps[first_name, "parse"], maps[second_name, "parse"]
    baseline = maps[first_name, "no_parse"][1]
    if maps[second_name, "no_parse"][1] != baseline:
        raise RuntimeError("no-parse baselines differ between controls")
    parser_first, parser_second = ids(first_tuples) - ids(baseline), ids(second_tuples) - ids(baseline)
    feature_difference = len(first_features ^ second_features)
    tuple_difference = len(ids(first_tuples) ^ ids(second_tuples))
    if feature_difference or tuple_difference:
        raise RuntimeError("parser-line bridge now separates the valid controls; review the lead decision")

    counts = {}
    for path in controls:
        for function in ("parsarium_parse", "parsarium_no_parse"):
            results = [calls(path, function) for _ in range(REPEATS)]
            if any(result != results[0] for result in results[1:]):
                raise RuntimeError(f"{path.name} {function}: repeated call trace changed")
            counts[path.name, function] = results[0]
    first_calls, second_calls = counts[first_name, "parsarium_parse"], counts[second_name, "parsarium_parse"]
    bucketed = lambda sites: {(site, afl_bucket(count)) for site, count in sites.items()}
    call_trace = {
        "kind": "Xdebug function trace, calls made from package source lines (call-site line > callee), AFL++ hit-count classes",
        "adapter": "lead-probes/php/json/cerbero_json_parser/call-trace.php",
        "repeats_per_control": REPEATS, "repeats_identical": True,
        "first_call_sites": len(first_calls), "second_call_sites": len(second_calls),
        "call_site_id_difference": len(set(first_calls) ^ set(second_calls)),
        "bucketed_call_site_difference": len(bucketed(first_calls) ^ bucketed(second_calls)),
        "first_total_calls": sum(first_calls.values()), "second_total_calls": sum(second_calls.values()),
        "no_parse_call_sites": {name: len(counts[name, "parsarium_no_parse"]) for name in CONTROL_NAMES},
        "note": "Same call-site set on both controls; only hit counts (input volume) differ. Not wired to an AFL++ map and not a repository feedback kind.",
    }
    if any(call_trace["no_parse_call_sites"].values()):
        raise RuntimeError("no-parse baseline made package calls")

    snapshot = json.loads((ROOT / "data/php/json/registry-snapshot.json").read_text())
    downloads = {hit["downloads"] for query in snapshot["search"] for hit in query["hits"]
                 if hit["name"] == PACKAGE}
    value, = downloads
    result = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "blocked_no_parser_feedback_differential",
        "package": PACKAGE, "release": RELEASE, "license": "MIT",
        "license_evidence": f"https://github.com/cerbero90/json-parser/blob/{REFERENCE}/LICENSE.md",
        "source_url": f"https://github.com/cerbero90/json-parser/tree/{REFERENCE}",
        "documentation": f"https://github.com/cerbero90/json-parser/blob/{REFERENCE}/README.md",
        "release_published_utc": "2025-01-17T18:41:04+00:00",
        "api": "Cerbero\\JsonParser\\JsonParser::parse(string|filename|resource)->lazy() iterated with foreach; nested values are Cerbero\\JsonParser\\Tokens\\Parser instances iterated the same way (README: Sources, Lazy pointers)",
        "compound_kind_source": "public Tokens\\Parser::lazyLoad()->current() before iteration yields the package Lexer's own CompoundBegin token ('{' or '['); not described in the README. Member key types (string keys, 0..n-1 indexes) cross-check every non-empty compound.",
        "composer_reference": REFERENCE,
        "composer_lock_sha256": sha256((PROBE / "composer.lock").read_bytes()).hexdigest(),
        "archive_url": f"https://codeload.github.com/cerbero90/json-parser/legacy.zip/{REFERENCE}",
        "archive_sha256": ARCHIVE_SHA256,
        "installed_source_matches_archive": True,
        "popularity": {
            "metric": "Packagist total downloads", "value": value,
            "source": "https://packagist.org/packages/cerbero/json-parser",
            "captured_at_utc": snapshot["captured_at_utc"],
            "snapshot": "data/php/json/registry-snapshot.json",
            "recheck": RECHECK,
        },
        "image_id": image_id, "afl_image_id": afl_image_id, "platform": PLATFORM,
        **runtime,
        "probe_file_sha256": {name: sha256((PROBE / name).read_bytes()).hexdigest() for name in PROBE_FILES},
        "bridge_file_sha256": {name: sha256((ROOT / "fuzzing/afl-bridge" / name).read_bytes()).hexdigest()
                               for name in ("afl_proxy.c", "php_trace.php")},
        "control_sha256": {path.name: sha256(path.read_bytes()).hexdigest() for path in controls},
        "observed": observed,
        "oracle": "Python json.loads with ordered, duplicate-checked members, independently type-tagged",
        "type_tagged_trees_match_oracle": True,
        "file_and_stream_sources_match": True,
        "repeats_per_control": REPEATS,
        "parser_family": "cerbero/json-parser own byte Lexer and token-state Parser (Tokens/, ValueObjects/State.php, Tree.php) for structure in lazy() mode; each key and scalar token is decoded by its default JsonDecoder, i.e. ext/json json_decode on one token (shared scalar decoding with json/php/stdlib_json_decode). The eager default (no lazy pointers) hands whole top-level member values to json_decode, so nested values then belong to the ext/json family.",
        "docker_source_coverage": {
            "first_control": first_name, "first_lines_covered": len(lines[first_name]),
            "second_control": second_name, "second_lines_covered": len(lines[second_name]),
            "line_set_difference": len(lines[first_name] ^ lines[second_name]),
            "note": "Xdebug line sets under /work/vendor/cerbero/json-parser/ on the string source; they include class-file load lines.",
        },
        "afl_feedback": {
            "feedback_kind": "php_parser_source_lines_to_afl_bitmap",
            "afl_package": afl_version, "afl_map_size": 65536,
            "subject_prefix": "/work/vendor/cerbero/json-parser/",
            "repeats_per_case": REPEATS, "repeats_identical": True,
            "first_parser_features": len(first_features), "second_parser_features": len(second_features),
            "parser_feature_difference": feature_difference,
            "first_afl_tuples": len(first_tuples), "second_afl_tuples": len(second_tuples),
            "afl_tuple_difference": tuple_difference,
            "no_parse_baseline_features": {name: len(maps[name, "no_parse"][0]) for name in CONTROL_NAMES},
            "no_parse_baseline_tuples": {name: len(maps[name, "no_parse"][1]) for name in CONTROL_NAMES},
            "first_parser_only_tuples": len(parser_first), "second_parser_only_tuples": len(parser_second),
            "feature_note": "Bridge features are a subset of the probe lines: php_trace.php starts coverage after harness.php and the Composer autoloader are loaded.",
            "baseline_note": "PARSARIUM_PARSE_FUNCTION=parsarium_no_parse runs the same input checks without calling the package; its tuples are the instrumented proxy's own edges.",
            "mutation_campaign_run": False,
        },
        "call_trace_observation": call_trace,
        "blocker": "The repository's PHP parser-line AFL++ bridge executes the same package line set on both valid controls, so the AFL++ maps have identical tuple ids beyond the no-parse baseline. Xdebug 3.5 returns no branch or path data in this image, and Xdebug line coverage has no hit counts. A call-count bridge would separate the controls only by hit-count class, which is not a repository feedback kind.",
        "adapter": "lead-probes/php/json/cerbero_json_parser/harness.php",
    }
    destination = ROOT / "data/php/json/cerbero-json-parser-lead-check.json"
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"Both valid controls match the oracle; {len(lines[first_name])} package lines on each, "
          f"{feature_difference} parser features and {tuple_difference} AFL++ tuple ids differ -> {destination}")


if __name__ == "__main__":
    main()
