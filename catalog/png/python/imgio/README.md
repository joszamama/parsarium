# imgio — PNG / Python

- **Pinned release:** `1.7.4`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** imgio via Pillow on macOS
- **Local input API:** `imgio.imread(local path)`
- **Documentation:** [API reference](<https://github.com/toaarnio/imgio/blob/master/imgio/imgio.py>)
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

Observed or documented wrapper path; this package is counted as a distinct API package, not an independent PNG engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/imgio/README.md)

```sh
python3 parsarium.py build png python imgio
python3 parsarium.py run png python imgio controls/png/red-green.png
```
