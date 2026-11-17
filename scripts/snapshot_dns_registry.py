"""Capture bounded registry searches and one adoption metric per lead for the DNS pilot.

Writes data/<ecosystem>/dns/registry-snapshot.json for the eight ecosystems.
Search hits and targeted names are leads only; nothing here verifies a parser.
Each query records its URL, the first <=100 hits, the reported total and the
capture time. Targeted names come from project documentation and are looked up
directly because registry search order is not an adoption order.

C and C++ use the pinned Debian popcon sourcemax table already in the
repository (data/curation/popcon-sourcemax-by_inst.gz) and the Conan Center
recipe tree. No DNS server, resolver or socket is used: only registry HTTPS APIs.

Usage: python3 scripts/snapshot_dns_registry.py [ecosystem ...]
(the macOS python.org build needs SSL_CERT_FILE=/etc/ssl/cert.pem)
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
import gzip
from hashlib import sha256
import html
import json
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 100
UA = "parsarium-pilot (registry metadata only)"
SOURCEMAX = ROOT / "data/curation/popcon-sourcemax-by_inst.gz"
SOURCEMAX_SHA256 = "9d5e341c8ede7267acab176e255be83aca763f09901477eef5324d644cdaebf8"

QUERIES = {
    "javascript": ["dns", "dns packet", "dns parser", "dns message"],
    "rust": ["dns", "dns parser", "dns packet", "dns message"],
    "php": ["dns", "dns parser", "dns message"],
    "java": ["dns", "dns codec", "dns message"],
    "go": ["dns", "dns message", "dns parser", "dns packet"],
}
# Targeted names from project documentation (looked up after the search).
LEADS = {
    "javascript": ["dns-packet", "@leichtgewicht/dns-packet", "dns2", "native-dns-packet", "dns-js",
                   "mdns-js-packet", "dns-message", "@dnsquery/dns-packet", "multicast-dns",
                   "@serverless-dns/dns-parser", "dnspacket-ts"],
    "python": ["dnspython", "dnslib", "dpkt", "scapy", "pycares", "aiodns", "py3dns", "dnslib-ng",
               "pypacker", "dnserver"],
    "rust": ["hickory-proto", "trust-dns-proto", "domain", "simple-dns", "dns-parser",
             "dns-message-parser", "rustdns", "dns_parse", "packet-dissector-dns", "dnsparse",
             "mdns-sd", "dns-protocol"],
    "php": ["react/dns", "daverandom/libdns", "amphp/dns", "pear/net_dns2", "mikepultz/netdns2",
            "purplepixie/phpdns", "yswery/dns", "jdwx/dns-query", "remotelyliving/php-dns",
            "spatie/dns", "badcow/dns", "appserver-io/dnsserver"],
    "java": ["dnsjava:dnsjava", "io.netty:netty-codec-dns", "org.minidns:minidns-core",
             "org.pcap4j:pcap4j-core", "io.vertx:vertx-core", "org.xbill:dnsjava",
             "de.measite.minidns:minidns-core"],
    "go": ["github.com/miekg/dns", "golang.org/x/net/dns/dnsmessage", "codeberg.org/miekg/dns",
           "github.com/google/gopacket/layers", "github.com/gopacket/gopacket/layers",
           "github.com/phuslu/fastdns", "github.com/coredns/coredns/plugin/pkg/dnsutil"],
    "c": ["c-ares", "ldns", "knot", "getdns", "udns", "adns", "unbound", "bind9", "libevent", "glibc",
          "musl", "libspf2"],
    "cpp": ["libtins", "pcapplusplus", "poco", "qtbase-opensource-src", "boost1.83", "asio",
            "pdns", "dnsdist", "pdns-recursor"],
}
SEARCH_HINTS = {
    "python": ["dns"],
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get(url: str, accept: str | None = None) -> bytes:
    headers = {"User-Agent": UA}
    if accept:
        headers["Accept"] = accept
    request = urllib.request.Request(url, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                data = response.read()
                if response.headers.get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)
                return data
        except urllib.error.HTTPError as error:
            if error.code in (429, 502, 503) and attempt < 4:
                time.sleep(5 * (attempt + 1))
                continue
            raise
        except (TimeoutError, OSError):
            if attempt == 4:
                raise
            time.sleep(3)
    raise AssertionError


def getj(url: str, accept: str | None = None):
    return json.loads(get(url, accept))


def guarded(function, *args):
    try:
        return function(*args)
    except Exception as error:  # recorded, not hidden
        return {"value": None, "error": repr(error), "captured_at_utc": now()}


def npm() -> dict:
    searches = []
    for query in QUERIES["javascript"]:
        url = f"https://registry.npmjs.org/-/v1/search?text={urllib.parse.quote(query)}&size={LIMIT}&from=0"
        body = getj(url)
        searches.append({"query": query, "url": url, "total": body.get("total"), "limit": LIMIT,
                         "captured_at_utc": now(), "ordering": "npm registry search default relevance order",
                         "hits": [{"rank": rank, "name": item["package"]["name"],
                                   "version": item["package"].get("version")}
                                  for rank, item in enumerate(body["objects"], 1)]})
    end = date.today() - timedelta(days=2)
    start = end - timedelta(days=29)
    window = f"{start.isoformat()}:{end.isoformat()}"

    def downloads(name: str) -> dict:
        url = f"https://api.npmjs.org/downloads/point/{window}/{urllib.parse.quote(name, safe='@')}"
        return {"downloads": getj(url).get("downloads"), "url": url, "captured_at_utc": now()}

    with ThreadPoolExecutor(6) as pool:
        packages = dict(zip(LEADS["javascript"], pool.map(lambda n: guarded(downloads, n), LEADS["javascript"])))
    return {"search_surface": "npm registry search API", "search_api_docs":
            "https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md", "search": searches,
            "download_metric": {"name": f"npm downloads, {window} (30 days)",
                                "documentation": "https://github.com/npm/registry/blob/main/docs/download-counts.md",
                                "packages": packages}}


def pypi() -> dict:
    url = "https://pypi.org/simple/"
    index = getj(url, "application/vnd.pypi.simple.v1+json")
    names = sorted((item["name"] for item in index["projects"]), key=str.lower)
    searches = []
    for needle in SEARCH_HINTS["python"]:
        matches = [name for name in names if needle in name.lower()]
        searches.append({"query": f"project name contains '{needle}'", "url": url, "total": len(matches),
                         "limit": LIMIT, "captured_at_utc": now(),
                         "ordering": "case-insensitive project-name order; not a popularity order",
                         "hits": [{"rank": rank, "name": name} for rank, name in enumerate(matches[:LIMIT], 1)]})
    known = {name.lower() for name in names}

    def downloads(name: str) -> dict:
        source = f"https://pypistats.org/api/packages/{name.lower()}/recent"
        time.sleep(1)
        body = getj(source)
        return {"downloads": body["data"]["last_month"], "url": source, "captured_at_utc": now(),
                "in_simple_index": name.lower() in known}

    packages = {name: guarded(downloads, name) for name in LEADS["python"]}
    return {"search_surface": "PyPI Simple JSON project-name index, filtered locally; no relevance ranking",
            "search_api_docs": "https://docs.pypi.org/api/index-api/",
            "search_index_serial": index.get("meta", {}).get("_last-serial"), "search": searches,
            "download_metric": {"name": "PyPI Stats last_month downloads excluding known mirrors",
                                "documentation": "https://pypistats.org/api/", "packages": packages}}


def crates() -> dict:
    searches = []
    for query in QUERIES["rust"]:
        url = f"https://crates.io/api/v1/crates?q={urllib.parse.quote(query)}&per_page={LIMIT}&page=1"
        body = getj(url)
        searches.append({"query": query, "url": url, "total": body["meta"]["total"], "limit": LIMIT,
                         "captured_at_utc": now(), "ordering": "crates.io default (relevance) order",
                         "hits": [{"rank": rank, "name": item["name"],
                                   "version": item.get("max_stable_version") or item.get("max_version"),
                                   "recent_downloads_90d": item.get("recent_downloads")}
                                  for rank, item in enumerate(body["crates"], 1)]})
        time.sleep(1)

    def crate(name: str) -> dict:
        url = f"https://crates.io/api/v1/crates/{name}"
        body = getj(url)["crate"]
        time.sleep(1)
        return {"recent_downloads": body.get("recent_downloads"), "downloads": body.get("downloads"),
                "max_stable_version": body.get("max_stable_version"), "url": url, "captured_at_utc": now()}

    packages = {name: guarded(crate, name) for name in LEADS["rust"]}
    return {"search_surface": "crates.io API first page, default registry order",
            "search_api_docs": "https://crates.io/data-access", "search": searches,
            "popularity_metric": {"name": "crates.io recent_downloads (90 days)", "packages": packages}}


def packagist() -> dict:
    searches = []
    for query in QUERIES["php"]:
        url = f"https://packagist.org/search.json?q={urllib.parse.quote(query)}&per_page={LIMIT}"
        body = getj(url)
        searches.append({"query": query, "url": url, "total": body.get("total"), "limit": LIMIT,
                         "captured_at_utc": now(), "ordering": "Packagist search default order",
                         "hits": [{"rank": rank, "name": item["name"], "downloads": item.get("downloads")}
                                  for rank, item in enumerate(body["results"], 1)]})

    def package(name: str) -> dict:
        url = f"https://packagist.org/packages/{name}.json"
        body = getj(url)["package"]
        return {"downloads": body["downloads"]["total"], "url": url, "captured_at_utc": now(),
                "abandoned": body.get("abandoned", False)}

    packages = {name: guarded(package, name) for name in LEADS["php"]}
    return {"search_surface": "Packagist public search JSON API", "search_api_docs": "https://packagist.org/apidoc",
            "search": searches,
            "download_metric": {"name": "Packagist total downloads", "packages": packages}}


def maven() -> dict:
    searches = []
    for query in QUERIES["java"]:
        url = f"https://search.maven.org/solrsearch/select?q={urllib.parse.quote(query)}&rows={LIMIT}&wt=json"
        body = getj(url)["response"]
        searches.append({"query": query, "url": url, "total": body["numFound"], "limit": LIMIT,
                         "captured_at_utc": now(), "ordering": "Maven Central Solr default order",
                         "hits": [{"rank": rank, "name": doc["id"], "latest_version": doc.get("latestVersion")}
                                  for rank, doc in enumerate(body["docs"], 1)]})

    def deps_dev(coordinate: str) -> dict:
        name = urllib.parse.quote(coordinate, safe="")
        base = f"https://api.deps.dev/v3alpha/systems/MAVEN/packages/{name}"
        versions = getj(base)["versions"]
        default = [item["versionKey"]["version"] for item in versions if item.get("isDefault")]

        def count(version: str) -> tuple[str, int]:
            url = f"{base}/versions/{urllib.parse.quote(version, safe='')}:dependents"
            try:
                return version, getj(url).get("directDependentCount", 0)
            except urllib.error.HTTPError as error:
                if error.code == 404:  # version unknown to the dependents index
                    return version, 0
                raise

        with ThreadPoolExecutor(12) as pool:
            counts = dict(pool.map(count, [item["versionKey"]["version"] for item in versions]))
        peak = max(counts, key=counts.get)
        return {"direct_dependent_count": sum(counts.values()), "releases": len(counts),
                "default_version": default[0] if default else None,
                "max_release": peak, "max_release_direct_dependent_count": counts[peak],
                "default_release_direct_dependent_count": counts.get(default[0]) if default else None,
                "url": base, "captured_at_utc": now()}

    packages = {coordinate: guarded(deps_dev, coordinate) for coordinate in LEADS["java"]}
    return {"search_surface": "Maven Central Solr artifact search; targeted deps.dev lookups",
            "search_api_docs": "https://central.sonatype.org/search/rest-api-guide/", "search": searches,
            "popularity_metric": {"name": "deps.dev directDependentCount summed over all releases",
                                  "documentation": "https://docs.deps.dev/api/v3alpha/",
                                  "packages": packages}}


def gopkg() -> dict:
    searches = []
    for query in QUERIES["go"]:
        url = f"https://pkg.go.dev/search?q={urllib.parse.quote(query)}&limit={LIMIT}&m=package"
        page = get(url).decode("utf-8", "replace")
        hits = []
        for block in page.split('class="SearchSnippet"')[1:]:
            match = re.search(r'data-clicked-package="([^"]+)"', block) or \
                re.search(r'data-test-id="snippet-title"[^>]*href="/([^"?]+)', block)
            if not match:
                continue
            imported = re.search(r'Imported by[\s\S]*?<strong>([\d,]+)</strong>', block)
            hits.append({"rank": len(hits) + 1, "packagePath": html.unescape(match.group(1)),
                         "imported_by": int(imported.group(1).replace(",", "")) if imported else None})
        searches.append({"query": query, "url": url, "total": None, "limit": LIMIT, "captured_at_utc": now(),
                         "total_note": "The HTML page does not state a total result count.",
                         "ordering": "pkg.go.dev search relevance order", "hits": hits[:LIMIT]})
        time.sleep(2)

    def imported_by(path: str) -> dict:
        url = f"https://pkg.go.dev/{path}?tab=importedby"
        page = get(url).decode("utf-8", "replace")
        match = re.search(r'Known importing packages:</strong>\s*([\d,]+)', page)
        modules = re.search(r'Known importing modules:</strong>\s*([\d,]+)', page)
        time.sleep(2)
        return {"imported_by_packages": int(match.group(1).replace(",", "")) if match else None,
                "importing_modules": int(modules.group(1).replace(",", "")) if modules else None,
                "url": url, "captured_at_utc": now()}

    packages = {path: guarded(imported_by, path) for path in LEADS["go"]}
    return {"search_surface": "pkg.go.dev public HTML package search", "search_api_docs": "https://pkg.go.dev/search-help",
            "search": searches,
            "popularity_metric": {"name": "pkg.go.dev Imported by package count", "packages": packages}}


def popcon(ecosystem: str) -> dict:
    raw = SOURCEMAX.read_bytes()
    if sha256(raw).hexdigest() != SOURCEMAX_SHA256:
        raise ValueError("pinned popcon sourcemax table changed")
    rows = {}
    for line in gzip.decompress(raw).decode().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        fields = line.split()
        if len(fields) >= 7 and fields[0].isdigit() and all(item.isdigit() for item in fields[2:7]):
            rows[fields[1]] = {"rank": int(fields[0]), "installed": int(fields[2]), "vote": int(fields[3]),
                               "old": int(fields[4]), "recent": int(fields[5]), "no_files": int(fields[6])}
    matches = sorted((name for name in rows if "dns" in name.lower()), key=lambda name: rows[name]["rank"])
    tree_url = "https://api.github.com/repos/conan-io/conan-center-index/git/trees/master"
    root = getj(tree_url)
    recipes_entry, = [item for item in root["tree"] if item["path"] == "recipes"]
    recipes = sorted(item["path"] for item in getj(recipes_entry["url"])["tree"])
    conan = [name for name in recipes if "dns" in name.lower()]
    return {
        "search_surface": "Debian popcon sourcemax source-package names (pinned table) and the Conan Center recipe tree",
        "search": [
            {"query": "debian-source:dns", "method": "case-insensitive substring 'dns' in Debian source-package names "
             "of the pinned popcon sourcemax table, first 100 in popcon rank order",
             "url": "https://popcon.debian.org/sourcemax/by_inst.gz", "total": len(matches), "limit": LIMIT,
             "captured_at_utc": now(),
             "hits": [{"rank": index, "name": name, "popcon_rank": rows[name]["rank"],
                       "installed": rows[name]["installed"]} for index, name in enumerate(matches[:LIMIT], 1)]},
            {"query": "conan:dns", "method": "case-insensitive substring 'dns' in Conan Center recipe names; alphabetic",
             "url": recipes_entry["url"], "conan_master_commit": root["sha"], "recipe_count": len(recipes),
             "total": len(conan), "limit": LIMIT, "captured_at_utc": now(),
             "hits": [{"rank": index, "name": name, "url": f"https://conan.io/center/recipes/{name}"}
                      for index, name in enumerate(conan[:LIMIT], 1)]},
            {"query": f"targeted {ecosystem} DNS message sources",
             "method": "exact Debian source-package and Conan recipe-name lookup of documented DNS message libraries",
             "total": len(LEADS[ecosystem]), "limit": LIMIT, "captured_at_utc": now(),
             "hits": [{"rank": index, "name": name, "debian_source_present": name in rows,
                       "conan_recipe_present": name in recipes}
                      for index, name in enumerate(LEADS[ecosystem], 1)]},
        ],
        "popularity_metric": {
            "name": "Debian popcon sourcemax installations (max over binary packages built from the source package)",
            "url": "https://popcon.debian.org/sourcemax/by_inst.gz",
            "snapshot": "data/curation/popcon-sourcemax-by_inst.gz", "sha256": SOURCEMAX_SHA256,
            "packages": {name: ({"installed": rows[name]["installed"], "rank": rows[name]["rank"]}
                                if name in rows else {"installed": None, "reason": "no Debian source package"})
                         for name in LEADS[ecosystem]}},
    }


CAPTURES = {"javascript": npm, "python": pypi, "rust": crates, "php": packagist, "java": maven, "go": gopkg,
            "c": lambda: popcon("c"), "cpp": lambda: popcon("cpp")}


def main() -> None:
    for ecosystem in sys.argv[1:] or CAPTURES:
        started = now()
        snapshot = {"ecosystem": ecosystem, "format": "dns", "captured_at_utc": started,
                    "search_limit_per_query": LIMIT,
                    "note": "Search hits and targeted names are leads, not verified parsers. No DNS server was queried.",
                    **CAPTURES[ecosystem]()}
        out = ROOT / "data" / ecosystem / "dns" / "registry-snapshot.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        previous = json.loads(out.read_text()) if out.is_file() else {}
        for key in ("releases",):  # release pins are added by verification commits
            if key in previous:
                snapshot[key] = previous[key]
        out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
        print(ecosystem, [(item["query"], item.get("total"), len(item["hits"])) for item in snapshot["search"]])


if __name__ == "__main__":
    main()
