# jcodec — PNG / Java

- **Pinned release:** `0.2.5`
- **Upstream:** [source repository](<https://github.com/jcodec/jcodec>) · [Maven Central](<https://central.sonatype.com/artifact/org.jcodec/jcodec>)
- **License:** BSD-2-Clause
- **Parsed scope:** PNG dimensions
- **Underlying family:** JCodec core PNG decoder
- **Local input API:** `new PNGDecoder().decodeFrame(ByteBuffer,byte[][])`
- **Documentation:** [API reference](<https://javadoc.io/static/org.jcodec/jcodec/0.2.5/org/jcodec/codecs/png/PNGDecoder.html>)
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

[Docker harness and verification receipt](../../../../projects/png/java/jcodec/README.md)

```sh
python3 parsarium.py build png java jcodec
python3 parsarium.py run png java jcodec controls/png/red-green.png
```
