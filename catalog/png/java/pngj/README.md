# pngj — PNG / Java

- **Pinned release:** `2.1.0`
- **Upstream:** [Maven Central](<https://central.sonatype.com/artifact/ar.com.hjg/pngj>)
- **License:** Apache-2.0
- **Parsed scope:** RGBA pixels
- **Underlying family:** PNGJ PNG decoder
- **Local input API:** `new PngReader(InputStream).readRow()`
- **Documentation:** [API reference](<https://javadoc.io/static/ar.com.hjg/pngj/2.1.0/ar/com/hjg/pngj/PngReader.html>)
- **Catalog evidence:** [parser record](../../../../data/java/png/parsers.json) · [control verification](../../../../data/java/png/verification.json) · [within-ecosystem ranking](../../../../data/java/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/java/pngj/README.md)

```sh
python3 parsarium.py build png java pngj
python3 parsarium.py run png java pngj controls/png/red-green.png
```
