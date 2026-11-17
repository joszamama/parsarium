#!/usr/bin/env python3
"""Assemble the JSON/XML/plain-MP3 expansion inventory from captured snapshots.

Inputs: scripts/expansion_leads.py, data/expansion/registry/*.json,
data/expansion/metrics/*.json, data/expansion/standard-receipts.json.
Outputs: data/expansion/formats.json, data/expansion/cells/<format>/<ecosystem>.json,
data/expansion/inventory.json. No lead is selected or verified here.
"""
import hashlib, json, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from expansion_leads import LEADS, SOURCE  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "data/expansion"
ECOS = ["c", "cpp", "go", "java", "javascript", "python", "rust", "php"]
REGISTRY_FILE = {e: ("c_cpp" if e in ("c", "cpp") else e) for e in ECOS}
OBSERVED = "2026-11-17"

CONTROL_EXPECTED = {
    "control.json": {"keys": ["count", "format", "items", "nested"], "items": 6, "nested.text": "café ✓", "count": 3},
    "control.xml": {"root": "{urn:parsarium:control}catalog", "element_children": 3, "item_ids": ["a", "b"], "item_texts": ["café", "x<y"]},
    "silent-plain-44k.mp3": {"mpeg_version": "MPEG-1", "layer": 3, "sample_rate": 44100, "channels": 1, "bitrate": 128000, "frames": 38, "samples_per_channel": 43776, "pcm": "all zero"},
    "tone-plain-16k.mp3": {"mpeg_version": "MPEG-2 (LSF)", "layer": 3, "sample_rate": 16000, "channels": 1, "bitrate": 32000, "frames": 30, "samples_per_channel": 17280, "pcm": "440 Hz sine, encoder delay/padding included"},
}

FORMATS = {
    "json": {
        "name": "JSON text",
        "definition": "A JSON text as defined by RFC 8259 / ECMA-404, read from local bytes, a string, a file or a stream into values or parse events.",
        "specifications": ["https://www.rfc-editor.org/rfc/rfc8259", "https://ecma-international.org/publications-and-standards/standards/ecma-404/"],
        "in_scope": "DOM, streaming/event, and data-binding parsers that tokenize JSON text themselves or through an identified family.",
        "out_of_scope": "Encoders/serializers only, schema validators or JSONPath/JMESPath layers without their own parse step (they inherit a parser family), CLI-only tools, remote services.",
        "ambiguity": "JSON5, Hjson, JSONC and UCL parsers accept supersets; only the strict-JSON control subset can be claimed. Wrappers over a runtime parser (JSON.parse, json_decode, encoding/json) share that family.",
        "controls": ["control.json"],
    },
    "xml": {
        "name": "XML 1.0 document",
        "definition": "A well-formed XML 1.0 document with namespaces, read from local bytes, a string, a file or a stream into a tree or event stream.",
        "specifications": ["https://www.w3.org/TR/xml/", "https://www.w3.org/TR/xml-names/"],
        "in_scope": "DOM, SAX, StAX/pull and tree parsers; object mappers count only with their tokenizer family identified.",
        "out_of_scope": "Writers/builders only, HTML-only parsers, XSLT/XPath layers without their own tokenizer, binary XML encodings, CLI-only tools.",
        "ambiguity": "Many wrappers delegate to Expat, libxml2, encoding/xml or a JDK SAX/StAX provider; family must be recorded. HTML parsers with an XML mode (htmlparser2, jsoup) are flagged.",
        "controls": ["control.xml"],
    },
    "mp3_plain": {
        "name": "Plain untagged MP3",
        "definition": "An MPEG-1 or MPEG-2 (LSF) Audio Layer III elementary stream (ISO/IEC 11172-3, ISO/IEC 13818-3) consisting only of contiguous audio frames: no ID3v1, ID3v2 or APE tag and no Xing/Info/VBRI header frame. A parser must interpret frame headers (sync, version, layer, bitrate, sample rate, channel mode) or decode samples.",
        "specifications": ["https://www.iso.org/standard/22412.html", "https://www.iso.org/standard/26797.html"],
        "in_scope": "Frame parsers, duration/property scanners that read frame headers, and PCM decoders.",
        "out_of_scope": "ID3-only or other tag-only readers, MIME/magic sniffing, external-process wrappers (ffmpeg/lame CLIs), encoders only.",
        "relation_to_mp3_id3v2": "The existing mp3_id3v2 cell tests tagged files; a parser verified there through ID3 fields does not establish frame-level MP3 parsing. Verification here needs a frame-level observable on an untagged control. Tagging libraries that also scan frame headers (mutagen, TagLib, jaudiotagger, getID3, mp3agic) remain leads until that frame-level result is shown.",
        "ambiguity": "MPEG-2.5 (8/11.025/12 kHz) is a non-ISO extension and is not used by the controls. Header-only scanners and full decoders produce different observables; the verified observable must be named per path.",
        "controls": ["silent-plain-44k.mp3", "tone-plain-16k.mp3"],
    },
}

STD = {  # official documentation per ecosystem and format
    ("c", "*"): ("none_documented_in_scoped_standard_library", ["https://www.open-std.org/jtc1/sc22/wg14/www/docs/"],
                 "ISO C documents byte and stream I/O but no JSON, XML or MPEG audio parser."),
    ("cpp", "*"): ("none_documented_in_scoped_standard_library", ["https://www.open-std.org/jtc1/sc22/wg21/docs/papers/"],
                   "ISO C++ standard library documents no JSON, XML or MPEG audio parser."),
    ("rust", "*"): ("none_documented_in_scoped_standard_library", ["https://doc.rust-lang.org/std/"],
                    "The Rust standard library documents no JSON, XML or MPEG audio parser."),
    ("go", "json"): ("standard_api_verified", ["https://pkg.go.dev/encoding/json", "https://pkg.go.dev/encoding/json/v2"],
                     "encoding/json is documented and verified. encoding/json/v2 and encoding/json/jsontext exist in Go 1.27.1 sources only under GOEXPERIMENT=jsonv2 (build tag goexperiment.jsonv2); they are recorded as experimental and not verified."),
    ("go", "xml"): ("standard_api_verified", ["https://pkg.go.dev/encoding/xml"], "encoding/xml Decoder is documented and verified."),
    ("go", "mp3_plain"): ("none_documented_in_scoped_standard_library", ["https://pkg.go.dev/std"], "The Go standard-library index lists no MPEG audio package."),
    ("java", "json"): ("none_documented_in_scoped_standard_library", ["https://docs.oracle.com/en/java/javase/21/docs/api/allpackages-index.html"],
                       "No Java SE 21 package contains a JSON API; Jakarta JSON-P is third-party (Parsson lead)."),
    ("java", "xml"): ("standard_api_verified", ["https://docs.oracle.com/en/java/javase/21/docs/api/java.xml/module-summary.html",
                      "https://docs.oracle.com/en/java/javase/21/docs/api/java.xml/javax/xml/parsers/DocumentBuilder.html",
                      "https://docs.oracle.com/en/java/javase/21/docs/api/java.xml/javax/xml/stream/XMLStreamReader.html"],
                      "java.xml DOM (javax.xml.parsers) and StAX (javax.xml.stream) verified; SAX shares the same JDK Xerces-derived provider and was not run separately."),
    ("java", "mp3_plain"): ("none_verified_negative_probe", ["https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/sound/sampled/AudioFileFormat.Type.html"],
                            "AudioFileFormat.Type documents WAVE, AU, AIFF, AIFF-C and SND only; AudioSystem.getAudioFileFormat rejected both untagged MP3 controls with UnsupportedAudioFileException on the tested JDK."),
    ("javascript", "json"): ("runtime_api_documented_pending_control", ["https://tc39.es/ecma262/#sec-json.parse"],
                             "JSON.parse is an ECMAScript built-in. The local Node.js binary failed to start (missing Homebrew libsimdjson.33.dylib), so no receipt was produced."),
    ("javascript", "xml"): ("runtime_api_documented_pending_control", ["https://nodejs.org/download/release/v26.10.0/docs/api/", "https://html.spec.whatwg.org/multipage/dynamic-markup-insertion.html#dom-parsing-and-serialization"],
                            "Node.js 26.10.0 API index lists no XML parser. Browser runtimes document DOMParser.parseFromString(..., 'application/xml'); not run here (no browser harness in this inventory)."),
    ("javascript", "mp3_plain"): ("runtime_api_documented_pending_control", ["https://nodejs.org/download/release/v26.10.0/docs/api/", "https://www.w3.org/TR/webaudio-1.1/#dom-baseaudiocontext-decodeaudiodata"],
                                  "Node.js lists no audio decoder. Browser decodeAudioData was verified only on the tagged mp3_id3v2 control (data/javascript/mp3_id3v2/standard.json); MP3 codec support is not mandated by the spec, and the untagged controls have not been run."),
    ("python", "json"): ("standard_api_verified", ["https://docs.python.org/3.13/library/json.html"], "json.loads verified."),
    ("python", "xml"): ("standard_api_verified", ["https://docs.python.org/3.13/library/xml.etree.elementtree.html", "https://docs.python.org/3.13/library/xml.dom.minidom.html",
                        "https://docs.python.org/3.13/library/pyexpat.html", "https://docs.python.org/3.13/library/xml.sax.html"],
                        "ElementTree, minidom and pyexpat verified; all share the bundled Expat family. xml.sax (also Expat) not run separately."),
    ("python", "mp3_plain"): ("none_documented_in_scoped_standard_library", ["https://docs.python.org/3.13/library/index.html"],
                              "CPython 3.13 documents no MPEG audio decoder; wave is WAV-only."),
    ("php", "json"): ("runtime_api_verified", ["https://www.php.net/manual/en/function.json-decode.php", "https://www.php.net/manual/en/json.installation.php"],
                      "json_decode verified; ext/json is a core extension, always enabled since PHP 8.0."),
    ("php", "xml"): ("runtime_api_verified", ["https://www.php.net/manual/en/book.simplexml.php", "https://www.php.net/manual/en/book.dom.php",
                     "https://www.php.net/manual/en/book.xmlreader.php", "https://www.php.net/manual/en/book.xml.php"],
                     "SimpleXML, DOM and XMLReader verified on this host's PHP build; all share libxml2. ext/xml (xml_parse) not run. These are default-enabled bundled extensions, not guaranteed in every build."),
    ("php", "mp3_plain"): ("none_documented_in_scoped_runtime_apis", ["https://www.php.net/manual/en/funcref.php"],
                           "The PHP function reference lists no MPEG audio decoder; Fileinfo MIME detection is excluded as format sniffing."),
}


def std_for(eco, fmt, receipts):
    status, docs, finding = STD.get((eco, fmt)) or STD[(eco, "*")]
    rs = [r for r in receipts if r["ecosystem"] == eco and r["format"] == fmt]
    return {"status": status, "official_documentation": docs, "observed": OBSERVED, "finding": finding,
            "receipts": [{"api": r["api"], "kind": r["kind"], "control": r["control"], "passed": r["passed"], "runtime": r["runtime"]} for r in rs],
            "receipt_file": "data/expansion/standard-receipts.json" if rs else None,
            "counts_toward_ten": False}


def lead_status(note):
    n = (note or "").lower()
    if "excluded" in n or "out of" in n:
        return "excluded_scope"
    return "lead"


def main():
    receipts = json.loads((EXP / "standard-receipts.json").read_text())["receipts"]
    (EXP / "formats.json").write_text(json.dumps({"observed": OBSERVED, "formats": FORMATS, "control_expected": CONTROL_EXPECTED,
        "control_sha256": {c: hashlib.sha256((EXP / "controls" / c).read_bytes()).hexdigest() for c in CONTROL_EXPECTED}},
        indent=1, ensure_ascii=False) + "\n")
    summary = []
    for fmt, by_eco in LEADS.items():
        for eco in ECOS:
            reg = json.loads((EXP / "registry" / f"{REGISTRY_FILE[eco]}.json").read_text())
            met = json.loads((EXP / "metrics" / f"{eco}.json").read_text())
            searches = [{"query": s["query"], "url": s["url"], "total": s.get("total"), "hits_recorded": len(s.get("hits", [])),
                         "limit": s.get("limit"), "error": s.get("error")} for s in reg["search"] if s["format"] == fmt]
            hit_names = {h["name"] for s in reg["search"] if s["format"] == fmt for h in s.get("hits", [])}
            leads = []
            for name, family, api, note in by_eco.get(eco, []):
                m = met["values"].get(name, {})
                src = SOURCE[eco].format(name) if "(no formula)" not in name else None
                leads.append({"name": name, "status": lead_status(note), "source": src, "family": family,
                              "api_lead": api, "api_lead_checked_against_pinned_release": False, "note": note,
                              "found_by": "registry_search" if name in hit_names else "targeted_documentation_lead",
                              "metric_value": m.get("value"), "metric_url": m.get("url"), "metric_error": m.get("error"),
                              "latest_release_observed": m.get("latest_release_observed"), "verified": False})
            ranked = sorted([l for l in leads if l["status"] == "lead" and (l["metric_value"] or 0) > 0], key=lambda l: -l["metric_value"])
            for i, l in enumerate(ranked, 1):
                l["lead_adoption_order"] = i
            fam = defaultdict(list)
            for l in leads:
                fam[l["family"]].append(l["name"])
            std = std_for(eco, fmt, receipts)
            cell = {
                "format": fmt, "ecosystem": eco, "status": "inventory_only_no_third_party_verified",
                "ceiling": 10, "selected_third_party": [], "selected_count": 0,
                "verified_standard_or_runtime_count": len({r["api"] for r in std["receipts"] if r["passed"] and r["kind"] == "positive"}),
                "search": {"surface": reg.get("search_surface"), "docs": reg.get("search_api_docs"), "captured_at_utc": reg["captured_at_utc"],
                           "limit_per_query": reg["search_limit_per_query"], "queries": searches,
                           "snapshot": f"data/expansion/registry/{REGISTRY_FILE[eco]}.json"},
                "metric": {"name": met["metric"], "docs": met["metric_docs"], "window": met.get("window"), "limitation": met.get("limitation"),
                           "comparability": met["comparability"], "snapshot": f"data/expansion/metrics/{eco}.json",
                           "lead_adoption_order_meaning": "Order among unverified leads with a positive value in this cell only. It is not a selection or a ranking of verified parsers."},
                "leads": leads,
                "shared_families": {k: v for k, v in fam.items() if len(v) > 1},
                "standard_or_runtime": std,
                "uncertainty": "No third-party path is verified: no pinned release, local API control run or receipt exists for any lead. Lead API names come from project documentation and were not checked against pinned releases. Search is bounded to the recorded queries and first 100 hits; targeted leads fill gaps from documentation knowledge and are labelled.",
            }
            out = EXP / "cells" / fmt / f"{eco}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(cell, indent=1, ensure_ascii=False) + "\n")
            summary.append({"format": fmt, "ecosystem": eco, "leads": sum(l["status"] == "lead" for l in leads),
                            "excluded_scope": sum(l["status"] == "excluded_scope" for l in leads),
                            "leads_with_metric": len(ranked), "selected_count": 0,
                            "standard_status": std["status"], "standard_verified_apis": cell["verified_standard_or_runtime_count"],
                            "search_totals": {s["query"]: s["total"] for s in searches}})
    # Cross-ecosystem parser families: substring match on curated family labels.
    roots = {"libxml2": "libxml2", "expat": "Expat", "simdjson": "simdjson", "rapidjson": "RapidJSON", "jiter": "jiter",
             "yyjson": "yyjson", "mpg123": "mpg123", "minimp3": "minimp3", "dr_mp3": "dr_mp3", "ffmpeg": "FFmpeg",
             "go-mp3": "go-mp3", "mediainfolib": "MediaInfoLib", "sax-js": "sax-js", "encoding/xml": "encoding/xml",
             "json.parse": "V8 JSON.parse", "json_decode": "ext/json json_decode", "libsndfile": "libsndfile", "getid3": "getID3", "jlayer": "JLayer"}
    cross = defaultdict(list)
    for fmt, by_eco in LEADS.items():
        for eco, rows in by_eco.items():
            for name, family, _, note in rows:
                for key, label in roots.items():
                    if key in family.lower():
                        cross[label].append({"format": fmt, "ecosystem": eco, "name": name, "status": lead_status(note)})
    (EXP / "shared-families.json").write_text(json.dumps({"observed": OBSERVED,
        "note": "Families are taken from curated lead labels and documentation; unverified. A shared family means results are not independent evidence.",
        "families": {k: v for k, v in sorted(cross.items()) if len(v) > 1}}, indent=1, ensure_ascii=False) + "\n")
    (EXP / "inventory.json").write_text(json.dumps({"observed": OBSERVED, "selected_third_party_total": 0, "cells": summary}, indent=1, ensure_ascii=False) + "\n")
    for s in summary:
        print(s["format"], s["ecosystem"], s["leads"], s["excluded_scope"], s["leads_with_metric"], s["standard_status"], s["standard_verified_apis"])


if __name__ == "__main__":
    main()
