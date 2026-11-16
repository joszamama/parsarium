# github.com/tdewolff/canvas/image — PNG / Go

- **Pinned release:** `v0.0.0-20260923214215-09804640d00c`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** canvas PNG image loader
- **Local input API:** `NewPNGImage(io.Reader); Image()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tdewolff/canvas/image@v0.0.0-20260923214215-09804640d00c>)
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

[Docker harness and verification receipt](../../../../projects/png/go/github_com_tdewolff_canvas_image/README.md)

```sh
python3 parsarium.py build png go github_com_tdewolff_canvas_image
python3 parsarium.py run png go github_com_tdewolff_canvas_image controls/png/red-green.png
```
