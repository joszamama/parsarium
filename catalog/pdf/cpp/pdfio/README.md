# pdfio — PDF / C++

- **Pinned release:** `1.6.5`
- **License:** Apache-2.0
- **Parsed scope:** PDF document page count and first page object
- **Underlying family:** PDFio PDF parser
- **Local input API:** `pdfioFileOpen(const char* local filename, ...); pdfioFileGetNumPages and pdfioFileGetPage, called from C++17`
- **Documentation:** [API reference](<https://www.msweet.org/pdfio/pdfio.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/pdf/parsers.json) · [control verification](../../../../data/cpp/pdf/verification.json) · [within-ecosystem ranking](../../../../data/cpp/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

Direct PDFio C API call from C++17; independent PDFio engine, built from its pinned source archive.

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/cpp/pdfio/README.md)

```sh
python3 parsarium.py build pdf cpp pdfio
python3 parsarium.py run pdf cpp pdfio controls/pdf/one-page.pdf
```
