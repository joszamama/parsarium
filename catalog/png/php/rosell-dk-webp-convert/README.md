# rosell-dk/webp-convert — PNG / PHP

- **Pinned release:** `2.9.5`
- **License:** MIT
- **Parsed scope:** PNG decoded to WebP with dimensions
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `WebPConvert::convert(local PNG path, local WebP path, gd converter)`
- **Documentation:** [API reference](<https://github.com/rosell-dk/webp-convert/blob/bce87de61cff098e899a91960f9fdb08e8867194/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "output_type": 18
}
```

Explicit GD converter decodes local PNG through bundled PHP GD before WebP encoding.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/rosell_dk_webp_convert/README.md)

```sh
python3 parsarium.py build png php rosell_dk_webp_convert
python3 parsarium.py run png php rosell_dk_webp_convert controls/png/red-green.png
```
