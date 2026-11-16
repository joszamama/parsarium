# sharp — PNG / JavaScript

- **Pinned release:** `0.35.5`
- **License:** Apache-2.0
- **Parsed scope:** pixels
- **Underlying family:** libvips
- **Local input API:** `sharp(Buffer).raw().toBuffer({resolveWithObject:true})`
- **Documentation:** [API reference](<https://sharp.pixelplumbing.com/api-constructor/>)
- **Catalog evidence:** [parser record](../../../../data/javascript/png/parsers.json) · [control verification](../../../../data/javascript/png/verification.json) · [within-ecosystem ranking](../../../../data/javascript/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba": [
    255,
    0,
    0,
    255,
    0,
    255,
    0,
    255
  ]
}
```

Native wrapper; libvips performs image loading. The PNG backend beneath libvips is not determined here.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
