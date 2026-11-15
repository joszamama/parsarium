# itools/svgsecuritycheck — SVG / PHP

- **Pinned release:** `v1.0.0`
- **License:** MIT
- **Parsed scope:** Format-aware SVG validation verdict on one valid two-rectangle document; no element tree returned.
- **Underlying family:** SvgSecurityCheck XMLReader-based SVG validator
- **Local input API:** `SvgSecurityCheck::checkFile(local path) streams SVG through XMLReader and SVG element/attribute allowlists`
- **Documentation:** [API reference](<https://github.com/interactivetools-com/SvgSecurityCheck/blob/588e2da66ef438f8a01bcf6c7f1906b3e9407886/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/svg/parsers.json) · [control verification](../../../../data/php/svg/verification.json) · [within-ecosystem ranking](../../../../data/php/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "accepted_svg": true,
  "violations": 0
}
```

Uses bundled libxml XMLReader for syntax and package-specific SVG allowlists for semantic checks.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
