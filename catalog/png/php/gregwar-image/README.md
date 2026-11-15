# gregwar/image — PNG / PHP

- **Pinned release:** `v2.1.0`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `Gregwar\Image\Image::open(local PNG path); width/height`
- **Documentation:** [API reference](<https://github.com/Gregwar/Image/blob/1cf64c34cbb22933b36727c16b15ed4d925b6fc6/Gregwar/Image/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

The adapter uses Gregwar’s GD backend to decode the PNG.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
