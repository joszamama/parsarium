# mediainfo.js — MP4 / JavaScript

- **Pinned release:** `0.3.8`
- **License:** BSD-2-Clause
- **Parsed scope:** tracks+title
- **Underlying family:** MediaInfoLib WASM
- **Local input API:** `MediaInfo().analyzeData(size,readChunk)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mediainfo.js>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "width": 2,
  "height": 2,
  "sampleRate": 8000
}
```

WebAssembly distribution of MediaInfoLib; same family as native MediaInfo.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
