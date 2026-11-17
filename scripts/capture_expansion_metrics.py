#!/usr/bin/env python3
"""Capture one primary adoption metric per lead, per ecosystem (never compared across ecosystems).

Writes data/expansion/metrics/<ecosystem>.json. Missing values stay null with the error recorded.
"""
import datetime, json, re, sys, time, urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from capture_expansion_registry import get, getj  # noqa: E402
from expansion_leads import LEADS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/expansion/metrics"

METRIC = {
    "javascript": ("npm downloads, last month", "https://api.npmjs.org/downloads/point/last-month/{}", "https://github.com/npm/registry/blob/main/docs/download-counts.md"),
    "python": ("PyPI downloads, last month (pypistats.org, mirrors excluded)", "https://pypistats.org/api/packages/{}/recent", "https://pypistats.org/api/"),
    "rust": ("crates.io recent_downloads (trailing 90 days)", "https://crates.io/api/v1/crates/{}", "https://crates.io/data-access"),
    "php": ("Packagist lifetime package downloads", "https://packagist.org/packages/{}.json", "https://packagist.org/apidoc"),
    "go": ("pkg.go.dev Imported by package count", "https://pkg.go.dev/{}", "https://pkg.go.dev/about"),
    "java": ("deps.dev directDependentCount of the default (latest) Maven version", "https://api.deps.dev/v3alpha/systems/maven/packages/{}", "https://docs.deps.dev/api/v3alpha/"),
    "c": ("Homebrew install-on-request count over 365 days", "https://formulae.brew.sh/api/formula/{}.json", "https://formulae.brew.sh/docs/api/"),
}
METRIC["cpp"] = METRIC["c"]


def one(eco, name, brew):
    q = urllib.parse.quote(name, safe="@/") if eco == "javascript" else urllib.parse.quote(name, safe="")
    url = METRIC[eco][1].format(q if eco not in ("rust", "php", "go", "c", "cpp") else name)
    if eco == "javascript":
        return getj(url)["downloads"], None, url
    if eco == "python":
        v = getj(f"https://pypi.org/pypi/{name}/json")["info"]["version"]
        return getj(url)["data"]["last_month"], v, url
    if eco == "rust":
        c = getj(url)["crate"]
        return c.get("recent_downloads"), c.get("max_stable_version") or c.get("max_version"), url
    if eco == "php":
        p = getj(url)["package"]
        return p["downloads"]["total"], None, url
    if eco == "go":
        page = get(url).decode("utf-8", "replace")
        ib = re.search(r'aria-label="Imported By: ([\d,]+)"', page)
        ver = re.search(r'data-test-id="UnitHeader-version"[\s\S]*?Version:\s*</span>\s*([^\s<]+)', page)
        if not ib:
            raise LookupError("Imported By count not found on package page")
        return int(ib.group(1).replace(",", "")), ver.group(1) if ver else None, url
    if eco == "java":
        pkg = getj(url)
        dv = next(v["versionKey"]["version"] for v in pkg["versions"] if v.get("isDefault"))
        durl = f"{url}/versions/{urllib.parse.quote(dv, safe='')}:dependents"
        return getj(durl).get("directDependentCount"), dv, durl
    if eco in ("c", "cpp"):
        f = getj(url)
        return brew.get(name), f["versions"]["stable"], url


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    brew = None
    for eco in sys.argv[1:] or METRIC:
        if eco in ("c", "cpp") and brew is None:
            a = getj("https://formulae.brew.sh/api/analytics/install-on-request/365d.json")
            brew = {i["formula"]: int(str(i["count"]).replace(",", "")) for i in a["items"]}
            window = (a.get("start_date"), a.get("end_date"))
        names = sorted({lead[0] for fmt in LEADS.values() for lead in fmt.get(eco, [])})
        rows = {}
        for n in names:
            row = {"value": None, "latest_release_observed": None, "url": None, "error": None,
                   "observed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
            if "(no formula)" in n or n.startswith("n/a"):
                row["error"] = "no registry entry for this ecosystem's metric source"
            else:
                try:
                    row["value"], row["latest_release_observed"], row["url"] = one(eco, n, brew)
                except Exception as e:
                    row["error"] = repr(e)[:300]
            rows[n] = row
            time.sleep(0.3 if eco != "go" else 1.5)
        meta = {"ecosystem": eco, "metric": METRIC[eco][0], "metric_docs": METRIC[eco][2],
                "comparability": "Compared only among leads in the same ecosystem and format cell; never across ecosystems.",
                "release_note": "latest_release_observed is a registry observation, not a pinned verified release."}
        if eco in ("c", "cpp"):
            meta["window"] = {"start": window[0], "end": window[1]}
            meta["limitation"] = "Formula-level count; umbrella formulas (ffmpeg, boost, qtbase, poco, folly) are not format-specific."
        (OUT / f"{eco}.json").write_text(json.dumps({**meta, "values": rows}, indent=1, ensure_ascii=False) + "\n")
        print(eco, sum(r["value"] is not None for r in rows.values()), "/", len(rows),
              [n for n, r in rows.items() if r["error"]])


if __name__ == "__main__":
    main()
