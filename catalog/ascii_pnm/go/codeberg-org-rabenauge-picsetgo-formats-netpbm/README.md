# codeberg.org/rabenauge/picsetgo/formats/netpbm — ASCII PNM / Go

- **Pinned release:** `v0.5.6`
- **License:** MIT
- **Parsed scope:** P3 pixels and dimensions
- **Underlying family:** picsetgo Netpbm
- **Local input API:** `Decode(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/codeberg.org/rabenauge/picsetgo/formats/netpbm@v0.5.6>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/codeberg_org_rabenauge_picsetgo_formats_netpbm/README.md)

```sh
python3 parsarium.py build ascii_pnm go codeberg_org_rabenauge_picsetgo_formats_netpbm
python3 parsarium.py run ascii_pnm go codeberg_org_rabenauge_picsetgo_formats_netpbm controls/ascii_pnm/red-green.ppm
```
