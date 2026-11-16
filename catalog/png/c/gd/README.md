# gd — PNG / C

- **Pinned release:** `2.3.3`
- **License:** GD
- **Parsed scope:** pixels
- **Underlying family:** GD PNG codec (libpng-backed)
- **Local input API:** `gdImageCreateFromPng(FILE*); gdImageGetPixel(...)`
- **Documentation:** [API reference](<https://github.com/libgd/libgd/blob/gd-2.3.3/src/gd.h>)
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

GD PNG codec calls libpng; this is a distinct C package API over a shared decoder family.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/c/gd/README.md)

```sh
python3 parsarium.py build png c gd
python3 parsarium.py run png c gd controls/png/red-green.png
```
