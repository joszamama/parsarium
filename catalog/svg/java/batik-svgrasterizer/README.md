# batik-svgrasterizer — SVG / Java

- **Pinned release:** `1.20`
- **License:** Apache-2.0
- **Parsed scope:** Rendered SVG pixels
- **Underlying family:** Apache Batik SVG renderer via transcoder
- **Local input API:** `SVGConverter.setSources(String[] local paths).setDst(File); execute()`
- **Documentation:** [API reference](<https://xmlgraphics.apache.org/batik/javadoc/org/apache/batik/apps/rasterizer/SVGConverter.html>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/java/batik_svgrasterizer/README.md)

```sh
python3 parsarium.py build svg java batik_svgrasterizer
python3 parsarium.py run svg java batik_svgrasterizer controls/svg/red-green.svg
```
