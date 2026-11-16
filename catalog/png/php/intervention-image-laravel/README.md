# intervention/image-laravel — PNG / PHP

- **Pinned release:** `4.1.1`
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** Intervention Image 4 / PHP GD PNG decoder
- **Local input API:** `Laravel Image facade::decodePath(local PNG path); width/height`
- **Documentation:** [API reference](<https://github.com/Intervention/image-laravel/blob/8a8bd2c7bb4a9aa2b046ff066fd1cd44b1de0da2/src/Facades/Image.php>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

Laravel facade forwards to Intervention Image 4 configured with PHP GD; the core Intervention package is separately listed.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/intervention_image_laravel/README.md)

```sh
python3 parsarium.py build png php intervention_image_laravel
python3 parsarium.py run png php intervention_image_laravel controls/png/red-green.png
```
