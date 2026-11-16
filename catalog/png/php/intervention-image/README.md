# intervention/image — PNG / PHP

- **Pinned release:** `4.4.1`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `ImageManager::usingDriver(GdDriver)::decodePath(local PNG path); Image::width/height`
- **Documentation:** [API reference](<https://github.com/Intervention/image/blob/3a47838f2e0f4ec6c8c9b43a5d73ac985b975830/readme.md>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

This package path delegates PNG decoding to the bundled PHP GD extension.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/intervention_image/README.md)

```sh
python3 parsarium.py build png php intervention_image
python3 parsarium.py run png php intervention_image controls/png/red-green.png
```
