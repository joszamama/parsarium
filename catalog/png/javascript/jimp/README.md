# jimp — PNG / JavaScript

- **Pinned release:** `1.6.1`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** pngjs
- **Local input API:** `Jimp.read(Buffer)`
- **Documentation:** [API reference](<https://github.com/jimp-dev/jimp/blob/main/packages/jimp/README.md>)
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

jimp@1.6.1 depends on @jimp/js-png@1.6.1, which depends on pngjs@^7.0.0.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/javascript/jimp/README.md)

```sh
python3 parsarium.py build png javascript jimp
python3 parsarium.py run png javascript jimp controls/png/red-green.png
```
