# vips — PNG / C

- **Pinned release:** `8.18.7`
- **Upstream:** [source repository](<https://github.com/libvips/libvips>) · [Debian](<https://tracker.debian.org/pkg/vips>)
- **License:** LGPL-2.1-or-later
- **Parsed scope:** pixels
- **Underlying family:** libvips PNG loader (libpng-backed)
- **Local input API:** `vips_image_new_from_file(const char*, ...); vips_image_write_to_memory(...)`
- **Documentation:** [API reference](<https://www.libvips.org/API/current/VipsImage.html>)
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

Image loader package path; PNG loader shares libpng lineage.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/c/vips/README.md)

```sh
python3 parsarium.py build png c vips
python3 parsarium.py run png c vips controls/png/red-green.png
```
