# verapdf-parser — PDF / Java

- **Pinned release:** `1.30.4`
- **License:** MPL-2.0 OR GPL-3.0-or-later
- **Parsed scope:** PDF page count
- **Underlying family:** veraPDF parser
- **Local input API:** `new PDDocument(String localPath).getNumberOfPages()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/verapdf/parser/1.30.4/parser-1.30.4-javadoc.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/pdf/parsers.json) · [control verification](../../../../data/java/pdf/verification.json) · [within-ecosystem ranking](../../../../data/java/pdf/ranking.md)
- **Valid control:** [`controls/pdf/one-page.pdf`](../../../../controls/pdf/one-page.pdf)

## Observed control result

```json
{
  "pages": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
