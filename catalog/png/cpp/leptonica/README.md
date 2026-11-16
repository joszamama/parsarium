# leptonica — PNG / C++

- **Pinned release:** `1.87.0`
- **License:** BSD-2-Clause
- **Parsed scope:** RGB pixels
- **Underlying family:** Leptonica PNG loader (libpng-backed)
- **Local input API:** `pixRead(const char* filename); pixGetRGBPixel(PIX*, x, y, ...)`
- **Documentation:** [API reference](<https://github.com/DanBloomberg/leptonica/blob/1.87.0/src/allheaders.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/png/parsers.json) · [control verification](../../../../data/cpp/png/verification.json) · [within-ecosystem ranking](../../../../data/cpp/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first_rgb": [
    255,
    0,
    0
  ],
  "second_rgb": [
    0,
    255,
    0
  ]
}
```

Recorded Leptonica dylib links libpng; output checks RGB pixels because the standard pixRead path strips alpha. Same underlying package and decoder as the C × PNG cell; this C++ path is not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/cpp/leptonica/README.md)

```sh
python3 parsarium.py build png cpp leptonica
python3 parsarium.py run png cpp leptonica controls/png/red-green.png
```
