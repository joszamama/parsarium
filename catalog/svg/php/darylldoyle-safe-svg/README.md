# darylldoyle/safe-svg — SVG / PHP

- **Pinned release:** `2.5.2`
- **License:** GPL-2.0-or-later
- **Parsed scope:** Standalone public helper replay with WordPress default option/filter behavior supplied by adapter; no full WordPress install claim.
- **Underlying family:** enshrined SVG sanitizer over libxml DOM
- **Local input API:** `SafeSvg\Svg_Sanitizer::sanitize_markup(local SVG bytes) calls configured SVG sanitizer`
- **Documentation:** [API reference](<https://github.com/10up/safe-svg/blob/21a0fc4ea0515513d7e099603eb738b576109568/includes/safe-svg-sanitizer.php>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rectangles": 2,
  "first_fill": "#ff0000"
}
```

WordPress package wraps the same enshrined/svg-sanitize 1.1.1 parser; not an independent engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
