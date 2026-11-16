# jairosvg — SVG / Java

- **Pinned release:** `1.0.16`
- **License:** MIT
- **Parsed scope:** Rendered SVG pixels
- **Underlying family:** JairoSVG Java2D SVG renderer
- **Local input API:** `JairoSVG.builder().fromFile(Path).toImage()`
- **Documentation:** [API reference](<https://github.com/brunoborges/jairosvg#library-api>)
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

[Docker harness and verification receipt](../../../../projects/svg/java/jairosvg/README.md)

```sh
python3 parsarium.py build svg java jairosvg
python3 parsarium.py run svg java jairosvg controls/svg/red-green.svg
```
