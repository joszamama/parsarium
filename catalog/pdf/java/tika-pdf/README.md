# tika-pdf — PDF / Java

- **Pinned release:** `4.2.0`
- **License:** Apache-2.0
- **Parsed scope:** PDF page count
- **Underlying family:** Apache Tika PDF module over PDFBox
- **Local input API:** `PDFParser.parse(TikaInputStream,ContentHandler,Metadata,ParseContext)`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/apache/tika/tika-parser-pdf-module/4.2.0/tika-parser-pdf-module-4.2.0-javadoc.jar>)
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
