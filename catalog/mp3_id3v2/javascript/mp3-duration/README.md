# mp3-duration — MP3 with ID3v2 / JavaScript

- **Pinned release:** `1.1.0`
- **License:** MIT
- **Parsed scope:** duration
- **Underlying family:** mp3-duration
- **Local input API:** `mp3Duration(Buffer,callback)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/mp3-duration>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3_id3v2/parsers.json) · [control verification](../../../../data/javascript/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "duration_ms": 1224
}
```

Frame duration includes MP3 padding and differs from nominal one-second source duration.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
