# ksubileau/color-thief-php — PNG / PHP

- **Pinned release:** `v3.0.0`
- **License:** MIT
- **Parsed scope:** decoded two-color palette
- **Underlying family:** PHP GD PNG decoder
- **Local input API:** `ColorThief(quality:1, preferredAdapter:Gd)::getPalette(local PNG path, 2); toHex`
- **Documentation:** [API reference](<https://github.com/ksubileau/color-thief-php/blob/2ca3d3a05c947f71c8cf22d2b0a85603b3f2df94/src/ColorThief/ColorThief.php>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "palette": [
    "#00ff00",
    "#ff0000"
  ]
}
```

ColorThief delegates PNG input to its GD adapter, then quantizes decoded pixels.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/php/ksubileau_color_thief_php/README.md)

```sh
python3 parsarium.py build png php ksubileau_color_thief_php
python3 parsarium.py run png php ksubileau_color_thief_php controls/png/red-green.png
```
