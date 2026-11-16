# pngjs-nozlib — PNG / JavaScript

- **Pinned release:** `1.0.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** pngjs
- **Local input API:** `PNG.sync.read(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pngjs-nozlib>)
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

Fork of the pngjs parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/javascript/pngjs_nozlib/README.md)

```sh
python3 parsarium.py build png javascript pngjs_nozlib
python3 parsarium.py run png javascript pngjs_nozlib controls/png/red-green.png
```
