#!/usr/bin/env python3
"""Reproduce valid-control and own-package feedback gates for five Go XML leads.

Each lead's test binary instruments only that lead's package (Go coverpkg blocks,
the same unit the Go AFL++ bridges map). Every lead/control pair runs twice in a
network-less container; the receipt records what the package returned, its
covered blocks per control, and the blocks that differ between the two valid
controls. No malformed input or fuzz campaign is run.
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

PROBE = Path(__file__).resolve().parent
ROOT = PROBE.parents[3]
IMAGE = "parsarium-lead/xml-go-wrapper-gates:local"
PLATFORM = "linux/arm64"
CONTROLS = ("controls/xml/catalog-ns.xml", "controls/xml/order-default-ns.xml")
GH = "github" + ".com/"
LEADS = {
    "goxml2json-decode": ("goxml2json.test", "TestGoxml2jsonDecode", GH + "basgys/goxml2json/"),
    "goxml2json-convert": ("goxml2json.test", "TestGoxml2jsonConvert", GH + "basgys/goxml2json/"),
    "simplexml-dom": ("simplexml-dom.test", "TestSimplexmlDom", GH + "VictorLowther/simplexml/dom/"),
    "go-xmldom": ("go-xmldom.test", "TestGoXmldom", GH + "subchen/go-xmldom/"),
    "xml2map": ("xml2map.test", "TestXml2map", GH + "sbabiv/xml2map/"),
    "quickxml": ("quickxml.test", "TestQuickxml", GH + "dgrr/quickxml/"),
}
SANDBOX = ["--network", "none", "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
           "--user", f"{os.getuid()}:{os.getgid()}", "--tmpfs", "/tmp:rw,nosuid,size=64m"]


def run(command: list[str], **kwargs) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True, **kwargs).stdout


def replay(binary: str, test: str, prefix: str, control: str, work: Path, label: str) -> tuple[object, set[str]]:
    output = run(["docker", "run", "--rm", "--platform", PLATFORM, *SANDBOX,
                  "-v", f"{ROOT / control}:/input/case:ro", "-v", f"{work}:/coverage",
                  "-e", "PARSARIUM_CASE=/input/case", "--entrypoint", f"/work/{binary}", IMAGE,
                  f"-test.run=^{test}$", "-test.v", f"-test.coverprofile=/coverage/{label}.cover"], timeout=120)
    observed, = [json.loads(line.removeprefix("OBSERVED_JSON:")) for line in output.splitlines()
                 if line.startswith("OBSERVED_JSON:")]
    blocks = set()
    for line in (work / f"{label}.cover").read_text().splitlines()[1:]:
        location, _, count = line.split()
        if count != "0" and location.startswith(prefix):
            blocks.add(location)
    return observed, blocks


def main() -> None:
    run(["docker", "build", "--quiet", "--platform", PLATFORM, "-t", IMAGE, str(PROBE)], timeout=900)
    image_id = run(["docker", "image", "inspect", "--format", "{{.Id}}", IMAGE]).strip()
    results = {}
    with tempfile.TemporaryDirectory(prefix="parsarium-go-xml-gates-") as temporary:
        work = Path(temporary)
        for name, (binary, test, prefix) in LEADS.items():
            runs = {}
            for control in CONTROLS:
                stem = Path(control).stem
                first = replay(binary, test, prefix, control, work, f"{name}-{stem}-1")
                second = replay(binary, test, prefix, control, work, f"{name}-{stem}-2")
                if first != second:
                    raise RuntimeError(f"{name}: repeated {control} replay changed")
                runs[control] = first
            (out_a, blocks_a), (out_b, blocks_b) = runs[CONTROLS[0]], runs[CONTROLS[1]]
            changed = sorted(blocks_a ^ blocks_b)
            results[name] = {"test": test, "package_prefix": prefix,
                             "observed": {control: runs[control][0] for control in CONTROLS},
                             "covered_blocks": {control: len(runs[control][1]) for control in CONTROLS},
                             "repeat_identical": True,
                             "own_block_difference": len(changed), "changed_blocks": changed}
            print(f"{name}: {len(blocks_a)} / {len(blocks_b)} own blocks, {len(changed)} differ")
    receipt = {"schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
               "probe": "lead-probes/go/xml/wrapper-gates", "image_id": image_id, "platform": PLATFORM,
               "go_image": "golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66",
               "control_sha256": {control: sha256((ROOT / control).read_bytes()).hexdigest() for control in CONTROLS},
               "probe_file_sha256": {name: sha256((PROBE / name).read_bytes()).hexdigest()
                                     for name in ("Dockerfile", "check.py", "go.mod", "go.sum", "probe_test.go")},
               "gate": "Own-package Go cover blocks (the unit mapped by the Go AFL++ bridges) must differ between the two fixed valid controls; encoding/xml blocks are not counted as the lead's own feedback.",
               "results": results}
    (ROOT / "data/go/xml/wrapper-gates-check.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
