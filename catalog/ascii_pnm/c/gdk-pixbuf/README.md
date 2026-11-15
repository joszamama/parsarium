# gdk-pixbuf — ASCII PNM / C

- **Pinned release:** `2.44.8`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** P3 dimensions and two decoded RGB pixels
- **Underlying family:** GdkPixbuf PNM loader
- **Local input API:** `gdk_pixbuf_new_from_file(const char*, GError**); gdk_pixbuf_read_pixels(...)`
- **Documentation:** [API reference](<https://docs.gtk.org/gdk-pixbuf/ctor.Pixbuf.new_from_file.html>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_pnm/parsers.json) · [control verification](../../../../data/c/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
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

ASCII P3 is read through this package image input API. The package may use shared lower-level image code; no independent-engine claim is made.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
