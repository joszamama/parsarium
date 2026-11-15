# netpbm — ASCII PNM / C

- **Pinned release:** `11.02.30`
- **License:** Netpbm mixed open-source
- **Parsed scope:** P3 dimensions, maxval, and two decoded RGB pixels
- **Underlying family:** Netpbm libppm parser
- **Local input API:** `ppm_readppm(FILE*, int*, int*, pixval*); PPM_GETR/G/B(...)`
- **Documentation:** [API reference](<https://netpbm.sourceforge.net/doc/libppm.html>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_pnm/parsers.json) · [control verification](../../../../data/c/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "maxval": 255,
  "first": [
    255,
    0,
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

Direct libnetpbm library API; PPM reader also accepts PBM/PGM with on-the-fly conversion per official manual. Only P3 is verified here.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
