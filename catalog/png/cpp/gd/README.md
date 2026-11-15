# gd — PNG / C++

- **Pinned release:** `2.3.3`
- **License:** GD
- **Parsed scope:** pixels
- **Underlying family:** GD PNG codec (libpng-backed)
- **Local input API:** `gdImageCreateFromPng(FILE*); gdImageGetPixel(...)`
- **Documentation:** [API reference](<https://github.com/libgd/libgd/blob/gd-2.3.3/src/gd.h>)
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

GD PNG codec calls libpng; this is a distinct C package API over a shared decoder family. Same underlying package and decoder as the C × PNG cell; this C++ path is not an independent engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
