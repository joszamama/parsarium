# github.com/gen2brain/pngn — PNG / Go

- **Pinned release:** `v0.1.3`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** pngn decoder
- **Local input API:** `Decode(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gen2brain/pngn@v0.1.3>)
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

[Docker harness and verification receipt](../../../../projects/png/go/github_com_gen2brain_pngn/README.md)

```sh
python3 parsarium.py build png go github_com_gen2brain_pngn
python3 parsarium.py run png go github_com_gen2brain_pngn controls/png/red-green.png
```
