# aplus/image — PNG / PHP

- **Pinned release:** `v3.0.2`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `Framework\Image\Image(local PNG path); getWidth/getHeight`
- **Documentation:** [API reference](<https://github.com/aplus-framework/image/blob/02a8145dc166b4e850b0e58bc11f41d4192bc4a7/src/Image.php>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

Aplus Image calls getimagesize then imagecreatefrompng in the bundled PHP GD extension.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
