# jcodec-javase — PNG / Java

- **Pinned release:** `0.2.5`
- **License:** BSD-2-Clause
- **Parsed scope:** PNG dimensions
- **Underlying family:** JCodec Java SE PNG wrapper over Java ImageIO
- **Local input API:** `new pngawt.PNGDecoder().decodeFrame(ByteBuffer,null)`
- **Documentation:** [API reference](<https://javadoc.io/static/org.jcodec/jcodec-javase/0.2.5/org/jcodec/codecs/pngawt/PNGDecoder.html>)
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
