#!/usr/bin/env python3
"""Capture one fresh adoption value per merged-MP3 candidate.

The MP3 + ID3v2 and plain MP3 cells were captured on different days. When the
two formats were merged into one MP3 format, the ecosystems whose union of
selected paths exceeded ten (C, Go, JavaScript, Python) needed a single
capture so the top ten could be chosen from one source and window. This script
fetches that capture and writes it to data/<eco>/mp3/registry-snapshot.json
under `merged_mp3_ranking_2026_11_17`. It never fills a missing value.
"""

from __future__ import annotations

import json
import re
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "parsarium-snapshot/1"}
KEY = "merged_mp3_ranking_2026_11_17"

C_FORMULAE = {  # catalog package -> Homebrew formula (None: no formula)
    "ffmpeg": "ffmpeg", "mpv": "mpv", "gstreamer": "gstreamer", "sox": "sox",
    "sdl_mixer": "sdl2_mixer", "mpg123": "mpg123", "libsndfile": "libsndfile",
    "lame": "lame", "taglib": "taglib", "libmad": "mad", "vlc": None,
}
GO_PACKAGES = [
    "github.com/faiface/beep/mp3", "github.com/dhowden/tag", "github.com/hajimehoshi/go-mp3",
    "github.com/hajimehoshi/ebiten/v2/audio/mp3", "github.com/bogem/id3v2/v2", "github.com/tcolgate/mp3",
    "github.com/gopxl/beep/v2/mp3", "github.com/tosone/minimp3", "github.com/ascherkus/go-id3/src/id3",
    "github.com/dustin/go-id3", "github.com/dmulholl/mp3lib",
]
NPM_PACKAGES = [
    "music-metadata", "mediainfo.js", "jsmediatags", "@audio/decode", "@audio/decode-mp3",
    "get-audio-duration", "node-id3", "id3js", "mp3-duration", "get-mp3-duration",
    "mediabunny", "codec-parser", "mp3-parser",
]
PYPI_PACKAGES = [
    "mutagen", "tinytag", "pydub", "soundfile", "audioread", "librosa", "pygame", "av",
    "ffmpeg-python", "moviepy", "hachoir",
]


def get(url: str) -> bytes:
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as response:
                return response.read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))
    raise AssertionError


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def capture_c() -> dict:
    url = "https://formulae.brew.sh/api/analytics/install-on-request/365d.json"
    data = json.loads(get(url))
    counts = {item["formula"]: int(item["count"].replace(",", "")) for item in data["items"]}
    packages = {}
    for name, formula in C_FORMULAE.items():
        packages[name] = {"formula": formula,
                          "install_on_request_365d": counts.get(formula) if formula else None}
    return {"metric": "Homebrew install-on-request count over 365 days", "source": url,
            "window": [data["start_date"], data["end_date"]], "captured_at_utc": now(),
            "packages": packages}


def capture_go() -> dict:
    packages = {}
    for path in GO_PACKAGES:
        url = f"https://pkg.go.dev/{path}"
        page = get(url).decode("utf-8", "replace")
        match = re.search(r"Imported by:\s*</span>\s*([\d,]+)", page)
        packages[path] = {"imported_by": int(match.group(1).replace(",", "")) if match else None,
                          "url": url, "observed_at_utc": now()}
        time.sleep(1)
    return {"metric": "pkg.go.dev Imported by package count", "source": "https://pkg.go.dev/<package>",
            "window": "point-in-time page value", "captured_at_utc": now(), "packages": packages}


def capture_npm() -> dict:
    end = datetime.now(timezone.utc).date() - timedelta(days=2)
    start = end - timedelta(days=29)
    window = f"{start.isoformat()}:{end.isoformat()}"
    packages = {}
    for name in NPM_PACKAGES:
        url = f"https://api.npmjs.org/downloads/point/{window}/{name}"
        packages[name] = {"downloads": json.loads(get(url)).get("downloads"), "url": url}
    return {"metric": "npm registry tarball downloads", "source": "https://api.npmjs.org/downloads/point/",
            "window": window, "captured_at_utc": now(), "packages": packages}


def capture_pypi() -> dict:
    packages = {}
    for name in PYPI_PACKAGES:
        url = f"https://pypistats.org/api/packages/{name}/recent?period=month"
        packages[name] = {"downloads": json.loads(get(url))["data"]["last_month"], "url": url}
        time.sleep(1)
    return {"metric": "PyPI Stats last_month downloads excluding known mirrors",
            "source": "https://pypistats.org/api/", "window": "API-defined last_month, captured the same UTC day",
            "captured_at_utc": now(), "packages": packages}


def main() -> None:
    for eco, capture in (("c", capture_c), ("go", capture_go), ("javascript", capture_npm),
                         ("python", capture_pypi)):
        record = capture()
        record["script"] = "scripts/snapshot_mp3_merge_metrics.py"
        out = ROOT / "data" / eco / "mp3" / "registry-snapshot.json"
        snapshot = json.loads(out.read_text()) if out.is_file() else {}
        snapshot[KEY] = record
        out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
        print(eco, {k: next((x for x in v.values() if isinstance(x, int)), None)
                    for k, v in record["packages"].items()})


if __name__ == "__main__":
    main()
