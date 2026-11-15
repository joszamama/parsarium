# sdl3_image — SVG / C++

- **Pinned release:** `3.4.8`
- **License:** Zlib
- **Parsed scope:** parsed SVG dimensions and rendered red/green RGBA pixels
- **Underlying family:** SDL3_image SVG loader with embedded NanoSVG parser/rasterizer
- **Local input API:** `SDL_IOFromFile(local filename); IMG_LoadSVG_IO(stream); SDL_ConvertSurface to RGBA32`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL3_image/IMG_LoadSVG_IO>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

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

The pinned IMG_svg.c includes embedded NanoSVG and nanosvgrast code; SDL3_image is a distinct package input API. Its C function is called from C and C++ adapters over one SVG engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
