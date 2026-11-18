# meyfa/php-svg — SVG / PHP

- **Pinned release:** `v0.16.1`
- **Upstream:** [source repository](<https://github.com/meyfa/php-svg>) · [Packagist](<https://packagist.org/packages/meyfa/php-svg>)
- **License:** MIT
- **Parsed scope:** One SVG document with two rectangle elements; no rasterization claim.
- **Underlying family:** meyfa PHP-SVG typed document parser
- **Local input API:** `SVG\SVG::fromFile(local path) returns typed SVG document and rect nodes`
- **Documentation:** [API reference](<https://github.com/meyfa/php-svg/blob/a62c2b9842826e83ea51f9b9e6ed28d2bdb1033c/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": "2",
  "height": "1",
  "rectangles": 2,
  "first_rect_width": "1"
}
```

jangobrick/php-svg is a Packagist alias for this identical source release and is excluded.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/php/meyfa_php_svg/README.md)

```sh
python3 parsarium.py build svg php meyfa_php_svg
python3 parsarium.py run svg php meyfa_php_svg controls/svg/red-green.svg
```
