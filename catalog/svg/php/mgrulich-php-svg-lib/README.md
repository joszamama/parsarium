# mgrulich/php-svg-lib — SVG / PHP

- **Pinned release:** `v0.5`
- **License:** LGPL-3.0
- **Parsed scope:** SVG root width and height only; full rendering not exercised.
- **Underlying family:** dompdf php-svg-lib XML/SVG parser
- **Local input API:** `Svg\Document::loadFile(local path), getDimensions parses SVG root dimensions`
- **Documentation:** [API reference](<https://github.com/mgrulich/php-svg-lib/blob/3abe69020e38c5fb4ca37e703a3a74dd18ea31c9/src/Svg/Document.php>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

Older fork of PhenX/dompdf php-svg-lib; shared parser lineage with dompdf/php-svg-lib.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
