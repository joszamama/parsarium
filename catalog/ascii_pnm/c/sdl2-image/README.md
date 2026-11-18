# sdl2_image — ASCII PNM / C

- **Pinned release:** `2.8.12`
- **Upstream:** [source repository](<https://github.com/libsdl-org/SDL_image>)
- **License:** Zlib
- **Parsed scope:** P3 dimensions and two decoded RGBA pixels
- **Underlying family:** SDL_image PNM decoder lineage
- **Local input API:** `IMG_Load(const char* file); SDL_ConvertSurfaceFormat(...) to RGBA pixels`
- **Documentation:** [API reference](<https://wiki.libsdl.org/SDL2_image/IMG_Load>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_pnm/parsers.json) · [control verification](../../../../data/c/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

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

SDL2_image IMG_Load parsed the P3 control; SDL3_image is a separate major-version package from the same upstream project and shares parser lineage.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/c/sdl2_image/README.md)

```sh
python3 parsarium.py build ascii_pnm c sdl2_image
python3 parsarium.py run ascii_pnm c sdl2_image controls/ascii_pnm/red-green.ppm
```
