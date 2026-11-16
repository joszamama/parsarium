# mp4-box-encoding — MP4 / JavaScript

- **Pinned release:** `1.4.1`
- **License:** MIT
- **Parsed scope:** ftyp
- **Underlying family:** mp4-box-encoding
- **Local input API:** `decode(Buffer containing ftyp box)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp4-box-encoding>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "type": "ftyp",
  "brand": "isom",
  "compatible": [
    "isom",
    "iso2",
    "avc1",
    "mp41"
  ]
}
```

Parses the ftyp box only; narrow container-header scope.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
