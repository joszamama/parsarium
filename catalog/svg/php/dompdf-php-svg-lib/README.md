# dompdf/php-svg-lib — SVG / PHP

- **Pinned release:** `1.0.2`
- **Upstream:** [source repository](<https://github.com/dompdf/php-svg-lib>) · [Packagist](<https://packagist.org/packages/dompdf/php-svg-lib>)
- **License:** LGPL-3.0-or-later
- **Parsed scope:** Root SVG dimensions; full raster rendering not exercised.
- **Underlying family:** dompdf php-svg-lib XML/SVG parser
- **Local input API:** `Svg\Document::loadFile(local path), getDimensions parses SVG width and height`
- **Documentation:** [API reference](<https://github.com/dompdf/php-svg-lib/blob/8259ffb930817e72b1ff1caef5d226501f3dfeb1/src/Svg/Document.php>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

phenx/php-svg-lib is a Packagist alias for this identical source release and is excluded.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/php/php_svg_lib/README.md)

```sh
python3 parsarium.py build svg php php_svg_lib
python3 parsarium.py run svg php php_svg_lib controls/svg/red-green.svg
```
