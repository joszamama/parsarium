# vips — PNG / C++

- **Pinned release:** `8.18.7`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** pixels
- **Underlying family:** libvips PNG loader (libpng-backed)
- **Local input API:** `vips_image_new_from_file(const char*, ...); vips_image_write_to_memory(...)`
- **Documentation:** [API reference](<https://www.libvips.org/API/current/VipsImage.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/png/parsers.json) · [control verification](../../../../data/cpp/png/verification.json) · [within-ecosystem ranking](../../../../data/cpp/png/ranking.md)
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

Image loader package path; PNG loader shares libpng lineage. Same underlying package and decoder as the C × PNG cell; this C++ path is not an independent engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
