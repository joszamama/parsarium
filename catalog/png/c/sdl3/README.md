# sdl3 — PNG / C

- **Pinned release:** `3.4.20`
- **License:** Zlib
- **Parsed scope:** pixels
- **Underlying family:** SDL3 bundled stb_image PNG decoder
- **Local input API:** `SDL_LoadPNG(const char* file); SDL_ConvertSurface(...) to RGBA pixels`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL3/SDL_LoadPNG>)
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

SDL3 core package path; implementation in SDL_stb.c uses stb_image, shared with the stb package.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
