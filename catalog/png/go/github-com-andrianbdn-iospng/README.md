# github.com/andrianbdn/iospng — PNG / Go

- **Pinned release:** `v0.0.0-20180730113000-dccef1992541`
- **License:** MIT
- **Parsed scope:** dimensions+converted_bytes
- **Underlying family:** iOS PNG converter
- **Local input API:** `PngRevertOptimizationWithSize(io.Reader,io.Writer)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/andrianbdn/iospng@v0.0.0-20180730113000-dccef1992541>)
- **Catalog evidence:** [parser record](../../../../data/go/png/parsers.json) · [control verification](../../../../data/go/png/verification.json) · [within-ecosystem ranking](../../../../data/go/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "height": 1,
  "output_bytes": 71,
  "width": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/go/github_com_andrianbdn_iospng/README.md)

```sh
python3 parsarium.py build png go github_com_andrianbdn_iospng
python3 parsarium.py run png go github_com_andrianbdn_iospng controls/png/red-green.png
```
