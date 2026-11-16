# mathiasreker/php-svg-optimizer — SVG / PHP

- **Pinned release:** `10.0.0`
- **License:** MIT
- **Parsed scope:** One SVG document with two rectangles; first fill normalized from #ff0000 to red.
- **Underlying family:** MathiasReker native PHP SVG optimizer over libxml DOM
- **Local input API:** `SvgOptimizer::withRules(Rule::MinifyColors)->optimizeFile(local path) parses SVG and normalizes fill color`
- **Documentation:** [API reference](<https://github.com/MathiasReker/php-svg-optimizer/blob/16cdbb0f4193fc9f1d49f05d280946bf0e55a793/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rectangles": 2,
  "first_fill": "red"
}
```

Uses libxml DOM for XML syntax with SVG-specific optimization rules.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/php/mathiasreker_php_svg_optimizer/README.md)

```sh
python3 parsarium.py build svg php mathiasreker_php_svg_optimizer
python3 parsarium.py run svg php mathiasreker_php_svg_optimizer controls/svg/red-green.svg
```
