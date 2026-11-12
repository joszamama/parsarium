"""Pin crates.io release evidence and comparable recent downloads."""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def fetch(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "Parsarium format parser research (https://github.com/joszamama/parsarium)"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> None:
    cell = sys.argv[1] if len(sys.argv) > 1 else ""
    if cell not in {"png", "zip", "mp4", "wav", "mp3_id3v2"}:
        raise SystemExit("usage: python3 scripts/enrich_rust.py png|zip|mp4|wav|mp3_id3v2")
    directory = ROOT / "data" / "rust" / cell
    parser_path = directory / "parsers.json"
    parsers = json.loads(parser_path.read_text())
    snapshot_path = directory / "registry-snapshot.json"
    snapshot = json.loads(snapshot_path.read_text())
    releases = {}
    metrics = {}
    for parser in parsers:
        name, version = parser["name"], parser["version"]
        url = "https://crates.io/api/v1/crates/" + quote(name)
        data = fetch(url)
        release = next((item for item in data["versions"] if item["num"] == version), None)
        if release is None or release.get("yanked"):
            raise RuntimeError(f"Pinned release missing or yanked: {name}@{version}")
        license_text = release.get("license")
        checksum = release.get("checksum")
        if not license_text or not checksum:
            raise RuntimeError(f"Missing license or checksum: {name}@{version}")
        parser["license"] = license_text
        releases[name] = {
            "version": version, "license": license_text, "checksum": checksum,
            "url": url, "crate_download": "https://static.crates.io/crates/" + name + "/" + name + "-" + version + ".crate",
        }
        metrics[name] = {"recent_downloads": data["crate"].get("recent_downloads"), "url": url}
        time.sleep(0.1)
    parser_path.write_text(json.dumps(parsers, indent=2) + "\n")
    snapshot["releases"] = releases
    snapshot["popularity_metric"] = {
        "name": "crates.io recent downloads (90 days)",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "https://crates.io/api/v1/crates/{name}",
        "packages": metrics,
    }
    snapshot_path.write_text(json.dumps(snapshot, indent=2) + "\n")
    print(f"Pinned release licenses, checksums, and download counts for {len(parsers)} Rust crates")


if __name__ == "__main__":
    main()
