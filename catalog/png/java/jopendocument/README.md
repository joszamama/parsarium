# jOpenDocument — PNG / Java

- **Pinned release:** `1.3`
- **License:** GPL-3.0
- **Parsed scope:** PNG dimensions and format identity
- **Underlying family:** jOpenDocument bundled ImageInfo header parser
- **Local input API:** `ImageInfo.setInput(InputStream).check(); getFormatName/getWidth/getHeight`
- **Documentation:** [API reference](<https://javadoc.io/static/org.jopendocument/jOpenDocument/1.3/org/jopendocument/util/ImageInfo.html>)
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
