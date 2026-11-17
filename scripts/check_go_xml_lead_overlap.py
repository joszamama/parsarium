#!/usr/bin/env python3
"""Measure source overlap between Go XML leads and the selected path (or runtime) they derive from.

Each module archive is fetched from proxy.golang.org and checked against a pinned
SHA-256 before use; Go's own encoding/xml comes from the local Go 1.27.1 toolchain
(its xml.go hash is pinned to the same file the Docker images verify). For each
pair, every non-test .go file of the candidate package is aligned with the file of
the same name in the reference package (difflib matching blocks over
right-stripped lines); the overlap is matched candidate lines / all candidate
lines. Byte-identical files are counted separately. Writes
data/go/xml/lead-overlap-check.json. Nothing here runs the packages.
"""

from datetime import datetime, timezone
import difflib
from hashlib import sha256
import io
import json
from pathlib import Path
import subprocess
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/go/xml/lead-overlap-check.json"
GH = "github" + ".com/"
STDLIB_XML_SHA256 = "41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb"
MODULES = {
    "clbanning/mxj@v1.8.4": "8947cf617bdd9efc62817c8ddb17bafe497f35abdf10a3c60f295e387f633f70",
    "clbanning/mxj/v2@v2.7.0": "4451f64589cac692c9caa68be16551d6391949379a5bceae5455070198dd0918",
    "moovweb/gokogiri@v0.0.0-20180713195410-a1a828153468": "d2c93190df9ceca2a8769288997a917f0b08b6b03151e851972aba5d40250a3b",
    "jbowtie/gokogiri@v0.0.0-20250107075044-de0f9d4877a5": "45180292b808afd8ee8521cd025497870e0efe50c786102b2763fdd8532eedd3",
    "beego/x2j@v0.0.0-20131220205130-a0352aadc542": "f9a32026b2107f3cc3610ac6b75c4c64818646a316c35e648c8811d4276a9993",
    "clbanning/x2j@v0.0.0-20191024224557-825249438eec": "747daafe80e4ac504626c01a1d28b1a64b785586975a47b50d62853a444b72a0",
    "vmware/govmomi@v0.56.2": "195de21afbe5a372c5afedcc59fef87cec96d07e9564cecf50e037fa31d079d4",
    "nbio/xml@v0.0.0-20260302224236-9f64bb3b5a9e": "d988bcc03e13b8e4a589dfb39e7d3d656c6eaf2be6de25342dffed732ac2be2a",
    "samuel-jimenez/xml@v0.2.4": "4dffaaca69b433a3b0b6d82215f07ece7d3e62d77b24b1c10a0e38ef1fa45fbf",
    "minio/xxml@v0.0.3": "eec7f98185f849ac85b798a4a7b2b1cbd5aea8ea360f563b47e715ee7fbb5c6d",
    "printesoi/xml-go@v1.0.1": "c60525ccd0acea8e57201079a2d71d7d90d3b3a942bce88357748bf124d4ac61",
    "antchfx/xmlquery@v1.5.2": "cdb7830a6e1e3f52c3d3a084b55b4bdf84f73b8073c582bca8f5f00d15a5f94c",
    "antchfx/xquery@v0.0.0-20180515051857-ad5b8c7a47b0": "9ddc9d830f2d6c7a22604035f0c621228ffa4ed6ff1f1d34655ee477c203c899",
    "go-forks/go-pkg-xmlx@v0.0.0-20151201012946-76f54ee73233": "8c48f5f6f488c7f79c8f22caedde724bcc77bcc97a9e2d8be5e39f956346fece",
    "mattn/go-pkg-xmlx@v0.0.0-20180208005205-db53493302d1": "25c32a09dd2ef7217670d5fc9659de7adc004d4c4741d36b2c72730311fc24b4",
    "beevik/etree@v1.0.1": "96056015b3a70b4352ad10936df06e593e9d50c62bcdc5a35745ef44cf298846",
    "beevik/etree@v1.8.1": "c0338bfc955c839a435fc49156536be7e39525455412940f12ef1e0a903ee706",
    "zhuxiujia/GoMybatis@v6.5.12+incompatible": "35da19f50a26d26c0d8a39140b9e95d6ce832e24a7c4b9f39febac1f9f584812",
}
STD = "encoding/xml (Go 1.27.1 runtime)"
# (lead, lead module, lead package dir) compared with (reference, module, dir); reference None = runtime.
PAIRS = [
    ("github.com/clbanning/mxj/v2", "clbanning/mxj/v2@v2.7.0", ".", "github.com/clbanning/mxj (selected)", "clbanning/mxj@v1.8.4", "."),
    ("github.com/jbowtie/gokogiri/xml", "jbowtie/gokogiri@v0.0.0-20250107075044-de0f9d4877a5", "xml", "github.com/moovweb/gokogiri/xml (selected)", "moovweb/gokogiri@v0.0.0-20180713195410-a1a828153468", "xml"),
    ("github.com/clbanning/x2j", "clbanning/x2j@v0.0.0-20191024224557-825249438eec", ".", "github.com/beego/x2j (selected)", "beego/x2j@v0.0.0-20131220205130-a0352aadc542", "."),
    ("github.com/vmware/govmomi/vim25/xml (selected)", "vmware/govmomi@v0.56.2", "vim25/xml", STD, None, None),
    ("github.com/nbio/xml", "nbio/xml@v0.0.0-20260302224236-9f64bb3b5a9e", ".", "github.com/vmware/govmomi/vim25/xml (selected)", "vmware/govmomi@v0.56.2", "vim25/xml"),
    ("github.com/nbio/xml", "nbio/xml@v0.0.0-20260302224236-9f64bb3b5a9e", ".", STD, None, None),
    ("github.com/samuel-jimenez/xml", "samuel-jimenez/xml@v0.2.4", ".", "github.com/vmware/govmomi/vim25/xml (selected)", "vmware/govmomi@v0.56.2", "vim25/xml"),
    ("github.com/samuel-jimenez/xml", "samuel-jimenez/xml@v0.2.4", ".", STD, None, None),
    ("github.com/minio/xxml", "minio/xxml@v0.0.3", ".", "github.com/vmware/govmomi/vim25/xml (selected)", "vmware/govmomi@v0.56.2", "vim25/xml"),
    ("github.com/minio/xxml", "minio/xxml@v0.0.3", ".", STD, None, None),
    ("github.com/printesoi/xml-go", "printesoi/xml-go@v1.0.1", ".", "github.com/vmware/govmomi/vim25/xml (selected)", "vmware/govmomi@v0.56.2", "vim25/xml"),
    ("github.com/printesoi/xml-go", "printesoi/xml-go@v1.0.1", ".", STD, None, None),
    ("github.com/antchfx/xquery/xml", "antchfx/xquery@v0.0.0-20180515051857-ad5b8c7a47b0", "xml", "github.com/antchfx/xmlquery (selected)", "antchfx/xmlquery@v1.5.2", "."),
    ("github.com/mattn/go-pkg-xmlx", "mattn/go-pkg-xmlx@v0.0.0-20180208005205-db53493302d1", ".", "github.com/go-forks/go-pkg-xmlx (selected)", "go-forks/go-pkg-xmlx@v0.0.0-20151201012946-76f54ee73233", "."),
    ("github.com/zhuxiujia/GoMybatis/lib/github.com/beevik/etree", "zhuxiujia/GoMybatis@v6.5.12+incompatible", "lib/github.com/beevik/etree", "github.com/beevik/etree v1.0.1 (older release of the selected path)", "beevik/etree@v1.0.1", "."),
    ("github.com/zhuxiujia/GoMybatis/lib/github.com/beevik/etree", "zhuxiujia/GoMybatis@v6.5.12+incompatible", "lib/github.com/beevik/etree", "github.com/beevik/etree v1.8.1 (selected release)", "beevik/etree@v1.8.1", "."),
]


def escape(path: str) -> str:
    return "".join("!" + c.lower() if c.isupper() else c for c in path)


def fetch(spec: str, cache: Path) -> tuple[Path, str]:
    module, version = spec.split("@")
    expected = MODULES[spec]
    data = urllib.request.urlopen(f"https://proxy.golang.org/{escape(GH + module)}/@v/{escape(version)}.zip",
                                  timeout=120).read()
    digest = sha256(data).hexdigest()
    if digest != expected:
        raise RuntimeError(f"{spec}: archive SHA-256 {digest} differs from pin {expected}")
    target = cache / spec.replace("/", "_")
    zipfile.ZipFile(io.BytesIO(data)).extractall(target)
    return target / GH / f"{module}@{version}", digest


def go_files(directory: Path) -> dict[str, Path]:
    return {path.name: path for path in sorted(directory.glob("*.go")) if not path.name.endswith("_test.go")}


def lines(path: Path) -> list[str]:
    return [line.rstrip() for line in path.read_text(errors="replace").splitlines()]


def compare(candidate: Path, reference: Path) -> dict:
    lead, base = go_files(candidate), go_files(reference)
    files, total, matched, identical = [], 0, 0, 0
    for name, path in lead.items():
        ours = lines(path)
        total += len(ours)
        same = name in base and path.read_bytes() == base[name].read_bytes()
        hit = (sum(block.size for block in difflib.SequenceMatcher(None, lines(base[name]), ours, autojunk=False)
                   .get_matching_blocks()) if name in base else 0)
        matched += hit
        identical += same
        files.append({"file": name, "lines": len(ours), "matching_lines": hit, "byte_identical": same})
    return {"candidate_files": len(lead), "reference_files": len(base), "byte_identical_files": identical,
            "candidate_lines": total, "matching_lines": matched, "overlap": round(matched / total, 4),
            "only_in_reference": sorted(set(base) - set(lead)), "files": files}


def main() -> None:
    goroot = Path(subprocess.run(["go", "env", "GOROOT"], check=True, capture_output=True, text=True).stdout.strip())
    std = goroot / "src/encoding/xml"
    if sha256((std / "xml.go").read_bytes()).hexdigest() != STDLIB_XML_SHA256:
        raise RuntimeError("local encoding/xml/xml.go differs from the pinned Go 1.27.1 source")
    with tempfile.TemporaryDirectory(prefix="parsarium-go-xml-overlap-") as temporary:
        cache, roots, digests = Path(temporary), {}, {}
        for spec in sorted({pair[1] for pair in PAIRS} | {pair[4] for pair in PAIRS if pair[4]}):
            roots[spec], digests[spec] = fetch(spec, cache)
        results = []
        for lead, spec, sub, reference, ref_spec, ref_sub in PAIRS:
            reference_dir = std if ref_spec is None else roots[ref_spec] / ref_sub
            result = compare(roots[spec] / sub, reference_dir)
            results.append({"lead": lead, "lead_archive": spec, "lead_package_dir": sub,
                            "reference": reference, "reference_archive": ref_spec or "go1.27.1 GOROOT/src",
                            "reference_package_dir": ref_sub or "encoding/xml", **result})
            print(f"{lead} vs {reference}: {result['matching_lines']}/{result['candidate_lines']} = "
                  f"{100 * result['overlap']:.1f}% ({result['byte_identical_files']} byte-identical files)")
    receipt = {"schema_version": 1, "checked_at_utc": datetime.now(timezone.utc).isoformat(),
               "script": "scripts/check_go_xml_lead_overlap.py",
               "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "method": "difflib matching blocks over right-stripped lines of same-named non-test .go files; overlap = matched candidate lines / candidate lines",
               "rule": "A lead whose parsing package overlaps a selected path's package by about 70% or more, or is a predecessor/successor path or byte-identical fork of it, is excluded as the same parser path; the standard-library comparison is reported for encoding/xml forks only, since encoding/xml is an unranked runtime API.",
               "archive_sha256": digests, "encoding_xml_sha256": STDLIB_XML_SHA256, "results": results}
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
