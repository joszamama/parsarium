# mupdf — PDF / C

- **Pinned release:** `1.28.6`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** PDF document page count
- **Underlying family:** MuPDF C document parser
- **Local input API:** `fz_open_document(fz_context*, local filename); fz_count_pages()`
- **Documentation:** [API reference](<https://mupdf.readthedocs.io/en/1.28.6/cookbook/c/example.html>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Direct C API; same engine and release as C++ PDF call site.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
