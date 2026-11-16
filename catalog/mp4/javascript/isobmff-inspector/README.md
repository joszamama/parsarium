# isobmff-inspector — MP4 / JavaScript

- **Pinned release:** `0.5.0`
- **License:** MIT
- **Parsed scope:** boxes+brand
- **Underlying family:** isobmff-inspector
- **Local input API:** `inspectISOBMFF(Uint8Array)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/isobmff-inspector>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "boxes": [
    "ftyp",
    "moov",
    "free",
    "mdat"
  ],
  "brand": "isom"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
