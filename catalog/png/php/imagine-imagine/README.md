# imagine/imagine — PNG / PHP

- **Pinned release:** `1.5.4`
- **Upstream:** [source repository](<https://github.com/php-imagine/Imagine>) · [Packagist](<https://packagist.org/packages/imagine/imagine>)
- **License:** MIT
- **Parsed scope:** decoded image dimensions
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `Imagine\Gd\Imagine::open(local PNG path); Image::getSize`
- **Documentation:** [API reference](<https://github.com/php-imagine/Imagine/blob/dd57a4c290ff4d223d17bcd219dac9ac8bf1cc16/src/Gd/Imagine.php>)
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

[Docker harness and verification receipt](../../../../projects/png/php/imagine_imagine/README.md)

```sh
python3 parsarium.py build png php imagine_imagine
python3 parsarium.py run png php imagine_imagine controls/png/red-green.png
```
