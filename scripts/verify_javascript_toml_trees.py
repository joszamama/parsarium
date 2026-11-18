"""Check the JavaScript TOML paths on both valid TOML controls: the typed tree each verified
image prints from its parser's returned values must equal the committed expected tree, the
project's pinned copy, and the typed tree Python's tomllib (an independent parser) gives
for the same bytes."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile
import tomllib

from run_case import ROOT, project_for
from verify_javascript_toml_feedback import SLUGS, run, sandbox

sys.path.insert(0, str(ROOT / "controls/toml"))
from check_controls import canonical, typed  # noqa: E402


API = {
    "smol_toml": "parse(text, { integersAsBigInt: true }) after TextDecoder('utf-8', {fatal: true, ignoreBOM: true})",
    "toml_eslint_parser": "parseTOML(text, { tomlVersion: '1.0.0' }) after TextDecoder('utf-8', {fatal: true, ignoreBOM: true}); typed tree from the returned syntax tree",
    "ltd_j_toml": "TOML.parse[1.0](text, { joiner: '\\n', bigint: true }) after TextDecoder('utf-8', {fatal: true, ignoreBOM: true})",
    "decimalturn_toml_patch": "parse(text, { integersAsBigInt: true }) after TextDecoder('utf-8', {fatal: true, ignoreBOM: true})",
    "effected_toml": "TomlVisitor.visit(text) collected with Effect.runSync(Stream.runCollect(...)) after TextDecoder('utf-8', {fatal: true, ignoreBOM: true}); typed tree from the returned events and value nodes",
    "sgarciac_bombadil": "new TomlReader().readToml(text, true) after TextDecoder('utf-8', {fatal: true, ignoreBOM: true}); typed tree from the returned type tags and values",
}


def report_name(package: str) -> str:
    """Receipt file name for a package; scoped npm names lose '@' and '/' becomes '-'."""
    return package.removeprefix("@").replace("/", "-")


def verify(slug: str) -> Path:
    project, manifest = project_for("toml", "javascript", slug)
    base = json.loads((project / "verification.json").read_text())
    pinned = json.loads((project / "expected-trees.json").read_text())
    results = []
    with tempfile.TemporaryDirectory(prefix="parsarium-toml-js-tree-") as temporary:
        work = Path(temporary)
        for key, expected_key in (("control", "expected_output"),
                                  ("differential_control", "differential_expected_output")):
            path = ROOT / manifest[key]
            data = path.read_bytes()
            digest = sha256(data).hexdigest()
            if digest != manifest[f"{key}_sha256"]:
                raise ValueError(f"control hash mismatch: {path}")
            committed = json.loads(path.with_name(path.name.replace(".toml", ".expected.json")).read_text())
            oracle = typed(tomllib.loads(data.decode("utf-8")))
            if not (oracle == committed == pinned[digest]["tree"] == manifest[expected_key]):
                raise RuntimeError(f"{path.name}: expected trees disagree")
            observed = json.loads(run([*sandbox(manifest, path, work), "--entrypoint", "node",
                                       base["image_id"], "/work/replay.js", "/input/case"]))
            if observed != committed:
                raise RuntimeError(f"{path.name}: {manifest['package']} typed tree differs: {observed}")
            results.append({"control": manifest[key], "control_sha256": digest,
                            "tree_sha256": sha256(canonical(committed).encode()).hexdigest(),
                            "tree_matches_expected": True, "tree_matches_tomllib": True})
            print(f"{slug}: {path.name} typed tree matches", flush=True)
    report = ROOT / f"data/javascript/toml/{report_name(manifest['package'])}-tree-verification.json"
    report.write_text(json.dumps({
        "schema_version": 1,
        "project": f"toml/javascript/{slug}",
        "package": manifest["package"], "version": manifest["release"],
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "base_image_id": base["image_id"],
        "api": API[slug],
        "oracle": "controls/toml/*.expected.json (hand-written from the TOML 1.0.0 specification) and "
                  "Python tomllib through controls/toml/check_controls.py typed(); the project's "
                  "expected-trees.json holds equal copies keyed by control SHA-256",
        "results": results, "pass": True}, indent=2, ensure_ascii=False) + "\n")
    return report


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("slug", nargs="?", choices=SLUGS)
    args = cli.parse_args()
    for slug in (args.slug,) if args.slug else SLUGS:
        verify(slug)


if __name__ == "__main__":
    main()
