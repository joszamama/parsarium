# claviska/simpleimage — PNG / PHP

- **Pinned release:** `4.4.2`
- **License:** MIT
- **Parsed scope:** decoded dimensions and two RGB pixels
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `SimpleImage::fromFile(local PNG path); getWidth/getHeight/getColorAt`
- **Documentation:** [API reference](<https://github.com/claviska/SimpleImage/blob/f2397d67a06ed3334e5cfc22df55e55fb5f8bae1/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "left_rgb": [
    255,
    0,
    0
  ],
  "right_rgb": [
    0,
    255,
    0
  ]
}
```

This package path delegates PNG decoding to the bundled PHP GD extension.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
