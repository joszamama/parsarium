# librsvg — SVG / C

- **Pinned release:** `2.63.4`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** librsvg Rust SVG engine through C API
- **Local input API:** `rsvg_handle_new_from_file(local filename), rsvg_handle_get_intrinsic_size_in_pixels, rsvg_handle_render_document`
- **Documentation:** [API reference](<https://gnome.pages.gitlab.gnome.org/librsvg/Rsvg-2.0/class.Handle.html>)
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

The same librsvg source package and engine serve C and C++ call sites; this is one package path per ecosystem, not two independent parsers.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
