# meyfa/php-svg — SVG / PHP

- **Pinned release:** `v0.16.1`
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
