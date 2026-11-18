# image-size-next — ASCII PNM / JavaScript

- **Pinned release:** `2.1.1`
- **Upstream:** [source repository](<https://github.com/lcf2212dev/image-size-next>) · [npm](<https://www.npmjs.com/package/image-size-next>)
- **License:** MIT
- **Parsed scope:** P3 header dimensions and PNM type
- **Underlying family:** image-size fork
- **Local input API:** `imageSize(localBuffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/image-size-next>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "type": "pnm",
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/javascript/image_size_next/README.md)

```sh
python3 parsarium.py build ascii_pnm javascript image_size_next
python3 parsarium.py run ascii_pnm javascript image_size_next controls/ascii_pnm/red-green.ppm
```
