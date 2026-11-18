# sdl2_image — SVG / C

- **Pinned release:** `2.8.12`
- **Upstream:** [source repository](<https://github.com/libsdl-org/SDL_image>)
- **License:** Zlib
- **Parsed scope:** SVG dimensions and two rendered RGBA pixels through SDL2_image's format-specific reader
- **Underlying family:** SDL2_image SVG loader embedding NanoSVG
- **Local input API:** `SDL_RWFromFile(local SVG filename); IMG_LoadSVG_RW(SDL_RWops *); SDL_ConvertSurfaceFormat`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL2_image/IMG_LoadSVG_RW>)
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

A distinct SDL2_image package/API from SDL3_image, but both embed NanoSVG and share the standalone NanoSVG parser family. The installed SDL2 ABI is provided by sdl2-compat.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/c/sdl2_image/README.md)

```sh
python3 parsarium.py build svg c sdl2_image
python3 parsarium.py run svg c sdl2_image controls/svg/red-green.svg
```
