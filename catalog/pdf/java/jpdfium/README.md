# jpdfium — PDF / Java

- **Pinned release:** `1.3.1`
- **License:** MIT
- **Parsed scope:** PDF page count
- **Underlying family:** PDFium native engine via JPDFium FFM
- **Local input API:** `PdfDocument.open(Path).pageCount()`
- **Documentation:** [API reference](<https://github.com/Stirling-Tools/JPDFium>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/jpdfium/README.md)

```sh
python3 parsarium.py build pdf java jpdfium
python3 parsarium.py run pdf java jpdfium controls/pdf/one-page.pdf
```
