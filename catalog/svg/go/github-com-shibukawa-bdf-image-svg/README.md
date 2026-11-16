# github.com/shibukawa/bdf/image/svg — SVG / Go

- **Pinned release:** `v0.2.1`
- **License:** MIT
- **Parsed scope:** elements, root
- **Underlying family:** shibukawa SVG tree parser
- **Local input API:** `Parse([]byte, nil).Root.Children`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/shibukawa/bdf/image/svg@v0.2.1>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "elements": 2,
  "root": "svg"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_shibukawa_bdf_image_svg/README.md)

```sh
python3 parsarium.py build svg go github_com_shibukawa_bdf_image_svg
python3 parsarium.py run svg go github_com_shibukawa_bdf_image_svg controls/svg/red-green.svg
```
