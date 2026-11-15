# sdl3_image — PNG / C++

- **Pinned release:** `3.4.8`
- **License:** Zlib
- **Parsed scope:** pixels
- **Underlying family:** SDL_image 3 PNG loader (libpng in recorded build)
- **Local input API:** `IMG_Load(const char* file); SDL_ConvertSurface(...) to RGBA pixels`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL3_image/IMG_Load>)
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

Separate SDL3_image distribution path from SDL2_image; recorded binary links libpng. Source can fall back to SDL3 PNG loader in other builds. Same underlying package and decoder as the C × PNG cell; this C++ path is not an independent engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
