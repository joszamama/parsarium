# tika-image — PNG / Java

- **Pinned release:** `4.2.0`
- **License:** Apache-2.0
- **Parsed scope:** PNG dimensions
- **Underlying family:** Apache Tika ImageParser over Java ImageIO
- **Local input API:** `ImageParser.parse(InputStream,ContentHandler,Metadata,ParseContext) with image/png MIME`
- **Documentation:** [API reference](<https://tika.apache.org/4.2.0/api/org/apache/tika/parser/image/ImageParser.html>)
- **Catalog evidence:** [parser record](../../../../data/java/png/parsers.json) · [control verification](../../../../data/java/png/verification.json) · [within-ecosystem ranking](../../../../data/java/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
