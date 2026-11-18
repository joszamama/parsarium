# gsvg — SVG / Java

- **Pinned release:** `1.2.0`
- **Upstream:** [source repository](<https://github.com/Alipsa/gsvg>) · [Maven Central](<https://central.sonatype.com/artifact/se.alipsa.groovy/gsvg>)
- **License:** MIT
- **Parsed scope:** Typed SVG dimensions, rectangle elements, and fill attributes
- **Underlying family:** gsvg typed SVG model (Groovy library callable from Java)
- **Local input API:** `SvgReader.parse(File).findAll(Rect.class)`
- **Documentation:** [API reference](<https://github.com/Alipsa/gsvg#readparse-an-existing-svg-file-and-change-it>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rects": 2,
  "fills": "#ff0000,#00ff00"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/java/gsvg/README.md)

```sh
python3 parsarium.py build svg java gsvg
python3 parsarium.py run svg java gsvg controls/svg/red-green.svg
```
