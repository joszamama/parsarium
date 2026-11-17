#!/usr/bin/env python3
"""Reproduce zendframework/zend-json 3.1.2 decode routes on the valid JSON controls."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess

PROBE = Path(__file__).resolve().parent
ROOT = PROBE.parents[3]
IMAGE = "parsarium-lead/json-php-zendframework_zend_json:local"
PLATFORM = "linux/arm64"
RELEASE = "3.1.2"
REFERENCE = "e9ddb1192d93fe7fff846ac895249c39db75132b"
ARCHIVE_SHA256 = "c7f83996835481a6024b770aa30f1f89f9b9fb66e1566890de1a299c4d45206b"
LAMINAS_LOCK = ROOT / "projects/json/php/laminas_json/source-lock.json"
CONTROL_NAMES = ("nested-object.json", "nested-array.json")
DEFAULT = "Zend\\Json\\Json::decode"
BUILTIN = "Zend\\Json\\Json::decode with $useBuiltinEncoderDecoder = true"
LAMINAS = "Laminas\\Json\\Json::decode with $useBuiltinEncoderDecoder = true"
# Json::decode 47-49 and decodeViaPhpBuiltIn 290-294: cast, flag test, json_decode, JSON_ERROR_NONE return.
DELEGATION_LINES = {"src/Json.php": [47, 48, 49, 290, 292, 293, 294]}
# Json::decode 47, 48, 52: cast, flag test, return Decoder::decode.
ZEND_DISPATCH_LINES = [47, 48, 52]
DECODER = "src/Decoder.php"
DECODER_CLASS = {BUILTIN: "Zend\\Json\\Decoder", LAMINAS: "Laminas\\Json\\Decoder"}


def command(*args: str, cwd: Path = PROBE) -> str:
    result = subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True, timeout=900)
    return result.stdout.strip()


def unique_members(pairs: list) -> list:
    if len({key for key, _ in pairs}) != len(pairs):
        raise ValueError("duplicate key in control")
    return pairs


def tagged_scalar(value: object) -> dict:
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


def oracle(data: bytes) -> dict:
    # Members stay as ordered (key, value) tuples so empty {} and [] remain distinct below.
    def hook(pairs: list) -> object:
        return ObjectPairs(unique_members(pairs))

    class ObjectPairs(list):
        pass

    def convert(value: object) -> object:
        if isinstance(value, ObjectPairs):
            return {"type": "object", "members": [[key, convert(item)] for key, item in value]}
        if isinstance(value, list):
            return {"type": "array", "items": [convert(item) for item in value]}
        return tagged_scalar(value)

    return convert(json.loads(data.decode("utf-8"), object_pairs_hook=hook))


def main() -> None:
    command("docker", "build", "--quiet", "--platform", PLATFORM, "-t", IMAGE, ".")
    image_id = command("docker", "image", "inspect", "--format", "{{.Id}}", IMAGE)
    controls = [ROOT / "controls/json" / name for name in CONTROL_NAMES]
    report = json.loads(command(
        "docker", "run", "--rm", "--platform", PLATFORM, "--network", "none", "--read-only",
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "-v", f"{ROOT / 'controls/json'}:/input:ro", IMAGE,
        *(f"/input/{name}" for name in CONTROL_NAMES)))
    runs = {(run["control"], run["route"]): run for run in report["runs"]}
    if set(runs) != {(c, r) for c in CONTROL_NAMES for r in (DEFAULT, BUILTIN, LAMINAS)}:
        raise RuntimeError("all three routes did not decode both valid controls")
    expected = {path.name: oracle(path.read_bytes()) for path in controls}
    for (control, route), run in runs.items():
        if run["tree"] != expected[control]:
            raise RuntimeError(f"{control} via {route}: type-tagged tree differs from oracle")
        if not run["identical_to_json_decode"]:
            raise RuntimeError(f"{control} via {route}: result differs from json_decode")
    decoder_methods = report["decoder_methods"]
    if decoder_methods["Zend\\Json\\Decoder"] != decoder_methods["Laminas\\Json\\Decoder"]:
        raise RuntimeError("zend-json and laminas-json Decoder declare different methods")
    route_summary = {}
    for control in CONTROL_NAMES:
        default = runs[control, DEFAULT]
        if default["package_lines_executed"] != DELEGATION_LINES:
            raise RuntimeError(f"{control}: default route ran {default['package_lines_executed']}")
        builtin = runs[control, BUILTIN]
        if builtin["package_lines_executed"]["src/Json.php"] != ZEND_DISPATCH_LINES:
            raise RuntimeError(f"{control}: opt-in route did not dispatch to Decoder::decode")
        zend_methods = set(builtin["package_methods_executed"][DECODER])
        laminas_methods = set(runs[control, LAMINAS]["package_methods_executed"][DECODER])
        if zend_methods != laminas_methods or set(builtin["package_lines_executed"]) != {"src/Json.php", DECODER}:
            raise RuntimeError(f"{control}: zend-json Decoder ran {sorted(zend_methods)}, laminas {sorted(laminas_methods)}")
        route_summary[control] = {
            route: {name: len(lines) for name, lines in runs[control, route]["package_lines_executed"].items()}
            for route in (DEFAULT, BUILTIN, LAMINAS)}
    lock, = json.loads((PROBE / "composer.lock").read_text())["packages"]
    if (lock["version"], lock["source"]["reference"]) != (RELEASE, REFERENCE):
        raise RuntimeError("composer.lock differs from the pinned release")
    laminas = json.loads(LAMINAS_LOCK.read_text())["laminas/laminas-json"]
    if laminas["source_sha256"] not in (PROBE / "Dockerfile").read_text():
        raise RuntimeError("Dockerfile laminas-json archive differs from the verified project source lock")
    result = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "excluded_shared_laminas_decoder_family",
        "package": "zendframework/zend-json", "release": RELEASE, "license": "BSD-3-Clause",
        "license_evidence": f"https://github.com/zendframework/zend-json/blob/{REFERENCE}/LICENSE.md",
        "source_url": f"https://github.com/zendframework/zend-json/tree/{REFERENCE}",
        "documentation": f"https://github.com/zendframework/zend-json/blob/{REFERENCE}/docs/book/advanced.md#internal-encoderdecoder",
        "abandoned": "Packagist marks the package abandoned in favour of laminas/laminas-json",
        "api": "Zend\\Json\\Json::decode(string $encodedValue) over local JSON text; default route and the documented Json::$useBuiltinEncoderDecoder = true route",
        "composer_reference": REFERENCE,
        "composer_lock_sha256": sha256((PROBE / "composer.lock").read_bytes()).hexdigest(),
        "archive_url": f"https://codeload.github.com/zendframework/zend-json/legacy.zip/{REFERENCE}",
        "archive_sha256": ARCHIVE_SHA256,
        "installed_source_matches_archive": True,
        "successor_reference": {
            "package": "laminas/laminas-json", "release": laminas["release"],
            "composer_reference": laminas["composer_reference"], "archive_sha256": laminas["source_sha256"],
            "verified_project": "projects/json/php/laminas_json",
        },
        "popularity": {
            "metric": "Packagist total downloads", "value": 24719945,
            "source": "https://packagist.org/packages/zendframework/zend-json",
            "captured_at_utc": json.loads((ROOT / "data/php/json/registry-snapshot.json")
                                          .read_text())["captured_at_utc"],
            "snapshot": "data/php/json/registry-snapshot.json",
        },
        "image_id": image_id,
        "platform": PLATFORM,
        "php": report["php"], "xdebug": report["xdebug"], "toolchain": report["toolchain"],
        "probe_file_sha256": {name: sha256((PROBE / name).read_bytes()).hexdigest()
                              for name in ("Dockerfile", "composer.json", "composer.lock", "probe.php")},
        "control_sha256": {path.name: sha256(path.read_bytes()).hexdigest() for path in controls},
        "decoder_methods": decoder_methods,
        "route_line_counts": route_summary,
        "observed": list(runs.values()),
        "oracle": "Python json.loads with ordered, duplicate-checked members, independently type-tagged",
        "type_tagged_trees_match_oracle": True,
        "default_route": "Json::decode lines 47-49 call decodeViaPhpBuiltIn, which runs json_decode and returns on JSON_ERROR_NONE (lines 290-294). Zero Decoder.php lines run on both controls, so the default route shares the verified ext/json family (json/php/stdlib_json_decode).",
        "opt_in_route": "With the documented Json::$useBuiltinEncoderDecoder = true, Json::decode calls Decoder::decode (line 52), and the package's own PHP lexer and recursive-descent parser in Decoder.php decode both controls.",
        "source_reason": "The opt-in Decoder.php is the predecessor of the laminas/laminas-json 3.8.0 Decoder already verified as json/php/laminas_json. After renaming the Zend\\ namespace to Laminas\\, the two files declare the same nine methods. The only differences are coding-standard rewrites: use function imports, public const, switch to match, == to ===, and dropped parentheses on return. On both controls the two decoders run the same methods, produce identical type-tagged trees, and differ by at most a few executed lines in __construct and getNextToken, where match replaces switch.",
        "parser_family": "Laminas/Zend Json Decoder pure-PHP parser (zend-json lineage), already counted as json/php/laminas_json; the default route is PHP ext/json json_decode",
        "docker_source_coverage": "run; default route 0 Decoder.php lines, opt-in route runs the same Decoder methods as laminas-json 3.8.0 on both controls",
        "afl_feedback": "not_run: the only package-owned parser is the Zend/Laminas Decoder lineage already bridged as json/php/laminas_json; a zend-json bridge would duplicate that family, and a default-route bridge would instrument a json_decode wrapper",
        "adapter": "lead-probes/php/json/zendframework_zend_json/probe.php",
    }
    destination = ROOT / "data/php/json/zendframework-zend-json-lead-check.json"
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"Default route delegates to json_decode; opt-in route matches laminas-json Decoder -> {destination}")


if __name__ == "__main__":
    main()
