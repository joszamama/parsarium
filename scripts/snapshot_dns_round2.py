"""Add round-2 targeted metric lookups to a DNS pilot registry snapshot.

Round 1 (scripts/snapshot_dns_registry.py) recorded the bounded searches and one
metric for each documented lead. Round 2 keeps that snapshot and its metric
source and window, and only appends targeted lookups for names that were found
in the recorded search hits or project documentation but had no metric yet.
The lookups go under "round2_targeted" in data/<ecosystem>/dns/registry-snapshot.json
with their URL and capture time; existing entries are never rewritten.

npm lookups reuse the 30-day window recorded in the round-1 snapshot. C and C++
use the same pinned Debian popcon sourcemax table, and may add a binary-package
lookup (``bin:<package>``) from the pinned by_inst table for the format-specific
development-package fallback.

Only registry HTTPS APIs are contacted; no DNS server, resolver or socket to a
DNS service is used.

Usage: python3 scripts/snapshot_dns_round2.py <ecosystem> <name> [<name> ...]
(the macOS python.org build needs SSL_CERT_FILE=/etc/ssl/cert.pem)
"""

import gzip
from hashlib import sha256
import json
import re
import sys
import time
import urllib.error
import urllib.parse

from snapshot_dns_registry import ROOT, SOURCEMAX, SOURCEMAX_SHA256, get, getj, guarded, now

BY_INST = ROOT / "data/curation/popcon-by_inst.gz"


def npm(snapshot: dict, name: str) -> dict:
    window = re.search(r"(\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2})", snapshot["download_metric"]["name"]).group(1)
    url = f"https://api.npmjs.org/downloads/point/{window}/{urllib.parse.quote(name, safe='@')}"
    return {"downloads": getj(url).get("downloads"), "url": url, "captured_at_utc": now()}


def pypi(snapshot: dict, name: str) -> dict:
    url = f"https://pypistats.org/api/packages/{name.lower()}/recent"
    time.sleep(1)
    return {"downloads": getj(url)["data"]["last_month"], "url": url, "captured_at_utc": now()}


def crates(snapshot: dict, name: str) -> dict:
    url = f"https://crates.io/api/v1/crates/{name}"
    body = getj(url)["crate"]
    time.sleep(1)
    return {"recent_downloads": body.get("recent_downloads"), "downloads": body.get("downloads"),
            "max_stable_version": body.get("max_stable_version"), "url": url, "captured_at_utc": now()}


def packagist(snapshot: dict, name: str) -> dict:
    url = f"https://packagist.org/packages/{name}.json"
    body = getj(url)["package"]
    return {"downloads": body["downloads"]["total"], "url": url, "captured_at_utc": now(),
            "abandoned": body.get("abandoned", False)}


def maven(snapshot: dict, coordinate: str) -> dict:
    base = f"https://api.deps.dev/v3alpha/systems/MAVEN/packages/{urllib.parse.quote(coordinate, safe='')}"
    versions = getj(base)["versions"]
    default = [item["versionKey"]["version"] for item in versions if item.get("isDefault")]
    counts = {}
    for item in versions:
        version = item["versionKey"]["version"]
        url = f"{base}/versions/{urllib.parse.quote(version, safe='')}:dependents"
        try:
            counts[version] = getj(url).get("directDependentCount", 0)
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise
            counts[version] = 0
    peak = max(counts, key=counts.get)
    return {"direct_dependent_count": sum(counts.values()), "releases": len(counts),
            "default_version": default[0] if default else None, "max_release": peak,
            "max_release_direct_dependent_count": counts[peak],
            "default_release_direct_dependent_count": counts.get(default[0]) if default else None,
            "url": base, "captured_at_utc": now()}


def gopkg(snapshot: dict, path: str) -> dict:
    url = f"https://pkg.go.dev/{path}?tab=importedby"
    page = get(url).decode("utf-8", "replace")
    match = re.search(r'Known importing packages:</strong>\s*([\d,]+)', page)
    modules = re.search(r'Known importing modules:</strong>\s*([\d,]+)', page)
    time.sleep(2)
    return {"imported_by_packages": int(match.group(1).replace(",", "")) if match else None,
            "importing_modules": int(modules.group(1).replace(",", "")) if modules else None,
            "url": url, "captured_at_utc": now()}


def table(path, digest: str | None) -> dict:
    raw = path.read_bytes()
    if digest and sha256(raw).hexdigest() != digest:
        raise ValueError(f"pinned popcon table changed: {path}")
    rows = {}
    for line in gzip.decompress(raw).decode(errors="replace").splitlines():
        fields = line.split()
        if len(fields) >= 3 and fields[0].isdigit() and fields[2].isdigit():
            rows[fields[1]] = {"rank": int(fields[0]), "installed": int(fields[2])}
    return rows


def popcon(snapshot: dict, name: str) -> dict:
    if name.startswith("bin:"):
        if not BY_INST.is_file():
            return {"installed": None, "reason": f"{BY_INST.relative_to(ROOT)} not present"}
        rows = table(BY_INST, None)
        package = name[4:]
        return ({**rows[package], "table": str(BY_INST.relative_to(ROOT)),
                 "table_sha256": sha256(BY_INST.read_bytes()).hexdigest()}
                if package in rows else {"installed": None, "reason": "no Debian binary package"})
    rows = table(SOURCEMAX, SOURCEMAX_SHA256)
    return ({**rows[name], "table": "data/curation/popcon-sourcemax-by_inst.gz"}
            if name in rows else {"installed": None, "reason": "no Debian source package"})


LOOKUPS = {"javascript": npm, "python": pypi, "rust": crates, "php": packagist, "java": maven, "go": gopkg,
           "c": popcon, "cpp": popcon}


def main() -> None:
    ecosystem, *names = sys.argv[1:]
    path = ROOT / "data" / ecosystem / "dns" / "registry-snapshot.json"
    snapshot = json.loads(path.read_text())
    added = snapshot.setdefault("round2_targeted", {
        "note": "Round-2 targeted lookups with the round-1 metric source; names come from the recorded "
                "search hits or project documentation. Leads only, not verified parsers.",
        "packages": {}})
    for name in names:
        if name in added["packages"]:
            print(name, "already recorded; kept")
            continue
        added["packages"][name] = guarded(LOOKUPS[ecosystem], snapshot, name)
        print(name, json.dumps(added["packages"][name]))
    path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
