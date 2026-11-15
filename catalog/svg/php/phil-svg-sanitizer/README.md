# phil/svg-sanitizer — SVG / PHP

- **Pinned release:** `0.1.0-alpha`
- **License:** MIT
- **Parsed scope:** Valid two-rectangle SVG reconstructed through SVG element/attribute allowlists.
- **Underlying family:** PHIL SVG sanitizer over PHP Dom XMLDocument
- **Local input API:** `SvgSanitizer::sanitize(local SVG bytes) returns a reconstructed SVG document and removals`
- **Documentation:** [API reference](<https://github.com/parler-haut-interagir-librement/svg-sanitizer/blob/ca5b7d7ecde0f65a6c99ad15be706c2d7a39dd35/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rectangles": 2,
  "first_fill": "#ff0000"
}
```

Uses PHP 8.5 DOM for XML syntax and its own SVG allowlists; output observed with DOMDocument.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
