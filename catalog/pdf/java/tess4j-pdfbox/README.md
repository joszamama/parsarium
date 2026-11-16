# tess4j-pdfbox — PDF / Java

- **Pinned release:** `5.20.0`
- **License:** Apache-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** Tess4J PDF utility over PDFBox
- **Local input API:** `PdfBoxUtilities.getPdfPageCount(File)`
- **Documentation:** [API reference](<https://github.com/nguyenq/tess4j/blob/master/src/main/java/net/sourceforge/tess4j/util/PdfBoxUtilities.java>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/tess4j_pdfbox/README.md)

```sh
python3 parsarium.py build pdf java tess4j_pdfbox
python3 parsarium.py run pdf java tess4j_pdfbox controls/pdf/one-page.pdf
```
