# itext-kernel — PDF / Java

- **Pinned release:** `9.8.0`
- **License:** AGPL-3.0
- **Parsed scope:** PDF page count
- **Underlying family:** iText 7/9 kernel PDF reader
- **Local input API:** `new PdfDocument(new PdfReader(File)).getNumberOfPages()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/itextpdf/kernel/9.8.0/kernel-9.8.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/itext_kernel/README.md)

```sh
python3 parsarium.py build pdf java itext_kernel
python3 parsarium.py run pdf java itext_kernel controls/pdf/one-page.pdf
```
