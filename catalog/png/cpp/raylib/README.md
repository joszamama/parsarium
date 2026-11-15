# raylib — PNG / C++

- **Pinned release:** `6.2`
- **License:** Zlib
- **Parsed scope:** pixels
- **Underlying family:** raylib bundled stb_image PNG decoder
- **Local input API:** `LoadImage(const char* fileName); LoadImageColors(Image) to RGBA pixels`
- **Documentation:** [API reference](<https://github.com/raysan5/raylib/blob/6.2/src/raylib.h>)
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

Raylib package exposes local C image loading over its bundled stb_image; shares parser lineage with stb and SDL3 core. Same underlying package and decoder as the C × PNG cell; this C++ path is not an independent engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
