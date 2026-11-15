# francodacosta/phmagick — ASCII PNM / PHP

- **Pinned release:** `v5.0.2`
- **License:** MIT
- **Parsed scope:** converted PNG dimensions and MIME
- **Underlying family:** ImageMagick PNM decoder
- **Local input API:** `phMagick\Core\Runner::run(Convert(local P3 file, local PNG output)); inspect converted image dimensions`
- **Documentation:** [API reference](<https://github.com/francodacosta/phmagick/blob/8871ec58ca5d12cc458d08ce1b9801d66ef35f16/docs/Convert.html>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "mime": "image/png"
}
```

phMagick invokes the installed ImageMagick CLI to decode ASCII P3 and output PNG; it is not an independent decoder.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
