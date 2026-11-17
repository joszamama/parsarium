"""Capture npm search hits, 30-day downloads, and dependency/delegation facts for JavaScript XML leads."""

from datetime import datetime, timezone
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import tarfile
from urllib.parse import quote
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/javascript/xml/registry-snapshot.json"
QUERIES = ["xml parser", "xml", "sax xml", "xml dom parser", "xml to json", "xml stream parser"]
WINDOW = "2026-10-17:2026-11-15"
# Hand-picked XML document-parser candidates from the hits plus well-known names.
CANDIDATES = ["saxes", "sax", "htmlparser2", "fast-xml-parser", "@xmldom/xmldom", "xml2js",
              "xml-js", "xmldoc", "xmlbuilder2", "@xml-tools/parser", "xmldom", "libxmljs2",
              "txml", "@rgrove/parse-xml", "sax-wasm", "node-expat", "ltx", "xml-parser", "jsdom"]
PARSER_IMPORT = re.compile(r"""(?:require\(|from\s+|import\()\s*['"](sax|saxes|htmlparser2|@xmldom/xmldom|xmldom|"""
                           r"""fast-xml-parser|libxmljs2?|node-expat|@oozcitak/dom|chevrotain|parse5)['"/]""")


def fetch(url: str) -> bytes:
    with urlopen(url, timeout=60) as response:
        return response.read()


def inspect(name: str) -> dict:
    meta = json.loads(fetch(f"https://registry.npmjs.org/{quote(name, safe='@')}/latest"))
    tarball = fetch(meta["dist"]["tarball"])
    imports, natives, domparser = set(), [], []
    with tarfile.open(fileobj=io.BytesIO(tarball)) as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            if member.name.endswith((".node", ".wasm", ".gyp", ".cc", ".c")):
                natives.append(member.name)
            if member.name.endswith((".js", ".cjs", ".mjs")) and "/test" not in member.name:
                text = archive.extractfile(member).read().decode("utf-8", "replace")
                imports.update(PARSER_IMPORT.findall(text))
                if "new DOMParser" in text:
                    domparser.append(member.name)
    return {"version": meta["version"], "license": meta.get("license"),
            "integrity": meta["dist"]["integrity"], "tarball_sha256": sha256(tarball).hexdigest(),
            "dependencies": meta.get("dependencies", {}),
            "xml_parser_imports": sorted(imports), "native_or_wasm_files": sorted(natives)[:10],
            "domparser_call_files": sorted(domparser)[:10]}


def main() -> None:
    search = []
    for query in QUERIES:
        url = f"https://registry.npmjs.org/-/v1/search?text={quote(query)}&size=100&from=0"
        body = json.loads(fetch(url))
        search.append({"query": query, "url": url, "total": body["total"],
                       "hits": [{"rank": i + 1, "name": o["package"]["name"],
                                 "version": o["package"]["version"],
                                 "description": o["package"].get("description", "")}
                                for i, o in enumerate(body["objects"])]})
    downloads, inspection = {}, {}
    for name in CANDIDATES:
        url = f"https://api.npmjs.org/downloads/point/{WINDOW}/{name}"
        point = json.loads(fetch(url))
        downloads[name] = {"value": point["downloads"], "start": point["start"], "end": point["end"], "url": url}
        inspection[name] = inspect(name)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT.write_text(json.dumps({
        "ecosystem": "javascript", "format": "xml", "captured_at_utc": now,
        "search_surface": "npm registry search API",
        "search_api_docs": "https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md",
        "search_limit_per_query": 100,
        "note": "Search hits are leads, not verified parsers. Downloads and latest tarballs were fetched for a hand-picked set of XML document-parser candidates; this is not a download census of all hits. xml_parser_imports lists other XML parser packages a tarball imports.",
        "download_metric": f"npm downloads over the fixed window {WINDOW.replace(':', ' to ')} (30 days)",
        "download_metric_docs": "https://github.com/npm/registry/blob/main/docs/download-counts.md",
        "download_observed_at_utc": now, "downloads": downloads,
        "latest_release_inspection": inspection, "search": search,
    }, indent=2, ensure_ascii=False) + "\n")
    for name in sorted(downloads, key=lambda n: -downloads[n]["value"]):
        i = inspection[name]
        print(f"{downloads[name]['value']:>11,} {name} {i['version']} {i['license']} deps={list(i['dependencies'])} imports={i['xml_parser_imports']} native={len(i['native_or_wasm_files'])} dom={len(i['domparser_call_files'])}")


if __name__ == "__main__":
    main()
