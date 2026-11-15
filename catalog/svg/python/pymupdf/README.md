# PyMuPDF — SVG / Python

- **Pinned release:** `2.1`
- **License:** AGPL-3.0-only
- **Parsed scope:** SVG document page and dimensions
- **Underlying family:** MuPDF SVG document parser
- **Local input API:** `pymupdf.open(local_svg_path)`
- **Documentation:** [API reference](<https://pymupdf.readthedocs.io/en/latest/how-to-open-a-file.html>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "pages": 1,
  "size": [
    2,
    1
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
