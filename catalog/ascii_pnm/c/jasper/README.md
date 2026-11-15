# jasper — ASCII PNM / C

- **Pinned release:** `4.2.9`
- **License:** JasPer-2.0
- **Parsed scope:** P3 dimensions and two decoded RGB pixels
- **Underlying family:** JasPer PNM codec
- **Local input API:** `jas_stream_fopen(local path); jas_image_decode(stream,-1,NULL); jas_image_readcmptsample`
- **Documentation:** [API reference](<https://jasper-software.github.io/jasper-manual/latest/html/group__module__images.html>)
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
  ]
}
```

JasPer decodes P3 through its own PNM codec.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
