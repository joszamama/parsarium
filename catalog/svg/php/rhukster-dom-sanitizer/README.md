# rhukster/dom-sanitizer — SVG / PHP

- **Pinned release:** `1.0.20`
- **License:** MIT
- **Parsed scope:** Valid two-rectangle SVG accepted with SVG-specific sanitizer profile.
- **Underlying family:** Rhukster DOM/SVG sanitizer over libxml DOM
- **Local input API:** `DOMSanitizer(DOMSanitizer::SVG)->sanitize(local SVG bytes) applies SVG tag and attribute policy`
- **Documentation:** [API reference](<https://github.com/rhukster/dom-sanitizer/blob/83d618dac5aba78024d65983da1cc74514918e5f/README.md>)
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

Shares the PHP DOM XML syntax parser with other sanitizers, but supplies its own SVG policy.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
