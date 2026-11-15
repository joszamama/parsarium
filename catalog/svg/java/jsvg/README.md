# jsvg — SVG / Java

- **Pinned release:** `2.0.0`
- **License:** MIT
- **Parsed scope:** Rendered SVG pixels
- **Underlying family:** JSVG
- **Local input API:** `SVGLoader.load(InputStream, URI, LoaderContext).render(Component, Graphics2D, ViewBox)`
- **Documentation:** [API reference](<https://github.com/weisJ/jsvg>)
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

[Docker harness and verification receipt](../../../../projects/svg/java/jsvg/README.md)

```sh
python3 parsarium.py build svg java jsvg
python3 parsarium.py run svg java jsvg controls/svg/red-green.svg
```
