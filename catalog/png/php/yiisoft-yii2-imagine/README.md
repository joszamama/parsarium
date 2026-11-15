# yiisoft/yii2-imagine — PNG / PHP

- **Pinned release:** `2.3.1`
- **License:** BSD-3-Clause
- **Parsed scope:** decoded PNG dimensions after thumbnail
- **Underlying family:** Imagine / PHP GD PNG decoder
- **Local input API:** `Image::thumbnail(local PNG path, 2, 1); ImageInterface::getSize`
- **Documentation:** [API reference](<https://github.com/yiisoft/yii2-imagine/blob/7ec4332dc25893aec5a7cf084722b162b3a4d55d/src/BaseImage.php>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

Yii wrapper calls Imagine with its GD driver; the underlying Imagine and PHP GD families are shared with other paths.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
