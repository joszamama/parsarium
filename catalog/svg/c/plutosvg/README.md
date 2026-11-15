# plutosvg — SVG / C

- **Pinned release:** `0.0.8`
- **License:** MIT
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** PlutoSVG document parser with PlutoVG rasterizer
- **Local input API:** `plutosvg_document_load_from_file(local filename, -1, -1); plutosvg_document_render_to_surface; plutovg_convert_argb_to_rgba`
- **Documentation:** [API reference](<https://github.com/sammycage/plutosvg/blob/v0.0.8/source/plutosvg.h>)
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
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

PlutoSVG has a C document parser used from C and C++; both ecosystem paths share that engine. LunaSVG shares the PlutoVG rasterizer but has separate SVG document parsing code.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/c/plutosvg/README.md)

```sh
python3 parsarium.py build svg c plutosvg
python3 parsarium.py run svg c plutosvg controls/svg/red-green.svg
```
