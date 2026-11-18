# lunasvg — SVG / C++

- **Pinned release:** `3.5.0`
- **Upstream:** [source repository](<https://github.com/sammycage/lunasvg>)
- **License:** MIT
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** LunaSVG C++ document parser with PlutoVG rasterizer
- **Local input API:** `lunasvg::Document::loadFromFile(local filename); renderToBitmap; Bitmap::convertToRGBA`
- **Documentation:** [API reference](<https://github.com/sammycage/lunasvg/blob/v3.5.0/include/lunasvg.h>)
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
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

LunaSVG exposes a C++ document API; its C extern section has version and font helpers but no C document loader. It shares PlutoVG rasterization with PlutoSVG, while retaining separate SVG parsing logic.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/cpp/lunasvg/README.md)

```sh
python3 parsarium.py build svg cpp lunasvg
python3 parsarium.py run svg cpp lunasvg controls/svg/red-green.svg
```
