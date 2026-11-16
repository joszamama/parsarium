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

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/sybio_image_workshop/README.md)

```sh
python3 parsarium.py build png php sybio_image_workshop
python3 parsarium.py run png php sybio_image_workshop controls/png/red-green.png
```
