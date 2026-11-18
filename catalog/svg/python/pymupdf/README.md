# PyMuPDF — SVG / Python

- **Pinned release:** `2.1`
- **Upstream:** [source repository](<https://github.com/pymupdf/PyMuPDF>) · [PyPI](<https://pypi.org/project/PyMuPDF/>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/python/pymupdf/README.md)

```sh
python3 parsarium.py build svg python pymupdf
python3 parsarium.py run svg python pymupdf controls/svg/red-green.svg
```
