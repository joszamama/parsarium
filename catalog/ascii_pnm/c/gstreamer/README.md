# gstreamer — ASCII PNM / C

- **Pinned release:** `1.28.9`
- **Upstream:** [source repository](<https://gitlab.freedesktop.org/gstreamer/gstreamer>) · [Debian](<https://tracker.debian.org/pkg/gstreamer1.0>)
- **License:** LGPL-2.0-or-later AND LGPL-2.1-or-later AND MIT
- **Parsed scope:** P3 dimensions, RGB caps, and two decoded pixels
- **Underlying family:** GStreamer gst-plugins-bad pnmdec
- **Local input API:** `gst_parse_launch(filesrc ! pnmdec ! appsink); gst_app_sink_try_pull_sample(...)`
- **Documentation:** [API reference](<https://gstreamer.freedesktop.org/documentation/pnm/pnmdec.html>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_pnm/parsers.json) · [control verification](../../../../data/c/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "format": "RGB",
  "first": [
    255,
    0,
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

PNM decoder plugin from the pinned GStreamer 1.28.9 monorepo source release; local pnm plugin dylib separately checked by SHA-256.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/c/gstreamer/README.md)

```sh
python3 parsarium.py build ascii_pnm c gstreamer
python3 parsarium.py run ascii_pnm c gstreamer controls/ascii_pnm/red-green.ppm
```
