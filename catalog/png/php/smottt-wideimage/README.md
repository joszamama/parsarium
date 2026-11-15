# smottt/wideimage — PNG / PHP

- **Pinned release:** `1.1.4`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** decoded image dimensions
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `WideImage::load(local PNG path); getWidth/getHeight`
- **Documentation:** [API reference](<https://github.com/smottt/WideImage/blob/755d1b2b474ce9c32092aa6ac0357ebf857545f5/lib/WideImage/WideImage.php>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

WideImage uses its PNG mapper backed by PHP GD; Composer lists GPL-2.0 and LGPL-2.1, while the pinned LICENSE text states LGPL 2.1 or later.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
