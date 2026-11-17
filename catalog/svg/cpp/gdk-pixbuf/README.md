# gdk-pixbuf — SVG / C++

- **Pinned release:** `2.44.8`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** parsed SVG dimensions and rendered red/green RGBA pixels
- **Underlying family:** GdkPixbuf loader API with librsvg SVG plugin
- **Local input API:** `gdk_pixbuf_new_from_file(local SVG filename); gdk_pixbuf_get_width/height/read_pixels`
- **Documentation:** [API reference](<https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
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

[Docker harness and verification receipt](../../../../projects/svg/cpp/gdk_pixbuf/README.md)

```sh
python3 parsarium.py build svg cpp gdk_pixbuf
python3 parsarium.py run svg cpp gdk_pixbuf controls/svg/red-green.svg
```

**Coverage limit:** The C++17 harness calls the GDK-Pixbuf C file API. GDK-Pixbuf and its C++ wrapper share the same librsvg SVG syntax engine; the base libFuzzer target instruments the C++ harness, while AFL++ /work/replay provides librsvg parser feedback.
