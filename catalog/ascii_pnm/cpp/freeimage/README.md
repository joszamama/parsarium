# freeimage — ASCII PNM / C++

- **Pinned release:** `3.18.0`
- **License:** FreeImage
- **Parsed scope:** P3 dimensions and two decoded RGB pixels
- **Underlying family:** FreeImage PPM plugin
- **Local input API:** `FreeImage_Load(FIF_PPM, const char*, PNM_DEFAULT); FreeImage_GetPixelColor(...)`
- **Documentation:** [API reference](<https://freeimage.sourceforge.io/fnet/html/99F7C60B.htm>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_pnm/parsers.json) · [control verification](../../../../data/cpp/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_pnm/ranking.md)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
