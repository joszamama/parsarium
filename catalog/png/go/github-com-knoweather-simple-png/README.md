# github.com/knoweather/simple-png — PNG / Go

- **Pinned release:** `v1.5.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** simple-png decoder
- **Local input API:** `ParsePng(io.Reader); IDATsToColor()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/knoweather/simple-png@v1.5.0>)
- **Catalog evidence:** [parser record](../../../../data/go/png/parsers.json) · [control verification](../../../../data/go/png/verification.json) · [within-ecosystem ranking](../../../../data/go/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
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
  ],
  "width": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/go/github_com_knoweather_simple_png/README.md)

```sh
python3 parsarium.py build png go github_com_knoweather_simple_png
python3 parsarium.py run png go github_com_knoweather_simple_png controls/png/red-green.png
```
