# svg-salamander — SVG / Java

- **Pinned release:** `1.1.5.5`
- **License:** BSD-2-Clause
- **Parsed scope:** Rendered SVG pixels
- **Underlying family:** SVG Salamander
- **Local input API:** `SVGUniverse.loadSVG(InputStream, String).getDiagram(URI).render(Graphics2D)`
- **Documentation:** [API reference](<https://github.com/blackears/svgSalamander/blob/master/svg-core/src/main/java/com/kitfox/svg/SVGUniverse.java>)
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

[Docker harness and verification receipt](../../../../projects/svg/java/svg_salamander/README.md)

```sh
python3 parsarium.py build svg java svg_salamander
python3 parsarium.py run svg java svg_salamander controls/svg/red-green.svg
```
