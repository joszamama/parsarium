"""Capture the bounded Conan recipe search and Debian popcon counts for C XML parser leads.

Conan Center recipe names are matched case-insensitively against "xml", then
checked for targeted C XML names that lack that substring. Adoption is the
Debian popcon installation count of each lead's explicitly mapped runtime
library binary package. The source-package (sourcemax) table is also recorded:
it undercounts libxml2 because the libxml2 source now builds libxml2-16, so the
older libxml2 binary is no longer attributed to it. Homebrew 365-day install
counts are a second, non-comparable cross-check.
"""

from datetime import datetime, timezone
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/c/xml/registry-snapshot.json"
INDEX = "https://api.github.com/repos/conan-io/conan-center-index/git/trees/master?recursive=1"
POPCON = "https://popcon.debian.org/by_inst.gz"
SOURCEMAX = "https://popcon.debian.org/sourcemax/by_inst.gz"
BREW = "https://formulae.brew.sh/api/analytics/install/365d.json"
QUERY = "xml"
TARGETED = ("expat", "libxml2", "mxml", "yxml", "libroxml", "ezxml", "sxmlc")
# Lead -> (Debian source, Debian runtime library binaries, Homebrew formula); None: not packaged.
LEADS = {"expat": ("expat", ["libexpat1"], "expat"),
         "libxml2": ("libxml2", ["libxml2", "libxml2-16"], "libxml2"),
         "mxml": ("mxml", ["libmxml1"], "libmxml"),
         "libroxml": ("libroxml", ["libroxml0"], None),
         "yxml": (None, [], None), "ezxml": (None, [], None), "sxmlc": (None, [], None)}


def get(url: str) -> tuple[bytes, dict]:
    result = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location", "--max-time", "120",
                             "-A", "Parsarium C XML catalog", "--dump-header", "-", url], capture_output=True, check=True)
    head, body = result.stdout.split(b"\r\n\r\n", 1)
    while body.startswith(b"HTTP/"):
        head, body = body.split(b"\r\n\r\n", 1)
    headers = {}
    for line in head.decode("latin-1").split("\r\n"):
        key, sep, value = line.partition(":")
        if sep:
            headers[key.strip().title()] = value.strip()
    return body, headers


def main() -> None:
    raw, _ = get(INDEX)
    tree = json.loads(raw)
    names = sorted({item["path"].split("/")[1] for item in tree["tree"]
                    if item["path"].startswith("recipes/") and len(item["path"].split("/")) >= 2})
    matches = [name for name in names if QUERY in name.lower()]
    search = [{"query": QUERY, "method": "literal case-insensitive recipe-name substring; alphabetic, not usage ranked",
               "url": "https://github.com/conan-io/conan-center-index/tree/master/recipes",
               "total": len(matches), "limit": 100,
               "hits": [{"rank": i, "name": n, "url": f"https://conan.io/center/recipes/{n}"}
                        for i, n in enumerate(matches[:100], 1)]},
              {"query": "targeted C XML names", "method": "exact recipe-name presence",
               "total": len(TARGETED), "limit": 100,
               "hits": [{"rank": i, "name": n, "present": n in names,
                         "url": f"https://conan.io/center/recipes/{n}"} for i, n in enumerate(TARGETED, 1)]}]
    tables, metric = {}, {}
    for key, url in (("binary", POPCON), ("sourcemax", SOURCEMAX)):
        data, headers = get(url)
        metric[key] = {"url": url, "last_modified": headers.get("Last-Modified"), "sha256": sha256(data).hexdigest()}
        rows = tables[key] = {}
        for line in gzip.decompress(data).decode("utf-8", "replace").splitlines():
            parts = line.split()
            if len(parts) >= 7 and all(p.isdigit() for p in (parts[0], *parts[2:7])):
                rows[parts[1]] = {"rank": int(parts[0]), "installed": int(parts[2]), "regular_use_votes": int(parts[3]),
                                  "old": int(parts[4]), "recent": int(parts[5]), "no_files": int(parts[6])}
    brew, _ = get(BREW)
    brew = json.loads(brew)
    brew_counts = {item["formula"]: int(str(item["count"]).replace(",", "")) for item in brew["items"]}
    candidates = {}
    for name, (source, binaries, formula) in LEADS.items():
        packages = {b: tables["binary"].get(b) for b in binaries}
        present = [row["installed"] for row in packages.values() if row]
        candidates[name] = {"conan_recipe": name in names, "debian_source": source,
                            "debian_binary_packages": packages,
                            "primary_installed": max(present) if present else None,
                            "debian_sourcemax": tables["sourcemax"].get(source) if source else None,
                            "homebrew_formula": formula,
                            "homebrew_install_365d": brew_counts.get(formula) if formula else None}
    OUT.write_text(json.dumps({
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_surface": "Conan Center Index recipe tree (GitHub git-trees API), plus targeted C XML recipe names; adoption from Debian popcon sourcemax installation counts",
        "search_index_api": INDEX,
        "search_index_sha": tree.get("sha"),
        "recipe_count": len(names),
        "search": search,
        "adoption_metric": {"name": "Debian popcon installations of the lead's runtime library binary package (max when two sonames are listed)",
                            **metric["binary"]},
        "sourcemax_cross_check": metric["sourcemax"],
        "homebrew_cross_check": {"name": "Homebrew install count (365 days, includes dependency installs)",
                                 "url": BREW, "window": [brew["start_date"], brew["end_date"]]},
        "c_candidates": candidates,
    }, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({n: (c["primary_installed"], c["homebrew_install_365d"]) for n, c in candidates.items()}))
    print(matches)


if __name__ == "__main__":
    main()
