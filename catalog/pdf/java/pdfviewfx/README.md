# pdfviewfx — PDF / Java

- **Pinned release:** `3.6.1`
- **License:** Apache-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** PDFViewFX over PDFBox
- **Local input API:** `new PDFBoxDocument(File).getNumberOfPages()`
- **Documentation:** [API reference](<https://github.com/dlsc-software-consulting-gmbh/PDFViewFX/blob/master/pdfviewfx/src/main/java/com/dlsc/pdfviewfx/PDFBoxDocument.java>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/pdfviewfx/README.md)

```sh
python3 parsarium.py build pdf java pdfviewfx
python3 parsarium.py run pdf java pdfviewfx controls/pdf/one-page.pdf
```
