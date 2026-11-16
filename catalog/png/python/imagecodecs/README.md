# imagecodecs — PNG / Python

- **Pinned release:** `2026.10.10`
- **License:** BSD-3-Clause
- **Parsed scope:** pixels
- **Underlying family:** imagecodecs PNG codec
- **Local input API:** `imagecodecs.png_decode(local bytes)`
- **Documentation:** [API reference](<https://github.com/cgohlke/imagecodecs>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba0": [
    255,
    0,
    0,
    255
  ],
  "rgba1": [
    0,
    255,
    0,
    255
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/imagecodecs/README.md)

```sh
python3 parsarium.py build png python imagecodecs
python3 parsarium.py run png python imagecodecs controls/png/red-green.png
```
