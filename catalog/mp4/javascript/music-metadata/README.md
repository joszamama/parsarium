# music-metadata — MP4 / JavaScript

- **Pinned release:** `12.4.0`
- **License:** MIT
- **Parsed scope:** tracks+title
- **Underlying family:** music-metadata/ISO BMFF reader
- **Local input API:** `parseFile(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/music-metadata>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
