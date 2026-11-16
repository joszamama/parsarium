# pdftotext — PDF / Python

- **Pinned release:** `4.0.0`
- **License:** MIT
- **Parsed scope:** page text
- **Underlying family:** Poppler C++ binding
- **Local input API:** `pdftotext.PDF(local byte stream)`
- **Documentation:** [API reference](<https://pypi.org/project/pdftotext/4.0.0/>)
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

[Docker harness and verification receipt](../../../../projects/pdf/python/pdftotext/README.md)

```sh
python3 parsarium.py build pdf python pdftotext
python3 parsarium.py run pdf python pdftotext controls/pdf/one-page.pdf
```
