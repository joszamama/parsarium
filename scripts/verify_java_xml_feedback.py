"""Check the Java XML AFL++ bridges: repeated control probes match and a second valid input differs."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


PROJECTS = ("xercesimpl", "jdk_documentbuilder")
CONTROL = "controls/xml/catalog-ns.xml"
DIFFERENTIAL = "controls/xml/order-default-ns.xml"
# Structure of controls/xml/order-default-ns.xml, read off the file by hand:
# default namespace, a prefixed element and attribute, character references,
# a comment and processing instruction (not reported), and xmlns="" undeclaring.
DIFFERENTIAL_EXPECTED = {
    "attributes": ["n=1", "{urn:parsarium:price}currency=EUR", "n=2", 'note=say "hi"'],
    "elements": ["{urn:parsarium:order}order", "{urn:parsarium:order}line",
                 "{urn:parsarium:order}sku", "{urn:parsarium:price}amount",
                 "{urn:parsarium:order}line", "plain", "leaf"],
    "max_depth": 4, "namespace_declarations": 3,
    "namespaces": ["urn:parsarium:order", "urn:parsarium:price"],
    "root": "{urn:parsarium:order}order", "text": ["A-7", "12.50 \u20ac"],
}
REPORT = ROOT / "data/java/xml/afl-feedback.json"


def run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])


def probe(manifest: dict, image: str, case: Path, work: Path, name: str) -> tuple[set, set]:
    common = ["docker", "run", "--rm", "--platform", manifest["platform"],
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
    relative = Path("xml/java") / slug
    _, manifest = project_for("xml", "java", slug)
    if manifest["control"] != CONTROL:
        raise ValueError(f"{relative}: unexpected control")
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    image = receipt["image_id"]
    classpath = next(arg.removeprefix("--cp=") for arg in manifest["fuzz_smoke_args"]
                     if arg.startswith("--cp="))
    with tempfile.TemporaryDirectory(prefix="parsarium-xml-java-") as temporary:
        work = Path(temporary)
        first = probe(manifest, image, ROOT / CONTROL, work, "first")
        repeat = probe(manifest, image, ROOT / CONTROL, work, "repeat")
        other = probe(manifest, image, ROOT / DIFFERENTIAL, work, "other")
        parsed = subprocess.run(
            ["docker", "run", "--rm", "--platform", manifest["platform"], "--network", "none",
             "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
             "--user", f"{os.getuid()}:{os.getgid()}", "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
             "-v", f"{ROOT / DIFFERENTIAL}:/input/case:ro", "--entrypoint", "java", image,
             "-Dstdout.encoding=UTF-8", "-cp", classpath, "GenericHarness",
             "/input/case"], capture_output=True, text=True, timeout=120, check=True)
        differential_output = json.loads(parsed.stdout.strip().splitlines()[-1])
    if differential_output != DIFFERENTIAL_EXPECTED:
        raise RuntimeError(f"{relative}: differential output changed: {differential_output}")
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
    return {"project": str(relative), "pass": True,
            "feedback_kind": receipt["feedback_kind"],
            "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
            "control": CONTROL,
            "control_sha256": sha256((ROOT / CONTROL).read_bytes()).hexdigest(),
            "differential": DIFFERENTIAL,
            "differential_sha256": sha256((ROOT / DIFFERENTIAL).read_bytes()).hexdigest(),
            "differential_output": differential_output,
            "repeated_control_identical": True,
            "control_parser_features": len(first[0]),
            "control_afl_tuples": len(first[1]),
            "differential_parser_features": len(other[0]),
            "differential_afl_tuples": len(other[1]),
            "parser_feature_difference": feature_difference,
            "afl_tuple_difference": tuple_difference}


def main() -> None:
    results = [check(slug) for slug in PROJECTS]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_default_namespace_order",
        "results": results}, indent=2) + "\n")


if __name__ == "__main__":
    main()
