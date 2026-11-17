"""Record the bounded Debian source-name search and new lead counts for the C XML pilot.

Reads two hashed popcon files instead of fetching live data, so the rows stay
comparable with the cell's primary metric:

- the saved sourcemax table (data/curation/popcon-sourcemax-by_inst.gz), searched
  for Debian source names containing ``xml``;
- the binary-package by_inst.gz the cell's ranking already uses (pass its path;
  the SHA-256 must equal the snapshot's adoption_metric hash). It supplies the
  runtime library binary counts that rank C XML leads.

Every source-name hit is classified. Targeted lookups cover C XML-related
sources whose names lack ``xml`` (GLib's GMarkup, libgsf, qdbm, libstrophe,
iksemel, libroxml). The result is merged into data/c/xml/registry-snapshot.json.

Usage: python3 scripts/search_c_xml_debian.py PATH/TO/by_inst.gz
"""

import gzip
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data/c/xml/registry-snapshot.json"
SOURCEMAX = ROOT / "data/curation/popcon-sourcemax-by_inst.gz"
SOURCEMAX_SHA256 = "9d5e341c8ede7267acab176e255be83aca763f09901477eef5324d644cdaebf8"
QUERY = "xml"
SEARCHED_AT = "2026-11-17"

# Source names whose package is a C library that parses XML structure itself or through a named parser.
C_XML_PARSERS = {
    "libxml2.9": "C XML parser library (libxml2 family; older libxml2 source still attributed the libxml2 binary); selected as libxml2",
    "libxml2": "C XML parser library; selected (now builds libxml2-16)",
    "libxmlb": "C library that builds a queryable silo from XML through GLib's GMarkup parser; verified candidate, GMarkup family",
    "mxml": "C XML parser library (Mini-XML); selected",
    "libnxml": "C XML parser library (nXML) with its own reader; verified candidate",
}
# Other hits (C code or language-neutral tools) that are not general C XML parser libraries.
C_OTHER = {
    "xmlsec1": "C XML signature/encryption library over libxml2; excluded already (Conan xmlsec)",
    "xmlrpc-c": "C XML-RPC protocol library; parses XML-RPC messages through a bundled expat-derived parser or libxml2, not a general XML parser API",
    "xmlrpc-epi": "C XML-RPC protocol library over expat; not a general XML parser API",
    "wbxml2": "C WBXML (binary XML) codec that uses expat for textual XML; not a general XML parser API",
    "xmlstarlet": "command-line tool over libxml2/libxslt; no library API",
    "xml2": "command-line converters over libxml2; no library API",
    "html-xml-utils": "W3C command-line HTML/XML utilities; no library API",
    "xmlindent": "command-line XML indenter (flex scanner); no library API",
    "xmlto": "command-line DocBook converter (shell over xsltproc); no library API",
    "flexml": "generator of flex-based validating XML processors from a DTD; not a parser library",
    "liblouisxml": "braille transcription library that reads XML through libxml2; not a general XML parser API",
    "tclxml": "Tcl XML extension (libxml2/expat backends); Tcl API, not a C library API",
    "raxml": "phylogenetics program; not XML software",
}
CPP = {"libxml++2.6", "libxml++-5.0", "libxml++-4.0", "kxmlgui", "kf6-kxmlgui", "libkolabxml",
       "pugixml", "tinyxml2", "tinyxml", "qt6-scxml", "qtxmlpatterns-opensource-src", "rapidxml",
       "xml-security-c", "xmltooling", "kxmlrpcclient", "flxmlrpc", "ui-gxmlcpp", "castxml",
       "poxml", "blahtexml", "xmlcopyeditor"}
DATA = {"xml-core", "docbook-xml", "docbook5-xml", "stardict-xmlittre"}
OTHER_LANGUAGE = {
    "lxml": "Python", "defusedxml": "Python", "lxml-html-clean": "Python", "xml2rfc": "Python",
    "pygccxml": "Python", "pyaxmlparser": "Python", "pyjunitxml": "Python", "aioxmlrpc": "Python",
    "django-xmlrpc": "Python", "trac-xmlrpc": "Python", "xmldiff": "Python",
    "xml-commons-external": "Java", "xmlgraphics-commons": "Java", "xmlbeans": "Java", "kxml2": "Java",
    "freehep-xml": "Java", "xmlextras": "Java", "xmlunit": "Java", "plexus-xml": "Java",
    "jackson-dataformat-xml": "Java", "simple-xml": "Java", "practicalxml-java": "Java",
    "xml-maven-plugin": "Java", "xmlbeans-maven-plugin": "Java", "java-xmlbuilder": "Java",
    "axmlrpc": "Java", "scala-xml": "Scala", "scala-xml-2.12": "Scala", "xml-light": "OCaml",
    "xmlm": "OCaml", "tyxml": "OCaml", "ocaml-xmlplaylist": "OCaml", "esxml": "Emacs Lisp",
    "xml-rpc-el": "Emacs Lisp", "haxml": "Haskell", "erlang-p1-xml": "Erlang",
    "data-xml-clojure": "Clojure", "libxmlada": "Ada", "libxmlezout": "Ada", "xmlf90": "Fortran",
    "libxmlbird": "Vala", "gxml": "Vala (GObject over libxml2)", "latexml": "Perl",
    "webmin-xmlrpc": "Perl", "ooxml": "Tcl", "xmlstreambuffer": "Java",
    "xmltv": "Perl", "xmltoman": "Perl", "xmlformat": "Perl", "sortxml": "Python", "dctrl2xml": "Python", "lua-xmlrpc": "Lua", "php-xmlrpc": "PHP",
}
PREFIXES = (("perl", re.compile(r"^lib.*-perl$"), "Perl"), ("java", re.compile(r"^lib.*-java$"), "Java"),
            ("ruby", re.compile(r"^ruby-"), "Ruby"), ("python", re.compile(r"^python-"), "Python"),
            ("r", re.compile(r"^r-cran-"), "R"), ("haskell", re.compile(r"^haskell-"), "Haskell"),
            ("node", re.compile(r"^node-"), "JavaScript"), ("go", re.compile(r"^golang-"), "Go"),
            ("rust", re.compile(r"^rust-"), "Rust"), ("php", re.compile(r"^php-"), "PHP"),
            ("lisp", re.compile(r"^cl-"), "Common Lisp"))
TARGETED = {
    "expat": "selected C XML parser (name lacks xml)",
    "glib2.0": "GLib, whose GMarkup (g_markup_parse_context_parse) is a documented XML-subset parser; multi-library source",
    "libgsf": "structured-file I/O library whose GsfXMLIn wraps libxml2's SAX parser",
    "qdbm": "database library whose Cabin utility API includes XML tokenizing helpers",
    "libstrophe": "XMPP client library over expat or libxml2",
    "iksemel": "XMPP-oriented C library with its own XML SAX/tree parser",
    "libroxml": "C XML parser library (existing lead)",
}
# Lead -> runtime library binaries in the binary by_inst file (max of listed sonames is the primary value).
LEAD_BINARIES = {
    "libxmlb": ("libxmlb", ["libxmlb2", "libxmlb1"]),
    "libnxml": ("libnxml", ["libnxml0t64", "libnxml0"]),
    "iksemel": ("iksemel", ["libiksemel3"]),
    "glib2.0 (GMarkup)": ("glib2.0", ["libglib2.0-0t64", "libglib2.0-0"]),
    "libgsf": ("libgsf", ["libgsf-1-114"]),
    "qdbm (Cabin XML helpers)": ("qdbm", ["libqdbm14", "libqdbm14t64"]),
    "xmlrpc-epi": ("xmlrpc-epi", ["libxmlrpc-epi0", "libxmlrpc-epi0t64"]),
    "xmlrpc-c": ("xmlrpc-c", ["libxmlrpc-core-c3", "libxmlrpc-core-c3t64"]),
    "libstrophe": ("libstrophe", ["libstrophe0"]),
    "wbxml2": ("wbxml2", ["libwbxml2-0", "libwbxml2-1"]),
}
FORMAT_SPECIFIC_DEV = {"glib2.0 (GMarkup)": None}


def table(data: bytes) -> dict[str, dict]:
    rows = {}
    for line in gzip.decompress(data).decode("utf-8", "replace").splitlines():
        parts = line.split()
        if len(parts) >= 7 and all(p.isdigit() for p in (parts[0], *parts[2:7])):
            rows[parts[1]] = {"rank": int(parts[0]), "installed": int(parts[2]), "regular_use_votes": int(parts[3]),
                              "old": int(parts[4]), "recent": int(parts[5]), "no_files": int(parts[6])}
    return rows


def classify(name: str) -> tuple[str, str]:
    if name in C_XML_PARSERS:
        return "c_xml_parser_library", C_XML_PARSERS[name]
    if name in C_OTHER:
        return "not_general_c_xml_parser", C_OTHER[name]
    if name in CPP:
        return "cpp_not_this_cell", "C++ library or application; C++ cell, not C"
    if name in DATA:
        return "data_or_schema", "XML catalogs, DTDs or data; no parser"
    if name in OTHER_LANGUAGE:
        return "other_language", f"{OTHER_LANGUAGE[name]} package; not a C library"
    for _, pattern, language in PREFIXES:
        if pattern.search(name):
            return "other_language", f"{language} package; not a C library"
    raise SystemExit(f"unclassified Debian source hit: {name}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    snapshot = json.loads(SNAPSHOT.read_text())
    sourcemax_raw = SOURCEMAX.read_bytes()
    if sha256(sourcemax_raw).hexdigest() != SOURCEMAX_SHA256:
        raise SystemExit("sourcemax snapshot hash changed")
    binary_raw = Path(sys.argv[1]).read_bytes()
    if sha256(binary_raw).hexdigest() != snapshot["adoption_metric"]["sha256"]:
        raise SystemExit("binary by_inst file is not the cell's hashed adoption snapshot")
    sources, binaries = table(sourcemax_raw), table(binary_raw)
    hits = sorted(((row["rank"], name) for name, row in sources.items() if QUERY in name.lower()))
    records = []
    for position, (_, name) in enumerate(hits, 1):
        kind, reason = classify(name)
        records.append({"position": position, "name": name, **sources[name],
                        "classification": kind, "reason": reason})
    counts: dict[str, int] = {}
    for record in records:
        counts[record["classification"]] = counts.get(record["classification"], 0) + 1
    snapshot["debian_source_search"] = {
        "query": QUERY,
        "searched_at": SEARCHED_AT,
        "method": "case-insensitive substring 'xml' in Debian source-package names of the hashed sourcemax/by_inst table; ordered by installations; every hit recorded and classified",
        "source": "https://popcon.debian.org/sourcemax/by_inst.gz",
        "snapshot_file": "data/curation/popcon-sourcemax-by_inst.gz",
        "snapshot_sha256": SOURCEMAX_SHA256,
        "last_modified": snapshot["sourcemax_cross_check"]["last_modified"],
        "limit": None,
        "limit_note": "All hits are recorded and classified; the protocol's 100-result inspection bound is exceeded here, as in the C++ JSON Debian search, because the list is cheap to classify by name.",
        "total": len(records),
        "unique": len({record["name"] for record in records}),
        "classification_counts": dict(sorted(counts.items())),
        "hits": records,
    }
    snapshot["targeted_debian_lookups"] = {
        "searched_at": SEARCHED_AT,
        "method": "exact source-name lookup in the same hashed sourcemax table for C XML-related sources whose names do not contain 'xml'",
        "snapshot_sha256": SOURCEMAX_SHA256,
        "rows": [{"name": name, "note": note, "sourcemax": sources.get(name)} for name, note in TARGETED.items()],
    }
    candidates = snapshot["c_candidates"]
    for lead, (source, packages) in LEAD_BINARIES.items():
        rows = {package: binaries.get(package) for package in packages}
        present = [row["installed"] for row in rows.values() if row]
        candidates[lead] = {"conan_recipe": False, "debian_source": source,
                            "debian_binary_packages": rows,
                            "primary_installed": max(present) if present else None,
                            "debian_sourcemax": sources.get(source),
                            "homebrew_formula": None, "homebrew_install_365d": None,
                            "added_by": "scripts/search_c_xml_debian.py"}
    glib = candidates["glib2.0 (GMarkup)"]
    glib["primary_installed"] = None
    glib["primary_note"] = ("Unranked: glib2.0 builds all of GLib (GLib, GObject, GIO, GModule), so its "
                            "runtime counts are not XML-specific; Debian has no GMarkup-specific "
                            "development package, so the protocol's binary dev-package fallback has no row.")
    glib["libglib2.0-dev"] = binaries.get("libglib2.0-dev")
    SNAPSHOT.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"total": len(records), "counts": counts,
                      "leads": {k: v["primary_installed"] for k, v in candidates.items()}}))


if __name__ == "__main__":
    main()
