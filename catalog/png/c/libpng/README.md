# libpng — PNG / C

- **Pinned release:** `1.6.59`
- **License:** libpng-2.0
- **Parsed scope:** pixels
- **Underlying family:** libpng
- **Local input API:** `png_image_begin_read_from_file(png_image*, const char*); png_image_finish_read(...) to RGBA pixels`
- **Documentation:** [API reference](<https://github.com/pnggroup/libpng/blob/v1.6.59/example.c>)
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

Direct libpng decoder; static library is built from the pinned source archive.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/c/libpng/README.md)

```sh
python3 parsarium.py build png c libpng
python3 parsarium.py run png c libpng controls/png/red-green.png
```
