# libpnmrw — ASCII PNM / C++

- **Pinned release:** `14Aug2014`
- **License:** BSD-2-Clause
- **Parsed scope:** P3 dimensions, maxval, and two decoded RGB pixels
- **Underlying family:** libpnmrw PBMPLUS-derived parser
- **Local input API:** `pnm_readpnm(FILE*, int*, int*, xelval*, int*); PPM_GETR/G/B(...)`
- **Documentation:** [API reference](<https://acme.com/software/libpnmrw/>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_pnm/parsers.json) · [control verification](../../../../data/cpp/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_pnm/ranking.md)
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

A compact PBMPLUS-derived reader with a local FILE* API; it shares historical lineage with Netpbm but is a separately distributed parser implementation. The date-named archive is 14Aug2014; its README labels the code version 03jul2014.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/cpp/libpnmrw/README.md)

```sh
python3 parsarium.py build ascii_pnm cpp libpnmrw
python3 parsarium.py run ascii_pnm cpp libpnmrw controls/ascii_pnm/red-green.ppm
```
