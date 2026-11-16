# vips — ASCII PNM / C

- **Pinned release:** `8.18.7`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** P3 dimensions and two decoded RGB pixels
- **Underlying family:** libvips PPM loader
- **Local input API:** `vips_image_new_from_file(const char*, ...); vips_image_write_to_memory(...)`
- **Documentation:** [API reference](<https://www.libvips.org/API/current/VipsImage.html>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/c/vips/README.md)

```sh
python3 parsarium.py build ascii_pnm c vips
python3 parsarium.py run ascii_pnm c vips controls/ascii_pnm/red-green.ppm
```
