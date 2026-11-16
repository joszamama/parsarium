# mupdf — SVG / C

- **Pinned release:** `1.28.6`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** SVG dimensions and two rendered RGB pixels
- **Underlying family:** MuPDF native SVG document parser and renderer
- **Local input API:** `fz_open_document(local SVG filename); fz_load_page; fz_new_pixmap_from_page`
- **Documentation:** [API reference](<https://github.com/ArtifexSoftware/mupdf/blob/master/include/mupdf/fitz/document.h>)
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

Same MuPDF package also has a separate PDF cell path; this SVG path uses the native source/svg parser.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/c/mupdf/README.md)

```sh
python3 parsarium.py build svg c mupdf
python3 parsarium.py run svg c mupdf controls/svg/red-green.svg
```
