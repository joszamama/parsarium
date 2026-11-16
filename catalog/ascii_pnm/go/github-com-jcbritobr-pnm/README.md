# github.com/jcbritobr/pnm — ASCII PNM / Go

- **Pinned release:** `v0.1.0`
- **License:** MIT
- **Parsed scope:** P3 header: dimensions and maximum channel value
- **Underlying family:** jcbritobr PNM
- **Local input API:** `NewDecoder(io.Reader, PPMText).Decode(Image)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/jcbritobr/pnm@v0.1.0>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_pnm/parsers.json) · [control verification](../../../../data/go/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "height": 1,
  "maxval": 255,
  "width": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/github_com_jcbritobr_pnm/README.md)

```sh
python3 parsarium.py build ascii_pnm go github_com_jcbritobr_pnm
python3 parsarium.py run ascii_pnm go github_com_jcbritobr_pnm controls/ascii_pnm/red-green.ppm
```
