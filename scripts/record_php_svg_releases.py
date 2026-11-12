"""Record pinned Composer releases and Packagist search-snapshot downloads."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/svg"


def main() -> None:
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    parsers = json.loads((DATA / "parsers.json").read_text())
    search_downloads = {}
    for search in snapshot["search"]:
        for hit in search["hits"]:
            if hit["name"] in search_downloads:
                assert search_downloads[hit["name"]] == hit["downloads"]
            search_downloads[hit["name"]] = hit["downloads"]
    releases = {}
    downloads = {}
    for parser in parsers:
        name = parser["name"]
        locked = {item["name"]: item for item in json.loads(
            (ROOT / parser["composer_lock"]).read_text())["packages"]}[name]
        assert locked["version"] == parser["version"]
        assert parser["license"] in locked["license"]
        assert name in search_downloads
        releases[name] = {
            "version": parser["version"], "license": parser["license"],
            "license_evidence": parser["license_evidence"],
            "source_reference": locked["source"]["reference"],
            "source_url": locked["source"]["url"],
            "metadata_source": parser["composer_lock"],
            "url": f"https://packagist.org/packages/{name}#{parser['version']}",
        }
        downloads[name] = {"downloads": search_downloads[name],
                           "url": f"https://packagist.org/packages/{name}"}
        print(name, downloads[name]["downloads"])
    snapshot["releases"] = releases
    snapshot["download_metric"] = {
        "name": "Packagist lifetime package downloads",
        "captured_at_utc": snapshot["captured_at_utc"],
        "source": "Packagist public search JSON API saved in this snapshot",
        "scope": "All releases and uses of each package, not just SVG parsing; comparisons only within this PHP cell.",
        "packages": downloads,
    }
    (DATA / "registry-snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")


if __name__ == "__main__":
    main()
