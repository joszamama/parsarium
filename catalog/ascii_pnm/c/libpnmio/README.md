# libpnmio — ASCII PNM / C

- **Pinned release:** `1.2.7 (README; commit pinned)`
- **License:** BSD-3-Clause
- **Parsed scope:** P3 dimensions and two decoded RGB pixels, maxval
- **Underlying family:** libpnmio PPM reader
- **Local input API:** `read_ppm_header(FILE*,...); read_ppm_data(FILE*,int*,is_ascii)`
- **Documentation:** [API reference](<https://github.com/nkkav/libpnmio/blob/bd860723211ffdb3a0b0a7067afd7e94d583af7c/README.rst>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_pnm/parsers.json) · [control verification](../../../../data/c/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0
  ],
  "second": [
    0,
    255,
    0
  ],
  "maxval": 255
}
```

README declares 1.2.7, VERSION remains 1.2.6, and no tag exists; the exact source commit and archive hash identify the tested code. The README API text has an outdated pointer/value signature; the pinned header is authoritative.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
