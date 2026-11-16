# libvips — SVG / C

- **Pinned release:** `8.18.7`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** libvips SVG loader over librsvg
- **Local input API:** `vips_svgload(local filename, &image, NULL); vips_getpoint(image, ...)`
- **Documentation:** [API reference](<https://www.libvips.org/API/current/ctor.Image.svgload.html>)
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

Installed libvips core directly links librsvg 2.63.4. libvips is a distinct package input API but shares SVG syntax interpretation with the librsvg row.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/c/libvips/README.md)

```sh
python3 parsarium.py build svg c libvips
python3 parsarium.py run svg c libvips controls/svg/red-green.svg
```
