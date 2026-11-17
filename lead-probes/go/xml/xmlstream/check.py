#!/usr/bin/env python3
"""Reproduce the mellium.im/xmlstream v0.15.4 lead decision on both valid XML controls."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

PROBE = Path(__file__).resolve().parent
ROOT = PROBE.parents[3]
MODULE = "mellium.im/xmlstream"
VERSION = "v0.15.4"
ZIP_SHA256 = "8be6fef9570756ea72eb003e660c3a3370aac9b708f662f22024e67047632a80"
LICENSE_SHA256 = "2705eb412fa8499998dbaf56658fed3982bd7bd89872e58b25b3fc239eca08e1"
# Same encoding/xml/xml.go hash as the goxpp project's source lock.
ENCODING_XML_SHA256 = "41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb"
IMAGE = "golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66"
PLATFORM = "linux/arm64"
CONTROLS = ("catalog-ns.xml", "order-default-ns.xml")
MODES = ("readall", "iter", "innerreader")
REPEATS = 2
PACKAGE_PREFIX = "mellium.im/xmlstream@v0.15.4/"
COVER_PREFIXES = {"xmlstream": "mellium.im/xmlstream/", "encoding_xml": "encoding/xml/"}
GOXPP_MANIFEST = ROOT / "projects/xml/go/github_com_mmcdole_goxpp/manifest.json"
GOXPP_TEST = ROOT / "projects/xml/go/github_com_mmcdole_goxpp/harness_test.go"
OUTPUT = ROOT / "data/go/xml/xmlstream-lead-check.json"

SCRIPT = r"""
set -eu
export GOPATH=/tmp/gopath GOCACHE=/tmp/gocache GOFLAGS=-mod=readonly
cp -r /probe /tmp/probe-src
cd /tmp/probe-src
go version > /out/go-version.txt
go mod download -json mellium.im/xmlstream@v0.15.4 > /out/download.json
module=/tmp/gopath/pkg/mod/mellium.im/xmlstream@v0.15.4
sha256sum /tmp/gopath/pkg/mod/cache/download/mellium.im/xmlstream/@v/v0.15.4.zip \
  $module/LICENSE /usr/local/go/src/encoding/xml/xml.go > /out/hashes.txt
(cd $module && wc -l $(ls *.go | grep -v _test.go)) > /out/package-lines.txt
go build -cover -coverpkg=mellium.im/xmlstream,encoding/xml,parsarium.local/xmlstream-lead-probe -o /tmp/probe .
for mode in readall iter innerreader; do
  for control in catalog-ns.xml order-default-ns.xml; do
    for repeat in $(seq 1 "$REPEATS"); do
      name="$mode-$control-$repeat"
      mkdir -p "/tmp/cover/$name"
      GOCOVERDIR="/tmp/cover/$name" /tmp/probe "$mode" "/controls/$control" > "/out/$name.json"
      go tool covdata textfmt -i "/tmp/cover/$name" -o "/out/$name.cover"
    done
  done
done
"""


def blocks(cover: Path) -> dict[str, dict[str, set]]:
    """Return covered cover blocks and source lines per prefix for one run."""
    found = {key: {"blocks": set(), "lines": set()} for key in COVER_PREFIXES}
    for line in cover.read_text().splitlines()[1:]:
        location, _, count = line.split()
        if count == "0":
            continue
        for key, prefix in COVER_PREFIXES.items():
            if not location.startswith(prefix):
                continue
            filename, span = location.rsplit(":", 1)
            start, end = span.split(",")
            first, last = int(start.split(".")[0]), int(end.split(".")[0])
            if end.split(".")[1] == "1" and last > first:
                last -= 1  # Go cover block end positions are exclusive.
            found[key]["blocks"].add(location)
            found[key]["lines"].update(f"{filename}:{number}" for number in range(first, last + 1))
    return found


def expected_outputs() -> dict[str, dict]:
    manifest = json.loads(GOXPP_MANIFEST.read_text())
    marker = "if encoded != `"
    test = GOXPP_TEST.read_text()
    differential = json.loads(test[test.index(marker) + len(marker):].split("`", 1)[0])
    return {"catalog-ns.xml": manifest["expected_output"], "order-default-ns.xml": differential}


def main() -> None:
    expected = expected_outputs()
    with tempfile.TemporaryDirectory(prefix="parsarium-xmlstream-lead-") as temporary:
        out = Path(temporary)
        subprocess.run(
            ["docker", "run", "--rm", "--platform", PLATFORM, "--read-only",
             "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
             "--user", f"{os.getuid()}:{os.getgid()}", "-e", "HOME=/tmp",
             "-e", f"REPEATS={REPEATS}",
             "--tmpfs", "/tmp:rw,exec,nosuid,size=512m",
             "-v", f"{PROBE}:/probe:ro", "-v", f"{ROOT / 'controls/xml'}:/controls:ro",
             "-v", f"{out}:/out", "--entrypoint", "/bin/sh", IMAGE, "-c", SCRIPT],
            check=True, capture_output=True, text=True, timeout=600,
        )
        download = json.loads((out / "download.json").read_text())
        hashes = {line.split()[1].rsplit("/", 1)[-1]: line.split()[0]
                  for line in (out / "hashes.txt").read_text().splitlines()}
        if (download["Version"] != VERSION or hashes["v0.15.4.zip"] != ZIP_SHA256
                or hashes["LICENSE"] != LICENSE_SHA256
                or hashes["xml.go"] != ENCODING_XML_SHA256):
            raise RuntimeError(f"pinned sources differ from lead lock: {hashes}")
        package_lines = int((out / "package-lines.txt").read_text().split()[-2])
        runs = {}
        for mode in MODES:
            for control in CONTROLS:
                observed = [json.loads((out / f"{mode}-{control}-{repeat}.json").read_text())
                            for repeat in range(1, REPEATS + 1)]
                covered = [blocks(out / f"{mode}-{control}-{repeat}.cover")
                           for repeat in range(1, REPEATS + 1)]
                if any(item != observed[0] for item in observed) or any(
                        item != covered[0] for item in covered):
                    raise RuntimeError(f"{mode} {control}: repeated run changed")
                runs[mode, control] = observed[0]["result"], covered[0]
        go_version = (out / "go-version.txt").read_text().strip()

    modes = {}
    for mode in MODES:
        catalog, order = (runs[mode, control] for control in CONTROLS)
        record = {"repeated_runs_identical": True, "controls": {}}
        for control, (result, covered) in zip(CONTROLS, (catalog, order)):
            entry = {"observed": result,
                     **{f"{key}_cover_blocks": len(covered[key]["blocks"]) for key in COVER_PREFIXES},
                     **{f"{key}_source_lines": len(covered[key]["lines"]) for key in COVER_PREFIXES}}
            if mode != "innerreader":
                entry["matches_shared_namespace_oracle"] = result == expected[control]
                if not entry["matches_shared_namespace_oracle"]:
                    raise RuntimeError(f"{mode} {control}: oracle mismatch {result}")
            record["controls"][control] = entry
        for key in COVER_PREFIXES:
            changed = sorted(catalog[1][key]["blocks"] ^ order[1][key]["blocks"])
            record[f"{key}_block_difference"] = len(changed)
            if key == "xmlstream":
                record["changed_xmlstream_blocks"] = changed
        modes[mode] = record
    if any(not runs[key][1][prefix]["blocks"] for key in runs for prefix in COVER_PREFIXES):
        raise RuntimeError("a run recorded no xmlstream or encoding/xml coverage")

    if any(modes[mode]["xmlstream_block_difference"] for mode in ("readall", "iter")):
        raise RuntimeError("xmlstream blocks now differ on an oracle path; review the lead decision")
    inner = {control: runs["innerreader", control][0] for control in CONTROLS}
    if any("error" not in inner[control]["control"] for control in CONTROLS):
        raise RuntimeError("InnerReader now accepts a valid control; review the lead decision")

    result = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "negative_lead_token_stream_utility_over_encoding_xml",
        "package": MODULE, "release": VERSION,
        "release_published_utc": "2023-01-11T12:29:46Z",
        "release_commit": download.get("Origin", {}).get("Hash"),
        "source_url": "https://codeberg.org/mellium/xmlstream/src/tag/v0.15.4",
        "license": "BSD-2-Clause (LICENSE); some code copied from Go under LICENSE-GO",
        "license_file_sha256": LICENSE_SHA256,
        "module_zip_sha256": ZIP_SHA256,
        "module_sum": download["Sum"],
        "go_mod_sum": download["GoModSum"],
        "dependency": "mellium.im/reader v0.1.0",
        "image": IMAGE, "platform": PLATFORM, "go_toolchain": go_version,
        "underlying_source": "encoding/xml/xml.go",
        "underlying_source_sha256": ENCODING_XML_SHA256,
        "package_non_test_go_lines": package_lines,
        "popularity": {
            "metric": "pkg.go.dev Imported by package count",
            "value": 86, "importing_modules": 32,
            "source": "https://pkg.go.dev/mellium.im/xmlstream?tab=importedby",
            "captured_at_utc": "2026-11-17T13:31:41Z",
            "registry_snapshot": "data/go/xml/registry-snapshot.json",
            "caveat": "Package importers, not installations. The importer listing is dominated by mellium.im/xmpp and mellium.im/legacy packages from the same project and by forks of mellium.im/xmpp.",
        },
        "api_finding": {
            "local_bytes_parse_api": None,
            "io_reader_api": "InnerReader(io.Reader) io.Reader: decodes only the outer start/end element with encoding/xml RawToken and returns the inner XML bytes without parsing them",
            "token_apis": "ReadAll, NewIter, Inner, InnerElement, Skip, Copy, Pipe, MultiReader, TeeReader and the Transformer functions all accept an xml.TokenReader the caller constructs, in package examples and tests with xml.NewDecoder(io.Reader)",
            "tokenizer": "none; no xmlstream source file reads XML bytes into tokens. InnerReader calls encoding/xml.Decoder.RawToken; everything else consumes Token() from a caller-supplied reader",
            "api_reference": f"https://pkg.go.dev/{MODULE}@{VERSION}",
        },
        "parser_family": "Go encoding/xml.Decoder (same pinned encoding/xml source as stdlib_decoder, goxpp, x2j, mxj, etree and xmlquery); xmlstream adds token-stream composition only",
        "modes": modes,
        "inner_reader_on_valid_controls": "InnerReader returns an error on both unmodified controls because it sizes the body from bufio-buffered bytes and the controls end with a newline after the root end tag; with trailing whitespace trimmed it returns the inner bytes undecoded, with prefixes, entity references and CDATA as written",
        "decision": "Not counted as a parser path. xmlstream has no documented local byte or io.Reader API that returns parsed XML structure and no tokenizer of its own. The namespace-aware result on both controls comes from the caller-built encoding/xml.Decoder that Parsarium already counts as stdlib_decoder. Counting xmlstream.ReadAll(xml.NewDecoder(r)) or NewIter would count encoding/xml again under a token utility's name.",
        "docker_source_coverage": "measured in the pinned Go image with go build -cover over mellium.im/xmlstream and encoding/xml; no Parsarium project image was built",
        "parser_specific_feedback": {
            "oracle_paths": ["readall", "iter"],
            "xmlstream_block_difference": {mode: modes[mode]["xmlstream_block_difference"]
                                           for mode in ("readall", "iter")},
            "encoding_xml_block_difference": {mode: modes[mode]["encoding_xml_block_difference"]
                                              for mode in ("readall", "iter")},
            "finding": "On both paths that reproduce the namespace-aware result, the two valid controls execute the same xmlstream cover blocks; every block difference is in encoding/xml. An xmlstream-scoped AFL++ bridge would have no stable differential between the controls.",
        },
        "afl_feedback": "not_built_no_xmlstream_differential",
        "probe_file_sha256": {name: sha256((PROBE / name).read_bytes()).hexdigest()
                              for name in ("check.py", "go.mod", "go.sum", "main.go")},
        "adapter": "lead-probes/go/xml/xmlstream/main.go",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    for mode, record in modes.items():
        print(f"{mode}: xmlstream blocks differ by {record['xmlstream_block_difference']}, "
              f"encoding/xml blocks by {record['encoding_xml_block_difference']}")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
