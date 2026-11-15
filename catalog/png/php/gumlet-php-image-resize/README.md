# gumlet/php-image-resize — PNG / PHP

- **Pinned release:** `3.0.1`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `ImageResize(local PNG path); getSourceWidth/getSourceHeight`
- **Documentation:** [API reference](<https://github.com/gumlet/php-image-resize/blob/cd01c9e8aa2382211d760c825799c8102987a8c2/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

The package loads the local PNG through PHP GD.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
