# mp4-parser — MP4 / JavaScript

- **Pinned release:** `0.3.0`
- **License:** MIT
- **Parsed scope:** tags+duration
- **Underlying family:** mp4-parser
- **Local input API:** `fs.createReadStream(path).pipe(new MP4Parser())`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp4-parser>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "duration": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
