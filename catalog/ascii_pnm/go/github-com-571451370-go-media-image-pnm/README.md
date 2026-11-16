# github.com/571451370/go-media/image/pnm — ASCII PNM / Go

- **Pinned release:** `v0.0.0-20190312080447-697b98554cbd`
- **License:** BSD-3-Clause, Zlib
- **Parsed scope:** P3 pixels and dimensions
- **Underlying family:** go-media PNM
- **Local input API:** `Decode(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/571451370/go-media/image/pnm@v0.0.0-20190312080447-697b98554cbd>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_pnm/parsers.json) · [control verification](../../../../data/go/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "height": 1,
  "rgb0": [
    255,
    0,
    0
  ],
  "rgb1": [
    0,
    255,
    0
  ],
  "width": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/github_com_571451370_go_media_image_pnm/README.md)

```sh
python3 parsarium.py build ascii_pnm go github_com_571451370_go_media_image_pnm
python3 parsarium.py run ascii_pnm go github_com_571451370_go_media_image_pnm controls/ascii_pnm/red-green.ppm
```
