# atelier/svg — SVG / PHP

- **Pinned release:** `v1.1.0`
- **License:** MIT
- **Parsed scope:** Typed SVG document and two parsed rectangles.
- **Underlying family:** Atelier SVG typed DOM parser
- **Local input API:** `Atelier\Svg\Svg::load(local path) returns typed SVG document; querySelectorAll('rect')`
- **Documentation:** [API reference](<https://github.com/ateliersvg/svg/blob/e0bc37c4fa9da98f0c30e6aca83ea5f6d2478be1/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rectangles": 2
}
```

Uses PHP DOM for XML syntax and its own SVG element objects.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/php/atelier_svg/README.md)

```sh
python3 parsarium.py build svg php atelier_svg
python3 parsarium.py run svg php atelier_svg controls/svg/red-green.svg
```
