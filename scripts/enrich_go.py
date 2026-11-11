"""Pin pkg.go.dev package-page license and importer counts for verified Go rows."""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    cell = sys.argv[1] if len(sys.argv) > 1 else ""
    if cell not in {"zip", "png", "wav", "http11", "mp4"}:
        raise SystemExit("usage: python3 scripts/enrich_go.py zip|png|wav|http11|mp4")
    directory = ROOT / "data" / "go" / cell
    parser_path = directory / "parsers.json"
    parsers = json.loads(parser_path.read_text())
    snapshot_path = directory / "registry-snapshot.json"
    snapshot = json.loads(snapshot_path.read_text())
    releases = {}
    metrics = {}
    for parser in parsers:
        url = parser["documentation"]
        try:
            with urlopen(url, timeout=20) as response:
                page = BeautifulSoup(response.read(), "html.parser")
        except HTTPError as error:
            if error.code != 404:
                raise
            url = "https://pkg.go.dev/" + parser["name"]
            with urlopen(url, timeout=20) as response:
                page = BeautifulSoup(response.read(), "html.parser")
            parser["documentation"] = url
            parser["documentation_note"] = "Pinned pseudo-version is in go.mod/go.sum but pkg.go.dev returned 404 for its versioned page; unversioned API documentation used."
        except Exception as error:
            raise RuntimeError(f"Failed to read {url}: {error}") from error
        license_element = page.select_one('[data-test-id="UnitHeader-license"]')
        imported_element = page.select_one('a[href*="tab=importedby"]')
        if license_element is None:
            raise RuntimeError(f"No license evidence: {url}")
        license_text = license_element.get_text(" ", strip=True)
        count_match = re.search(r"Imported by:\s*([\d,]+)", imported_element.get_text(" ", strip=True)) if imported_element else None
        count = int(count_match.group(1).replace(",", "")) if count_match else None
        parser["license"] = license_text
        releases[parser["name"]] = {"module": parser["module"], "version": parser["version"], "license": license_text, "url": url}
        if "license_evidence" in parser:
            releases[parser["name"]]["license_evidence"] = parser["license_evidence"]
        metrics[parser["name"]] = {"imported_by_packages": count, "url": url}
    parser_path.write_text(json.dumps(parsers, indent=2) + "\n")
    snapshot["releases"] = releases
    snapshot["popularity_metric"] = {
        "name": "pkg.go.dev Imported by package count",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "packages": metrics,
    }
    snapshot_path.write_text(json.dumps(snapshot, indent=2) + "\n")
    print(f"Pinned license and importer counts for {len(parsers)} Go packages")


if __name__ == "__main__":
    main()
