# image-meta — ASCII PNM / JavaScript

- **Pinned release:** `0.2.2`
- **Upstream:** [source repository](<https://github.com/unjs/image-meta>) · [npm](<https://www.npmjs.com/package/image-meta>)
- **License:** MIT
- **Parsed scope:** P3 header dimensions and PNM type
- **Underlying family:** image-meta reader based on image-size
- **Local input API:** `imageMeta(localBuffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/image-meta>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/javascript/image_meta/README.md)

```sh
python3 parsarium.py build ascii_pnm javascript image_meta
python3 parsarium.py run ascii_pnm javascript image_meta controls/ascii_pnm/red-green.ppm
```
