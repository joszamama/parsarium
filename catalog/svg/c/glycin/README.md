# glycin — SVG / C

- **Pinned release:** `2.2.6`
- **License:** MPL-2.0 OR LGPL-2.1-or-later
- **Parsed scope:** detected SVG MIME type, parsed frame dimensions and red/green pixels
- **Underlying family:** Glycin C API and glycin-svg loader over librsvg
- **Local input API:** `gly_loader_new(GFile* local path); gly_loader_load; gly_image_next_frame; gly_frame_get_buf_bytes`
- **Documentation:** [API reference](<https://gnome.pages.gitlab.gnome.org/glycin/libglycin/ctor.Loader.new.html>)
- **Catalog evidence:** [parser record](../../../../data/c/svg/parsers.json) · [control verification](../../../../data/c/svg/verification.json) · [within-ecosystem ranking](../../../../data/c/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "mime": "image/svg+xml",
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

The released Glycin C binding and SVG loader form a distinct package input path, but the SVG syntax engine is librsvg. Verified in Linux because the macOS libglycin build did not install an SVG loader.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
