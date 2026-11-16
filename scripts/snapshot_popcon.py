"""Capture Debian source-package installation counts for vetted C/C++ parsers.

The source identity map is explicit. An identical short name is not enough to
associate an unrelated Debian source package with a Parsarium parser.
"""

from __future__ import annotations

from datetime import datetime, timezone
import gzip
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
URL = "https://popcon.debian.org/sourcemax/by_inst.gz"
DESTINATION = ROOT / "data/curation"

# Vetted source-package identities. Ambiguous short names (for example, mash
# and rig in the PLY cell) are intentionally absent.
SOURCE_PACKAGES = {
    "atril": "atril", "cairo": "cairo", "devil": "devil",
    "freeimage": "freeimage", "gdk-pixbuf": "gdk-pixbuf",
    "gegl": "gegl", "ghostscript": "ghostscript", "glycin": "glycin",
    "gmsh": "gmsh", "graphicsmagick": "graphicsmagick",
    "gstreamer": "gstreamer1.0", "gtk3": "gtk+3.0", "gtk4": "gtk4",
    "imlib2": "imlib2", "karchive": "karchive",
    "libgsf": "libgsf", "libmicrohttpd": "libmicrohttpd",
    "libopenshot": "libopenshot", "librsvg": "librsvg",
    "libsoup": "libsoup", "mupdf": "mupdf",
    "netpbm": "netpbm-free", "open-mesh": "openmesh",
    "poppler": "poppler", "qtsvg": "qtsvg-opensource-src",
    "qtbase": "qtbase-opensource-src",
    "qtdeclarative": "qtdeclarative-opensource-src",
    "qtwebengine": "qtwebengine-opensource-src",
    "serf": "serf", "vlc": "vlc", "vtk": "vtk9",
    "xpdf": "xpdf",
}


def main() -> None:
    with urlopen(URL, timeout=30) as response:
        raw = response.read()
        last_modified = response.headers.get("Last-Modified")
    text = gzip.decompress(raw).decode("utf-8")
    values = {}
    for line in text.splitlines():
        match = re.match(r"^\s*(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+", line)
        if match:
            rank, source, installations, votes = match.groups()
            values[source] = {"rank": int(rank), "installed": int(installations),
                              "regular_use_votes": int(votes)}
    missing = sorted(set(SOURCE_PACKAGES.values()) - set(values))
    if missing:
        raise ValueError(f"source packages absent from Debian snapshot: {missing}")
    DESTINATION.mkdir(parents=True, exist_ok=True)
    (DESTINATION / "popcon-sourcemax-by_inst.gz").write_bytes(raw)
    result = {
        "source": URL,
        "scope": "Maximum installed count among binary packages from each Debian source package, from voluntary Popcon submissions; not format-specific or comparable to GitHub stars.",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "last_modified": last_modified,
        "raw_sha256": sha256(raw).hexdigest(),
        "packages": {
            name: {"source_package": source,
                   "source_identity": f"https://sources.debian.org/src/{source}/",
                   **values[source]}
            for name, source in sorted(SOURCE_PACKAGES.items())
        },
    }
    (DESTINATION / "popcon-snapshot.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Captured {len(result['packages'])} source-package counts; "
          f"raw SHA-256 {result['raw_sha256']}")


if __name__ == "__main__":
    main()
