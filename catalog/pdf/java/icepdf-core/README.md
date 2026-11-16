# icepdf-core — PDF / Java

- **Pinned release:** `6.2.2`
- **License:** Apache-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** ICEpdf 6 core
- **Local input API:** `Document.setFile(String localPath).getNumberOfPages()`
- **Documentation:** [API reference](<https://javadoc.io/static/org.icepdf.os/icepdf-core/6.2.2/org/icepdf/core/pobjects/Document.html>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/icepdf_core/README.md)

```sh
python3 parsarium.py build pdf java icepdf_core
python3 parsarium.py run pdf java icepdf_core controls/pdf/one-page.pdf
```
