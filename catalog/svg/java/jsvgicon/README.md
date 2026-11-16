# jSVGIcon — SVG / Java

- **Pinned release:** `1.6`
- **License:** Unlicense
- **Parsed scope:** Rendered SVG pixels
- **Underlying family:** BWeng20 jSVGIcon Java2D shape converter
- **Local input API:** `SVGConverter.convert(InputStream); ShapePainter.paintShapeToBufferTransparent(BufferedImage, boolean)`
- **Documentation:** [API reference](<https://github.com/BWeng20/jSVGIcon/blob/main/src/main/java/com/bw/jtools/svg/SVGConverter.java>)
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

[Docker harness and verification receipt](../../../../projects/svg/java/jsvgicon/README.md)

```sh
python3 parsarium.py build svg java jsvgicon
python3 parsarium.py run svg java jsvgicon controls/svg/red-green.svg
```
