# renfordt/php-svg — SVG / PHP

- **Pinned release:** `v0.1.0`
- **License:** MIT
- **Parsed scope:** Typed SVG root dimensions and two rectangle nodes.
- **Underlying family:** meyfa PHP-SVG typed document parser
- **Local input API:** `SVG\SVG::fromFile(local path) parses SVG document and rectangle nodes`
- **Documentation:** [API reference](<https://codeberg.org/renfordt/php-svg/src/commit/98a0ea156569fea7a30b3b28c8c46999987ffff7/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": "2",
  "height": "1",
  "rectangles": 2
}
```

Fork of the PHP-SVG lineage; separate source release, shared core parser family with meyfa/php-svg.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/php/renfordt_php_svg/README.md)

```sh
python3 parsarium.py build svg php renfordt_php_svg
python3 parsarium.py run svg php renfordt_php_svg controls/svg/red-green.svg
```
