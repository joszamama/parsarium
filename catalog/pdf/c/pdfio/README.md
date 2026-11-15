# pdfio — PDF / C

- **Pinned release:** `1.6.5`
- **License:** Apache-2.0
- **Parsed scope:** PDF document page count and first page object
- **Underlying family:** PDFio PDF parser
- **Local input API:** `pdfioFileOpen(local filename, ...); pdfioFileGetNumPages() and pdfioFileGetPage()`
- **Documentation:** [API reference](<https://www.msweet.org/pdfio/pdfio.html>)
- **Catalog evidence:** [parser record](../../../../data/c/pdf/parsers.json) · [control verification](../../../../data/c/pdf/verification.json) · [within-ecosystem ranking](../../../../data/c/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Direct C API built from pinned source; same engine and release as C++ PDF call site.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/c/pdfio/README.md)

```sh
python3 parsarium.py build pdf c pdfio
python3 parsarium.py run pdf c pdfio controls/pdf/one-page.pdf
```
