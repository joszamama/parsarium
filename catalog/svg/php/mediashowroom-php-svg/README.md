# mediashowroom/php-svg — SVG / PHP

- **Pinned release:** `v0.7.0`
- **License:** MIT
- **Parsed scope:** Typed SVG document root and two direct rectangle child nodes.
- **Underlying family:** mediashowroom PHP-SVG typed document parser
- **Local input API:** `SVG\SVGImage::fromFile(local path) parses SVG document, dimensions, and child shapes`
- **Documentation:** [API reference](<https://github.com/mediashowroom/php-svg/blob/ceaa17895593f5a744daf09890f5d036255c6d94/README.md>)
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

Earlier PHP-SVG lineage shared with meyfa/php-svg; distinct source release and package path.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/php/mediashowroom_php_svg/README.md)

```sh
python3 parsarium.py build svg php mediashowroom_php_svg
python3 parsarium.py run svg php mediashowroom_php_svg controls/svg/red-green.svg
```
