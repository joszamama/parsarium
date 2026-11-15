# pgm-reader — ASCII PNM / Python

- **Pinned release:** `0.0.1`
- **License:** Apache-2.0
- **Parsed scope:** P2 grayscale pixels
- **Underlying family:** pgm-reader
- **Local input API:** `pgm_reader.Reader().read_pgm(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/pgm-reader/0.0.1/>)
- **Catalog evidence:** [parser record](../../../../data/python/ascii_pnm/parsers.json) · [control verification](../../../../data/python/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/python/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/black-white.pgm`](../../../../controls/ascii_pnm/black-white.pgm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "gray0": 0,
  "gray1": 255
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
