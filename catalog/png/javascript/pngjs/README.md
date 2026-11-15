# pngjs — PNG / JavaScript

- **Pinned release:** `7.0.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** pngjs
- **Local input API:** `PNG.sync.read(Buffer)`
- **Documentation:** [API reference](<https://github.com/pngjs/pngjs/blob/main/README.md>)
- **Catalog evidence:** [parser record](../../../../data/javascript/png/parsers.json) · [control verification](../../../../data/javascript/png/verification.json) · [within-ecosystem ranking](../../../../data/javascript/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba": [
    255,
    0,
    0,
    255,
    0,
    255,
    0,
    255
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/javascript/pngjs/README.md)

```sh
python3 parsarium.py build png javascript pngjs
python3 parsarium.py run png javascript pngjs controls/png/red-green.png
```
