# pnmpp — ASCII PNM / C++

- **Pinned release:** `1.0.1`
- **License:** MIT
- **Parsed scope:** P3 dimensions and two decoded RGBA pixels
- **Underlying family:** pnm++ native ASCII PNM reader
- **Local input API:** `pnm::read(localPath) as pnm::image<pnm::rgb_pixel>; width(), height(), image[y][x].red/green/blue`
- **Documentation:** [API reference](<https://github.com/ToruNiina/pnm/blob/v1.0.1/README.md>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_pnm/parsers.json) · [control verification](../../../../data/cpp/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0,
    255
  ],
  "second": [
    0,
    255,
    0,
    255
  ]
}
```

The upstream v1.0.1 header requires an eight-reference compatibility patch to compile with the local C++17 compiler: line_proxy comparisons refer to rhs.ny_ instead of rhs.iy_. The patch does not touch PNM decoding code. Original and patched header SHA-256 hashes are recorded.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
