# cairo — PNG / C

- **Pinned release:** `1.18.6`
- **Upstream:** [source repository](<https://gitlab.freedesktop.org/cairo/cairo>) · [Debian](<https://tracker.debian.org/pkg/cairo>)
- **License:** LGPL-2.1-only OR MPL-1.1
- **Parsed scope:** pixels
- **Underlying family:** Cairo PNG surface loader (libpng-backed)
- **Local input API:** `cairo_image_surface_create_from_png(const char* filename); cairo_image_surface_get_data(...)`
- **Documentation:** [API reference](<https://www.cairographics.org/manual/cairo-PNG-Support.html>)
- **Catalog evidence:** [parser record](../../../../data/c/png/parsers.json) · [control verification](../../../../data/c/png/verification.json) · [within-ecosystem ranking](../../../../data/c/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

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

Cairo PNG loader uses libpng; primary repository is freedesktop GitLab, so GitHub stars are unavailable for this ranking.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/c/cairo/README.md)

```sh
python3 parsarium.py build png c cairo
python3 parsarium.py run png c cairo controls/png/red-green.png
```
