# enshrined/svg-sanitize — SVG / PHP

- **Pinned release:** `1.1.1`
- **License:** GPL-2.0-or-later
- **Parsed scope:** Valid two-rectangle SVG accepted by SVG sanitizer; parsed output retains rect and fill attributes.
- **Underlying family:** enshrined SVG sanitizer over libxml DOM
- **Local input API:** `Sanitizer::sanitize(local SVG byte string) parses SVG/XML and applies SVG element and attribute policy`
- **Documentation:** [API reference](<https://github.com/darylldoyle/svg-sanitizer/blob/1976ff93c8d8a234cdd3ff99626bd43ecf11bf49/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "root": "svg",
  "rectangles": 2,
  "first_fill": "#ff0000"
}
```

Its output is reparsed with PHP DOM only for observing the sanitized SVG tree; the counted input parser is the sanitizer.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
