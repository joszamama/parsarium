# icepdf8 — PDF / Java

- **Pinned release:** `8.0.0`
- **License:** Apache-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** ICEpdf 8 community fork
- **Local input API:** `Document.setFile(String localPath).getNumberOfPages()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/github/pcorless/icepdf/icepdf-core/8.0.0/icepdf-core-8.0.0-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/pdf/java/icepdf8/README.md)

```sh
python3 parsarium.py build pdf java icepdf8
python3 parsarium.py run pdf java icepdf8 controls/pdf/one-page.pdf
```
