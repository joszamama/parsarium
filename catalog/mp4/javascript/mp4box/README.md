# mp4box — MP4 / JavaScript

- **Pinned release:** `2.5.0`
- **License:** BSD-3-Clause
- **Parsed scope:** tracks+brand
- **Underlying family:** GPAC MP4Box.js
- **Local input API:** `createFile().appendBuffer(ArrayBuffer with fileStart=0)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp4box>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "brand": "isom",
  "width": 2,
  "height": 2,
  "tracks": 2
}
```

GPAC MP4Box.js parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
