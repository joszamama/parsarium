# leptonica — ASCII PNM / C++

- **Pinned release:** `1.87.0`
- **License:** BSD-2-Clause
- **Parsed scope:** P3 dimensions and two decoded RGB pixels
- **Underlying family:** Leptonica PNM reader
- **Local input API:** `pixRead(const char* filename); pixGetRGBPixel(PIX*, x, y, ...)`
- **Documentation:** [API reference](<https://github.com/DanBloomberg/leptonica/blob/1.87.0/src/allheaders.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_pnm/parsers.json) · [control verification](../../../../data/cpp/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

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

Leptonica pixRead parsed P3 and returned RGB pixels.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/cpp/leptonica/README.md)

```sh
python3 parsarium.py build ascii_pnm cpp leptonica
python3 parsarium.py run ascii_pnm cpp leptonica controls/ascii_pnm/red-green.ppm
```
