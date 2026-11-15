# mp4-stream — MP4 / JavaScript

- **Pinned release:** `3.1.3`
- **License:** MIT
- **Parsed scope:** box_headers
- **Underlying family:** mp4-stream
- **Local input API:** `decode().end(Buffer); box events`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp4-stream>)
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
  ]
}
```

Parses top-level MP4 box headers only in this control.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
