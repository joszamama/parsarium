# pdf_oxide — PDF / Python

- **Pinned release:** `0.3.78`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** page text
- **Underlying family:** PDF Oxide Rust core
- **Local input API:** `pdf_oxide.PdfDocument(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/pdf-oxide/0.3.78/>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "text": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/python/pdf_oxide/README.md)

```sh
python3 parsarium.py build pdf python pdf_oxide
python3 parsarium.py run pdf python pdf_oxide controls/pdf/one-page.pdf
```
