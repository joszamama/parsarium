#!/usr/bin/env python3
"""Capture bounded YAML registry searches and one primary adoption metric per lead.

Writes data/<ecosystem>/yaml/registry-snapshot.json for the eight ecosystems.
Search hits and named leads are leads only; nothing captured here verifies a
parser. Each ecosystem uses the primary metric source of its existing JSON and
XML pilot cells:

  c, cpp      Debian popcon sourcemax/by_inst installations, from the pinned
              data/curation/popcon-sourcemax-by_inst.gz snapshot
  go          pkg.go.dev "Imported by" package count
  java        deps.dev directDependentCount summed over every Maven release
  javascript  npm downloads, last month
  python      PyPI Stats last_month downloads excluding mirrors
  rust        crates.io recent_downloads (90 days)
  php         Packagist lifetime downloads

Usage: python3 scripts/capture_yaml_registry.py [ecosystem ...]
(macOS python.org builds need SSL_CERT_FILE=/etc/ssl/cert.pem.)
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import gzip
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import time
import urllib.parse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import capture_expansion_registry as registry  # noqa: E402

registry.UA = "parsarium-research (yaml pilot inventory)"

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 100
POPCON = ROOT / "data/curation/popcon-sourcemax-by_inst.gz"
QUERIES = {"yaml": ["yaml"]}

# Named leads per ecosystem: registry identifier -> (family, documented input API hint, note).
# A lead is not verified until its pinned release passes the YAML pilot gate.
LEADS = {
    "c": {
        "libyaml": ("libyaml", "yaml_parser_set_input_string + yaml_parser_load / yaml_parser_parse", None),
        "libfyaml": ("libfyaml", "fy_document_build_from_string / fy_parser_parse", None),
        "libcyaml": ("libyaml", "cyaml_load_data", "Schema-driven loader over libyaml; needs a C schema per document shape."),
    },
    "cpp": {
        "yaml-cpp": ("yaml-cpp", "YAML::Load(std::string) / YAML::Load(std::istream&)", None),
        "rapidyaml": ("rapidyaml (ryml)", "ryml::parse_in_arena(csubstr)", "Not packaged in Debian; no primary popcon value."),
        "fkyaml": ("fkYAML", "fkyaml::node::deserialize", "Not packaged in Debian; no primary popcon value."),
    },
    "go": {
        "gopkg.in/yaml.v3": ("go-yaml v3", "yaml.Unmarshal([]byte, *yaml.Node)", None),
        "gopkg.in/yaml.v2": ("go-yaml v2", "yaml.Unmarshal([]byte, *interface{})", "YAML 1.1 resolver."),
        "github.com/goccy/go-yaml": ("goccy/go-yaml", "yaml.Unmarshal / parser.ParseBytes", None),
        "sigs.k8s.io/yaml": ("go-yaml (forked goyaml.v2) via JSON conversion", "yaml.YAMLToJSON / yaml.Unmarshal", "Wrapper over a vendored go-yaml fork; shared family."),
        "github.com/ghodss/yaml": ("go-yaml v2 via JSON conversion", "yaml.YAMLToJSON", "Wrapper over go-yaml v2; shared family."),
        "go.yaml.in/yaml/v3": ("go-yaml v3", "yaml.Unmarshal([]byte, *yaml.Node)", "YAML organization continuation of gopkg.in/yaml.v3; shared family."),
    },
    "java": {
        "org.yaml:snakeyaml": ("SnakeYAML", "new Yaml(new SafeConstructor(...)).load(String/InputStream)", "YAML 1.1 resolver."),
        "org.snakeyaml:snakeyaml-engine": ("SnakeYAML Engine", "new Load(LoadSettings).loadFromString", "YAML 1.2 core schema."),
        "com.fasterxml.jackson.dataformat:jackson-dataformat-yaml": ("SnakeYAML (Engine in 3.x) via Jackson", "YAMLMapper.readTree", "Jackson data format over SnakeYAML; shared family."),
        "com.esotericsoftware.yamlbeans:yamlbeans": ("YamlBeans", "new YamlReader(Reader).read()", None),
        "com.amihaiemil.web:eo-yaml": ("eo-yaml", "Yaml.createYamlInput(String).readYamlMapping()", None),
    },
    "javascript": {
        "js-yaml": ("js-yaml", "yaml.load(string)", None),
        "yaml": ("eemeli/yaml", "YAML.parse(string) / parseDocument", None),
        "yaml-ast-parser": ("yaml-ast-parser (js-yaml fork)", "load(string) AST", "Fork of js-yaml 3.x; shared lineage."),
        "yamljs": ("yamljs", "YAML.parse(string)", None),
        "@stoplight/yaml": ("yaml-ast-parser (js-yaml fork)", "parseWithPointers(string)", "Wraps @stoplight/yaml-ast-parser; shared lineage."),
    },
    "python": {
        "PyYAML": ("PyYAML pure Python (CLoader is the libyaml family)", "yaml.safe_load(str/bytes/stream)", "YAML 1.1 resolver; the pure SafeLoader and the C-accelerated CSafeLoader are separate paths."),
        "ruamel.yaml": ("ruamel.yaml (PyYAML-derived, YAML 1.2)", "YAML(typ='safe', pure=True).load", "Derived from PyYAML; ruamel.yaml.clib is its optional libyaml-derived C loader."),
        "strictyaml": ("ruamel.yaml via strictyaml", "strictyaml.load(str)", "Wraps ruamel.yaml; returns strings unless a schema types them."),
        "oyaml": ("PyYAML", "oyaml.safe_load", "Ordered-dict shim over PyYAML; shared family."),
        "yamlcore": ("PyYAML with YAML 1.2 core resolver", "yamlcore.CoreLoader", "Resolver subclass of PyYAML; shared family."),
        "rapidyaml": ("rapidyaml (ryml)", "ryml.parse_in_arena", "Python binding of C++ rapidyaml."),
    },
    "rust": {
        "serde_yaml": ("unsafe-libyaml (libyaml translation)", "serde_yaml::from_str::<Value>", "Archived upstream; libyaml port via unsafe-libyaml."),
        "yaml-rust": ("yaml-rust", "YamlLoader::load_from_str", "Unmaintained; continued as yaml-rust2."),
        "yaml-rust2": ("yaml-rust2 (yaml-rust lineage)", "YamlLoader::load_from_str", None),
        "saphyr": ("saphyr (yaml-rust2 lineage)", "Yaml::load_from_str", None),
        "saphyr-parser": ("saphyr (yaml-rust2 lineage)", "Parser::new_from_str event stream", None),
        "serde_yml": ("libyml (libyaml translation)", "serde_yml::from_str::<Value>", "Fork of serde_yaml."),
        "unsafe-libyaml": ("unsafe-libyaml (libyaml translation)", "yaml_parser_parse", "c2rust translation of libyaml."),
        "serde_norway": ("unsafe-libyaml-norway (libyaml translation)", "serde_norway::from_str::<Value>", "Fork of serde_yaml."),
        "serde-saphyr": ("saphyr-parser", "serde_saphyr::from_str", None),
        "marked-yaml": ("yaml-rust2 lineage", "marked_yaml::parse_yaml", None),
    },
    "php": {
        "symfony/yaml": ("Symfony Yaml Parser", "Symfony\\Component\\Yaml\\Yaml::parse(string)", None),
        "mustangostang/spyc": ("Spyc", "Spyc::YAMLLoadString(string)", None),
        "dallgoot/yaml": ("dallgoot/yaml", "Yaml::parse(string)", None),
        "pecl/yaml": ("libyaml via PECL ext-yaml", "yaml_parse(string)", "PECL extension, not a Composer package; no Packagist metric. Third-party libyaml-family binding."),
    },
}

DEBIAN = {  # lead -> Debian source package in the sourcemax table
    "libyaml": "libyaml", "libfyaml": "libfyaml", "libcyaml": "libcyaml",
    "yaml-cpp": "yaml-cpp", "rapidyaml": "rapidyaml", "fkyaml": "fkyaml",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def popcon_rows() -> list[dict]:
    rows = []
    for line in gzip.decompress(POPCON.read_bytes()).decode("utf-8", "replace").splitlines():
        if line.startswith("#") or line.startswith("-") or not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 7 and all(part.isdigit() for part in (parts[0], *parts[2:7])):
            rows.append({"rank": int(parts[0]), "source": parts[1], "inst": int(parts[2]),
                         "vote": int(parts[3]), "old": int(parts[4]), "recent": int(parts[5]),
                         "no_files": int(parts[6])})
    return rows


def debian(eco: str) -> dict:
    rows = popcon_rows()
    by_name = {row["source"]: row for row in rows}
    hits = [row for row in rows if "yaml" in row["source"].lower()]
    metrics = {}
    for lead in LEADS[eco]:
        row = by_name.get(DEBIAN[lead])
        metrics[lead] = {"debian_source": DEBIAN[lead], "value": row["inst"] if row else None,
                         "error": None if row else "no Debian source package of this name in the snapshot"}
    return {"search_surface": "Debian popcon sourcemax/by_inst source-package names (pinned snapshot), shared by C and C++",
            "search": [{"query": "yaml", "method": "case-insensitive substring 'yaml' in Debian source-package names; ordered by installations",
                        "url": "https://popcon.debian.org/sourcemax/by_inst.gz",
                        "snapshot_file": "data/curation/popcon-sourcemax-by_inst.gz",
                        "snapshot_sha256": sha256(POPCON.read_bytes()).hexdigest(),
                        "total": len(hits), "limit": LIMIT, "hits": hits[:LIMIT]}],
            "metric": {"name": "Debian popcon sourcemax/by_inst installations of the lead's source package",
                       "source": "data/curation/popcon-sourcemax-by_inst.gz",
                       "limitation": "Package installations, often transitive (libyaml is pulled in by PyYAML and Ruby); not YAML-specific use and blind to vendored copies."},
            "metrics": metrics}


def deps_dev(coordinate: str) -> dict:
    name = urllib.parse.quote(coordinate, safe="")
    base = f"https://api.deps.dev/v3alpha/systems/MAVEN/packages/{name}"
    versions = registry.getj(base)["versions"]
    default, = [item["versionKey"]["version"] for item in versions if item.get("isDefault")]

    def count(version: str) -> tuple[str, int]:
        url = f"{base}/versions/{urllib.parse.quote(version, safe='')}:dependents"
        return version, registry.getj(url).get("directDependentCount", 0)

    with ThreadPoolExecutor(8) as pool:
        counts = dict(pool.map(count, [item["versionKey"]["version"] for item in versions]))
    peak = max(counts, key=counts.get)
    return {"value": sum(counts.values()), "default_version": default, "releases": len(counts),
            "max_release": peak, "max_release_direct_dependent_count": counts[peak],
            "default_release_direct_dependent_count": counts[default], "url": base}


def metric(eco: str, lead: str, hits: dict) -> dict:
    if eco == "javascript":
        url = f"https://api.npmjs.org/downloads/point/last-month/{urllib.parse.quote(lead, safe='@/')}"
        data = registry.getj(url)
        return {"value": data["downloads"], "window": [data["start"], data["end"]], "url": url}
    if eco == "python":
        url = f"https://pypistats.org/api/packages/{lead.lower()}/recent?period=month"
        release = registry.getj(f"https://pypi.org/pypi/{lead}/json")["info"]["version"]
        return {"value": registry.getj(url)["data"]["last_month"], "latest_release_observed": release, "url": url}
    if eco == "rust":
        url = f"https://crates.io/api/v1/crates/{lead}"
        crate = registry.getj(url)["crate"]
        time.sleep(1)
        return {"value": crate.get("recent_downloads"), "latest_release_observed":
                crate.get("max_stable_version") or crate.get("max_version"), "url": url}
    if eco == "php":
        if lead.startswith("pecl/"):
            return {"value": None, "url": "https://pecl.php.net/package/yaml",
                    "error": "PECL extension; Packagist has no download count for it"}
        stats = f"https://packagist.org/packages/{lead}/stats.json"
        return {"value": registry.getj(stats)["downloads"]["total"], "url": stats}
    if eco == "go":
        if lead in hits and hits[lead] is not None:
            return {"value": hits[lead], "url": f"https://pkg.go.dev/search?q=yaml&limit={LIMIT}&m=package",
                    "source": "search snippet"}
        url = f"https://pkg.go.dev/{lead}"
        page = registry.get(url).decode("utf-8", "replace")
        found = re.search(r'aria-label="Imported By: ([\d,]+)"', page)
        time.sleep(2)
        if not found:
            return {"value": None, "url": url, "error": "Imported By count not found on package page"}
        return {"value": int(found.group(1).replace(",", "")), "url": url, "source": "package page"}
    if eco == "java":
        return deps_dev(lead)
    raise ValueError(eco)


SEARCH = {"javascript": registry.npm, "python": registry.pypi, "rust": registry.crates,
          "php": registry.packagist, "java": registry.maven, "go": registry.gopkg}
METRIC_NAME = {
    "javascript": "npm downloads, last month",
    "python": "PyPI Stats last_month downloads excluding known mirrors",
    "rust": "crates.io recent_downloads (trailing 90 days)",
    "php": "Packagist lifetime package downloads",
    "go": "pkg.go.dev Imported by package count",
    "java": "deps.dev directDependentCount summed over all Maven releases",
}


def capture(eco: str) -> dict:
    started = now()
    if eco in ("c", "cpp"):
        snapshot = debian(eco)
    else:
        registry.QUERIES = QUERIES
        found = SEARCH[eco]()
        hits = {hit["name"]: hit.get("imported_by") for search in found["search"] for hit in search.get("hits", [])}
        metrics = {}
        for lead in LEADS[eco]:
            try:
                metrics[lead] = {**metric(eco, lead, hits), "observed_at_utc": now()}
            except Exception as error:  # recorded, not hidden
                metrics[lead] = {"value": None, "error": repr(error)[:300], "observed_at_utc": now()}
        snapshot = {**found, "metric": {"name": METRIC_NAME[eco]}, "metrics": metrics}
    for search in snapshot["search"]:
        names = {hit.get("name") or hit.get("source") for hit in search.get("hits", [])}
        search["named_leads_in_hits"] = sorted(lead for lead in LEADS[eco]
                                               if lead in names or DEBIAN.get(lead) in names)
    leads = [{"name": lead, "family": family, "api_hint": api, "note": note,
              "found_by": "registry_search" if any(lead in s["named_leads_in_hits"] for s in snapshot["search"])
              else "targeted_documentation_lead",
              "metric_value": snapshot["metrics"][lead].get("value")}
             for lead, (family, api, note) in LEADS[eco].items()]
    return {"ecosystem": eco, "format": "yaml", "captured_at_utc": started,
            "search_limit_per_query": LIMIT,
            "note": "Search hits and named leads are leads, not verified parsers.", **snapshot,
            "leads": leads}


def main() -> None:
    for eco in sys.argv[1:] or list(LEADS):
        out = ROOT / "data" / eco / "yaml" / "registry-snapshot.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        snapshot = capture(eco)
        out.write_text(json.dumps(snapshot, indent=1, ensure_ascii=False) + "\n")
        print(eco, [(s.get("query"), s.get("total"), len(s.get("hits", [])), s.get("error"))
                    for s in snapshot["search"]],
              {lead["name"]: lead["metric_value"] for lead in snapshot["leads"]})


if __name__ == "__main__":
    main()
