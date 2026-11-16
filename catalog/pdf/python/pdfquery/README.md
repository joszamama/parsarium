# pdfquery — PDF / Python

- **Pinned release:** `0.4.3`
- **License:** MIT
- **Parsed scope:** layout tree text
- **Underlying family:** pdfquery via pdfminer.six
- **Local input API:** `pdfquery.PDFQuery(local path).load()`
- **Documentation:** [API reference](<https://github.com/jcushman/pdfquery>)
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

[Docker harness and verification receipt](../../../../projects/pdf/python/pdfquery/README.md)

```sh
python3 parsarium.py build pdf python pdfquery
python3 parsarium.py run pdf python pdfquery controls/pdf/one-page.pdf
```
