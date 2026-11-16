# openpdf — PDF / Java

- **Pinned release:** `3.0.5`
- **License:** LGPL-2.1-or-later OR MPL-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** OpenPDF PDF reader (iText lineage)
- **Local input API:** `new org.openpdf.text.pdf.PdfReader(String localPath).getNumberOfPages()`
- **Documentation:** [API reference](<https://javadoc.io/static/com.github.librepdf/openpdf/3.0.5/com.github.librepdf.openpdf/org/openpdf/text/pdf/PdfReader.html>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/openpdf/README.md)

```sh
python3 parsarium.py build pdf java openpdf
python3 parsarium.py run pdf java openpdf controls/pdf/one-page.pdf
```
