# pikepdf — PDF / Python

- **Pinned release:** `10.18.0`
- **Upstream:** [source repository](<https://github.com/pikepdf/pikepdf>) · [PyPI](<https://pypi.org/project/pikepdf/>)
- **License:** MPL-2.0
- **Parsed scope:** page count and document title
- **Underlying family:** QPDF
- **Local input API:** `pikepdf.open(local path)`
- **Documentation:** [API reference](<https://pikepdf.readthedocs.io/en/latest/tutorial.html>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "title": "Parsarium PDF control"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/python/pikepdf/README.md)

```sh
python3 parsarium.py build pdf python pikepdf
python3 parsarium.py run pdf python pikepdf controls/pdf/one-page.pdf
```
