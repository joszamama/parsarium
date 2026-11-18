# sdl3 — PNG / C++

- **Pinned release:** `3.4.20`
- **Upstream:** [source repository](<https://github.com/libsdl-org/SDL>)
- **License:** Zlib
- **Parsed scope:** pixels
- **Underlying family:** SDL3 bundled stb_image PNG decoder
- **Local input API:** `SDL_LoadPNG(const char* file); SDL_ConvertSurface(...) to RGBA pixels`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL3/SDL_LoadPNG>)
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

SDL3 core package path; implementation in SDL_stb.c uses stb_image, shared with the stb package. Same underlying package and decoder as the C × PNG cell; this C++ path is not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/cpp/sdl3/README.md)

```sh
python3 parsarium.py build png cpp sdl3
python3 parsarium.py run png cpp sdl3 controls/png/red-green.png
```
