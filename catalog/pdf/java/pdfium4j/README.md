# pdfium4j — PDF / Java

- **Pinned release:** `1.3.0`
- **License:** Apache-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** PDFium native engine via PDFium4j FFM
- **Local input API:** `PdfDocument.open(Path).pageCount()`
- **Documentation:** [API reference](<https://github.com/grimmory-tools/PDFium4j>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/pdfium4j/README.md)

```sh
python3 parsarium.py build pdf java pdfium4j
python3 parsarium.py run pdf java pdfium4j controls/pdf/one-page.pdf
```
