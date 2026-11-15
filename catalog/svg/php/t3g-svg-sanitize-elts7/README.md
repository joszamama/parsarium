# t3g/svg-sanitize-elts7 — SVG / PHP

- **Pinned release:** `0.15.4.1`
- **License:** GPL-2.0-or-later
- **Parsed scope:** Valid two-rectangle SVG on PHP 7.4; no full TYPO3 installation exercised.
- **Underlying family:** enshrined SVG sanitizer over libxml DOM
- **Local input API:** `enshrined\svgSanitize\Sanitizer::sanitize(local SVG bytes) parses SVG with TYPO3 fork policy`
- **Documentation:** [API reference](<https://github.com/TYPO3GmbH/svg-sanitize-elts7/blob/3e6fcdfbcc74946c48b52244473033a2d9f36568/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rectangles": 2,
  "first_fill": "#ff0000"
}
```

Older TYPO3 fork/replacement of enshrined/svg-sanitize, sharing parser lineage and namespace.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
