# decmuc/svgsanitizer — SVG / PHP

- **Pinned release:** `v1.1.1`
- **License:** MIT
- **Parsed scope:** Valid SVG accepted and reconstructed with two rectangle nodes; no security assessment made.
- **Underlying family:** decMuc SVG sanitizer over libxml DOM
- **Local input API:** `SvgSanitizer::isSafe(local SVG bytes) parses DOM and filters allowed SVG elements and attributes`
- **Documentation:** [API reference](<https://github.com/decMuc/SvgSanitizer/blob/96b62d02514fc3370c4c09108bafc744b7aa4a28/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rectangles": 2,
  "first_fill": "#ff0000"
}
```

Shares libxml DOM XML syntax parser with other sanitizer packages; SVG allowlist implementation differs.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/php/decmuc_svgsanitizer/README.md)

```sh
python3 parsarium.py build svg php decmuc_svgsanitizer
python3 parsarium.py run svg php decmuc_svgsanitizer controls/svg/red-green.svg
```
