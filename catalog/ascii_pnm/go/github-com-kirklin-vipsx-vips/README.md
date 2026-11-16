# github.com/kirklin/vipsx/vips — ASCII PNM / Go

- **Pinned release:** `v0.5.1`
- **License:** MIT
- **Parsed scope:** P3 dimensions
- **Underlying family:** libvips ppmload
- **Local input API:** `Startup(); PpmloadBuffer([]byte, nil)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/kirklin/vipsx/vips@v0.5.1>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_pnm/parsers.json) · [control verification](../../../../data/go/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "height": 1,
  "width": 2
}
```

Shared code lineage or native parser; package count does not imply independent parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/github_com_kirklin_vipsx_vips/README.md)

```sh
python3 parsarium.py build ascii_pnm go github_com_kirklin_vipsx_vips
python3 parsarium.py run ascii_pnm go github_com_kirklin_vipsx_vips controls/ascii_pnm/red-green.ppm
```
