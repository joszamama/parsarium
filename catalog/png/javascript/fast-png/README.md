# fast-png — PNG / JavaScript

- **Pinned release:** `8.0.0`
- **Upstream:** [source repository](<https://github.com/image-js/fast-png>) · [npm](<https://www.npmjs.com/package/fast-png>)
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** fast-png
- **Local input API:** `decode(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/fast-png>)
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

[Docker harness and verification receipt](../../../../projects/png/javascript/fast_png/README.md)

```sh
python3 parsarium.py build png javascript fast_png
python3 parsarium.py run png javascript fast_png controls/png/red-green.png
```
