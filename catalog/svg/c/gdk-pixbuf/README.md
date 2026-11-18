# gdk-pixbuf — SVG / C

- **Pinned release:** `2.44.8`
- **Upstream:** [source repository](<https://gitlab.gnome.org/GNOME/gdk-pixbuf>) · [Debian](<https://tracker.debian.org/pkg/gdk-pixbuf>)
- **License:** LGPL-2.1-or-later
- **Parsed scope:** parsed SVG dimensions and rendered red/green RGBA pixels
- **Underlying family:** GdkPixbuf loader API with librsvg SVG plugin
- **Local input API:** `gdk_pixbuf_new_from_file(local SVG filename); gdk_pixbuf_get_width/height/read_pixels`
- **Documentation:** [API reference](<https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html>)
- **Catalog evidence:** [parser record](../../../../data/c/svg/parsers.json) · [control verification](../../../../data/c/svg/verification.json) · [within-ecosystem ranking](../../../../data/c/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0,
    255
  ],
  "second": [
    0,
    255,
    0,
    255
  ]
}
```

The installed GdkPixbuf SVG loader module comes from librsvg 2.63.4, which is separately counted. This is a distinct package input API over the same librsvg SVG syntax engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/c/gdk_pixbuf/README.md)

```sh
python3 parsarium.py build svg c gdk_pixbuf
python3 parsarium.py run svg c gdk_pixbuf controls/svg/red-green.svg
```

**Coverage limit:** The base libFuzzer target instruments the C harness. Use the AFL++ one-shot /work/replay file target for librsvg Rust parser feedback.
