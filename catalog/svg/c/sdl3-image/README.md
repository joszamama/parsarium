# sdl3_image — SVG / C

- **Pinned release:** `3.4.8`
- **Upstream:** [source repository](<https://github.com/libsdl-org/SDL_image>)
- **License:** Zlib
- **Parsed scope:** parsed SVG dimensions and rendered red/green RGBA pixels
- **Underlying family:** SDL3_image SVG loader with embedded NanoSVG parser/rasterizer
- **Local input API:** `SDL_IOFromFile(local filename); IMG_LoadSVG_IO(stream); SDL_ConvertSurface to RGBA32`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL3_image/IMG_LoadSVG_IO>)
- **Catalog evidence:** [parser record](../../../../data/c/svg/parsers.json) · [control verification](../../../../data/c/svg/verification.json) · [within-ecosystem ranking](../../../../data/c/svg/ranking.md)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/c/sdl3_image/README.md)

```sh
python3 parsarium.py build svg c sdl3_image
python3 parsarium.py run svg c sdl3_image controls/svg/red-green.svg
```
