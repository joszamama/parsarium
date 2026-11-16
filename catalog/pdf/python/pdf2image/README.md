# pdf2image — PDF / Python

- **Pinned release:** `1.17.0`
- **License:** MIT
- **Parsed scope:** rendered page dimensions
- **Underlying family:** Poppler pdftoppm subprocess
- **Local input API:** `pdf2image.convert_from_path(local path)`
- **Documentation:** [API reference](<https://github.com/Belval/pdf2image>)
- **Catalog evidence:** [parser record](../../../../data/python/pdf/parsers.json) · [control verification](../../../../data/python/pdf/verification.json) · [within-ecosystem ranking](../../../../data/python/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1,
  "width": 1700,
  "height": 2200
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
