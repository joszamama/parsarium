# simpleimageio — PNG / Python

- **Pinned release:** `1.13.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** SimpleImageIO native reader
- **Local input API:** `simpleimageio.read(local path)`
- **Documentation:** [API reference](<https://github.com/pgrit/SimpleImageIO>)
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

[Docker harness and verification receipt](../../../../projects/png/python/simpleimageio/README.md)

```sh
python3 parsarium.py build png python simpleimageio
python3 parsarium.py run png python simpleimageio controls/png/red-green.png
```
