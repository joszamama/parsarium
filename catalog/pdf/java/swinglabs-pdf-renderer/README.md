# swinglabs-pdf-renderer — PDF / Java

- **Pinned release:** `1.0.5`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** PDF page count
- **Underlying family:** Sun PDF Renderer
- **Local input API:** `new PDFFile(ByteBuffer).getNumPages()`
- **Documentation:** [API reference](<https://javadoc.io/static/org.swinglabs/pdf-renderer/1.0.5/com/sun/pdfview/PDFFile.html>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/swinglabs_pdf_renderer/README.md)

```sh
python3 parsarium.py build pdf java swinglabs_pdf_renderer
python3 parsarium.py run pdf java swinglabs_pdf_renderer controls/pdf/one-page.pdf
```
