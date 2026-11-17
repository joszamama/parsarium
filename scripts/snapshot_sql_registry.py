"""Capture bounded registry searches and the primary adoption metric for the SQL pilot.

Writes data/<ecosystem>/sql/registry-snapshot.json for the eight ecosystems.
Each query records its URL, total, the first <=100 hits and a timestamp. The
metric for each lead is the ecosystem's existing primary source, the same one
the JSON and XML pilot cells use: npm last-month downloads, PyPI Stats
last_month, crates.io recent (90-day) downloads, Packagist total downloads,
pkg.go.dev "Imported by", deps.dev directDependentCount summed over Maven
releases, and Debian popcon sourcemax installations for C and C++ (from the
pinned snapshot in data/curation). Search hits are leads, not verified parsers.

Usage: python3 scripts/snapshot_sql_registry.py [ECOSYSTEM ...]
The python.org macOS build needs SSL_CERT_FILE=/etc/ssl/cert.pem.
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
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
UA = "parsarium-research (sql pilot)"
POPCON = ROOT / "data/curation/popcon-sourcemax-by_inst.gz"

QUERIES = {
    "javascript": ["sql parser", "sql ast", "sqlparser"],
    "python": ["sqlpars", "sqlglot", "sql-ast", "pg-query", "pglast"],
    "rust": ["sql parser", "sqlparser", "sql ast"],
    "php": ["sql parser", "sql-parser", "sqlparser"],
    "go": ["sql parser", "sqlparser", "sql ast"],
    "java": ["sql parser", "sqlparser", "jsqlparser"],
    "c": ["sql"],
    "cpp": ["sql"],
}
# Targeted documentation leads looked up after the search, because registry
# relevance order is not an adoption order.
LEADS = {
    "javascript": ["node-sql-parser", "pgsql-ast-parser", "sql-parser-cst", "libpg-query",
                   "@pgsql/parser", "pg-query-emscripten", "sqlite-parser", "js-sql-parser",
                   "dt-sql-parser", "sql-parser", "@florajs/sql-parser", "sql-formatter",
                   "@guanmingchiu/sqlparser-ts", "sql-ddl-to-json-schema", "pg-query-parser"],
    "python": ["sqlparse", "sqlglot", "pglast", "mo-sql-parsing", "sql-metadata", "sqloxide",
               "sqlfluff", "simple-ddl-parser", "sqltree", "psqlparse", "pg-query", "sqlglotrs",
               "sql-formatter", "moz-sql-parser"],
    "rust": ["sqlparser", "pg_query", "sqlite3-parser", "nom-sql", "sql-parse", "sqlformat",
             "datafusion-sql", "gluesql-core", "sqlparser_derive", "polyglot-sql", "sql_query_builder"],
    "php": ["phpmyadmin/sql-parser", "greenlion/php-sql-parser", "doctrine/sql-formatter",
            "jdorn/sql-formatter", "iamcal/sql-parser", "udfs/php-sql-parser",
            "sqlftw/sqlftw", "cweagans/sql-parser"],
    "go": ["vitess.io/vitess/go/vt/sqlparser", "github.com/pingcap/tidb/pkg/parser",
           "github.com/pingcap/parser", "github.com/pganalyze/pg_query_go/v6",
           "github.com/xwb1989/sqlparser", "github.com/blastrain/vitess-sqlparser/sqlparser",
           "github.com/auxten/postgresql-parser/pkg/sql/parser",
           "github.com/AfterShip/clickhouse-sql-parser/parser",
           "github.com/rqlite/sql", "github.com/cockroachdb/cockroachdb-parser/pkg/sql/parser",
           "github.com/krasun/gosqlparser", "github.com/akito0107/xsqlparser"],
    "java": ["com.github.jsqlparser:jsqlparser", "org.apache.calcite:calcite-core",
             "io.trino:trino-parser", "com.facebook.presto:presto-parser",
             "com.alibaba:druid", "org.jooq:jooq", "com.github.vertical-blank:sql-formatter",
             "org.apache.shardingsphere:shardingsphere-sql-parser-engine",
             "net.sf.jsqlparser:jsqlparser", "io.prestosql:presto-parser",
             "org.apache.spark:spark-catalyst_2.13"],
    "c": ["sqlite3", "libpg-query", "libgda5", "postgresql-18", "sqlcipher", "duckdb"],
    "cpp": ["duckdb", "libpg-query", "soci", "cppdb", "libodb", "mysql++", "libvsqlitepp"],
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get(url: str, accept: str | None = None) -> bytes:
    headers = {"User-Agent": UA, **({"Accept": accept} if accept else {})}
    request = urllib.request.Request(url, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                data = response.read()
                if response.headers.get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)
                return data
        except urllib.error.HTTPError as error:
            if error.code in (429, 502, 503) and attempt < 4:
                time.sleep(5 * (attempt + 1))
                continue
            raise
        except (TimeoutError, urllib.error.URLError):
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
        return {"value": None, "error": repr(error)[:300]}


# ---------------------------------------------------------------- searches

def search_npm(query):
    url = f"https://registry.npmjs.org/-/v1/search?text={urllib.parse.quote(query)}&size={LIMIT}&from=0"
    body = getj(url)
    return {"url": url, "total": body.get("total"), "ordering": "npm search default relevance",
            "hits": [{"rank": i, "name": o["package"]["name"], "version": o["package"].get("version"),
                      "description": (o["package"].get("description") or "")[:160]}
                     for i, o in enumerate(body["objects"][:LIMIT], 1)]}


_PYPI_NAMES = None


def search_pypi(needle):
    global _PYPI_NAMES
    url = "https://pypi.org/simple/"
    if _PYPI_NAMES is None:
        body = getj(url, "application/vnd.pypi.simple.v1+json")
        _PYPI_NAMES = sorted((p["name"] for p in body["projects"]), key=str.lower)
    matches = [name for name in _PYPI_NAMES
               if needle in re.sub(r"[-_.]+", "-", name.lower())]
    return {"url": url, "query_method": f"normalized project name contains '{needle}'",
            "total": len(matches), "ordering": "case-insensitive name order; not a popularity order",
            "hits": [{"rank": i, "name": name} for i, name in enumerate(matches[:LIMIT], 1)]}


def search_crates(query):
    url = f"https://crates.io/api/v1/crates?q={urllib.parse.quote(query)}&per_page={LIMIT}&page=1"
    body = getj(url)
    time.sleep(1)
    return {"url": url, "total": body["meta"]["total"], "ordering": "crates.io default relevance",
            "hits": [{"rank": i, "name": c["name"],
                      "version": c.get("max_stable_version") or c.get("max_version"),
                      "description": (c.get("description") or "")[:160],
                      "recent_downloads": c.get("recent_downloads")}
                     for i, c in enumerate(body["crates"], 1)]}


def search_packagist(query):
    url = f"https://packagist.org/search.json?q={urllib.parse.quote(query)}&per_page={LIMIT}"
    body = getj(url)
    return {"url": url, "total": body.get("total"), "ordering": "Packagist search default order",
            "hits": [{"rank": i, "name": r["name"], "downloads": r.get("downloads"),
                      "description": (r.get("description") or "")[:160]}
                     for i, r in enumerate(body["results"][:LIMIT], 1)]}


def search_go(query):
    url = f"https://pkg.go.dev/search?q={urllib.parse.quote(query)}&limit={LIMIT}&m=package"
    page = get(url).decode("utf-8", "replace")
    hits = []
    for block in page.split('class="SearchSnippet"')[1:]:
        match = re.search(r'data-clicked-package="([^"]+)"', block)
        if not match:
            continue
        imported = re.search(r'Imported by[\s\S]*?<strong>([\d,]+)</strong>', block)
        hits.append({"rank": len(hits) + 1, "name": html.unescape(match.group(1)),
                     "imported_by": int(imported.group(1).replace(",", "")) if imported else None})
    time.sleep(2)
    return {"url": url, "total": None, "total_note": "pkg.go.dev shows no total count",
            "ordering": "pkg.go.dev search relevance", "hits": hits[:LIMIT]}


def search_maven(query):
    url = f"https://search.maven.org/solrsearch/select?q={urllib.parse.quote(query)}&rows={LIMIT}&wt=json"
    body = getj(url)["response"]
    return {"url": url, "total": body["numFound"], "ordering": "Maven Central Solr default order",
            "hits": [{"rank": i, "name": doc["id"], "latest_version": doc.get("latestVersion")}
                     for i, doc in enumerate(body["docs"], 1)]}


def popcon_rows():
    rows = {}
    for line in gzip.decompress(POPCON.read_bytes()).decode("utf-8", "replace").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 3 and parts[0].isdigit() and parts[2].isdigit():
            rows[parts[1]] = {"rank": int(parts[0]), "inst": int(parts[2])}
    return rows


def search_popcon(needle):
    rows = popcon_rows()
    matches = sorted((name for name in rows if needle in name), key=lambda n: rows[n]["rank"])
    return {"url": "data/curation/popcon-sourcemax-by_inst.gz",
            "snapshot_sha256": sha256(POPCON.read_bytes()).hexdigest(),
            "query_method": f"Debian source package name contains '{needle}', popcon rank order",
            "total": len(matches), "ordering": "popcon sourcemax installation rank",
            "hits": [{"rank": i, "name": name, "popcon_inst": rows[name]["inst"]}
                     for i, name in enumerate(matches[:LIMIT], 1)]}


SEARCH = {"javascript": search_npm, "python": search_pypi, "rust": search_crates,
          "php": search_packagist, "go": search_go, "java": search_maven,
          "c": search_popcon, "cpp": search_popcon}

# ---------------------------------------------------------------- metrics


def metric_npm(name):
    url = f"https://api.npmjs.org/downloads/point/last-month/{urllib.parse.quote(name, safe='@/')}"
    body = getj(url)
    latest = getj(f"https://registry.npmjs.org/{urllib.parse.quote(name, safe='@')}/latest")
    return {"value": body["downloads"], "window": [body.get("start"), body.get("end")],
            "latest_version": latest.get("version"), "license": latest.get("license"), "url": url}


def metric_pypi(name):
    url = f"https://pypistats.org/api/packages/{name.lower()}/recent"
    info = getj(f"https://pypi.org/pypi/{name}/json")["info"]
    time.sleep(1.5)
    return {"value": getj(url)["data"]["last_month"], "latest_version": info["version"],
            "summary": (info.get("summary") or "")[:160], "url": url}


def metric_crates(name):
    url = f"https://crates.io/api/v1/crates/{name}"
    crate = getj(url)["crate"]
    time.sleep(1)
    return {"value": crate.get("recent_downloads"),
            "latest_version": crate.get("max_stable_version") or crate.get("max_version"),
            "description": (crate.get("description") or "")[:160], "url": url}


def metric_packagist(name):
    url = f"https://packagist.org/packages/{name}.json"
    package = getj(url)["package"]
    return {"value": package["downloads"]["total"], "url": url,
            "description": (package.get("description") or "")[:160]}


def metric_go(name):
    url = f"https://pkg.go.dev/{name}"
    page = get(url).decode("utf-8", "replace")
    imported = re.search(r'aria-label="Imported By: ([\d,]+)"', page)
    version = re.search(r'data-test-id="UnitHeader-version"[\s\S]*?Version:\s*</span>\s*([^\s<]+)', page)
    time.sleep(2)
    if not imported:
        raise LookupError("Imported By count not found")
    return {"value": int(imported.group(1).replace(",", "")),
            "latest_version": version.group(1) if version else None, "url": url}


def metric_maven(coordinate):
    name = urllib.parse.quote(coordinate, safe="")
    base = f"https://api.deps.dev/v3alpha/systems/MAVEN/packages/{name}"
    versions = getj(base)["versions"]
    default = [v["versionKey"]["version"] for v in versions if v.get("isDefault")]

    def count(version):
        url = f"{base}/versions/{urllib.parse.quote(version, safe='')}:dependents"
        try:
            return version, getj(url)["directDependentCount"]
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return version, 0
            raise

    with ThreadPoolExecutor(12) as pool:
        counts = dict(pool.map(count, [v["versionKey"]["version"] for v in versions]))
    peak = max(counts, key=counts.get)
    return {"value": sum(counts.values()), "releases": len(counts),
            "default_version": default[0] if default else None,
            "max_release": peak, "max_release_direct_dependent_count": counts[peak],
            "url": base}


def metric_popcon(name):
    row = popcon_rows().get(name)
    if row is None:
        return {"value": None, "error": "no Debian source package of this name in the snapshot"}
    return {"value": row["inst"], "popcon_rank": row["rank"],
            "url": "https://popcon.debian.org/sourcemax/by_inst.gz",
            "snapshot": "data/curation/popcon-sourcemax-by_inst.gz",
            "snapshot_sha256": sha256(POPCON.read_bytes()).hexdigest()}


METRIC = {
    "javascript": ("npm downloads, last month", metric_npm),
    "python": ("PyPI Stats last_month downloads (mirrors excluded)", metric_pypi),
    "rust": ("crates.io recent_downloads (trailing 90 days)", metric_crates),
    "php": ("Packagist total downloads", metric_packagist),
    "go": ("pkg.go.dev Imported by package count", metric_go),
    "java": ("deps.dev directDependentCount summed over every Maven release", metric_maven),
    "c": ("Debian popcon sourcemax installations by source package (pinned snapshot)", metric_popcon),
    "cpp": ("Debian popcon sourcemax installations by source package (pinned snapshot)", metric_popcon),
}


def capture(ecosystem: str) -> dict:
    snapshot = {"ecosystem": ecosystem, "format": "sql", "captured_at_utc": now(),
                "search_limit_per_query": LIMIT,
                "note": "Search hits are leads, not verified parsers.", "search": []}
    for query in QUERIES[ecosystem]:
        started = now()
        try:
            entry = SEARCH[ecosystem](query)
        except Exception as error:
            entry = {"error": repr(error)[:300]}
        snapshot["search"].append({"query": query, "captured_at_utc": started, "limit": LIMIT, **entry})
    name, function = METRIC[ecosystem]
    snapshot["metric"] = {"name": name, "captured_at_utc": now(),
                          "comparability": "Compared only among SQL leads of this ecosystem.",
                          "leads": {lead: {**guarded(function, lead), "observed_at_utc": now()}
                                    for lead in LEADS[ecosystem]}}
    return snapshot


def main() -> None:
    for ecosystem in sys.argv[1:] or list(QUERIES):
        snapshot = capture(ecosystem)
        out = ROOT / "data" / ecosystem / "sql" / "registry-snapshot.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
        print(ecosystem, [(s["query"], s.get("total"), len(s.get("hits", [])), s.get("error"))
                          for s in snapshot["search"]])
        for lead, row in sorted(snapshot["metric"]["leads"].items(),
                                key=lambda pair: -(pair[1].get("value") or -1)):
            print(f"  {row.get('value')!s:>12}  {lead}  {row.get('latest_version') or row.get('default_version') or ''} {row.get('error') or ''}")


if __name__ == "__main__":
    main()
