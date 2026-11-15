# gtk3 — SVG / C

- **Pinned release:** `3.24.52`
- **License:** LGPL-2.0-or-later
- **Parsed scope:** SVG dimensions and red/green pixels through GTK 3 image loader
- **Underlying family:** GTK 3 image loader over GdkPixbuf and librsvg
- **Local input API:** `gtk_image_new_from_file(local SVG filename); gtk_image_get_pixbuf and GdkPixbuf pixel access`
- **Documentation:** [API reference](<https://docs.gtk.org/gtk3/ctor.Image.new_from_file.html>)
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
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

GTK 3 is a separate released toolkit API. It delegates SVG interpretation to the installed GdkPixbuf SVG loader from librsvg, already recorded as its own package path. No independent SVG syntax engine is claimed.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
