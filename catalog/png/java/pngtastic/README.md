# pngtastic — PNG / Java

- **Pinned release:** `1.8`
- **License:** MIT
- **Parsed scope:** PNG dimensions
- **Underlying family:** PNGTastic PNG chunk parser
- **Local input API:** `new PngImage(InputStream).getWidth/getHeight`
- **Documentation:** [API reference](<https://github.com/depsypher/pngtastic/blob/master/src/main/java/com/googlecode/pngtastic/core/PngImage.java>)
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
