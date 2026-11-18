# jcodec-javase — PNG / Java

- **Pinned release:** `0.2.5`
- **Upstream:** [source repository](<https://github.com/jcodec/jcodec>) · [Maven Central](<https://central.sonatype.com/artifact/org.jcodec/jcodec-javase>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/png/java/jcodec_javase/README.md)

```sh
python3 parsarium.py build png java jcodec_javase
python3 parsarium.py run png java jcodec_javase controls/png/red-green.png
```
