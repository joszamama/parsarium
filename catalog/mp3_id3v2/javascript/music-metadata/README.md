# music-metadata — MP3 with ID3v2 / JavaScript

- **Pinned release:** `12.4.0`
- **License:** MIT
- **Parsed scope:** tags+audio_header
- **Underlying family:** music-metadata
- **Local input API:** `parseFile(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/music-metadata>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3_id3v2/parsers.json) · [control verification](../../../../data/javascript/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "sampleRate": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
