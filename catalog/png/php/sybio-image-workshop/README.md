# sybio/image-workshop — PNG / PHP

- **Pinned release:** `3.0.0-beta1`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `ImageWorkshop::initFromPath(local PNG path); getWidth/getHeight`
- **Documentation:** [API reference](<https://github.com/Sybio/ImageWorkshop/blob/ae252ab16c8f1f8b797c7ecd3a60c3cde0e8b569/src/ImageWorkshop.php>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

ImageWorkshop initializes an image layer from local PNG through PHP GD.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
