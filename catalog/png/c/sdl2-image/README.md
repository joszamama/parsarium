# sdl2_image — PNG / C

- **Pinned release:** `2.8.12`
- **License:** Zlib
- **Parsed scope:** pixels
- **Underlying family:** SDL_image 2 PNG loader (libpng-backed)
- **Local input API:** `IMG_Load(const char* file); SDL_ConvertSurfaceFormat(...) to RGBA pixels`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL2_image/IMG_Load>)
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

Separate SDL2_image distribution path from SDL3_image; recorded binary links libpng. Both share the SDL_image project family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
