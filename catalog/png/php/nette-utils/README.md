# nette/utils — PNG / PHP

- **Pinned release:** `v4.1.6`
- **Upstream:** [source repository](<https://github.com/nette/utils>) · [Packagist](<https://packagist.org/packages/nette/utils>)
- **License:** BSD-3-Clause OR GPL-2.0-only OR GPL-3.0-only
- **Parsed scope:** decoded dimensions and PNG type
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `Nette\Utils\Image::fromFile(local PNG path, detected type); getWidth/getHeight`
- **Documentation:** [API reference](<https://github.com/nette/utils/blob/6bf24518accf32cf845bca305e0b92078700fd01/src/Utils/Image.php>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "type": 3
}
```

Nette Utils Image delegates PNG decoding to bundled PHP GD; package-level downloads cover many unrelated utility APIs.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/nette_utils/README.md)

```sh
python3 parsarium.py build png php nette_utils
python3 parsarium.py run png php nette_utils controls/png/red-green.png
```
