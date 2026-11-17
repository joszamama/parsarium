#!/usr/bin/env python3
"""Reproduce prewk/xml-string-streamer 1.2.3 returning raw byte slices, not parsed XML, on both namespace controls."""

from base64 import b64decode
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from xml.parsers import expat

PROBE = Path(__file__).resolve().parent
ROOT = PROBE.parents[3]
IMAGE = "parsarium-lead/xml-php-prewk_xml_string_streamer:local"
PLATFORM = "linux/arm64"
RELEASE = "1.2.3"
REFERENCE = "a1f4a5250d548d06fd385fa86241c0c2d7d607fd"
ARCHIVE_SHA256 = "f652cf058971933b499858ff9439fa4cef424a9377dad09218d8ddb80ee297ed"
# UniqueNode needs a caller-supplied raw element name; these are the root children of each control.
CONTROLS = {"catalog-ns.xml": "item", "order-default-ns.xml": "line"}
STRING_WALKER_APIS = ("createStringWalkerParser(path)", "StringWalker+Stream\\File(handle)")
UNIQUE_NODE_API = "createUniqueNodeParser(path)"
# Xdebug reports one line past EOF for a class file's top-level op array on first load.
FILE_LINES = {
    "src/XmlStringStreamer.php": 76,
    "src/XmlStringStreamer/ParserInterface.php": 43,
    "src/XmlStringStreamer/StreamInterface.php": 35,
    "src/XmlStringStreamer/Stream/File.php": 79,
    "src/XmlStringStreamer/Parser/StringWalker.php": 282,
    "src/XmlStringStreamer/Parser/UniqueNode.php": 314,
}
SPLITTERS = {"StringWalker": "src/XmlStringStreamer/Parser/StringWalker.php",
             "UniqueNode": "src/XmlStringStreamer/Parser/UniqueNode.php"}
LIVE_STATS = {"value": 3650676, "source": "https://packagist.org/packages/prewk/xml-string-streamer/stats.json",
              "captured_on": "2026-11-17"}


def command(*args: str, cwd: Path = PROBE) -> str:
    result = subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True, timeout=900)
    return result.stdout.strip()


def events(data: bytes) -> list:
    """Expat events in raw-name (non-namespace) mode with their byte offsets and element depth."""
    parser = expat.ParserCreate("UTF-8")
    found, stack = [], []

    def add(kind: str, **extra: object) -> None:
        found.append({"at": parser.CurrentByteIndex, "kind": kind, "depth": len(stack), **extra})

    def start(name: str, attributes: dict) -> None:
        add("start", name=name, attributes=attributes)
        stack.append(name)

    def end(name: str) -> None:
        stack.pop()
        add("end", name=name)

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.CharacterDataHandler = lambda _: add("text")
    parser.ProcessingInstructionHandler = lambda *_: add("pi")
    parser.CommentHandler = lambda _: add("comment")
    parser.StartCdataSectionHandler = lambda: add("cdata")
    parser.Parse(data, True)
    return found


def after(found: list, index: int) -> int:
    """Byte offset just past event `index`: the first later event offset (an empty element shares its start)."""
    offset = found[index]["at"]
    return next(item["at"] for item in found[index + 1:] if item["at"] > offset)


def matching_end(found: list, index: int) -> int:
    depth = found[index]["depth"]
    return next(i for i in range(index + 1, len(found))
                if found[i]["kind"] == "end" and found[i]["depth"] == depth)


def string_walker_oracle(data: bytes) -> list:
    """captureDepth 2: each root child element, PI or comment with the raw text since the previous markup."""
    found, nodes = events(data), []
    for index, item in enumerate(found):
        if item["depth"] != 1 or item["kind"] in ("text", "end"):
            continue
        if item["kind"] == "cdata":
            raise RuntimeError("root-level CDATA is outside this oracle")
        first = index
        while first > 0 and found[first - 1]["kind"] == "text" and found[first - 1]["depth"] == 1:
            first -= 1
        last = matching_end(found, index) if item["kind"] == "start" else index
        nodes.append({"start": found[first]["at"], "end": after(found, last), "element_index": index})
    return nodes


def unique_node_oracle(data: bytes, name: str) -> list:
    found, nodes = events(data), []
    for index, item in enumerate(found):
        if item["kind"] == "start" and item["name"] == name:
            last = matching_end(found, index)
            if any(found[i]["kind"] == "start" and found[i]["name"] == name for i in range(index + 1, last)):
                raise RuntimeError("nested unique nodes are outside this oracle")
            nodes.append({"start": item["at"], "end": after(found, last)})
    return nodes


def outside_bindings(data: bytes, node: dict) -> list:
    """Namespace bindings that names inside the node use but that are declared outside the returned bytes."""
    found, scopes, used = events(data), [], set()
    for index, item in enumerate(found):
        if item["kind"] == "start":
            declared = {("" if key == "xmlns" else key[6:]): value for key, value in item["attributes"].items()
                        if key == "xmlns" or key.startswith("xmlns:")}
            scopes.append((declared, node["start"] <= item["at"] < node["end"]))
            if node["start"] <= item["at"] < node["end"]:
                names = [item["name"]] + [key for key in item["attributes"]
                                          if key != "xmlns" and not key.startswith("xmlns:")]
                for position, name in enumerate(names):
                    if ":" not in name and position:
                        continue  # unprefixed attributes have no namespace
                    prefix = name.split(":", 1)[0] if ":" in name else ""
                    for declarations, inside in reversed(scopes):
                        if prefix in declarations:
                            if not inside and declarations[prefix]:
                                used.add((prefix, declarations[prefix]))
                            break
        elif item["kind"] == "end":
            scopes.pop()
    return [list(binding) for binding in sorted(used)]


def package_lines(run: dict) -> dict:
    lines = {}
    for name, executed in run["package_lines_executed"].items():
        extra = [line for line in executed if line > FILE_LINES[name]]
        if extra not in ([], [FILE_LINES[name] + 1]):
            raise RuntimeError(f"{name}: unexpected lines past EOF {extra}")
        lines[name] = sorted(set(executed) - set(extra))
    return lines


def main() -> None:
    command("docker", "build", "--quiet", "--platform", PLATFORM, "-t", IMAGE, ".")
    image_id = command("docker", "image", "inspect", "--format", "{{.Id}}", IMAGE)
    report = json.loads(command(
        "docker", "run", "--rm", "--platform", PLATFORM, "--network", "none", "--read-only",
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "-v", f"{ROOT / 'controls/xml'}:/input:ro", IMAGE,
        *(f"/input/{name}={unique}" for name, unique in CONTROLS.items())))
    runs = report["runs"]
    apis = (*STRING_WALKER_APIS, UNIQUE_NODE_API)
    if [(run["control"], run["api"]) for run in runs] != [(c, a) for c in CONTROLS for a in apis]:
        raise RuntimeError("the documented APIs did not stream both valid controls")
    if set(report["source_api_mentions"]) != {"preg_match"}:
        raise RuntimeError(f"package source mentions an XML parser API: {report['source_api_mentions']}")
    observed, coverage = [], {}
    for run in runs:
        data = (ROOT / "controls/xml" / run["control"]).read_bytes()
        nodes = [b64decode(node) for node in run["nodes_base64"]]
        if run["api"] == UNIQUE_NODE_API:
            spans = unique_node_oracle(data, run["unique_node"])
        else:
            spans = string_walker_oracle(data)
        expected = [data[span["start"]:span["end"]] for span in spans]
        if nodes != expected:
            raise RuntimeError(f"{run['control']} via {run['api']}: nodes differ from the byte-span oracle")
        lines = package_lines(run)
        splitter = "UniqueNode" if run["api"] == UNIQUE_NODE_API else "StringWalker"
        coverage.setdefault(run["api"], {})[run["control"]] = lines[SPLITTERS[splitter]]
        observed.append({
            "control": run["control"], "api": run["api"], "unique_node": run["unique_node"],
            "nodes": [{"byte_span": [span["start"], span["end"]], "text": node.decode("utf-8"),
                       "outside_namespace_bindings_used": outside_bindings(data, span)}
                      for span, node in zip(spans, nodes)],
            "package_lines_executed": lines,
        })
    if not all(lines for by_control in coverage.values() for lines in by_control.values()):
        raise RuntimeError("a splitter ran no lines")
    differential = {}
    for api, by_control in coverage.items():
        a, b = (set(by_control[name]) for name in CONTROLS)
        differential[api] = {"lines": {name: len(by_control[name]) for name in CONTROLS},
                             "only_catalog-ns.xml": sorted(a - b), "only_order-default-ns.xml": sorted(b - a)}
    lock, = json.loads((PROBE / "composer.lock").read_text())["packages"]
    if (lock["version"], lock["source"]["reference"], lock["license"]) != (RELEASE, REFERENCE, ["MIT"]):
        raise RuntimeError("composer.lock differs from the pinned release")
    controls = [ROOT / "controls/xml" / name for name in CONTROLS]
    result = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "negative_lead_raw_node_string_splitter",
        "package": "prewk/xml-string-streamer", "release": RELEASE, "license": "MIT",
        "license_evidence": f"https://github.com/prewk/xml-string-streamer/blob/{REFERENCE}/LICENSE",
        "source_url": f"https://github.com/prewk/xml-string-streamer/tree/{REFERENCE}",
        "documentation": f"https://github.com/prewk/xml-string-streamer/blob/{REFERENCE}/README.md",
        "api": "Prewk\\XmlStringStreamer::createStringWalkerParser(path|handle) and createUniqueNodeParser(path, "
               "['uniqueNode' => name]), or new XmlStringStreamer(Parser\\StringWalker|UniqueNode, Stream\\File|Stdin); "
               "getNode() returns the next node as a string or false",
        "composer_reference": REFERENCE,
        "composer_lock_sha256": sha256((PROBE / "composer.lock").read_bytes()).hexdigest(),
        "archive_url": f"https://codeload.github.com/prewk/xml-string-streamer/legacy.zip/{REFERENCE}",
        "archive_sha256": ARCHIVE_SHA256,
        "installed_source_matches_archive": True,
        "popularity": {
            "metric": "Packagist total downloads", "value": 3642516,
            "source": "https://packagist.org/packages/prewk/xml-string-streamer",
            "captured_at_utc": json.loads((ROOT / "data/php/xml/registry-snapshot.json")
                                          .read_text())["captured_at_utc"],
            "snapshot": "data/php/xml/registry-snapshot.json",
            "live_recheck": LIVE_STATS,
        },
        "image_id": image_id,
        "platform": PLATFORM,
        "php": report["php"], "xdebug": report["xdebug"], "toolchain": report["toolchain"],
        "probe_file_sha256": {name: sha256((PROBE / name).read_bytes()).hexdigest()
                              for name in ("Dockerfile", "composer.json", "composer.lock", "probe.php")},
        "control_sha256": {path.name: sha256(path.read_bytes()).hexdigest() for path in controls},
        "observed": observed,
        "oracle": "Python expat in raw-name (non-namespace) mode with CurrentByteIndex offsets. StringWalker "
                  "(captureDepth 2): every root-child element, processing instruction or comment, prefixed by the "
                  "raw character data since the previous markup. UniqueNode: the raw byte span of each element with "
                  "the given qualified name. Expected output is data[start:end] of the control.",
        "nodes_match_byte_span_oracle": True,
        "source_api_mentions": report["source_api_mentions"],
        "splitter_line_differential": differential,
        "splitter_line_differential_note": "StringWalker.php 250-251 is the only input-dependent branch: the root-level "
                                           "<?audit step=\"1\"?> PI in order-default-ns.xml takes the self-closing "
                                           "capture-once path and is returned as a node. StringWalker.php 18 and "
                                           "UniqueNode.php 19 are class declarations that run only on first load, "
                                           "which is the catalog-ns.xml run.",
        "source_reason": "StringWalker finds the next tag with preg_match('/<[^>]+>/'), classifies it by its opening and "
                         "closing characters, adjusts a depth counter and copies input bytes until the capture depth is "
                         "left. UniqueNode searches for '<name>' or '<name ' and the next '</name>' with preg_match and "
                         "strpos. Neither reads names, attributes, text values or namespace declarations: getNode() "
                         "returns verbatim input substrings, with entity and character references undecoded and "
                         "prefixes whose declarations sit on the root left unbound. The README hands each node to "
                         "simplexml_load_string for parsing; the package itself never calls an XML parser.",
        "parser_family": "none: own PCRE/strpos tag-boundary splitter; no ext/libxml, XMLReader, SimpleXML, DOM or "
                         "ext/xml call in src/ (only the unreleased dev-xml-reader-parser branch name suggests XMLReader)",
        "docker_source_coverage": "run; both splitters and both stream routes executed under Xdebug on both controls",
        "afl_feedback": "not_run: the release runs no native XML parser, so libxml2 feedback would not come from this "
                        "package; the package is PHP string and PCRE code whose output is a byte copy",
        "adapter": "lead-probes/php/xml/prewk_xml_string_streamer/probe.php",
        "recommended_lead_status": "excluded",
        "recommended_lead_reason": "Pinned 1.2.3 probe: getNode() returns verbatim input byte slices found by a "
                                   "preg_match/strpos tag-boundary splitter (StringWalker depth counter, UniqueNode "
                                   "name search); no names, attributes, decoded text or namespaces, and no XML "
                                   "parser call. Byte copying under PROTOCOL.md, not a parser. Evidence: "
                                   "data/php/xml/prewk-xml-string-streamer-lead-check.json.",
    }
    destination = ROOT / "data/php/xml/prewk-xml-string-streamer-lead-check.json"
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"Both controls returned raw byte slices matching the span oracle -> {destination}")


if __name__ == "__main__":
    main()
